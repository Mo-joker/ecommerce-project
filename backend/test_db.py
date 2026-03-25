"""
测试数据库连接
右键运行这个文件测试数据库是否正常
"""
import pymysql


def test_connection():
    """测试数据库连接"""
    try:
        # 尝试连接数据库
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='ecommerce',
            charset='utf8mb4'
        )

        print("✅ 数据库连接成功！")

        # 执行简单查询
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📦 MySQL 版本: {version[0]}")

            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"🗄️  当前数据库: {db_name[0]}")

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 数据表数量: {len(tables)}")

            if tables:
                print("数据表列表:")
                for table in tables:
                    print(f"  - {table[0]}")

        conn.close()
        print("\n🎉 一切正常！")

    except pymysql.err.OperationalError as e:
        print(f"❌ 连接失败: {e}")
        print("\n请检查:")
        print("1. MySQL 服务是否已启动")
        print("2. 用户名和密码是否正确")
        print("3. 数据库是否存在")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    test_connection()