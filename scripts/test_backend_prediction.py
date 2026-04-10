#!/usr/bin/env python3
import requests
import json
import csv

# 读取历史数据
history = []
with open('real_lottery_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        history.append({
            'period': int(row['period']),
            'zodiac': int(row['zodiac'])
        })

# 取最后50期
history = history[-50:]

# 调用API
response = requests.post('http://127.0.0.1:5001/api/predict', json={'history': history})
result = response.json()

print('=' * 60)
print('2026099期生肖预测结果')
print('=' * 60)

# 生肖映射
zodiac_map = {1: '马', 2: '蛇', 3: '龙', 4: '兔', 5: '虎', 6: '牛', 7: '鼠', 8: '猪', 9: '狗', 10: '鸡', 11: '猴', 12: '羊'}
zodiac_emoji = {1: '🐎', 2: '🐍', 3: '🐉', 4: '🐇', 5: '🐅', 6: '🐂', 7: '🐀', 8: '🐖', 9: '🐕', 10: '🐓', 11: '🐒', 12: '🐑'}

print('\n🏆 Top 3 推荐:')
for i, item in enumerate(result['top3'], 1):
    rank = '🥇' if i == 1 else '🥈' if i == 2 else '🥉'
    print(f'  {rank} {i}. {zodiac_emoji[item["id"]]} {item["name"]} (ID: {item["id"]}) - {(item["probability"] * 100):.2f}%')

print('\n📊 所有生肖概率:')
for item in result['predictions']:
    bar = '█' * int(item['probability'] * 30)
    print(f'  {zodiac_emoji[item["id"]]} {item["name"]:2s} (ID: {item["id"]:2d}) - {(item["probability"] * 100):6.2f}% {bar}')

print('\n' + '=' * 60)
