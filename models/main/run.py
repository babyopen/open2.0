#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主模型预测脚本 - zodiac_model.pkl
训练数据：829期真实历史数据
"""

import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

from models.predict_model import predict_with_model

if __name__ == "__main__":
    result = predict_with_model('zodiac_model.pkl', '主模型 (829期完整数据)')
