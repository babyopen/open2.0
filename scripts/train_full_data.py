#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用完整历史数据训练模型
"""

import sys
sys.path.insert(0, '/Users/macbook/Documents/open/新版2.0docker/新版2.0/python')

from zodiac_ml_predictor import (
    load_data, prepare_training_data, train_model,
    evaluate_model, predict_next, save_model
)
import pandas as pd

def main():
    print("="*60)
    print("使用完整历史数据训练模型")
    print("="*60)
    
    # 1. 加载数据
    print("\n1. 加载历史数据...")
    df = load_data('real_lottery_history.csv')
    print(f"   数据加载完成: {len(df)} 条记录")
    
    # 2. 准备训练数据
    print("\n2. 准备训练数据...")
    X, y, feature_names = prepare_training_data(df)
    print(f"   特征维度: {X.shape[1]}")
    print(f"   样本数: {X.shape[0]}")
    
    # 3. 训练模型
    print("\n3. 训练模型...")
    model = train_model(X, y)
    
    # 4. 评估模型
    print("\n4. 评估模型...")
    metrics = evaluate_model(model, X, y)
    print(f"   准确率: {metrics['accuracy']:.4f}")
    print(f"   Top-3准确率: {metrics['top3_accuracy']:.4f}")
    print(f"   对数损失: {metrics['log_loss']:.4f}")
    
    # 5. 预测下一期
    print("\n5. 预测下一期...")
    probabilities = predict_next(model, df)
    
    # 6. 保存模型
    print("\n6. 保存模型...")
    save_model(model, 'zodiac_model.pkl')
    print("   模型已保存: zodiac_model.pkl")
    
    print("\n" + "="*60)
    print("训练完成！")
    print("="*60)

if __name__ == '__main__':
    main()
