
from nameFormat import NameFormat

from FaissDB_Utils import FaissDB_Utils
from keys import OpenAI_API_KEY



faissDB_Utils = FaissDB_Utils(api_key=OpenAI_API_KEY)




persist_directory='liudongxingpipei'
filename=NameFormat.format(name=persist_directory)

db = faissDB_Utils.create_or_import_to_db('data/file/liudongxingpipei.docx',filename=filename, userName='clw')

# 查询数据
query = "流动性覆盖率的公式？"
results = faissDB_Utils.search_documents(query=query, userName='clw')

for i, result in enumerate(results):
    print(f"Result {i + 1}:")
    print(result.page_content)
    print("\n")