#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试ML模型预测
"""

import json
import csv
import requests

# 读取历史数据
history_data = []
with open('../data/lottery_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        history_data.append({
            'period': int(row['period']),
            'zodiac': int(row['zodiac'])
        })

print(f"读取到 {len(history_data)} 期历史数据")

# 准备API请求数据
payload = {
    'history': history_data
}

# 调用API
try:
    response = requests.post('http://localhost:5001/api/predict', json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()
    
    print("\n预测结果:")
    print("=" * 60)
    
    if result.get('success'):
        print("\n推荐生肖:")
        recommendation = result.get('recommendation', {})
        print(f"🐉 {recommendation.get('name')} (ID: {recommendation.get('id')})")
        print(f"五行: {recommendation.get('element')}")
        print(f"波色: {recommendation.get('color')}")
        print(f"概率: {recommendation.get('probability', 0) * 100:.2f}%")
        
        print("\nTop 3 预测:")
        top3 = result.get('top3', [])
        for i, item in enumerate(top3, 1):
            print(f"{i}. {item.get('name')} (ID: {item.get('id')}) - {item.get('probability', 0) * 100:.2f}%")
        
        print("\n详细预测概率:")
        print("-" * 60)
        predictions = result.get('predictions', [])
        for item in predictions:
            name = item.get('name')
            prob = item.get('probability', 0) * 100
            print(f"{name:4s} - {prob:5.2f}%")
    else:
        print(f"预测失败: {result.get('error')}")
        
except requests.exceptions.RequestException as e:
    print(f"API调用失败: {e}")
except json.JSONDecodeError:
    print("API返回无效的JSON数据")
