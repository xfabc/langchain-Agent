from geopy.geocoders import Nominatim

import urllib
from urllib import request as urllib_request
import urllib.parse

def get_weather(city=None):
   """

   :param city:
   :return:
   """
   print(type(city))
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

print(get_weather('福州'))

