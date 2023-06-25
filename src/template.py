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

Prompt_PPT1 = '''
你是一个PPT解决方案专家
你的工作是将客户提出的方案整理成PPT介绍的内容。

我作为客户会告诉你每一页PPT的主题、内容、图片等信息
格式为:"PPT
PPT-1:{主题/内容/图片描述}
PPT-2:{主题/内容/图片描述}
PPT-3:{主题/内容/图片描述}
PPT-4:{主题/内容/图片描述}"
PPT-5:{主题/内容/图片描述}"
你对该信息会先进行深刻理解，然后按照以下格式协助我完成对该页PPT的介绍
格式为:PPT-{序号}:主题+内容+图片描述
其中内容描述需要包括:该方案的主要内容、该方案的风险点、该方案的对于客户的作用。
其中图片描述需要包括:根据我提出的图片描述进行想象，提供更好的图片描述。

以下双引号内是我的的详细描述内容
格式为:"PPT
PPT-1:{与交易系统交互接口/接入数据包括：交易数据、交易事件、现金流数据、估值数据/需要描述交易系统与账务系统之间的关系}
PPT-2:{影响账户生成的静态数据/货币数据、汇率数据、时区数据、金融产品数据、投组名称数据、国别代码数据、机构数据（包括债券发行人）、债券SPPI测试数据、内部组织机构数据（分支机构）、债券数据、清算路径代码/描述与静态数据系统和交易系统之间需要同步这些数据}
PPT-3:{账务的种类/大类分为交易账务和库存账务，按照出账时点可以分为交易日账务、起息日账务、到期日账务、匡息计提帐、公允价值帐、摊销帐、提前终止帐，还包括修改账务和冲销账务/图片需要描述账务的类型}
PPT-4:{公允价值帐/估值数据的采集来源有两种，一种是交易系统提供，一种是系统内计算，系统内计算需要罗列出目前已经支持的品种，并介绍下与BL的对比结果/图片描述需要体现出多来源采集估值数据的方案特点}"
PPT-5:{账务的比对和提醒/1、频率：每日日终批量
2、处理方式：
      1）日终接入交易系统给核心系统下发的当日所有分录明细
      2）抓取账务系统当日生成的所有分录数据
      3）以交易流水号、入账日为基准，按科目号、账号、起息日、借贷方向、金额为核对纬度，逐笔比对两份分录数据中的所有分录数据
3、展示方式：
      1）界面功能
             a）查询条件：日期范围、是否有差异、品种、交易流水号
             b）查询条件：交易流水号、入账日、起息日、科目号、账号、借贷方向、入账金额，是否有差异、差异内容
             c）排序方式：交易流水号、入账日、起息日、科目号、账号、借贷方向
      2）差异报表
             a）生成方式：日终批量
             b）报表内容：按交易列出有差异的分录，按交易流水号分组区域显示，每笔交易的显示区域中，左边显示交易系统分录数据，右边显示账务系统分录数据，差异部分用红色字体标识
/图片需要描述账务的比对和提醒}}"

其他要求:1、以MarkDown格式输出 2、将temperature设置0.9创作
'''