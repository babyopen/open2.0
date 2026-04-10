#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练服务 - 处理模型的训练和评估
"""

import numpy as np
from sklearn.metrics import accuracy_score, log_loss, classification_report
from src.services.model_service import model_service
from src.services.data_service import data_service
from src.config.zodiac_config import ZODIAC_MAP


class TrainService:
    """
    训练服务类 - 处理模型的训练和评估
    """
    
    def __init__(self):
        """
        初始化训练服务
        """
        pass
    
    def train_and_evaluate(self, file_name='real_lottery_history.csv'):
        """
        训练并评估模型
        
        Args:
            file_name: 训练数据文件名
        
        Returns:
            dict: 评估结果
        """
        # 加载数据
        df = data_service.get_history_data(file_name)
        if df is None:
            print("数据加载失败")
            return None
        
        # 构建特征
        X, y, feature_names = model_service.build_training_features(df)
        if X.shape[0] == 0:
            print("特征构建失败")
            return None
        
        # 划分训练集和测试集（按时间顺序）
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        print(f"训练集大小: {len(X_train)}")
        print(f"测试集大小: {len(X_test)}")
        
        # 训练模型
        model = model_service.train_model(X_train, y_train)
        
        # 评估模型
        metrics = self.evaluate_model(model, X_test, y_test)
        
        # 特征重要性
        self.get_feature_importance(model, feature_names)
        
        # 预测下一期
        self.predict_next(model, df)
        
        # 保存模型
        model_service.save_model('zodiac_model.pkl')
        
        return metrics
    
    def evaluate_model(self, model, X_test, y_test):
        """
        评估模型性能
        
        Args:
            model: 训练好的模型
            X_test: 测试特征
            y_test: 测试标签
        
        Returns:
            dict: 评估指标
        """
        print("\n========== 模型评估 ==========")
        
        # 预测概率
        y_pred_proba = model.predict_proba(X_test)
        
        # 预测类别
        y_pred = model.predict(X_test)
        
        # 准确率
        accuracy = accuracy_score(y_test, y_pred)
        print(f"准确率: {accuracy:.4f}")
        
        # Top-3 准确率
        top3_correct = 0
        for i in range(len(y_test)):
            top3_indices = np.argsort(y_pred_proba[i])[-3:]
            if y_test[i] in top3_indices:
                top3_correct += 1
        top3_accuracy = top3_correct / len(y_test)
        print(f"Top-3 准确率: {top3_accuracy:.4f}")
        
        # 对数损失
        try:
            loss = log_loss(y_test, y_pred_proba, labels=list(range(12)))
            print(f"对数损失: {loss:.4f}")
        except:
            loss = 0
            print(f"对数损失: 无法计算（测试集类别不全）")
        
        # 分类报告
        print("\n分类报告:")
        target_names = [ZODIAC_MAP[i+1] for i in range(12)]
        try:
            print(classification_report(y_test, y_pred, target_names=target_names, labels=list(range(12))[:len(np.unique(y_test))]))
        except:
            print("分类报告: 无法生成（测试集类别不全）")
        
        return {
            'accuracy': accuracy,
            'top3_accuracy': top3_accuracy,
            'log_loss': loss
        }
    
    def get_feature_importance(self, model, feature_names, top_n=20):
        """
        获取特征重要性
        
        Args:
            model: 训练好的模型
            feature_names: 特征名称列表
            top_n: 显示前N个重要特征
        """
        if not hasattr(model, 'feature_importances_'):
            return
        
        print(f"\n========== 前{top_n}个重要特征 ==========")
        
        importance = model.feature_importances_
        indices = np.argsort(importance)[::-1]
        
        for i in range(min(top_n, len(feature_names))):
            idx = indices[i]
            print(f"{i+1:2d}. {feature_names[idx]:30s} {importance[idx]:.4f}")
    
    def predict_next(self, model, df):
        """
        预测下一期
        
        Args:
            model: 训练好的模型
            df: 历史数据
        """
        print("\n========== 下一期预测 ==========")
        
        last_row = df.iloc[-1]
        probabilities = model_service.predict_next(last_row, df)
        
        # 排序并显示概率
        zodiac_probs = [(i+1, ZODIAC_MAP[i+1], probabilities[i]) 
                       for i in range(12)]
        zodiac_probs.sort(key=lambda x: x[2], reverse=True)
        
        print("\n生肖预测概率（按概率排序）:")
        print("-" * 40)
        for zodiac_id, zodiac_name, prob in zodiac_probs:
            bar = "█" * int(prob * 50)
            print(f"{zodiac_id:2d}. {zodiac_name}: {prob:.4f} {bar}")
        
        print(f"\n推荐生肖: {zodiac_probs[0][1]} (概率: {zodiac_probs[0][2]:.4f})")
        print(f"次选生肖: {zodiac_probs[1][1]} (概率: {zodiac_probs[1][2]:.4f})")
        print(f"备选生肖: {zodiac_probs[2][1]} (概率: {zodiac_probs[2][2]:.4f})")


# 全局训练服务实例
train_service = TrainService()
