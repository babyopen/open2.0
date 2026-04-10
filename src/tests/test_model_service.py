#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试模型服务
"""

import unittest
import pandas as pd
import numpy as np
from src.services.model_service import model_service


class TestModelService(unittest.TestCase):
    """测试模型服务"""
    
    def setUp(self):
        """设置测试数据"""
        # 创建测试数据
        self.test_data = pd.DataFrame({
            'period': list(range(1, 60)),
            'zodiac': [i % 12 + 1 for i in range(59)]
        })
    
    def test_build_features(self):
        """测试构建特征"""
        # 测试构建特征向量
        features = model_service._build_features(self.test_data)
        self.assertIsInstance(features, list)
        self.assertGreater(len(features), 0)
    
    def test_build_training_features(self):
        """测试构建训练特征"""
        # 测试构建训练特征
        X, y, feature_names = model_service.build_training_features(self.test_data)
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)
        self.assertIsInstance(feature_names, list)
        self.assertGreater(X.shape[0], 0)
        self.assertGreater(len(feature_names), 0)
    
    def test_load_model(self):
        """测试加载模型"""
        # 测试模型加载接口
        self.assertTrue(callable(model_service.load_model))
    
    def test_train_model(self):
        """测试训练模型"""
        # 构建训练特征
        X, y, _ = model_service.build_training_features(self.test_data)
        if X.shape[0] > 0:
            # 测试训练模型
            model = model_service.train_model(X, y)
            self.assertIsNotNone(model)
    
    def test_predict_next(self):
        """测试预测下一期"""
        # 构建训练特征
        X, y, _ = model_service.build_training_features(self.test_data)
        if X.shape[0] > 0:
            # 训练模型
            model = model_service.train_model(X, y)
            # 测试预测
            last_row = self.test_data.iloc[-1]
            predictions = model_service.predict_next(last_row, self.test_data)
            self.assertIsInstance(predictions, np.ndarray)
            # 确保预测结果是一个数组
            self.assertGreater(len(predictions), 0)


if __name__ == '__main__':
    unittest.main()
