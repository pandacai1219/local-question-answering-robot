import configparser

# 读取config.py文件中的用户名和密码
def get_username_password(user):
    config = configparser.ConfigParser()
    config.read('config.py')
    username = config[user]['username']
    password = config[user]['password']
    return username, password