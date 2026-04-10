#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试缓存工具函数
"""

import unittest
import time
from src.utils.cache_utils import CacheManager, data_cache, file_cache


class TestCacheUtils(unittest.TestCase):
    """测试缓存工具函数"""
    
    def test_cache_manager(self):
        """测试缓存管理器"""
        # 创建缓存管理器，设置较短的过期时间
        cache = CacheManager(ttl=1)
        
        # 测试设置和获取缓存
        cache.set('key1', 'value1')
        self.assertEqual(cache.get('key1'), 'value1')
        
        # 测试缓存大小
        self.assertEqual(cache.get_size(), 1)
        
        # 测试删除缓存
        cache.delete('key1')
        self.assertIsNone(cache.get('key1'))
        self.assertEqual(cache.get_size(), 0)
        
        # 测试清空缓存
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        self.assertEqual(cache.get_size(), 2)
        cache.clear()
        self.assertEqual(cache.get_size(), 0)
        
        # 测试缓存过期
        cache.set('key1', 'value1')
        time.sleep(1.1)  # 等待缓存过期
        self.assertIsNone(cache.get('key1'))
    
    def test_global_caches(self):
        """测试全局缓存实例"""
        # 测试数据缓存
        data_cache.set('test_data', 'test_value')
        self.assertEqual(data_cache.get('test_data'), 'test_value')
        
        # 测试文件缓存
        file_cache.set('test_file', 'test_content')
        self.assertEqual(file_cache.get('test_file'), 'test_content')


if __name__ == '__main__':
    unittest.main()
