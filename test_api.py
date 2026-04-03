#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试文件
用于验证开奖记录接口的正确性和稳定性
"""

import unittest
import requests
import json
from unittest.mock import Mock, patch
from api.index import app

class TestLotteryAPI(unittest.TestCase):
    """测试开奖记录API"""
    
    def setUp(self):
        """设置测试环境"""
        app.testing = True
        self.client = app.test_client()
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['message'], 'API is running')
    
    def test_zodiac_mapping(self):
        """测试生肖映射接口"""
        response = self.client.get('/api/zodiac-mapping')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('zodiacs', data)
        self.assertEqual(len(data['zodiacs']), 12)
        # 检查是否包含预期的生肖
        self.assertIn('马', data['zodiacs'].values())
    
    @patch('api.index.requests.get')
    def test_latest_lottery_success(self, mock_get):
        """测试获取最新开奖记录接口（成功）"""
        # 模拟外部API响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'expect': '2024001',
                    'openCode': '1,2,3,4,5,6,7'
                },
                {
                    'expect': '2024002',
                    'openCode': '8,9,10,11,12,13,14'
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/lottery/latest')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 2)
    
    @patch('api.index.requests.get')
    def test_latest_lottery_api_error(self, mock_get):
        """测试获取最新开奖记录接口（API错误）"""
        # 模拟外部API失败
        mock_get.side_effect = requests.RequestException('API error')
        
        response = self.client.get('/api/lottery/latest')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'API_ERROR')
    
    @patch('api.index.requests.get')
    def test_history_lottery_success(self, mock_get):
        """测试获取历史开奖记录接口（成功）"""
        # 模拟外部API响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'expect': '2024001',
                    'openCode': '1,2,3,4,5,6,7'
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/lottery/history?year=2024')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data'], list)
    
    def test_zodiac_history_success(self):
        """测试获取生肖开奖记录接口（成功）"""
        response = self.client.get('/api/lottery/zodiac')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['data'], list)
    
    def test_cache_clear(self):
        """测试清空缓存接口"""
        response = self.client.post('/api/cache/clear')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], '缓存已清空')

if __name__ == '__main__':
    unittest.main()
