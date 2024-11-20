# 1. 演示使用提示词，让模型回答问题、推理、生成、摘要等任务。

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load the API key from the .env file 从.env文件中加载API密钥
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# "Prompt"是指在使用大型语言模型（LLM）时提供给模型的输入文本或指令。
# 这可以是一个问题、一个描述或一个任务说明，目的是引导模型生成相关的文本输出。
# Prompt的质量和清晰度对于获得满意的模型输出至关重要，因为它直接影响了模型对任务或问题的理解和响应。
prompt = ChatPromptTemplate.from_messages([ 
    ("system", "You are a warm hearted AI assistant."), # "system"是指在对话系统中代表“上帝视角”的环境、人设信息。可以提供性格设定、功能限制、对话流程、输出格式等信息。
    ("user", "{input}") # "user"是指在对话系统中代表用户的角色或信息。它通常用于提供用户输入、需求、问题、反馈等信息。一般受到system的限制，但也存在失效的可能。
])

# Model: Create the OpenAI chatbot 创建聊天机器人
model = ChatOpenAI(name="gpt-4o-mini") 
# model = ChatOpenAI(name="gpt-4o") 

# OutputParser: Create an output parser 创建输出解析器
parser = StrOutputParser()

# Chain: Create and invoke a chain 创建并调用链
chain = prompt | model | parser

# 回答问题
# _prompt = "你好，我想成为一个大语言模型应用程序员，请问我应该学习哪些知识？(用列表回答)"

# 推理
# _prompt = "你好，我是一个程序员，名字叫陈小明，大家都叫我小明。我会Python和Java。请问我是谁？(只回答名字)"
# _prompt = "小明有一个哥哥叫大毛，还有一个弟弟叫小毛，那么小明叫什么？" # gpt-4o-mini 有时无法正确回答，有时可以

# 生成
# _prompt = "你好，我是一个程序员，名字叫陈小明，大家都叫我小明。请问我是谁？(用json结构回答)"
# _prompt = """我认识一个朋友叫王明，可以通过13800138000联系到他。他住在北京市朝阳区酒仙桥中路10号电子城IT产业园区B座801室，邮编是100016。
#     (用json结构回答，包含name, mobile, city, dictrict, details_address, zipcode这几个字段)
#     """

# 摘要
# _prompt = """请用白话文150字总结以下诗歌内容，尤其是诗人自身的情感：\n
# 浔阳江头夜送客，枫叶荻花秋瑟瑟。主人下马客在船，举酒欲饮无管弦。醉不成欢惨将别，别时茫茫江浸月。
# 忽闻水上琵琶声，主人忘归客不发。寻声暗问弹者谁，琵琶声停欲语迟。移船相近邀相见，添酒回灯重开宴。千呼万唤始出来，犹抱琵琶半遮面。转轴拨弦三两声，未成曲调先有情。弦弦掩抑声声思，似诉平生不得志。低眉信手续续弹，说尽心中无限事。轻拢慢捻抹复挑，初为《霓裳》后《六幺》。大弦嘈嘈如急雨，小弦切切如私语。嘈嘈切切错杂弹，大珠小珠落玉盘。间关莺语花底滑，幽咽泉流冰下难。冰泉冷涩弦凝绝，凝绝不通声暂歇。别有幽愁暗恨生，此时无声胜有声。银瓶乍破水浆迸，铁骑突出刀枪鸣。曲终收拨当心画，四弦一声如裂帛。东船西舫悄无言，唯见江心秋月白。
# 沉吟放拨插弦中，整顿衣裳起敛容。自言本是京城女，家在虾蟆陵下住。十三学得琵琶成，名属教坊第一部。曲罢曾教善才服，妆成每被秋娘妒。五陵年少争缠头，一曲红绡不知数。钿头银篦击节碎，血色罗裙翻酒污。今年欢笑复明年，秋月春风等闲度。弟走从军阿姨死，暮去朝来颜色故。门前冷落鞍马稀，老大嫁作商人妇。商人重利轻别离，前月浮梁买茶去。去来江口守空船，绕船月明江水寒。夜深忽梦少年事，梦啼妆泪红阑干。
# 我闻琵琶已叹息，又闻此语重唧唧。同是天涯沦落人，相逢何必曾相识！我从去年辞帝京，谪居卧病浔阳城。浔阳地僻无音乐，终岁不闻丝竹声。住近湓江地低湿，黄芦苦竹绕宅生。其间旦暮闻何物？杜鹃啼血猿哀鸣。春江花朝秋月夜，往往取酒还独倾。岂无山歌与村笛？呕哑嘲哳难为听。今夜闻君琵琶语，如听仙乐耳暂明。莫辞更坐弹一曲，为君翻作《琵琶行》。感我此言良久立，却坐促弦弦转急。凄凄不似向前声，满座重闻皆掩泣。座中泣下谁最多？江州司马青衫湿。
# """

# 数学计算（LLM的数学计算能力有限，不建议使用。如有需要，参考后期的agent与tools部分。）
_prompt = "请问121+212等于多少？"

result = chain.invoke({"input": _prompt})

# Print the response 打印回复
print(result)