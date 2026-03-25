"""
测试数据库连接
"""
import pymysql


def test_connection():
    """测试数据库连接"""
    # 使用你的实际密码
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',  # 改成你的密码
        'charset': 'utf8mb4',
    }

    print("正在测试数据库连接...")
    print(f"连接配置: {config['user']}@{config['host']}")

    try:
        # 尝试连接
        conn = pymysql.connect(**config)
        print("✅ 数据库连接成功！")

        # 获取 MySQL 版本
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📦 MySQL 版本: {version[0]}")

            # 查看现有数据库
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"\n📋 现有数据库:")
            for db in databases:
                print(f"  - {db[0]}")

        conn.close()
        return True

    except pymysql.err.OperationalError as e:
        print(f"❌ 连接失败: {e}")
        print("\n可能的原因:")
        print("1. MySQL 服务未启动")
        print("2. 密码不正确")
        print("3. 用户名不正确")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


if __name__ == "__main__":
    test_connection()