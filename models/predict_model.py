#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用模型预测脚本
"""

import sys
import os
import pickle
import pandas as pd
import numpy as np

# 添加父目录到路径
sys.path.insert(0, os.path.abspath('../python'))

from zodiac_ml_predictor import ZodiacMLPredictor

def load_model(model_path):
    """加载训练好的模型"""
    try:
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            model = model_data.get('model', model_data)
            print(f"✓ 模型加载成功: {model_path}")
            return model
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        return None

def load_history_data():
    """加载历史数据"""
    history_path = '../data/real_lottery_history.csv'
    try:
        df = pd.read_csv(history_path)
        print(f"✓ 历史数据加载成功: {len(df)} 条记录")
        return df
    except Exception as e:
        print(f"✗ 历史数据加载失败: {e}")
        return None

def predict_with_model(model_path, model_name="模型"):
    """使用指定模型进行预测"""
    print(f"\n{'='*60}")
    print(f"【{model_name}】预测")
    print(f"{'='*60}")
    
    # 加载模型
    model = load_model(model_path)
    if model is None:
        return None
    
    # 加载历史数据
    df = load_history_data()
    if df is None:
        return None
    
    # 创建预测器
    predictor = ZodiacMLPredictor()
    
    # 构建历史数据格式
    history = []
    for _, row in df.iterrows():
        history.append({
            'period': int(row['period']),
            'zodiac': int(row['zodiac'])
        })
    
    # 进行预测
    result = predictor.predict(model, history)
    
    if result:
        print(f"\n{model_name} - 预测结果:")
        for zodiac in result['predictions'][:3]:
            print(f"  {zodiac['name']} (ID: {zodiac['id']}) - 概率: {zodiac['probability']:.2%}")
        
        print(f"\n推荐: {result['recommendation']['name']}")
        return result
    
    return None

if __name__ == "__main__":
    print("生肖预测器")
    print("请在各模型文件夹中运行对应的脚本")
