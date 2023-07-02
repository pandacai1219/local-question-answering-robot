import sqlite3

class DatabaseOperations:
    def __init__(self):
        self.conn = self.connect_to_database()
        
        # 检查文件名表是否存在，如果不存在则创建
        if not self.check_files_table_exists():
            self.create_files_table()

        # 检查历史问答表是否存在，如果不存在则创建
        if not self.check_qa_history_table_exists():
            self.create_qa_history_table()
    
    # 连接到数据库（如果数据库不存在，则会创建一个新的数据库）
    def connect_to_database(self):
        conn = sqlite3.connect('data/sqldata/database.db')
        return conn
    
        # 检查文件名表是否存在
    def check_files_table_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files';")
        result = cursor.fetchone()
        return result is not None
        
    # 检查文件名表是否存在
    def check_files_table_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files';")
        result = cursor.fetchone()
        return result is not None
    
    # 检查历史问答表是否存在
    def check_qa_history_table_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='qa_history';")
        result = cursor.fetchone()
        return result is not None
    
    # 创建文件名表
    def create_files_table(self):
        self.conn.execute('''CREATE TABLE files (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stored_filename TEXT NOT NULL,
                            current_filename TEXT NOT NULL,
                            insert_datetime TEXT NOT NULL,
                            operator TEXT NOT NULL
                        );''')
    
    # 创建历史问答表
    def create_qa_history_table(self):
        self.conn.execute('''CREATE TABLE qa_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question TEXT NOT NULL,
                            answer TEXT NOT NULL,
                            insert_datetime TEXT NOT NULL,
                            questioner TEXT NOT NULL
                        );''')
    
    # 插入文件名数据
    def insert_file_data(self, stored_filename, current_filename, insert_datetime, operator):
        self.conn.execute("INSERT INTO files (stored_filename, current_filename, insert_datetime, operator) VALUES (?, ?, ?, ?)",
                          (stored_filename, current_filename, insert_datetime, operator))
        self.conn.commit()
    
    # 插入历史问答数据
    def insert_qa_data(self, question, answer, insert_datetime, questioner):
        self.conn.execute("INSERT INTO qa_history (question, answer, insert_datetime, questioner) VALUES (?, ?, ?, ?)",
                          (question, answer, insert_datetime, questioner))
        self.conn.commit()
    
    # 查询文件名数据
    def get_file_data(self):
        cursor = self.conn.execute("SELECT * FROM files")
        data = cursor.fetchall()
        return data
    
    # 查询历史问答数据
    def get_qa_data(self):
        cursor = self.conn.execute("SELECT * FROM qa_history")
        data = cursor.fetchall()
        return data
    
    # 关闭数据库连接
    def close_connection(self):
        self.conn.close()
