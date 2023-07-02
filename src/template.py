# 使用精确搜索方式
prompt_template_Document ='''Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        the answer must be chinese.
        {context}

        Question: {question}
        Answer:
        '''
# 使用联想搜索方式
prompt_template_GPT ='''Prioritize finding answers from the context. When it is discovered that the question is related to the context and requires breaking through the context limitations, forget the context content and re-consult GPT to obtain the answer.
        {context}

        Question: {question}
        Answer:
        '''

#根据现有知识回答问题
prompt_template_CS ='''I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".

Q: What is human life expectancy in the United States?
A: Human life expectancy in the United States is 78 years.

Q: Who was president of the United States in 1955?
A: Dwight D. Eisenhower was president of the United States in 1955.

Q: Which party did he belong to?
A: He belonged to the Republican Party.

Q: What is the square root of banana?
A: Unknown

Q: How does a telescope work?
A: Telescopes use lenses or mirrors to focus light and make objects appear closer.

Q: Where were the 1992 Olympics held?
A: The 1992 Olympics were held in Barcelona, Spain.

Q: How many squigs are in a bonk?
A: Unknown

Q: Where is the Valley of Kings?
A:'''


prompt_template_CSCH ='''我是一个高度智能的问答机器人。如果你问我一个基于事实的问题，我会给你答案。如果你问我一个无稽之谈、欺骗性的问题或者没有明确答案的问题，我会回答“未知”。

问：美国人的预期寿命是多少？
答：美国人的预期寿命是 78 岁。

问：1955 年美国总统是谁？
答：德怀特·D·艾森豪威尔 (Dwight D. Eisenhower) 1955 年担任美国总统。

问：他属于哪个党派？
答：他属于共和党。

问：香蕉的平方根是多少？
答：未知 

问：望远镜如何工作？
答：望远镜使用透镜或镜子来聚焦光线，使物体看起来更近。

问：1992年奥运会在哪里举行？
答：1992年奥运会在西班牙巴塞罗那举行。

问：一堆史奎格有多少只？
答：未知 

问：帝王谷在哪里？
A：'''

#Convert movie titles into emoji.
prompt_template_emoji ='''Convert movie titles into emoji.

Back to the Future: 👨👴🚗🕒 
Batman: 🤵🦇 
Transformers: 🚗🤖 
Star Wars:'''

  
#病情检查
prompt_template_bqxw ='''
请扮演一名医生，帮病人分析每个指数的可能影响，一步一步的分析，并在指数分析和病情总结里填写内容。
医生岗位：{Doctor information}
病人近期信息：{Patient information}.
上升的指数如下：{context2}.
指数分析：
病情总结：
'''

#方案编写
Prompt = '''
你是一个解决方案专家
你的工作是将客户的系统需求通过简单的描述转化为行业通用的功能并总结出该服务的价值。

我作为客户会告诉你系统名称、一级功能名称、二级功能名称等系统功能清单
格式为:"系统名称:{功能A(功能C、功能D)功能B(功能E、功能F...)}"
你对该信息会先进行深刻理解，然后按照以下格式协助我完成对于二级功能进行使用场景及服务的描述写作
格式为:系统名称、一级功能、二级功能、二级功能服务描述
其中二级功能服务描述需要包含:针对的客户对象、应用的场景、服务的价值。

以下双引号内是我的系统功能清单
"{系统功能清单}"
以下双引号内是该系统的参考信息
"{系统及功能参考信息]}"

其他要求:1、以MarkDown格式输出 2、将temperature设置0.9创作 3、参考信息内容需要进行二次创作，不要直接使用。
'''

#PPT介绍方案
Prompt_PPT = '''
你是一个解决方案专家
你的工作是将客户提出的方案整理成PPT介绍的内容。

我作为客户会告诉你每一页PPT的主题、内容、图片等信息
格式为:"PPT-{序号}:{主题+内容+图片描述}"
你对该信息会先进行深刻理解，然后按照以下格式协助我完成对该页PPT的介绍
格式为:PPT-{序号}:主题+内容+图片描述
其中内容描述需要包括:该方案的主要内容、该方案的风险点、该方案的对于客户的作用。
其中图片描述需要包括:根据我提出的图片描述进行想象，提供更好的图片描述。

以下双引号内是我的系统功能清单
"{系统功能清单}"
以下双引号内是该系统的参考信息
"{系统及功能参考信息]}"

其他要求:1、以MarkDown格式输出 2、将temperature设置0.9创作 3、参考信息内容需要进行二次创作，不要直接使用。
'''


Prompt_Graphviz = '''我需要一个使用Graphviz创建的数据流程图。数据流程图应该包含以下元素：

- 数据源：{数据源名称}
- 处理步骤1：{步骤1名称}，输入为{步骤1输入}，输出为{步骤1输出}
- 处理步骤2：{步骤2名称}，输入为{步骤2输入}，输出为{步骤2输出}
- 数据输出：{数据输出名称}

请为我生成一个.dot文件的代码示例。谢谢！
'''

'''我需要一个使用Graphviz创建的数据流程图。数据流程图应该包含以下元素：

- 数据源：MUREX
- 
- 处理步骤1：{步骤1名称}，输入为{步骤1输入}，输出为{步骤1输出}
- 处理步骤2：{步骤2名称}，输入为{步骤2输入}，输出为{步骤2输出}
- 数据输出：{数据输出名称}

请为我生成一个.dot文件的代码示例。谢谢！
'''