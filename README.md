# 问答机器人

基于PYTHON的问答机器人，使用了langchain、Faiss、ChatGPT、streamlit和gtts技术。
## 安装
1. 克隆此仓库
2. conda create -n myRobot python=3.10
3. conda activate myRobot
4. 安装依赖库：`pip install -r requirements.txt`
5. 下载并配置模型和数据文件
    config,设置可模块和密码
    keys,设置默认的openai Key
## 使用
1. 运行：`streamlit run src/main.py`
2. 在浏览器中访问：`http://localhost:8501`
3、向量数据保存在dbf/模块名，每个模块的数据都会保存在同一个index里。
4、上传文件的切片目前暂时设定为200，0，可以根据文档的大小进行调整。
5、max_context_tokens暂时设定为-1
6、k值目前在代码里写了3，每次向量数据库查询获取3份文件。
7、每次上传后备份文件在bak目录


## 许可

本项目遵循MIT许可。
