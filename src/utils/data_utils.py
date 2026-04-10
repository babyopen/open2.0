#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据工具函数 - 处理数据相关的公共操作
"""

import pandas as pd
import numpy as np
import os
from src.config.zodiac_config import ZODIAC_MAP, ZODIAC_ELEMENT_MAP, ZODIAC_COLOR_MAP


def load_csv_data(file_path):
    """
    加载CSV数据并按期号排序
    
    Args:
        file_path: CSV文件路径
    
    Returns:
        DataFrame: 排序后的数据
    """
    try:
        df = pd.read_csv(file_path)
        # 确保数据类型正确
        df['period'] = df['period'].astype(int)
        df['zodiac'] = df['zodiac'].astype(int)
        
        # 按期号排序
        df = df.sort_values('period').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None


def get_zodiac_attributes(zodiac_id):
    """
    获取生肖的各种属性
    
    Args:
        zodiac_id: 生肖ID
    
    Returns:
        dict: 生肖属性
    """
    # 单双
    odd_even = zodiac_id % 2  # 0=双, 1=单
    
    # 大小 (1-6小, 7-12大)
    big_small = 1 if zodiac_id >= 7 else 0  # 0=小, 1=大
    
    # 区间 (1-4, 5-8, 9-12)
    if zodiac_id <= 4:
        zone = 0
    elif zodiac_id <= 8:
        zone = 1
    else:
        zone = 2
    
    # 头数 (1-9为0, 10-12为1)
    head = 1 if zodiac_id >= 10 else 0
    
    # 尾数
    tail = zodiac_id % 10
    
    return {
        'odd_even': odd_even,
        'big_small': big_small,
        'zone': zone,
        'head': head,
        'tail': tail,
        'element': ZODIAC_ELEMENT_MAP[zodiac_id],
        'color': ZODIAC_COLOR_MAP[zodiac_id]
    }


def calculate_miss_counts(history, n_zodiacs=12):
    """
    计算每个生肖的遗漏次数
    
    Args:
        history: 历史数据
        n_zodiacs: 生肖数量
    
    Returns:
        dict: 每个生肖的遗漏次数
    """
    miss_counts = {i: 0 for i in range(1, n_zodiacs + 1)}
    
    for z in range(1, n_zodiacs + 1):
        last_appear = -1
        for i, row in history.iterrows():
            if row['zodiac'] == z:
                last_appear = i
        
        if last_appear == -1:
            miss_counts[z] = len(history)
        else:
            miss_counts[z] = len(history) - last_appear - 1
    
    return miss_counts


def calculate_max_miss(history, n_zodiacs=12):
    """
    计算每个生肖的最大遗漏次数
    
    Args:
        history: 历史数据
        n_zodiacs: 生肖数量
    
    Returns:
        dict: 每个生肖的最大遗漏次数
    """
    max_miss = {i: 0 for i in range(1, n_zodiacs + 1)}
    
    for z in range(1, n_zodiacs + 1):
        current_miss = 0
        for i, row in history.iterrows():
            if row['zodiac'] == z:
                max_miss[z] = max(max_miss[z], current_miss)
                current_miss = 0
            else:
                current_miss += 1
    
    return max_miss


def calculate_consecutive(history, n_zodiacs=12):
    """
    计算每个生肖的连开次数
    
    Args:
        history: 历史数据
        n_zodiacs: 生肖数量
    
    Returns:
        dict: 每个生肖的连开次数
    """
    consecutive = {i: 0 for i in range(1, n_zodiacs + 1)}
    
    for z in range(1, n_zodiacs + 1):
        cons = 0
        # 从最后一期开始往前遍历
        for i in range(len(history) - 1, -1, -1):
            if history.iloc[i]['zodiac'] == z:
                cons += 1
            else:
                break
        consecutive[z] = cons
    
    return consecutive


def calculate_break_state(history, n_zodiacs=12):
    """
    计算每个生肖的连断状态
    
    Args:
        history: 历史数据
        n_zodiacs: 生肖数量
    
    Returns:
        dict: 每个生肖的连断状态
    """
    break_state = {i: 0 for i in range(1, n_zodiacs + 1)}
    
    if len(history) >= 2:
        last = history.iloc[-1]['zodiac']
        second_last = history.iloc[-2]['zodiac']
        
        for z in range(1, n_zodiacs + 1):
            break_state[z] = 1 if (last == z and second_last != z) else 0
    
    return break_state


def calculate_ranks(history, n_zodiacs=12, period=20):
    """
    计算每个生肖的热门排名
    
    Args:
        history: 历史数据
        n_zodiacs: 生肖数量
        period: 统计周期
    
    Returns:
        dict: 每个生肖的排名
    """
    recent_data = history.tail(period)
    counts = recent_data['zodiac'].value_counts().to_dict()
    ranks = {}
    
    for z in range(1, n_zodiacs + 1):
        count = counts.get(z, 0)
        # 计算排名（出现次数越多，排名越靠前）
        rank = 1
        for other_z in range(1, n_zodiacs + 1):
            if counts.get(other_z, 0) > count:
                rank += 1
        ranks[z] = rank
    
    return ranks


def get_element_relation(element1, element2):
    """
    获取两个五行元素之间的关系
    
    Args:
        element1: 第一个五行元素
        element2: 第二个五行元素
    
    Returns:
        int: 0=相克, 1=相同, 2=相生
    """
    from src.config.zodiac_config import ELEMENT_GENERATE
    
    if element1 == element2:
        return 1  # 相同
    elif ELEMENT_GENERATE.get(element1) == element2:
        return 2  # 相生
    else:
        return 0  # 相克
