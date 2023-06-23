
from FaissDB_Utils import FaissDB_Utils
from keys import OpenAI_API_KEY

faissDB_Utils = FaissDB_Utils(api_key=OpenAI_API_KEY)

# 从文件创建或导入到数据库
db = faissDB_Utils.create_or_import_to_db('data/liudongxingpipei.docx', persist_directory='dbf')

# 查询数据
query = "流动性匹配率的公式？"
results = faissDB_Utils.search_documents(persist_directory='dbf', query=query)

for i, result in enumerate(results):
    print(f"Result {i + 1}:")
    print(result.page_content)
    print("\n")