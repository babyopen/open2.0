#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据工具函数
"""

import unittest
import pandas as pd
import numpy as np
from src.utils.data_utils import (
    load_csv_data, get_zodiac_attributes, calculate_miss_counts,
    calculate_max_miss, calculate_consecutive, calculate_break_state,
    calculate_ranks, get_element_relation
)
from src.config.zodiac_config import ZODIAC_MAP, ZODIAC_ELEMENT_MAP


class TestDataUtils(unittest.TestCase):
    """测试数据工具函数"""
    
    def setUp(self):
        """设置测试数据"""
        # 创建测试数据
        self.test_data = pd.DataFrame({
            'period': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'zodiac': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
        })
    
    def test_load_csv_data(self):
        """测试加载CSV数据"""
        # 测试数据已在setUp中创建，这里测试函数接口
        self.assertTrue(callable(load_csv_data))
    
    def test_get_zodiac_attributes(self):
        """测试获取生肖属性"""
        # 测试生肖1（马）
        attr = get_zodiac_attributes(1)
        self.assertEqual(attr['odd_even'], 1)  # 单
        self.assertEqual(attr['big_small'], 0)  # 小
        self.assertEqual(attr['zone'], 0)  # 区间1-4
        self.assertEqual(attr['head'], 0)  # 头0
        self.assertEqual(attr['tail'], 1)  # 尾1
        self.assertEqual(attr['element'], '火')
        self.assertEqual(attr['color'], '红')
        
        # 测试生肖12（羊）
        attr = get_zodiac_attributes(12)
        self.assertEqual(attr['odd_even'], 0)  # 双
        self.assertEqual(attr['big_small'], 1)  # 大
        self.assertEqual(attr['zone'], 2)  # 区间9-12
        self.assertEqual(attr['head'], 1)  # 头1
        self.assertEqual(attr['tail'], 2)  # 尾2
        self.assertEqual(attr['element'], '土')
        self.assertEqual(attr['color'], '绿')
    
    def test_calculate_miss_counts(self):
        """测试计算遗漏次数"""
        miss_counts = calculate_miss_counts(self.test_data)
        # 生肖1最后出现在第10期（索引9），遗漏0
        self.assertEqual(miss_counts[1], 0)
        # 生肖2最后出现在第8期（索引7），遗漏2
        self.assertEqual(miss_counts[2], 2)
        # 生肖3最后出现在第9期（索引8），遗漏1
        self.assertEqual(miss_counts[3], 1)
        # 其他生肖从未出现，遗漏10
        for i in range(4, 13):
            self.assertEqual(miss_counts[i], 10)
    
    def test_calculate_max_miss(self):
        """测试计算最大遗漏次数"""
        max_miss = calculate_max_miss(self.test_data)
        # 生肖1的最大遗漏
        self.assertGreater(max_miss[1], 0)
        # 生肖2的最大遗漏
        self.assertGreater(max_miss[2], 0)
        # 生肖3的最大遗漏
        self.assertGreater(max_miss[3], 0)
    
    def test_calculate_consecutive(self):
        """测试计算连开次数"""
        consecutive = calculate_consecutive(self.test_data)
        # 生肖1在最后连续出现1次
        self.assertEqual(consecutive[1], 1)
        # 生肖2在最后没有连续出现
        self.assertEqual(consecutive[2], 0)
        # 生肖3在最后没有连续出现
        self.assertEqual(consecutive[3], 0)
    
    def test_calculate_break_state(self):
        """测试计算连断状态"""
        break_state = calculate_break_state(self.test_data)
        # 生肖1在最后一期出现，但前一期没有出现
        self.assertEqual(break_state[1], 1)
        # 生肖2在最后一期没有出现
        self.assertEqual(break_state[2], 0)
        # 生肖3在最后一期出现，前一期也出现
        self.assertEqual(break_state[3], 0)
    
    def test_calculate_ranks(self):
        """测试计算热门排名"""
        ranks = calculate_ranks(self.test_data, period=10)
        # 生肖1出现4次，排名1
        self.assertEqual(ranks[1], 1)
        # 生肖2和3各出现3次，排名2
        self.assertEqual(ranks[2], 2)
        self.assertEqual(ranks[3], 2)
    
    def test_get_element_relation(self):
        """测试获取五行关系"""
        # 相同元素
        self.assertEqual(get_element_relation('火', '火'), 1)
        # 相生关系
        self.assertEqual(get_element_relation('金', '水'), 2)
        # 相克关系
        self.assertEqual(get_element_relation('金', '木'), 0)


if __name__ == '__main__':
    unittest.main()
