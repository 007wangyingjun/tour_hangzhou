import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import (st_folium)

from PIL import Image
import base64
from io import BytesIO

# 页面配置
st.set_page_config(
    page_title="杭州旅游攻略 2025",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .weather-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }

    .attraction-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }

    .day-tab {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }

    .day-tab:hover {
        background: #e9ecef;
        transform: translateY(-2px);
    }

    .tip-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .food-item {
        background: #ffeaa7;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        color: #2d3436;
        font-weight: 500;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown("""
<div class="main-header">
    <h1>🏮 杭州旅游攻略</h1>
    <h3>2025年7月7日 - 7月9日 · 三日精华游</h3>
    <p>上有天堂，下有苏杭 🌸</p>
</div>
""", unsafe_allow_html=True)

# 实时时间显示
current_time = datetime.now()
st.markdown(f"**当前时间**: {current_time.strftime('%Y年%m月%d日 %H:%M:%S')}")

# 侧边栏
st.sidebar.header("🗓️ 行程规划")
selected_day = st.sidebar.selectbox(
    "选择游览日期",
    ["第一天 (7月7日)", "第二天 (7月8日)", "第三天 (7月9日)"]
)

st.sidebar.header("🎯 快速导航")
nav_option = st.sidebar.radio(
    "选择查看内容",
    ["📅 行程总览", "🌤️ 天气预报", "🏛️ 景点详情", "🍜 美食推荐", "🗺️ 路线地图", "💰 预算规划"]
)

# 天气数据
weather_data = {
    '7月7日': {'temp_high': 35, 'temp_low': 28, 'desc': '晴转多云', 'humidity': 75, 'rain': 10},
    '7月8日': {'temp_high': 33, 'temp_low': 26, 'desc': '多云有雨', 'humidity': 80, 'rain': 70},
    '7月9日': {'temp_high': 34, 'temp_low': 27, 'desc': '阵雨转晴', 'humidity': 70, 'rain': 40}
}

# 景点数据
attractions_data = {
    '第一天 (7月7日)': [
        {
            'name': '西湖风景区',
            'time': '09:00-17:00',
            'duration': '4小时',
            'rating': 4.8,
            'price': '免费',
            'description': '杭州最著名的景点，"上有天堂，下有苏杭"的经典体现',
            'highlights': ['断桥残雪', '苏堤春晓', '雷峰夕照', '花港观鱼'],
            'tips': '建议早上游览，避开人流高峰；可租借共享单车环湖',
            'transport': '地铁1号线龙翔桥站',
            'lat': 30.2741, 'lon': 120.1551
        },
        {
            'name': '雷峰塔',
            'time': '08:00-18:30',
            'duration': '1.5小时',
            'rating': 4.5,
            'price': '40元',
            'description': '白娘子传说的经典场景，登塔可俯瞰西湖全景',
            'highlights': ['塔内文物展示', '西湖全景', '夕阳美景', '白蛇传说'],
            'tips': '傍晚时分景色最美，建议下午4点后游览',
            'transport': '公交K4、504路雷峰塔站',
            'lat': 30.2316, 'lon': 120.1477
        },
        {
            'name': '河坊街',
            'time': '全天开放',
            'duration': '2小时',
            'rating': 4.3,
            'price': '免费',
            'description': '杭州历史文化街区，品尝地道小吃和购买特产',
            'highlights': ['胡庆余堂', '朱炳仁铜雕艺术博物馆', '特色小吃', '手工艺品'],
            'tips': '晚上更加热闹，小吃丰富；注意保管随身物品',
            'transport': '地铁1号线定安路站',
            'lat': 30.2447, 'lon': 120.1676
        }
    ],
    '第二天 (7月8日)': [
        {
            'name': '灵隐寺',
            'time': '07:30-17:15',
            'duration': '2.5小时',
            'rating': 4.7,
            'price': '30元+45元飞来峰',
            'description': '中国佛教古寺，香火鼎盛，历史悠久',
            'highlights': ['大雄宝殿', '飞来峰石窟造像', '永福寺', '三生石'],
            'tips': '需要先购买飞来峰门票才能进入灵隐寺；建议早上参观',
            'transport': '公交7、807、游2路灵隐站',
            'lat': 30.2408, 'lon': 120.1018
        },
        {
            'name': '西溪湿地',
            'time': '08:30-17:30',
            'duration': '3小时',
            'rating': 4.6,
            'price': '80元',
            'description': '中国第一个国家湿地公园，生态环境优美',
            'highlights': ['摇橹船体验', '湿地生态', '非诚勿扰拍摄地', '候鸟观赏'],
            'tips': '建议乘坐电瓶船游览，注意防蚊虫叮咬',
            'transport': '公交K506、596路西溪湿地站',
            'lat': 30.2742, 'lon': 120.0516
        },
        {
            'name': '宋城',
            'time': '10:00-21:00',
            'duration': '4小时',
            'rating': 4.4,
            'price': '310元(含演出)',
            'description': '大型宋文化主题公园，体验宋代风情',
            'highlights': ['宋城千古情演出', '清明上河图', '鬼屋', '宋代市井'],
            'tips': '演出场次有限，建议提前预订；千古情演出不容错过',
            'transport': '公交4、39、308路宋城站',
            'lat': 30.2076, 'lon': 120.0736
        }
    ],
    '第三天 (7月9日)': [
        {
            'name': '良渚博物院',
            'time': '09:00-16:30',
            'duration': '2小时',
            'rating': 4.5,
            'price': '免费',
            'description': '展示良渚文化的专题博物馆，5000年文明史见证',
            'highlights': ['良渚玉器', '5000年文明', '考古发现', '文物精品'],
            'tips': '需要提前预约，周一闭馆；建议上午参观',
            'transport': '公交389、372路良渚博物院站',
            'lat': 30.4139, 'lon': 120.0297
        },
        {
            'name': '九溪烟树',
            'time': '全天开放',
            'duration': '2.5小时',
            'rating': 4.4,
            'price': '免费',
            'description': '西湖新十景之一，山水田园风光绝美',
            'highlights': ['十八涧', '烟树景观', '龙井茶园', '山涧溪流'],
            'tips': '适合徒步，穿舒适的鞋子；夏季注意防晒',
            'transport': '公交27、87、103路九溪站',
            'lat': 30.2097, 'lon': 120.1186
        },
        {
            'name': '钱塘江大桥',
            'time': '全天开放',
            'duration': '1小时',
            'rating': 4.2,
            'price': '免费',
            'description': '中国第一座自主设计建造的双层铁路公路大桥',
            'highlights': ['历史意义', '钱塘江景色', '夜景灯光', '建筑艺术'],
            'tips': '晚上灯光很美，适合拍照；可结合钱塘江夜游',
            'transport': '公交39、308路钱塘江大桥站',
            'lat': 30.2108, 'lon': 120.1344
        }
    ]
}

# 美食推荐
food_recommendations = [
    '西湖醋鱼', '东坡肉', '龙井虾仁', '叫花鸡',
    '片儿川', '知味小笼', '定胜糕', '藕粉',
    '油爆虾', '糖桂花', '吴山酥油饼', '猫耳朵'
]

# 根据导航选择显示内容
if nav_option == "📅 行程总览":
    st.header("📅 三日行程总览")

    # 创建行程概览表
    schedule_data = []
    for day, attractions in attractions_data.items():
        for attraction in attractions:
            schedule_data.append({
                '日期': day,
                '景点': attraction['name'],
                '时间': attraction['time'],
                '游览时长': attraction['duration'],
                '评分': attraction['rating'],
                '门票': attraction['price']
            })

    df_schedule = pd.DataFrame(schedule_data)
    st.dataframe(df_schedule, use_container_width=True)

    # 显示每日主题
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="day-tab">
            <h4>🌊 第一天</h4>
            <p><strong>西湖核心区</strong></p>
            <p>经典景点打卡，感受西湖美景</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="day-tab">
            <h4>🏛️ 第二天</h4>
            <p><strong>文化体验日</strong></p>
            <p>深度体验杭州历史文化</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="day-tab">
            <h4>🌿 第三天</h4>
            <p><strong>深度探索日</strong></p>
            <p>探索杭州的另一面</p>
        </div>
        """, unsafe_allow_html=True)

elif nav_option == "🌤️ 天气预报":
    st.header("🌤️ 天气预报")

    # 天气预报卡片
    col1, col2, col3 = st.columns(3)

    for i, (day, data) in enumerate(weather_data.items()):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="weather-card">
                <h3>{day}</h3>
                <h2>{data['temp_low']}°C - {data['temp_high']}°C</h2>
                <p>{data['desc']}</p>
                <p>💧 湿度: {data['humidity']}%</p>
                <p>🌧️ 降雨概率: {data['rain']}%</p>
            </div>
            """, unsafe_allow_html=True)

    # 温度趋势图
    st.subheader("🌡️ 温度趋势")

    days = list(weather_data.keys())
    high_temps = [data['temp_high'] for data in weather_data.values()]
    low_temps = [data['temp_low'] for data in weather_data.values()]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=high_temps, mode='lines+markers',
                             name='最高温度', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=days, y=low_temps, mode='lines+markers',
                             name='最低温度', line=dict(color='blue', width=3)))

    fig.update_layout(
        title='杭州三日温度趋势',
        xaxis_title='日期',
        yaxis_title='温度 (°C)',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # 旅游建议
    st.markdown("""
    <div class="tip-box">
        <h4>🎯 7月杭州旅游贴士</h4>
        <ul>
            <li><strong>防暑降温</strong>：7月是杭州最热的月份，建议避开10:00-15:00的高温时段</li>
            <li><strong>雨具准备</strong>：多雨季节，随身携带雨伞或雨衣</li>
            <li><strong>服装建议</strong>：穿透气轻薄的棉质衣物，带上防晒用品</li>
            <li><strong>补水保湿</strong>：湿度较高，多喝水，注意防中暑</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif nav_option == "🏛️ 景点详情":
    st.header("🏛️ 景点详情")

    # 选择的日期对应的景点
    attractions = attractions_data[selected_day]

    for attraction in attractions:
        st.markdown(f"""
        <div class="attraction-card">
            <h3>{attraction['name']}</h3>
            <p><strong>⭐ 评分:</strong> {attraction['rating']}/5.0</p>
            <p><strong>🎫 门票:</strong> {attraction['price']}</p>
            <p><strong>⏰ 开放时间:</strong> {attraction['time']}</p>
            <p><strong>⏱️ 建议游览时长:</strong> {attraction['duration']}</p>
            <p><strong>📍 交通:</strong> {attraction['transport']}</p>
            <p><strong>📝 描述:</strong> {attraction['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 展示亮点
        st.markdown("**🌟 精彩亮点:**")
        cols = st.columns(len(attraction['highlights']))
        for i, highlight in enumerate(attraction['highlights']):
            with cols[i]:
                st.markdown(f"<span class='food-item'>{highlight}</span>", unsafe_allow_html=True)

        # 贴心提示
        st.info(f"💡 **贴心提示:** {attraction['tips']}")

        st.markdown("---")

    # 景点评分可视化
    st.subheader("📊 景点评分对比")

    attraction_names = [a['name'] for a in attractions]
    ratings = [a['rating'] for a in attractions]

    fig = px.bar(
        x=attraction_names,
        y=ratings,
        title=f"{selected_day} 景点评分对比",
        labels={'x': '景点', 'y': '评分'},
        color=ratings,
        color_continuous_scale='viridis'
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        template='plotly_white',
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

elif nav_option == "🍜 美食推荐":
    st.header("🍜 杭州必尝美食")

    st.markdown("### 🥢 经典杭帮菜")

    # 美食网格展示
    cols = st.columns(4)
    for i, food in enumerate(food_recommendations):
        with cols[i % 4]:
            st.markdown(f"<div class='food-item'>{food}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 美食地图推荐
    st.subheader("🗺️ 推荐美食区域")

    food_areas = {
        '河坊街': {'lat': 30.2447, 'lon': 120.1676, 'desc': '传统小吃一条街'},
        '南宋御街': {'lat': 30.2518, 'lon': 120.1672, 'desc': '高档餐厅聚集地'},
        '湖滨银泰': {'lat': 30.2586, 'lon': 120.1651, 'desc': '现代美食广场'},
        '西湖天地': {'lat': 30.2469, 'lon': 120.1398, 'desc': '国际美食区'}
    }

    for area, info in food_areas.items():
        st.markdown(f"""
        <div class="attraction-card">
            <h4>{area}</h4>
            <p>{info['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 美食价格分布
    st.subheader("💰 美食价格参考")

    food_prices = {
        '街边小吃': '10-30元',
        '普通餐厅': '50-100元',
        '知名餐厅': '100-200元',
        '高档餐厅': '200-500元'
    }

    for category, price in food_prices.items():
        st.markdown(f"**{category}:** {price}")

elif nav_option == "🗺️ 路线地图":
    st.header("🗺️ 旅游路线地图")

    # 创建杭州地图
    hangzhou_map = folium.Map(
        location=[30.2741, 120.1551],  # 西湖中心
        zoom_start=12,
        tiles='OpenStreetMap'
    )

    # 添加景点标记
    colors = ['red', 'blue', 'green']
    day_names = ['第一天', '第二天', '第三天']

    for i, (day, attractions) in enumerate(attractions_data.items()):
        for attraction in attractions:
            folium.Marker(
                location=[attraction['lat'], attraction['lon']],
                popup=f"""
                <b>{attraction['name']}</b><br>
                {day_names[i]}<br>
                评分: {attraction['rating']}/5.0<br>
                门票: {attraction['price']}<br>
                时长: {attraction['duration']}
                """,
                icon=folium.Icon(color=colors[i], icon='info-sign')
            ).add_to(hangzhou_map)

    # 显示地图
    map_data = st_folium(hangzhou_map, width=700, height=500)

    # 添加图例
    st.markdown("""
    **图例说明:**
    - 🔴 红色标记：第一天景点
    - 🔵 蓝色标记：第二天景点
    - 🟢 绿色标记：第三天景点
    """)

    # 交通建议
    st.subheader("🚇 交通建议")

    st.markdown("""
    <div class="tip-box">
        <h4>🚌 推荐交通方式</h4>
        <ul>
            <li><strong>地铁</strong>：杭州地铁覆盖主要景点，推荐购买三日票</li>
            <li><strong>公交</strong>：旅游专线直达各大景点</li>
            <li><strong>共享单车</strong>：西湖周边骑行体验佳</li>
            <li><strong>出租车/网约车</strong>：方便快捷，但注意高峰期堵车</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif nav_option == "💰 预算规划":
    st.header("💰 旅游预算规划")

    # 预算计算器
    st.subheader("🧮 预算计算器")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🎫 门票费用**")
        ticket_cost = 0
        for day, attractions in attractions_data.items():
            for attraction in attractions:
                price_str = attraction['price']
                if '免费' not in price_str:
                    # 提取数字
                    import re

                    numbers = re.findall(r'\d+', price_str)
                    if numbers:
                        ticket_cost += int(numbers[0])

        st.metric("门票总费用", f"¥{ticket_cost}")

    with col2:
        st.markdown("**🍽️ 餐饮费用**")
        meal_cost = st.selectbox(
            "选择餐饮标准",
            ["经济型 (¥150/天)", "舒适型 (¥250/天)", "豪华型 (¥400/天)"]
        )

        meal_daily = int(meal_cost.split('¥')[1].split('/')[0])
        total_meal = meal_daily * 3
        st.metric("餐饮总费用", f"¥{total_meal}")

    # 住宿费用
    st.subheader("🏨 住宿费用")

    hotel_options = {
        "青年旅社": 80,
        "经济型酒店": 200,
        "星级酒店": 400,
        "豪华酒店": 800
    }

    selected_hotel = st.selectbox("选择住宿类型", list(hotel_options.keys()))
    hotel_cost = hotel_options[selected_hotel] * 2  # 2晚

    st.metric("住宿总费用", f"¥{hotel_cost}")

    # 交通费用
    st.subheader("🚗 交通费用")

    transport_cost = st.number_input("预估交通费用", min_value=0, value=150, step=10)

    # 总费用计算
    total_cost = ticket_cost + total_meal + hotel_cost + transport_cost

    st.subheader("📊 费用汇总")

    cost_breakdown = {
        '类别': ['门票', '餐饮', '住宿', '交通'],
        '费用': [ticket_cost, total_meal, hotel_cost, transport_cost]
    }

    df_cost = pd.DataFrame(cost_breakdown)

    # 费用分布饼图
    fig = px.pie(
        df_cost,
        values='费用',
        names='类别',
        title='旅游费用分布',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig, use_container_width=True)

    # 总费用显示
    st.success(f"### 💰 预估总费用: ¥{total_cost}")

    # 省钱小贴士
    st.markdown("""
    <div class="tip-box">
        <h4>💡 省钱小贴士</h4>
        <ul>
            <li><strong>门票优惠</strong>：关注官方微信公众号，经常有优惠活动</li>
            <li><strong>交通优惠</strong>：购买杭州地铁三日票，比单次购票便宜</li>
            <li><strong>住宿优惠</strong>：提前预订，选择非市中心区域可节省费用</li>
            <li><strong>餐饮优惠</strong>：尝试当地小吃，性价比高且地道</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🏮 杭州旅游攻略 · 让您的杭州之行更加完美 🏮</p>
    <p>祝您旅途愉快！</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏额外信息
st.sidebar.markdown("---")
st.sidebar.info("""
📱 **实用APP推荐**
- 杭州地铁
- 支付宝(杭州专区)
- 高德地图
- 大众点评
""")

st.sidebar.success("""
🎯 **紧急联系方式**
- 旅游热线：0571-96123
- 急救电话：120
- 报警电话：110
""")