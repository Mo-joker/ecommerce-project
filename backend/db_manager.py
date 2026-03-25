"""
数据库管理工具 - 在 PyCharm 中直接运行
"""
import pymysql
from pymysql.cursors import DictCursor


class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='123456', database='ecommerce'):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }

    def get_connection(self):
        """获取数据库连接"""
        try:
            conn = pymysql.connect(**self.config)
            print(f"✅ 成功连接到数据库: {self.config['database']}")
            return conn
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return None

    def execute_query(self, sql, params=None):
        """执行查询语句"""
        conn = self.get_connection()
        if not conn:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
                conn.commit()
                return result
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def execute_update(self, sql, params=None):
        """执行更新语句"""
        conn = self.get_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                conn.commit()
                print(f"✅ 更新成功，影响 {affected_rows} 行")
                return affected_rows
        except Exception as e:
            print(f"❌ 更新失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def create_database(self, db_name='ecommerce'):
        """创建数据库"""
        conn = pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            charset='utf8mb4'
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ 数据库 {db_name} 创建成功")
        except Exception as e:
            print(f"❌ 创建失败: {e}")
        finally:
            conn.close()


# 使用示例
if __name__ == "__main__":
    db = DatabaseManager()

    # 1. 创建数据库
    db.create_database()

    # 2. 创建表
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        email VARCHAR(100) UNIQUE NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        hashed_password VARCHAR(200) NOT NULL,
        full_name VARCHAR(100),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    db.execute_update(create_users_table)

    # 3. 插入测试数据
    insert_user = """
    INSERT INTO users (email, username, hashed_password, full_name) 
    VALUES (%s, %s, %s, %s)
    """
    # 注意：这里密码应该是加密的
    db.execute_update(insert_user, ('test@example.com', 'testuser', 'hashed_password', '测试用户'))

    # 4. 查询数据
    users = db.execute_query("SELECT * FROM users")
    for user in users:
        print(user)