"""
插入更多商品数据（无图片）
"""
import pymysql
from pymysql.cursors import DictCursor
import os

# 数据库配置 - 从环境变量读取或使用默认值
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': 'root',
    'password': os.getenv('MYSQL_ROOT_PASSWORD', 'YourSecurePassword2026!'),  # 修改为实际密码
    'database': 'ecommerce',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# 商品数据
PRODUCTS = [
    # 电子产品
    {
        'name': 'iPhone 15 Pro',
        'description': 'A17 Pro芯片，钛金属设计，4800万像素主摄，USB-C接口',
        'price': 7999.00,
        'stock': 50,
        'category': '电子产品'
    },
    {
        'name': '华为 Mate 60 Pro',
        'description': '卫星通话，玄武架构，鸿蒙操作系统，超光变主摄',
        'price': 6999.00,
        'stock': 80,
        'category': '电子产品'
    },
    {
        'name': '小米 14 Pro',
        'description': '徕卡光学镜头，骁龙8 Gen3，澎湃OS，120W快充',
        'price': 4999.00,
        'stock': 120,
        'category': '电子产品'
    },
    {
        'name': 'iPad Pro 12.9寸',
        'description': 'M2芯片， Liquid视网膜XDR屏，支持Apple Pencil悬停',
        'price': 8999.00,
        'stock': 40,
        'category': '电子产品'
    },
    {
        'name': 'MacBook Air 15寸',
        'description': 'M3芯片，超薄设计，长达18小时续航',
        'price': 10499.00,
        'stock': 30,
        'category': '电子产品'
    },
    {
        'name': '戴尔 XPS 13',
        'description': '13.4寸OLED屏，英特尔酷睿Ultra7，超窄边框',
        'price': 12999.00,
        'stock': 25,
        'category': '电子产品'
    },
    {
        'name': '索尼 WH-1000XM5',
        'description': '业界领先降噪，30小时续航，轻量化设计',
        'price': 1999.00,
        'stock': 150,
        'category': '电子产品'
    },
    {
        'name': 'AirPods Pro 2',
        'description': '主动降噪，自适应音频，USB-C充电盒',
        'price': 1899.00,
        'stock': 200,
        'category': '电子产品'
    },
    {
        'name': 'Apple Watch Series 9',
        'description': '全天候视网膜屏，双指互点手势，更亮显示屏',
        'price': 2999.00,
        'stock': 100,
        'category': '电子产品'
    },
    {
        'name': '大疆 DJI Mini 4 Pro',
        'description': '全向避障，4K/60fps，34分钟续航',
        'price': 4788.00,
        'stock': 20,
        'category': '电子产品'
    },

    # 服装
    {
        'name': '优衣库 摇粒绒外套',
        'description': '柔软保暖，轻便舒适，多种颜色可选',
        'price': 199.00,
        'stock': 300,
        'category': '服装'
    },
    {
        'name': '耐克 Air Max 运动鞋',
        'description': '经典气垫设计，舒适缓震，时尚百搭',
        'price': 899.00,
        'stock': 150,
        'category': '服装'
    },
    {
        'name': '阿迪达斯 三叶草卫衣',
        'description': '经典三叶草标志，舒适棉质，休闲风格',
        'price': 399.00,
        'stock': 200,
        'category': '服装'
    },
    {
        'name': 'ZARA 羊毛大衣',
        'description': '含羊毛面料，修身剪裁，简约大气',
        'price': 899.00,
        'stock': 80,
        'category': '服装'
    },
    {
        'name': '李宁 运动套装',
        'description': '透气面料，弹性好，适合运动休闲',
        'price': 299.00,
        'stock': 180,
        'category': '服装'
    },
    {
        'name': '太平鸟 羽绒服',
        'description': '90%白鸭绒，防风保暖，时尚设计',
        'price': 699.00,
        'stock': 100,
        'category': '服装'
    },
    {
        'name': '海澜之家 商务衬衫',
        'description': '免烫工艺，抗皱易打理，商务必备',
        'price': 199.00,
        'stock': 250,
        'category': '服装'
    },
    {
        'name': 'URBAN REVIVO 连衣裙',
        'description': '法式优雅，收腰设计，气质款',
        'price': 299.00,
        'stock': 120,
        'category': '服装'
    },
    {
        'name': '迪卡侬 冲锋衣',
        'description': '防水防风，透气性好，户外运动必备',
        'price': 399.00,
        'stock': 160,
        'category': '服装'
    },
    {
        'name': '波司登 极寒羽绒服',
        'description': '高蓬松度鹅绒，抗寒-30℃，保暖性能卓越',
        'price': 1999.00,
        'stock': 50,
        'category': '服装'
    },

    # 家居用品
    {
        'name': '小米 智能扫地机器人',
        'description': '激光导航，大吸力，智能规划路线',
        'price': 1999.00,
        'stock': 60,
        'category': '家居用品'
    },
    {
        'name': '戴森 V15 吸尘器',
        'description': '激光探测灰尘，强劲吸力，整机HEPA过滤',
        'price': 5490.00,
        'stock': 30,
        'category': '家居用品'
    },
    {
        'name': '摩飞 多功能锅',
        'description': '一锅多用，煎烤炖煮，家庭聚餐神器',
        'price': 1099.00,
        'stock': 80,
        'category': '家居用品'
    },
    {
        'name': '九阳 破壁机',
        'description': '低噪音，免手洗，一键制作豆浆',
        'price': 799.00,
        'stock': 120,
        'category': '家居用品'
    },
    {
        'name': '宜家 北欧风床品四件套',
        'description': '纯棉面料，亲肤柔软，北欧简约设计',
        'price': 299.00,
        'stock': 200,
        'category': '家居用品'
    },
    {
        'name': '米家 智能台灯',
        'description': '护眼无频闪，多模式调光，支持小爱同学',
        'price': 179.00,
        'stock': 300,
        'category': '家居用品'
    },
    {
        'name': '极米 Z6X 投影仪',
        'description': '1080P全高清，哈曼卡顿音响，自动对焦',
        'price': 2799.00,
        'stock': 40,
        'category': '家居用品'
    },
    {
        'name': '美的 空气炸锅',
        'description': '无油烹饪，智能菜单，大容量',
        'price': 399.00,
        'stock': 150,
        'category': '家居用品'
    },
    {
        'name': '水星家纺 蚕丝被',
        'description': '100%桑蚕丝，透气保暖，冬暖夏凉',
        'price': 899.00,
        'stock': 100,
        'category': '家居用品'
    },
    {
        'name': '苏泊尔 电饭煲',
        'description': 'IH电磁加热，球釜内胆，智能预约',
        'price': 499.00,
        'stock': 180,
        'category': '家居用品'
    },

    # 图书
    {
        'name': '《三体》全集',
        'description': '刘慈欣科幻巨作，雨果奖获奖作品',
        'price': 89.00,
        'stock': 500,
        'category': '图书'
    },
    {
        'name': '《Python编程：从入门到实践》',
        'description': '畅销Python教程，适合初学者',
        'price': 79.00,
        'stock': 300,
        'category': '图书'
    },
    {
        'name': '《人类简史》',
        'description': '尤瓦尔·赫拉利作品，畅销全球',
        'price': 68.00,
        'stock': 400,
        'category': '图书'
    },
    {
        'name': '《活着》',
        'description': '余华代表作，感动千万读者',
        'price': 45.00,
        'stock': 350,
        'category': '图书'
    },

    # 美妆护肤
    {
        'name': 'SK-II 神仙水',
        'description': '精华护肤，改善肤质，提亮肤色',
        'price': 1590.00,
        'stock': 100,
        'category': '美妆护肤'
    },
    {
        'name': '兰蔻 小黑瓶',
        'description': '肌底精华，修护肌肤，年轻态',
        'price': 1080.00,
        'stock': 120,
        'category': '美妆护肤'
    },
    {
        'name': '雅诗兰黛 小棕瓶',
        'description': '修护精华，抗初老，夜间修护',
        'price': 980.00,
        'stock': 130,
        'category': '美妆护肤'
    },
    {
        'name': '资生堂 红腰子',
        'description': '维稳修护，增强肌肤免疫力',
        'price': 860.00,
        'stock': 110,
        'category': '美妆护肤'
    }
]


