#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加推荐历史记录到本地存储
"""

import json
import time
from datetime import datetime

# 生肖映射
ZODIAC_MAP = {
    1: '马', 2: '蛇', 3: '龙', 4: '兔', 5: '虎', 6: '牛',
    7: '鼠', 8: '猪', 9: '狗', 10: '鸡', 11: '猴', 12: '羊'
}

# 生成当前时间戳
def get_timestamp():
    return int(time.time() * 1000)

# 生成日期字符串
def get_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 创建ML预测历史记录
def create_ml_prediction_history():
    predictions = [
        {
            "id": 7, "name": "鼠", "probability": 0.1221,
            "element": "水", "color": "红"
        },
        {
            "id": 11, "name": "猴", "probability": 0.1169,
            "element": "金", "color": "蓝"
        },
        {
            "id": 6, "name": "牛", "probability": 0.1008,
            "element": "土", "color": "绿"
        }
    ]
    
    return {
        "id": f"ml_{get_timestamp()}",
        "time": get_date(),
        "timestamp": get_timestamp(),
        "predictions": predictions,
        "top3": predictions[:3],
        "recommendation": predictions[0],
        "period": "2026100",  # 下一期
        "source": "ML模型"
    }

# 创建生肖预测历史记录
def create_zodiac_prediction_history():
    return {
        "id": f"zodiac_{get_timestamp()}",
        "time": get_date(),
        "timestamp": get_timestamp(),
        "period": "2026100",
        "predictions": [
            {"id": 7, "name": "鼠", "probability": 0.12},
            {"id": 11, "name": "猴", "probability": 0.11},
            {"id": 6, "name": "牛", "probability": 0.10}
        ],
        "source": "传统算法"
    }

# 创建精选特码历史记录
def create_special_history():
    return {
        "id": f"special_{get_timestamp()}",
        "time": get_date(),
        "timestamp": get_timestamp(),
        "period": "2026100",
        "numbers": [7, 11, 6, 8, 4],
        "mode": "hot",
        "count": 5
    }

# 创建特码热门TOP5历史记录
def create_hot_numbers_history():
    return {
        "id": f"hot_{get_timestamp()}",
        "time": get_date(),
        "timestamp": get_timestamp(),
        "period": "2026100",
        "numbers": [7, 11, 6, 8, 4],
        "source": "综合分析"
    }

# 创建历史记录数据
def create_history_data():
    # 创建多条历史记录
    ml_history = []
    zodiac_history = []
    special_history = []
    hot_history = []
    
    # 生成5条历史记录
    for i in range(5):
        # 为每条记录生成不同的时间戳
        time.sleep(0.1)
        
        # ML预测历史
        ml_item = create_ml_prediction_history()
        ml_item['period'] = f"2026{100 - i}"
        ml_history.append(ml_item)
        
        # 生肖预测历史
        zodiac_item = create_zodiac_prediction_history()
        zodiac_item['period'] = f"2026{100 - i}"
        zodiac_history.append(zodiac_item)
        
        # 精选特码历史
        special_item = create_special_history()
        special_item['period'] = f"2026{100 - i}"
        special_history.append(special_item)
        
        # 特码热门TOP5历史
        hot_item = create_hot_numbers_history()
        hot_item['period'] = f"2026{100 - i}"
        hot_history.append(hot_item)
    
    return {
        "mlPredictionHistory": ml_history,
        "zodiacPredictionHistory": zodiac_history,
        "specialHistory": special_history,
        "hotNumbersHistory": hot_history
    }

# 保存历史记录到JSON文件
def save_history():
    history_data = create_history_data()
    
    # 保存到JSON文件
    with open('prediction_history.json', 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)
    
    print("推荐历史记录已生成并保存到 prediction_history.json")
    print(f"生成的记录数量:")
    print(f"- ML预测历史: {len(history_data['mlPredictionHistory'])}")
    print(f"- 生肖预测历史: {len(history_data['zodiacPredictionHistory'])}")
    print(f"- 精选特码历史: {len(history_data['specialHistory'])}")
    print(f"- 特码热门TOP5历史: {len(history_data['hotNumbersHistory'])}")

if __name__ == '__main__':
    save_history()
