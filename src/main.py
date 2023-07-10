import time
import streamlit as st
import gtts

from FaissDB_Utils import FaissDB_Utils
from config import config

import os
import chardet

from langchain.callbacks import get_openai_callback
from template import prompt_template_Document, prompt_template_GPT
from keys import OpenAI_API_KEY2
from nameFormat import NameFormat
from logger_config import logger

# 设置streamlit页面
st.set_page_config(
    page_title="问答机器人",
    page_icon="./assets/robet.ico",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown('<style>' + open('./assets/styles.css',encoding='utf-8').read() + '</style>', unsafe_allow_html=True)
# 添加标题图片
st.image("./assets/title_image.jpg", width=50)
# 创建登录表单
def login():
    with st.form(key='login_form'):
        st.header("模块登录")
        username_input = st.text_input("知识库名称", "", key="username_input")
        password_input = st.text_input("密码", "", key="password_input", type="password")
        submit_button = st.form_submit_button("登录")
        if submit_button:
            process_login(username_input, password_input)
          
def process_login(username, password):
    for user_key in config["users"]:
        user = config["users"][user_key]
        if username == user["username"] and password == user["password"]:
            st.session_state.username = username
            st.session_state.logged_in = True
            break
    else:
        st.error("知识库名称或密码错误")      
      
def values_to_session_state(st, values):
    #对以下代码创建一个公共方法
    if "temperature" not in st.session_state:
          st.session_state.temperature = values['temperature']
    if "max_context_tokens" not in st.session_state:
          st.session_state.max_context_tokens = values['max_context_tokens']
    if "max_response_tokens" not in st.session_state:
          st.session_state.max_response_tokens = values['max_response_tokens']
    if "file_chunk_size" not in st.session_state:
          st.session_state.file_chunk_size = values['file_chunk_size']
    if "api_key" not in st.session_state:
          st.session_state.api_key = values['api_key']

# 使用Streamlit auth模块控制应用程序的访问权限
if not st.session_state.get('logged_in', False):
    # 如果用户未登录，则显示登录表单
    login()
else:
    # 如果用户已登录，则显示应用程序内容
    st.write(f"欢迎回来，{st.session_state.username}！")
    logger.info(f"欢迎回来，{st.session_state.username}！")
    # 页面标题
    st.title("问答机器人")

    # 创建复选框，使用函数设置标签
    is_suggestion = st.checkbox("回答是否超出本地文档",value=False, key="is_suggestion")

    # 根据复选框状态，选择使用哪种搜索方式
    st.session_state.prompt_template = prompt_template_Document
    if is_suggestion:
        # 使用联想搜索方式
        st.session_state.prompt_template = prompt_template_GPT
        logger.info("使用联想搜索方式")
    else:
        # 使用精确搜索方式
        st.session_state.prompt_template = prompt_template_Document
        logger.info("使用精确搜索方式")
    logger.info(st.session_state.prompt_template)
    #相关参数提供默认值
    values = {'temperature': 0.5, 'max_context_tokens': -1, 'max_response_tokens': -1, 'file_chunk_size': 200,'api_key':OpenAI_API_KEY2}
    values_to_session_state(st, values)
    # 用户输入
    question = st.text_input("请输入您的问题:", "", key="question_input")
    # 添加一个按钮来触发 read_doc_file 函数
    username = st.session_state.username
    # 提交按钮
    my_bar = st.progress(0, text="等待投喂问题")
    if st.button("提交", key="submit_button"):
        if question:
          logger.info("0-Loading..." + str(question))
          st.session_state.faissDB_Utils = FaissDB_Utils(prompt_template=st.session_state.prompt_template,temperature=st.session_state.temperature,max_context_tokens=st.session_state.max_context_tokens,max_response_tokens=st.session_state.max_response_tokens,file_chunk_size=st.session_state.file_chunk_size,api_key=st.session_state.api_key)
          langchain_util = st.session_state.faissDB_Utils
          llm = langchain_util.llm
          logger.info("1-Loading question answering chain..." + str(llm))
          my_bar.progress(10, text="正在加载问题回答模型")
          try:
              logger.info("username:"+username)
              docsearch = langchain_util.search_documents(query=question, userName=username)
              logger.info("2-Searching for similar documents..." + str(docsearch))
          
              my_bar.progress(50, text="正在加载问题回答模型")
              chain = langchain_util.chain
              logger.info("3-Answering question..." + str(chain))
              my_bar.progress(80, text="正在回答问题")
              with get_openai_callback() as cb:
                answer = chain.run(input_documents=docsearch, question=question, verbose=True)
              logger.info("4-Answering question..." + str(answer))
              my_bar.progress(100, text="问题回答完毕")

              st.success(answer,icon="🤖")
              
              #查询文件的内容以及对应的原文件
              faiss_research= ""
              for i, result in enumerate(docsearch):
                file_path = result.metadata['source']
                file_name = file_path.split('/')[-1]  # 使用分隔符 '/' 分割路径并获取最后一个部分作为文件名
                faiss_research=faiss_research+"\n"+result.page_content+"\n"+file_name;
              
              with st.expander('相关材料'):
                  st.info(faiss_research)
              with st.expander('使用模板'):
                  st.info(st.session_state.prompt_template)
              with st.expander('消费金额'):
                  st.write(f"总令牌数: {cb.total_tokens}")
                  st.write(f"提示令牌数: {cb.prompt_tokens}")
                  st.write(f"完成令牌数: {cb.completion_tokens}")
                  st.write(f"总成本: {cb.total_cost} 美元")

              # 将答案转换为语音并播放
              if answer:
                audio = gtts.gTTS(answer, lang='zh-cn')
                audio.save('answer.wav')
                st.audio('answer.wav', start_time=0)
                #删除answer.wav文件
                os.remove('answer.wav')
          except Exception as e:
              st.write(f"Error answering question: {e}")
              logger.error(f"Error answering question: {e}")
        else:
            st.warning("请输入问题。")

    # Create the container and progress bars


    with st.sidebar:
        expander = st.expander("可展开/可折叠", expanded=True)
        expander.write("参数")
        with expander:
          with st.form("settings_form"):
              #st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
              #temperature = st.slider("温度", min_value=0.0, max_value=1.0, step=0.05, value=0.7)
              #st.markdown("</div>", unsafe_allow_html=True)
              
              #st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
              #max_context_tokens = st.slider("上下文最大的Token数", min_value=500, max_value=4096, step=200, value=1024)
              #st.markdown("</div>", unsafe_allow_html=True)
              
              #st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
              #max_response_tokens = st.slider("每个回复的最大Token数", min_value=256, max_value=4096, step=200, value=500)
              #st.markdown("</div>", unsafe_allow_html=True)

              st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
              file_chunk_size = st.slider("切分每份文件的大小", min_value=50, max_value=1000, step=50, value=200)
              st.markdown("</div>", unsafe_allow_html=True)

              #To add an input box for the API key
              api_key = st.text_input("API Key", "")

              submit_button = st.form_submit_button("设置")

    if submit_button:
        # Update variables with the current slider values
        #values['temperature'] = temperature
        #values['max_context_tokens'] = max_context_tokens
        #values['max_response_tokens'] = max_response_tokens
        values['file_chunk_size'] = file_chunk_size
        values['api_key'] = api_key
        values_to_session_state(st, values)

        # Display the current values
        #st.sidebar.write(f"温度: {values['temperature']}")
        #st.sidebar.write(f"上下文最大的Token数: {values['max_context_tokens']}")
        st.sidebar.write(f"每个回复的最大Token数: {values['max_response_tokens']}")
        st.sidebar.write(f"切分每份文件的大小: {values['file_chunk_size']}")
        st.sidebar.write(f"API KEY:{values['api_key']}")

        # Pause for a short period to avoid high CPU usage
        time.sleep(0.1)




    if st.sidebar.button("data/file批量上传", key="batch_button"):
        logger.info("Start Batch import")
        # 读取文档
        st.session_state.faissDB_Utils = FaissDB_Utils(prompt_template=st.session_state.prompt_template,temperature=st.session_state.temperature,max_context_tokens=st.session_state.max_context_tokens,max_response_tokens=st.session_state.max_response_tokens,file_chunk_size=st.session_state.file_chunk_size,api_key=st.session_state.api_key)
        st.session_state.faissDB_Utils.path_to_db(directory_path="data/file",  userName=username)
        #将data文件夹中的所有文件迁移至BAK文件夹
        for filename in os.listdir("data/file"):
            #忽略没有后缀的文件夹
            if not os.path.splitext(filename)[1]:
                continue
            with open(os.path.join("data/file", filename), "rb") as f:
                data = f.read()
                result = chardet.detect(data)
                file_encoding = result['encoding']
                logger.info(file_encoding)              
            with open(os.path.join("bak", filename), "wb") as f: 
                f.write(data)
            newFileName=NameFormat.format(name=filename)
            NameFormat.rename(os.path.join("bak", filename),os.path.join("bak", newFileName))
              
          #删除data文件夹下的所有文件
        try:
            for root, dirs, files in os.walk("data/file", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except Exception as e:
              st.write(f"Error answering question: {e}")
          #streamlit输出提示“文件上传成功”
        st.success("文件上传成功,被切割成"+str(st.session_state.faissDB_Utils.docCount)+"个片段。")     

        
    # 使用 file_uploader 函数添加文件上传部件
    uploaded_file = st.sidebar.file_uploader("上传文件", type=["docx","doc", "pdf", "txt","csv"])

    # 如果有文件被上传，则在右侧栏中显示文件信息
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name}

        st.sidebar.write(file_details)
        # 添加一个按钮来触发 read_doc_file 函数
        if st.sidebar.button("单文件提交", key="single_button"):
          # 将上传的文件保存到项目主目录的data文件夹中
          with open(os.path.join("data/file", uploaded_file.name), "wb") as f:
              f.write(uploaded_file.getbuffer())
              st.session_state.faissDB_Utils = FaissDB_Utils(prompt_template=st.session_state.prompt_template,temperature=st.session_state.temperature,max_context_tokens=st.session_state.max_context_tokens,max_response_tokens=st.session_state.max_response_tokens,file_chunk_size=st.session_state.file_chunk_size,api_key=st.session_state.api_key)
          logger.info("1-Reading document...") 
          logger.info(file_details)
          # 读取文档
          file_path=os.path.join("data/file", uploaded_file.name)
          st.session_state.faissDB_Utils.create_or_import_to_db(file_path=file_path, filename=uploaded_file.name, userName=username)
          #将data文件夹中的文件迁移至BAK文件夹
          with open(os.path.join("data/file", uploaded_file.name), "rb") as f:
              data = f.read()
              result = chardet.detect(data)
              file_encoding = result['encoding']
              logger.info(file_encoding)              
          with open(os.path.join("bak", uploaded_file.name), "wb") as f: 
              f.write(data)
          newFileName=NameFormat.format(name=uploaded_file.name)
          NameFormat.rename(os.path.join("bak", uploaded_file.name),os.path.join("bak", newFileName))
          #删除data文件夹下的所有文件
          try:
            for root, dirs, files in os.walk("data/file", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
          except Exception as e:
              st.write(f"Error answering question: {e}")
          #streamlit输出提示“文件上传成功”
          st.success("文件上传成功"+str(file_details)+",被切割成"+str(st.session_state.faissDB_Utils.docCount)+"个片段。")

        
          
