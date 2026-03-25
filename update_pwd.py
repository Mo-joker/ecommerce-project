"""
更新数据库中用户的密码哈希
"""
import pymysql
import bcrypt

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'ecommerce',
    'charset': 'utf8mb4'
}


def hash_password(password: str) -> str:
    """使用 bcrypt 加密密码"""
    # 确保密码不超过 72 字节
    password_bytes = password.encode('utf-8')[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def update_passwords():
    """更新用户密码"""

    print("更新用户密码...")

    try:
        conn = pymysql.connect(**DB_CONFIG)

        with conn.cursor() as cursor:
            # 更新 testuser 的密码
            new_hash = hash_password('123456')
            cursor.execute(
                "UPDATE users SET hashed_password = %s WHERE username = %s",
                (new_hash, 'testuser')
            )
            print(f"✅ 更新 testuser 密码")

            # 更新 admin 的密码
            new_hash = hash_password('admin123')
            cursor.execute(
                "UPDATE users SET hashed_password = %s WHERE username = %s",
                (new_hash, 'admin')
            )
            print(f"✅ 更新 admin 密码")

            conn.commit()
            print("\n🎉 密码更新完成！")

    except Exception as e:
        print(f"❌ 更新失败：{e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    update_passwords()