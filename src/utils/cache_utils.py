#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存工具函数 - 处理缓存相关的公共操作
"""

import time
from src.config.zodiac_config import DATA_CONFIG


class CacheManager:
    """
    缓存管理器 - 处理数据和文件缓存
    """
    
    def __init__(self, ttl=DATA_CONFIG['DATA_CACHE_TTL']):
        """
        初始化缓存管理器
        
        Args:
            ttl: 缓存过期时间（秒）
        """
        self.ttl = ttl
        self.caches = {}
    
    def get(self, key):
        """
        获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，如果缓存不存在或已过期则返回None
        """
        if key not in self.caches:
            return None
        
        value, timestamp = self.caches[key]
        if time.time() - timestamp > self.ttl:
            # 缓存已过期
            del self.caches[key]
            return None
        
        return value
    
    def set(self, key, value):
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        self.caches[key] = (value, time.time())
    
    def delete(self, key):
        """
        删除缓存
        
        Args:
            key: 缓存键
        """
        if key in self.caches:
            del self.caches[key]
    
    def clear(self):
        """
        清空所有缓存
        """
        self.caches.clear()
    
    def get_size(self):
        """
        获取缓存大小
        
        Returns:
            int: 缓存条目数量
        """
        return len(self.caches)


# 全局缓存管理器实例
data_cache = CacheManager()
file_cache = CacheManager(ttl=300)  # 文件缓存时间更长
