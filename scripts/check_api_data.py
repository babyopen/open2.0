#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查前端API数据并与后端CSV对比
"""

import requests
import csv
import json

def get_frontend_api_data():
    """
    从前端使用的API获取数据
    """
    url = 'https://history.macaumarksix.com/history/macaujc2/y/2026'
    
    try:
        print(f"正在访问API: {url}")
        response = requests.get(url, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API请求失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"访问API时出错: {e}")
        return None

def parse_api_data(data):
    """
    解析API数据，提取最近10期
    """
    if not data or 'data' not in data:
        return None
    
    raw_data = data['data']
    
    # 过滤有效数据
    valid_data = []
    for item in raw_data:
        expect = item.get('expect', '')
        open_code = item.get('openCode', '')
        if expect and open_code and len(open_code.split(',')) == 7:
            valid_data.append(item)
    
    # 去重并排序
    unique_map = {}
    for item in valid_data:
        expect_num = int(item['expect'])
        if expect_num and expect_num not in unique_map:
            unique_map[expect_num] = item
    
    sorted_data = sorted(unique_map.values(), 
                         key=lambda x: int(x['expect']), 
                         reverse=True)
    
    return sorted_data[:10]  # 返回最近10期

def get_zodiac_from_api_item(item):
    """
    从API数据项中提取生肖
    """
    zodiac_arr = (item.get('zodiac', ',,,,,,,,,,,').split(','))
    # 简化映射
    zodiac_map = {
        '鼠': '鼠', '牛': '牛', '虎': '虎', '兔': '兔',
        '龍': '龙', '龙': '龙', '蛇': '蛇', '馬': '马', '马': '马',
        '羊': '羊', '猴': '猴', '雞': '鸡', '鸡': '鸡', '狗': '狗',
        '豬': '猪', '猪': '猪'
    }
    
    if len(zodiac_arr) >= 7:
        zodiac_raw = zodiac_arr[6]
        return zodiac_map.get(zodiac_raw, zodiac_raw)
    return '-'

def load_backend_csv():
    """
    加载后端CSV数据
    """
    data = []
    try:
        with open('real_lottery_history.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过标题
            for row in reader:
                if len(row) >= 2:
                    data.append({
                        'period': int(row[0]),
                        'zodiac_id': int(row[1])
                    })
    except Exception as e:
        print(f"加载CSV失败: {e}")
    
    return data[-10:]  # 返回最近10期

def main():
    print("=" * 80)
    print("前端与后端开奖记录对比")
    print("=" * 80)
    
    # 后端生肖映射（新顺序）
    backend_zodiac_map = {
        1: '马', 2: '蛇', 3: '龙', 4: '兔', 5: '虎', 6: '牛',
        7: '鼠', 8: '猪', 9: '狗', 10: '鸡', 11: '猴', 12: '羊'
    }
    
    # 1. 获取后端CSV数据
    print("\n1. 后端CSV数据（最近10期）")
    print("-" * 80)
    backend_data = load_backend_csv()
    
    print(f"{'期号':<10} {'生肖ID':<8} {'后端生肖':<10}")
    print("-" * 30)
    for item in backend_data:
        zodiac_name = backend_zodiac_map.get(item['zodiac_id'], '未知')
        print(f"{item['period']:<10} {item['zodiac_id']:<8} {zodiac_name:<10}")
    
    # 2. 尝试获取前端API数据
    print("\n2. 前端API数据")
    print("-" * 80)
    api_data = get_frontend_api_data()
    
    if api_data:
        parsed_data = parse_api_data(api_data)
        if parsed_data:
            print(f"{'期号':<10} {'生肖':<10}")
            print("-" * 20)
            for item in parsed_data:
                zodiac = get_zodiac_from_api_item(item)
                print(f"{item['expect']:<10} {zodiac:<10}")
            
            # 3. 对比数据
            print("\n3. 数据对比")
            print("-" * 80)
            
            backend_periods = {item['period']: item for item in backend_data}
            
            match_count = 0
            total_count = 0
            
            print(f"{'期号':<10} {'后端生肖':<10} {'前端生肖':<10} {'匹配':<6}")
            print("-" * 46)
            
            for item in parsed_data:
                period = int(item['expect'])
                frontend_zodiac = get_zodiac_from_api_item(item)
                
                if period in backend_periods:
                    total_count += 1
                    backend_item = backend_periods[period]
                    backend_zodiac = backend_zodiac_map.get(backend_item['zodiac_id'], '未知')
                    
                    match = "✓" if backend_zodiac == frontend_zodiac else "✗"
                    if match == "✓":
                        match_count += 1
                    
                    print(f"{period:<10} {backend_zodiac:<10} {frontend_zodiac:<10} {match:<6}")
            
            print("-" * 46)
            if total_count > 0:
                match_rate = (match_count / total_count) * 100
                print(f"匹配率: {match_count}/{total_count} ({match_rate:.1f}%)")
        else:
            print("无法解析API数据")
    else:
        print("无法访问前端API，无法进行对比")
    
    print("\n" + "=" * 80)
    print("对比完成")
    print("=" * 80)

if __name__ == '__main__':
    main()
