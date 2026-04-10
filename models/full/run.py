#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整数据集模型预测脚本
训练数据：完整历史数据集
"""

import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

from models.predict_model import predict_with_model

if __name__ == "__main__":
    result = predict_with_model('zodiac_model_完整数据集.pkl', '完整数据集模型')
