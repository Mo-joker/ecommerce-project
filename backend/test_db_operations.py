"""
测试数据库操作
"""
from app.core.database import SessionLocal
from app.models.users import User
from app.core.security import get_password_hash


def test_create_user():
    """测试创建用户"""
    db = SessionLocal()
    try:
        # 创建用户
        user = User(
            username="testuser2",
            email="test2@example.com",
            hashed_password=get_password_hash("123456"),
            full_name="测试用户2"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ 用户创建成功: ID={user.id}, 用户名={user.username}")
        return user
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        db.rollback()
    finally:
        db.close()


def test_query_users():
    """测试查询用户"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\n📋 用户列表 (共 {len(users)} 个):")
        for user in users:
            print(f"  - ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
    finally:
        db.close()


def test_update_user(user_id, new_name):
    """测试更新用户"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.full_name = new_name
            db.commit()
            print(f"✅ 用户更新成功: {user.username} -> {new_name}")
        else:
            print(f"❌ 用户 ID {user_id} 不存在")
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        db.rollback()
    finally:
        db.close()


def test_delete_user(user_id):
    """测试删除用户"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            print(f"✅ 用户删除成功: {user.username}")
        else:
            print(f"❌ 用户 ID {user_id} 不存在")
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=== 数据库操作测试 ===\n")

    # 测试创建
    test_create_user()

    # 测试查询
    test_query_users()

    # 测试更新
    test_update_user(1, "更新的用户名")

    # 再次查询验证
    test_query_users()