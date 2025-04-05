
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent,AgentType,Tool

import requests
from geopy.geocoders import Nominatim
from lunarcalendar import Solar, Lunar

import urllib
from urllib import request as urllib_request
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import API.llm as rp
app = Flask(__name__)
CORS(app)  # 允许跨域请求

def llm_main(question=None):
    return rp.main(question)
#获取天气用
def get_weather(city=None):
   """

   :param city:
   :return:
   """
   city = eval(city)
   print(city)

   if not city:
       # 获取当前位置
       geolocator = Nominatim(user_agent="weather_app")
       location = geolocator.geocode("")
       city = location.address.split(",")[0]  # 获取城市名称
       # 使用天气API获取天气信息（以OpenWeatherMap为例）
   api_url = 'http://apis.juhe.cn/simpleWeather/query'
   params_dict = {
       "city": city,  # 查询天气的城市名称，如：北京、苏州、上海
       "key": "您申请的接口API接口请求Key",  # 您申请的接口API接口请求Key
   }
   params = urllib.parse.urlencode(params_dict)
   req = urllib_request.Request(api_url, params.encode())  # 使用 urllib_request.Request
   response = urllib_request.urlopen(req)
   content = response.read()
   return content.decode('utf-8')

#获取日期列表
def get_date_list(start_date):
    """
    获取日期列表，包括阳历、农历和黄历信息
    """
    # 获取当前日期
    solar_date = Solar(datetime.now().year, datetime.now().month, datetime.now().day)
    lunar_date = Lunar.from_date(solar_date)
    lunar_info = f"农历：{lunar_date.year}年{lunar_date.month}月{lunar_date.day}日"


    # 设置url
    url = 'https://api.shwgij.com/api/lunars/lunarpro?key=您申请的接口API接口请求Key'

    # 发送post请求
    response = requests.post(url, data={'key1': 'value1', 'key2': 'value2'})

    # 获取响应内容
    result = response.json()

    return {
        "start_date": start_date,
        "lunar_info": lunar_info,
        "almanac_info": result
    }

# 注册工具
tools = [
    Tool(
        name="Get Weather",
        func=get_weather,
        description="获取指定城市的天气信息。输入格式：'城市名称'，例如：'北京'"
    ),
    Tool(
        name="Get Date List",
        func=get_date_list,
        description="获取当天，包括阳历、农历和黄历信息。"
    ),
    Tool(
        name="LLM",
        func=llm_main,
        description="使用LLM进行推理对话。输入格式：'问题'，例如：'今天天气如何？'"
    )
]

# 创建记忆缓存
# memory = ConversationBufferMemory()

# 初始化 LLM（例如 OpenAI GPT）
myllm = ChatOpenAI(
    base_url="https://api.deepseek.com",  # API端点
    api_key="您申请的接口API接口请求Key",
    model="deepseek-reasoner",  # 指定推理模型
    temperature=0.3,  # 控制随机性
    max_tokens=256  # 限制输出长度
)

# 初始化 Agent
agents = initialize_agent(
    tools,
    myllm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.route('/api/chat', methods=['POST'])
def chat_handler():
    data = request.get_json()
    user_message = data.get('message', '')

    try:
        # 单轮对话，不传递 chat_history
        response = agents.run({"input": user_message})
    except Exception as e:
        response = f"处理请求时出错：{str(e)}"

    return jsonify({
        "response": response,
        "status": "success"
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)