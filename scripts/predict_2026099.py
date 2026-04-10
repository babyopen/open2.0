#!/usr/bin/env python3
import json
import subprocess
import sys

# 读取最后50期数据
history = []
with open('real_lottery_history.csv', 'r') as f:
    lines = f.readlines()
    # 跳过标题行
    data_lines = lines[1:]
    # 取最后50条
    last_50 = data_lines[-50:]
    for line in last_50:
        period, zodiac = line.strip().split(',')
        history.append({"period": int(period), "zodiac": int(zodiac)})

# 构建请求数据
request_data = {"history": history}

# 转换为JSON字符串
json_data = json.dumps(request_data)

# 使用curl调用API
curl_cmd = [
    'curl', '-s', '-X', 'POST', 'http://localhost:5001/api/predict',
    '-H', 'Content-Type: application/json',
    '-d', json_data
]

# 执行命令
result = subprocess.run(curl_cmd, capture_output=True, text=True)

if result.returncode == 0:
    response = json.loads(result.stdout)
    if response.get('success'):
        predictions = response['predictions']
        # 按概率排序
        sorted_preds = sorted(predictions, key=lambda x: x['probability'], reverse=True)
        print("="*60)
        print(f"2026099期生肖预测结果")
        print("="*60)
        print(f"推荐生肖: {sorted_preds[0]['name']} (概率: {sorted_preds[0]['probability']:.4f})")
        print(f"次选生肖: {sorted_preds[1]['name']} (概率: {sorted_preds[1]['probability']:.4f})")
        print(f"备选生肖: {sorted_preds[2]['name']} (概率: {sorted_preds[2]['probability']:.4f})")
        print()
        print("详细概率排名:")
        print("-"*40)
        for i, pred in enumerate(sorted_preds, 1):
            bar = "█" * int(pred['probability'] * 40)
            print(f"{i:2d}. {pred['name']}({pred['id']}): {pred['probability']:.4f} {bar}")
    else:
        print(f"API错误: {response.get('error', '未知错误')}")
else:
    print(f"请求失败: {result.stderr}")