#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生肖预测2.0 - 主训练脚本
使用模块化服务进行模型训练和评估
"""

from src.services.train_service import train_service

def main():
    """
    主程序
    """
    print("=" * 60)
    print("生肖预测2.0 - 模型训练")
    print("=" * 60)
    
    # 训练并评估模型
    metrics = train_service.train_and_evaluate('real_lottery_history.csv')
    
    if metrics:
        print("\n" + "=" * 60)
        print("训练完成")
        print("=" * 60)
        print(f"最终评估结果:")
        print(f"准确率: {metrics['accuracy']:.4f}")
        print(f"Top-3准确率: {metrics['top3_accuracy']:.4f}")
        print(f"对数损失: {metrics['log_loss']:.4f}")
    else:
        print("\n训练失败")


if __name__ == '__main__':
    main()
