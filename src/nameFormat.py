import unicodedata

import pypinyin

import os

class NameFormat:
    @staticmethod
    def get_pinyin(chinese_str):
        pinyin_list = pypinyin.lazy_pinyin(chinese_str)
        pinyin_str = ''.join(pinyin_list)
        return pinyin_str
    @staticmethod
    def is_chinese(characters):
        try:
            return 'CJK UNIFIED' in unicodedata.name(characters)
        except ValueError:
            return False
    @staticmethod
    def format(name):    
        isEnglish = False
        for char in name:
            if NameFormat.is_chinese(characters=char):
                print(f"{char} 是中文")
                isEnglish = True

        #判断是否为中文
        filename=name
        if isEnglish:
            #转换成英文
            filename = NameFormat.get_pinyin(chinese_str=name)
            print(f"persist_directory：{filename}")
        return filename
    
    #将文件名改为newFileName
    @staticmethod
    def rename(oldFileName,newFileName):
        os.rename(oldFileName,newFileName)
        print("修改成功!")

