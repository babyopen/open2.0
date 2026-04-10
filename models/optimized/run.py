#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化参数模型预测脚本
训练数据：完整数据 + 调整参数
"""

import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

from models.predict_model import predict_with_model

if __name__ == "__main__":
    result = predict_with_model('zodiac_model_完整数据-调整参数.pkl', '优化参数模型')
