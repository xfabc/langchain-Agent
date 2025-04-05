from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from getpass import getpass  # 安全输入API Key
from langchain_community.llms import Ollama
# 配置DeepSeek API
# api_key = getpass("请输入DeepSeek API Key: ")  # 安全输入密钥

# 创建自定义LLM对象
llm = ChatOpenAI(
    base_url="https://api.deepseek.com",  # API端点
    api_key="您申请的接口API接口请求Key",
    model="deepseek-reasoner",  # 指定推理模型
    temperature=0.3,  # 控制随机性
    max_tokens=256  # 限制输出长度
)

# 定义不同任务类型的系统提示词
system_prompts = {
    "reasoning": '''
你是一个智能分析助手：
【推理指令】
请对提供的问题进行逻辑推理并给出详细的解释。
'''}

# 根据任务类型创建提示词模板
def create_prompt_template(task_type):
    prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompts[task_type]),
            ("user", "{question}"),
        ])

    return prompt_template

# 创建处理链函数
def create_chain(prompt_template):
    return prompt_template | llm

def main(question):
    try:
        while True:
            # 获取用户输入
            # user_input = input("\n请输入您的问题（输入q退出）: ").strip()
            user_input = question
            if user_input.lower() == "q":
                break

            task_type = "reasoning"
            formatted_question = user_input


            # 创建相应的提示词模板并生成处理链
            prompt_template = create_prompt_template(task_type)
            chain = create_chain(prompt_template)

            # 执行链式调用
            response = chain.invoke({"question": formatted_question})

            # 输出结果
            # print("\n[思考过程]")
            # print(response.content)
            return response.content

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()