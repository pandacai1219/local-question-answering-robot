import logging
from logging.handlers import RotatingFileHandler

def configure_logger():
   # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,  # 设置日志级别为ERROR或更高级别
        format="%(asctime)s - %(levelname)s - %(message)s",  # 日志记录格式
        datefmt="%Y-%m-%d %H:%M:%S"  # 日期时间格式

    )

    # 创建日志记录器
    logger = logging.getLogger()

    # 创建文件处理程序，进行日志轮转
    file_handler = RotatingFileHandler("./log/app.log", maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(logging.INFO)  # 设置文件处理程序的日志级别为ERROR
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # 文件日志记录格式
    file_handler.setFormatter(file_formatter)

    # 添加文件处理程序到日志记录器
    logger.addHandler(file_handler)

    return logger

# 在需要记录日志的地方导入并使用logger
logger = configure_logger()

