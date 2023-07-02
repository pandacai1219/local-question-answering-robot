
import pypinyin


def get_pinyin(chinese_str):
    pinyin_list = pypinyin.lazy_pinyin(chinese_str)
    pinyin_str = ''.join(pinyin_list)
    return pinyin_str


#对chinese_to_english进行单元测试
print(get_pinyin(chinese_str="流动性匹配率"))
