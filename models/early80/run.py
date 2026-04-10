#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前80期数据模型预测脚本
训练数据：前80期历史数据
"""

import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

from models.predict_model import predict_with_model

if __name__ == "__main__":
    result = predict_with_model('zodiac_model_前80期数据.pkl', '前80期数据模型')
