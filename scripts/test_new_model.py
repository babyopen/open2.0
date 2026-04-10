#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新训练的模型
"""

import requests
import csv

# 1. 健康检查
print("1. 健康检查...")
response = requests.get('http://localhost:5001/api/health')
print(f"   结果: {response.json()}")

# 2. 生肖映射
print("\n2. 生肖映射...")
response = requests.get('http://localhost:5001/api/zodiac-mapping')
result = response.json()
if result['success']:
    print("   生肖顺序:")
    print(f"   {' '.join(result['order'])}")

# 3. 测试预测
print("\n3. 测试预测...")

# 读取历史数据
history = []
with open('real_lottery_history.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        history.append({
            'period': int(row[0]),
            'zodiac': int(row[1])
        })

# 只使用最后50期
recent_history = history[-50:]

# 发送预测请求
response = requests.post('http://localhost:5001/api/predict', json={'history': recent_history})
result = response.json()

if result['success']:
    print("\n2026099期预测结果:")
    print("-" * 60)
    for i, item in enumerate(result['predictions'][:3]):
        emoji_map = {
            '马': '🐎', '蛇': '🐍', '龙': '🐉', '兔': '🐇',
            '虎': '🐅', '牛': '🐂', '鼠': '🐀', '猪': '🐖',
            '狗': '🐕', '鸡': '🐓', '猴': '🐒', '羊': '🐑'
        }
        emoji = emoji_map.get(item['name'], '')
        if i == 0:
            print(f"🥇 第1名: {emoji} {item['name']} (ID: {item['zodiac']}) - 概率: {item['probability']:.4f}")
        elif i == 1:
            print(f"🥈 第2名: {emoji} {item['name']} (ID: {item['zodiac']}) - 概率: {item['probability']:.4f}")
        elif i == 2:
            print(f"🥉 第3名: {emoji} {item['name']} (ID: {item['zodiac']}) - 概率: {item['probability']:.4f}")
    
    print("\n完整概率排名:")
    print("-" * 60)
    for i, item in enumerate(result['predictions']):
        emoji_map = {
            '马': '🐎', '蛇': '🐍', '龙': '🐉', '兔': '🐇',
            '虎': '🐅', '牛': '🐂', '鼠': '🐀', '猪': '🐖',
            '狗': '🐕', '鸡': '🐓', '猴': '🐒', '羊': '🐑'
        }
        emoji = emoji_map.get(item['name'], '')
        prob = item['probability']
        bar_length = int(prob * 40)
        bar = '█' * bar_length
        print(f"{i+1:2d}. {emoji} {item['name']:2} (ID: {item['zodiac']:2d}) - {prob:.4f} {bar}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
