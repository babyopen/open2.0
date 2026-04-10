#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证生肖映射是否正确
"""

import json
import requests

# 新的生肖顺序
NEW_ZODIAC = ["马", "蛇", "龙", "兔", "虎", "牛", "鼠", "猪", "狗", "鸡", "猴", "羊"]

print("="*60)
print("验证生肖ID映射")
print("="*60)

# 获取API的生肖映射
response = requests.get('http://localhost:5001/api/zodiac-mapping')
result = response.json()

if result['success']:
    mapping = result['mapping']
    order = result['order']
    
    print("\nAPI返回的生肖顺序:")
    print(f"  {' '.join(order)}")
    
    print("\nAPI返回的ID映射:")
    for id in sorted(mapping.keys(), key=lambda x: int(x)):
        print(f"  ID {id}: {mapping[id]}")
    
    print("\n验证是否与期望一致:")
    expected_correct = True
    
    # 验证顺序
    if order == NEW_ZODIAC:
        print("  ✓ 生肖顺序正确")
    else:
        print(f"  ✗ 生肖顺序错误")
        print(f"    期望: {' '.join(NEW_ZODIAC)}")
        print(f"    实际: {' '.join(order)}")
        expected_correct = False
    
    # 验证ID映射
    id_mapping_correct = True
    for i, name in enumerate(NEW_ZODIAC):
        id_num = i + 1
        if mapping.get(str(id_num)) == name:
            pass
        else:
            print(f"  ✗ ID {id_num} 映射错误: 期望 {name}, 实际 {mapping.get(str(id_num))}")
            id_mapping_correct = False
    
    if id_mapping_correct:
        print("  ✓ ID映射正确")
    
    # 验证最近几期数据
    print("\n" + "="*60)
    print("验证最近几期数据")
    print("="*60)
    
    # 读取历史数据
    import csv
    with open('real_lottery_history.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
        last_4 = lines[-4:]  # 最后4期
    
    print("\n最近4期数据:")
    for line in reversed(last_4):
        period = line[0]
        id_num = int(line[1])
        zodiac_name = mapping.get(str(id_num), "未知")
        print(f"  {period}: ID={id_num} → {zodiac_name}")
    
    print("\n验证用户指定的期号:")
    expected_data = {
        "2026098": "虎",
        "2026097": "猴",
        "2026096": "鼠",
        "2026095": "猴"
    }
    
    all_correct = True
    for line in reversed(last_4):
        period = line[0]
        id_num = int(line[1])
        zodiac_name = mapping.get(str(id_num), "未知")
        
        if period in expected_data:
            expected = expected_data[period]
            if zodiac_name == expected:
                print(f"  ✓ {period}: {zodiac_name} (正确)")
            else:
                print(f"  ✗ {period}: {zodiac_name} (错误，期望: {expected})")
                all_correct = False
    
    print("\n" + "="*60)
    if all_correct and expected_correct and id_mapping_correct:
        print("✓ 所有验证通过！")
    else:
        print("✗ 存在验证错误")
    print("="*60)