def insert_products():
    """插入商品数据"""

    print("🚀 开始插入更多商品数据...")
    print("=" * 60)

    try:
        conn = pymysql.connect(**DB_CONFIG)

        with conn.cursor() as cursor:
            # 获取所有分类
            cursor.execute("SELECT id, name FROM categories")
            categories = {cat['name']: cat['id'] for cat in cursor.fetchall()}
            print(f"现有分类: {list(categories.keys())}")

            # 检查是否有"图书"和"美妆护肤"分类，如果没有则创建
            if '图书' not in categories:
                cursor.execute("INSERT INTO categories (name, sort_order) VALUES (%s, %s)", ('图书', 4))
                cursor.execute("SELECT LAST_INSERT_ID() as id")
                categories['图书'] = cursor.fetchone()['id']
                print("✅ 创建图书分类")

            if '美妆护肤' not in categories:
                cursor.execute("INSERT INTO categories (name, sort_order) VALUES (%s, %s)", ('美妆护肤', 5))
                cursor.execute("SELECT LAST_INSERT_ID() as id")
                categories['美妆护肤'] = cursor.fetchone()['id']
                print("✅ 创建美妆护肤分类")

            # 插入商品
            inserted_count = 0
            for product in PRODUCTS:
                category_id = categories.get(product['category'])
                if not category_id:
                    print(f"⚠️ 跳过 {product['name']}: 分类 {product['category']} 不存在")
                    continue

                # 检查商品是否已存在
                cursor.execute(
                    "SELECT id FROM products WHERE name = %s",
                    (product['name'],)
                )
                if cursor.fetchone():
                    print(f"⏭️ 跳过 {product['name']}: 已存在")
                    continue

                cursor.execute("""
                    INSERT INTO products (name, description, price, stock, category_id, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    product['name'],
                    product['description'],
                    product['price'],
                    product['stock'],
                    category_id,
                    True
                ))
                inserted_count += 1
                print(f"✅ 插入: {product['name']} (¥{product['price']})")

            conn.commit()

            print("=" * 60)
            print(f"🎉 数据插入完成！共插入 {inserted_count} 件商品")

            # 统计各分类商品数量
            cursor.execute("""
                SELECT c.name, COUNT(p.id) as count
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id
                GROUP BY c.id
                ORDER BY c.sort_order
            """)
            stats = cursor.fetchall()
            print("\n📊 商品统计:")
            for stat in stats:
                print(f"  {stat['name']}: {stat['count']} 件")

    except Exception as e:
        print(f"❌ 插入失败: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()


def list_products():
    """列出所有商品"""
    print("\n" + "=" * 60)
    print("商品列表预览:")
    print("=" * 60)

    try:
        conn = pymysql.connect(**DB_CONFIG)

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.name, p.price, p.stock, c.name as category
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY c.sort_order, p.id
                LIMIT 20
            """)
            products = cursor.fetchall()

            for product in products:
                print(f"  [{product['category']}] {product['name']} - ¥{product['price']} (库存: {product['stock']})")

            cursor.execute("SELECT COUNT(*) as total FROM products")
            total = cursor.fetchone()['total']
            print(f"\n... 共 {total} 件商品")

    except Exception as e:
        print(f"❌ 查询失败: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    insert_products()
    list_products()