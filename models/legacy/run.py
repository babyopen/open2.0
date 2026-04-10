#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遗留模型预测脚本
模型：best_zodiac_model.pkl (旧版最佳模型)
"""

import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

from models.predict_model import predict_with_model

if __name__ == "__main__":
    result = predict_with_model('best_zodiac_model.pkl', '遗留最佳模型')
