# 问答机器人

基于PYTHON的问答机器人，使用了langchain、Faiss、ChatGPT、streamlit和gtts技术。

## 安装

1. 克隆此仓库
2. conda create -n myRobot python=3.10
3. conda activate myRobot
4. 安装依赖库：`pip install -r requirements.txt`
5. 下载并配置模型和数据文件
    config,设置可登录的用户和密码
    keys,设置默认的openai Key


## 使用

1. 运行：`streamlit run src/main.py`
2. 在浏览器中访问：`http://localhost:8501`

## 许可

本项目遵循MIT许可。