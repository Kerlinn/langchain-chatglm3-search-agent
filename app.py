from langchain_community.llms.chatglm3 import ChatGLM3

glm = ChatGLM3(
    endpoint_url="http://127.0.0.1:8000/v1/chat/completions",
    temperature = 0,
    top_p = 0.9
)
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMRequestsChain

prompt = PromptTemplate.from_template('''
请根据如下搜索结果，回答用户问题。
-----------搜索结果---------
{requests_result}
------------答案------------
问题：{question}
回答：
''')

llm_chain = LLMChain(llm=glm, prompt=prompt, verbose=True)

chain = LLMRequestsChain(llm_chain=llm_chain)

question = '小米SU7有哪些配置，价格是多少？'

# 这里搜索引擎用的是360搜索，也可根据需要替换成其他搜索引擎的API或者调用方式
# 谷歌搜索(需要加载模型之后再科学上网)：'https://www.google.com/s?q='
inputs = {
    'question': question,
    'url': 'https://www.so.com/s?q=' + question.replace(' ', '+')
}

result = chain.invoke(inputs)
# {'question': '小米SU7有哪些配置，价格是多少？', 'url': 'https://www.so.com/s?q=小米SU7有哪些配置，价格是多少？', 'output': '小米SU7有以下配置：\n1. 普通版：售价21.59万元；\n2. Pro版：售价25.99万元；\n3. Max版：售价29.99万元；\n4. FE版：售价21.99万元。\n请注意，以上价格仅供参考，实际购买价格可能因渠道、促销活动等原因有所不同。'}

# 输出的result是json格式，选择其中的output来输出
print(result['output'])
# > Finished chain.
# 小米SU7有以下配置：
# 1. 普通版：售价21.59万元；
# 2. Pro版：售价25.99万元；
# 3. Max版：售价29.99万元；
# 4. FE版：售价21.99万元。
# 请注意，以上价格仅供参考，实际购买价格可能因渠道、促销活动等原因有所不同。
