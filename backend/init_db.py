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
        Base.metadata.drop_all(bind=engine)
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
            Category(name="图书", sort_order=4),
            Category(name="美妆护肤", sort_order=5),
        ]
        for cat in categories:
            db.add(cat)
        db.commit()
        print("✅ 分类创建成功")

        # 获取分类 ID
        electronics = db.query(Category).filter(Category.name == "电子产品").first()
        clothing = db.query(Category).filter(Category.name == "服装").first()
        home = db.query(Category).filter(Category.name == "家居用品").first()
        books = db.query(Category).filter(Category.name == "图书").first()
        beauty = db.query(Category).filter(Category.name == "美妆护肤").first()

        # 创建商品 - 完整商品列表
        print("创建商品...")
        products_data = [
            # 电子产品
            {
                "name": "iPhone 15 Pro",
                "description": "A17Pro 芯片，钛金属设计，4800 万像素主摄，USB-C 接口",
                "price": 7999.00,
                "stock": 50,
                "category_id": electronics.id,
            },
            {
                "name": "华为 Mate 60 Pro",
                "description": "卫星通话，玄武架构，鸿蒙操作系统，超光变主摄",
                "price": 6999.00,
                "stock": 80,
                "category_id": electronics.id,
            },
            {
                "name": "小米 14 Pro",
                "description": "徕卡光学镜头，骁龙 8 Gen3，澎湃 OS，120W 快充",
                "price": 4999.00,
                "stock": 120,
                "category_id": electronics.id,
            },
            {
                "name": "iPad Pro 12.9 寸",
                "description": "M2 芯片，Liquid 视网膜 XDR 屏，支持 Apple Pencil 悬停",
                "price": 8999.00,
                "stock": 40,
                "category_id": electronics.id,
            },
            {
                "name": "MacBook Air 15 寸",
                "description": "M3 芯片，超薄设计，长达 18 小时续航",
                "price": 10499.00,
                "stock": 30,
                "category_id": electronics.id,
            },
            {
                "name": "戴尔 XPS 13",
                "description": "13.4 寸 OLED 屏，英特尔酷睿 Ultra7，超窄边框",
                "price": 12999.00,
                "stock": 25,
                "category_id": electronics.id,
            },
            {
                "name": "索尼 WH-1000XM5",
                "description": "业界领先降噪，30 小时续航，轻量化设计",
                "price": 1999.00,
                "stock": 150,
                "category_id": electronics.id,
            },
            {
                "name": "AirPods Pro 2",
                "description": "主动降噪，自适应音频，USB-C 充电盒",
                "price": 1899.00,
                "stock": 200,
                "category_id": electronics.id,
            },
            {
                "name": "Apple Watch Series 9",
                "description": "全天候视网膜屏，双指互点手势，更亮显示屏",
                "price": 2999.00,
                "stock": 100,
                "category_id": electronics.id,
            },
            {
                "name": "大疆 DJI Mini 4 Pro",
                "description": "全向避障，4K/60fps，34 分钟续航",
                "price": 4788.00,
                "stock": 20,
                "category_id": electronics.id,
            },
            # 服装
            {
                "name": "优衣库 摇粒绒外套",
                "description": "柔软保暖，轻便舒适，多种颜色可选",
                "price": 199.00,
                "stock": 300,
                "category_id": clothing.id,
            },
            {
                "name": "耐克 Air Max 运动鞋",
                "description": "经典气垫设计，舒适缓震，时尚百搭",
                "price": 899.00,
                "stock": 150,
                "category_id": clothing.id,
            },
            {
                "name": "阿迪达斯 三叶草卫衣",
                "description": "经典三叶草标志，舒适棉质，休闲风格",
                "price": 399.00,
                "stock": 200,
                "category_id": clothing.id,
            },
            {
                "name": "ZARA 羊毛大衣",
                "description": "含羊毛面料，修身剪裁，简约大气",
                "price": 899.00,
                "stock": 80,
                "category_id": clothing.id,
            },
            {
                "name": "李宁 运动套装",
                "description": "透气面料，弹性好，适合运动休闲",
                "price": 299.00,
                "stock": 180,
                "category_id": clothing.id,
            },
            {
                "name": "太平鸟 羽绒服",
                "description": "90% 白鸭绒，防风保暖，时尚设计",
                "price": 699.00,
                "stock": 100,
                "category_id": clothing.id,
            },
            {
                "name": "海澜之家 商务衬衫",
                "description": "免烫工艺，抗皱易打理，商务必备",
                "price": 199.00,
                "stock": 250,
                "category_id": clothing.id,
            },
            {
                "name": "URBAN REVIVO 连衣裙",
                "description": "法式优雅，收腰设计，气质款",
                "price": 299.00,
                "stock": 120,
                "category_id": clothing.id,
            },
            {
                "name": "迪卡侬 冲锋衣",
                "description": "防水防风，透气性好，户外运动必备",
                "price": 399.00,
                "stock": 160,
                "category_id": clothing.id,
            },
            {
                "name": "波司登 极寒羽绒服",
                "description": "高蓬松度鹅绒，抗寒 -30℃，保暖性能卓越",
                "price": 1999.00,
                "stock": 50,
                "category_id": clothing.id,
            },
            # 家居用品
            {
                "name": "小米 智能扫地机器人",
                "description": "激光导航，大吸力，智能规划路线",
                "price": 1999.00,
                "stock": 60,
                "category_id": home.id,
            },
            {
                "name": "戴森 V15 吸尘器",
                "description": "激光探测灰尘，强劲吸力，整机 HEPA 过滤",
                "price": 5490.00,
                "stock": 30,
                "category_id": home.id,
            },
            {
                "name": "摩飞 多功能锅",
                "description": "一锅多用，煎烤炖煮，家庭聚餐神器",
                "price": 1099.00,
                "stock": 80,
                "category_id": home.id,
            },
            {
                "name": "九阳 破壁机",
                "description": "低噪音，免手洗，一键制作豆浆",
                "price": 799.00,
                "stock": 120,
                "category_id": home.id,
            },
            {
                "name": "宜家 北欧风床品四件套",
                "description": "纯棉面料，亲肤柔软，北欧简约设计",
                "price": 299.00,
                "stock": 200,
                "category_id": home.id,
            },
            {
                "name": "米家 智能台灯",
                "description": "护眼无频闪，多模式调光，支持小爱同学",
                "price": 179.00,
                "stock": 300,
                "category_id": home.id,
            },
            {
                "name": "极米 Z6X 投影仪",
                "description": "1080P 全高清，哈曼卡顿音响，自动对焦",
                "price": 2799.00,
                "stock": 40,
                "category_id": home.id,
            },
            {
                "name": "美的 空气炸锅",
                "description": "无油烹饪，智能菜单，大容量",
                "price": 399.00,
                "stock": 150,
                "category_id": home.id,
            },
            {
                "name": "水星家纺 蚕丝被",
                "description": "100% 桑蚕丝，透气保暖，冬暖夏凉",
                "price": 899.00,
                "stock": 100,
                "category_id": home.id,
            },
            {
                "name": "苏泊尔 电饭煲",
                "description": "IH 电磁加热，球釜内胆，智能预约",
                "price": 499.00,
                "stock": 180,
                "category_id": home.id,
            },
            # 图书
            {
                "name": "《三体》全集",
                "description": "刘慈欣科幻巨作，雨果奖获奖作品",
                "price": 89.00,
                "stock": 500,
                "category_id": books.id,
            },
            {
                "name": "《Python 编程：从入门到实践》",
                "description": "畅销 Python 教程，适合初学者",
                "price": 79.00,
                "stock": 300,
                "category_id": books.id,
            },
            {
                "name": "《人类简史》",
                "description": "尤瓦尔·赫拉利作品，畅销全球",
                "price": 68.00,
                "stock": 400,
                "category_id": books.id,
            },
            {
                "name": "《活着》",
                "description": "余华代表作，感动千万读者",
                "price": 45.00,
                "stock": 350,
                "category_id": books.id,
            },
            # 美妆护肤
            {
                "name": "SK-II 神仙水",
                "description": "精华护肤，改善肤质，提亮肤色",
                "price": 1590.00,
                "stock": 100,
                "category_id": beauty.id,
            },
            {
                "name": "兰蔻 小黑瓶",
                "description": "肌底精华，修护肌肤，年轻态",
                "price": 1080.00,
                "stock": 120,
                "category_id": beauty.id,
            },
            {
                "name": "雅诗兰黛 小棕瓶",
                "description": "修护精华，抗初老，夜间修护",
                "price": 980.00,
                "stock": 130,
                "category_id": beauty.id,
            },
            {
                "name": "资生堂 红腰子",
                "description": "维稳修护，增强肌肤免疫力",
                "price": 860.00,
                "stock": 110,
                "category_id": beauty.id,
            },
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
        print("  普通用户：testuser / 123456")
        print("  管理员：admin / admin123")
        print("\n商品分类:")
        print("  电子产品 (10 件)，服装 (10 件)，家居用品 (10 件)，图书 (4 件)，美妆护肤 (4 件)")
        print(f"  总计：{len(products_data)} 件商品")

    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    init_database()