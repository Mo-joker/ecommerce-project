"""
修复后的数据库初始化脚本
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.core.security import get_password_hash
from sqlalchemy.orm import Session


def init_database():
    """初始化数据库"""
    print("🚀 开始初始化数据库...")
    print("=" * 50)

    try:
        # 导入所有模型（这很重要！）
        from app.models import User, Product, Category, Order, OrderItem, CartItem

        # 1. 创建所有表
        print("📦 创建数据表...")
        Base.metadata.drop_all(bind=engine)  # 先删除所有表（谨慎使用）
        Base.metadata.create_all(bind=engine)
        print("✅ 数据表创建成功")

        # 2. 插入测试数据
        print("\n📝 插入测试数据...")
        db = Session(bind=engine)

        # 创建用户
        print("创建用户...")
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("123456"),
            full_name="测试用户",
            is_active=True
        )
        db.add(test_user)

        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="管理员",
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ 用户创建成功")

        # 创建分类
        print("创建分类...")
        categories = [
            Category(name="电子产品", sort_order=1),
            Category(name="服装", sort_order=2),
            Category(name="家居用品", sort_order=3),
        ]
        for cat in categories:
            db.add(cat)
        db.commit()
        print("✅ 分类创建成功")

        # 获取分类ID
        electronics = db.query(Category).filter(Category.name == "电子产品").first()
        clothing = db.query(Category).filter(Category.name == "服装").first()
        home = db.query(Category).filter(Category.name == "家居用品").first()

        # 创建商品
        print("创建商品...")
        products_data = [
            {
                "name": "智能手机",
                "price": 3999.00,
                "stock": 100,
                "category_id": electronics.id,
                "description": "最新款5G智能手机，6.5英寸全面屏，5000万像素摄像头"
            },
            {
                "name": "笔记本电脑",
                "price": 5999.00,
                "stock": 50,
                "category_id": electronics.id,
                "description": "高性能轻薄本，16GB内存，512GB SSD"
            },
            {
                "name": "无线耳机",
                "price": 899.00,
                "stock": 200,
                "category_id": electronics.id,
                "description": "主动降噪，30小时续航"
            },
            {
                "name": "纯棉T恤",
                "price": 99.00,
                "stock": 300,
                "category_id": clothing.id,
                "description": "100%纯棉，舒适透气"
            },
            {
                "name": "牛仔裤",
                "price": 199.00,
                "stock": 150,
                "category_id": clothing.id,
                "description": "修身直筒，经典款式"
            },
            {
                "name": "咖啡机",
                "price": 1299.00,
                "stock": 30,
                "category_id": home.id,
                "description": "全自动咖啡机，一键制作"
            }
        ]

        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)

        db.commit()
        print(f"✅ 创建了 {len(products_data)} 个商品")

        db.close()

        print("=" * 50)
        print("🎉 数据库初始化完成！")
        print("\n测试账号:")
        print("  普通用户: testuser / 123456")
        print("  管理员: admin / admin123")
        print("\n商品分类:")
        print("  电子产品, 服装, 家居用品")

    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    init_database()