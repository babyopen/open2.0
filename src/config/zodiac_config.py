#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生肖配置文件 - 集中管理所有生肖相关的配置
"""

# 生肖ID到名称的映射
ZODIAC_MAP = {
    1: '马', 2: '蛇', 3: '龙', 4: '兔', 5: '虎', 6: '牛',
    7: '鼠', 8: '猪', 9: '狗', 10: '鸡', 11: '猴', 12: '羊'
}

# 生肖到五行的映射
ZODIAC_ELEMENT_MAP = {
    1: '火',   # 马
    2: '火',   # 蛇
    3: '土',   # 龙
    4: '木',   # 兔
    5: '木',   # 虎
    6: '土',   # 牛
    7: '水',   # 鼠
    8: '水',   # 猪
    9: '土',   # 狗
    10: '金',  # 鸡
    11: '金',  # 猴
    12: '土'   # 羊
}

# 生肖到波色的映射
ZODIAC_COLOR_MAP = {
    1: '红', 2: '红', 3: '红', 4: '绿', 5: '蓝', 6: '绿',
    7: '红', 8: '蓝', 9: '绿', 10: '红', 11: '蓝', 12: '绿'
}

# 五行相生关系
ELEMENT_GENERATE = {
    '金': '水',
    '水': '木',
    '木': '火',
    '火': '土',
    '土': '金'
}

# 五行相克关系
ELEMENT_OVERCOME = {
    '金': '木',
    '木': '土',
    '土': '水',
    '水': '火',
    '火': '金'
}

# 模型配置
MODEL_CONFIG = {
    'n_estimators': 200,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42
}

# 数据配置
DATA_CONFIG = {
    'DATA_CACHE_TTL': 60,  # 数据缓存时间（秒）
    'MIN_HISTORY_LENGTH': 50,  # 最小历史数据长度
    'RECENT_PERIODS': {
        'short': 10,  # 短期
        'medium': 20,  # 中期
        'long': 50  # 长期
    }
}

# API配置
API_CONFIG = {
    'HOST': '0.0.0.0',
    'PORT': 8000,
    'DEBUG': False
}
