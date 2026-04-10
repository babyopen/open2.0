#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据服务 - 处理数据的加载、缓存和预处理
"""

import os
import pandas as pd
from src.utils.data_utils import load_csv_data
from src.utils.cache_utils import data_cache
from src.config.zodiac_config import DATA_CONFIG, ZODIAC_MAP


class DataService:
    """
    数据服务类 - 处理数据的加载、缓存和预处理
    """
    
    def __init__(self):
        """
        初始化数据服务
        """
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    
    def get_history_data(self, file_name='lottery_history.csv'):
        """
        获取历史数据，带缓存机制
        
        Args:
            file_name: 数据文件名
        
        Returns:
            DataFrame: 历史数据
        """
        # 检查缓存
        cache_key = f'history_data_{file_name}'
        cached_data = data_cache.get(cache_key)
        if cached_data is not None:
            return cached_data
        
        # 读取数据
        data_path = os.path.join(self.data_dir, file_name)
        df = load_csv_data(data_path)
        
        # 更新缓存
        if df is not None:
            data_cache.set(cache_key, df)
        
        return df
    
    def get_real_history_data(self):
        """
        获取真实历史数据
        
        Returns:
            DataFrame: 真实历史数据
        """
        return self.get_history_data('real_lottery_history.csv')
    
    def process_frontend_data(self, frontend_data):
        """
        处理前端传递的历史数据
        
        Args:
            frontend_data: 前端传递的历史数据
        
        Returns:
            DataFrame: 处理后的数据
        """
        if not frontend_data:
            return None
        
        # 转换数据格式
        periods = []
        zodiacs = []
        
        for item in frontend_data:
            if 'period' in item and 'zodiac' in item:
                # 处理前端传递的生肖名称，转换为数字
                zodiac_name = item['zodiac']
                # 反向映射：生肖名称到数字
                zodiac_num = None
                for num, name in ZODIAC_MAP.items():
                    if name == zodiac_name:
                        zodiac_num = num
                        break
                
                if zodiac_num:
                    periods.append(item['period'])
                    zodiacs.append(zodiac_num)
        
        # 创建DataFrame
        if periods and zodiacs:
            df = pd.DataFrame({'period': periods, 'zodiac': zodiacs})
            # 按期号排序
            df = df.sort_values('period').reset_index(drop=True)
            return df
        
        return None
    
    def ensure_min_history_length(self, df, min_length=DATA_CONFIG['MIN_HISTORY_LENGTH']):
        """
        确保历史数据长度足够
        
        Args:
            df: 历史数据
            min_length: 最小长度
        
        Returns:
            DataFrame: 处理后的数据
        """
        if df is None:
            return None
        
        if len(df) >= min_length:
            return df
        
        # 数据量不足，使用本地数据作为补充
        local_df = self.get_history_data()
        if local_df is not None and len(local_df) > len(df):
            return local_df
        
        return df
    
    def get_latest_period_data(self, df):
        """
        获取最新一期的数据
        
        Args:
            df: 历史数据
        
        Returns:
            Series: 最新一期的数据
        """
        if df is None or len(df) == 0:
            return None
        
        return df.iloc[-1]


# 全局数据服务实例
data_service = DataService()
