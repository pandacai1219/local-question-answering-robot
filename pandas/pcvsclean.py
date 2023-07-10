import pandas as pd
df = pd.read_csv('./data/file/wiki5.csv')

#同一个title下删除重复行数据，保留version最大的行数据
df = df.sort_values('version', ascending=False)  # 按version降序排序
df = df.drop_duplicates(['title'])
#删除重复行后，重置索引
df = df.reset_index(drop=True)
#将处理后的数据重新写入csv文件
df.to_csv('./data/file/wiki5-N.csv',index=False)


print(df)