#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型服务 - 处理模型的加载、训练和预测
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.config.zodiac_config import MODEL_CONFIG, ZODIAC_MAP, ZODIAC_ELEMENT_MAP
from src.utils.data_utils import (
    calculate_miss_counts, calculate_max_miss, calculate_consecutive,
    calculate_break_state, calculate_ranks, get_zodiac_attributes,
    get_element_relation
)


class ModelService:
    """
    模型服务类 - 处理模型的加载、训练和预测
    """
    
    def __init__(self):
        """
        初始化模型服务
        """
        self.model = None
        self.n_zodiacs = 12
    
    def load_model(self, model_path):
        """
        加载模型
        
        Args:
            model_path: 模型文件路径
        
        Returns:
            model: 加载的模型
        """
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            return self.model
        except Exception as e:
            print(f"模型加载失败: {e}")
            return None
    
    def train_model(self, X_train, y_train):
        """
        训练模型
        
        Args:
            X_train: 训练特征
            y_train: 训练标签
        
        Returns:
            model: 训练好的模型
        """
        # 计算类别权重
        class_counts = np.bincount(y_train)
        total = len(y_train)
        class_weights = {i: total / (12 * count) if count > 0 else 1.0 
                        for i, count in enumerate(class_counts)}
        
        # 创建样本权重
        sample_weights = np.array([class_weights[y] for y in y_train])
        
        # 创建RandomForest分类器
        model = RandomForestClassifier(
            n_estimators=MODEL_CONFIG['n_estimators'],
            max_depth=MODEL_CONFIG['max_depth'],
            min_samples_split=MODEL_CONFIG['min_samples_split'],
            min_samples_leaf=MODEL_CONFIG['min_samples_leaf'],
            random_state=MODEL_CONFIG['random_state'],
            class_weight='balanced',
            n_jobs=-1
        )
        
        # 训练模型
        model.fit(X_train, y_train, sample_weight=sample_weights)
        
        self.model = model
        return model
    
    def save_model(self, model_path):
        """
        保存模型
        
        Args:
            model_path: 保存路径
        """
        if self.model:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            return True
        return False
    
    def predict_next(self, last_period_data, all_history):
        """
        预测下一期的生肖概率
        
        Args:
            last_period_data: 最近一期的数据
            all_history: 所有历史数据
        
        Returns:
            probabilities: 12个生肖的概率
        """
        if not self.model:
            return None
        
        # 构建特征
        features = self._build_features(all_history)
        X = np.array([features])
        
        # 预测概率
        probabilities = self.model.predict_proba(X)[0]
        
        return probabilities
    
    def _build_features(self, history):
        """
        构建特征向量
        
        Args:
            history: 历史数据
        
        Returns:
            features: 特征向量
        """
        features = []
        idx = len(history)
        
        # 基础统计特征
        miss_counts = calculate_miss_counts(history, self.n_zodiacs)
        max_miss = calculate_max_miss(history, self.n_zodiacs)
        consecutive = calculate_consecutive(history, self.n_zodiacs)
        break_state = calculate_break_state(history, self.n_zodiacs)
        ranks = calculate_ranks(history, self.n_zodiacs, period=20)
        
        # 近N期统计
        recent_10 = history.tail(10)
        recent_20 = history.tail(20)
        recent_50 = history.tail(50)
        
        # 添加基础统计特征
        for z in range(1, self.n_zodiacs + 1):
            miss = miss_counts[z]
            max_m = max_miss[z] if max_miss[z] > 0 else 1
            
            features.extend([
                miss,                                           # 当前遗漏
                miss / max_m,                                   # 遗漏比例
                (recent_10['zodiac'] == z).sum(),              # 近10期次数
                (recent_20['zodiac'] == z).sum(),              # 近20期次数
                (recent_50['zodiac'] == z).sum(),              # 近50期次数
                (recent_10['zodiac'] == z).sum() / 10,         # 近10期频率
                (recent_20['zodiac'] == z).sum() / 20,         # 近20期频率
                ranks[z],                                       # 热门排名
                consecutive[z],                                 # 连开次数
                break_state[z],                                 # 连断状态
            ])
        
        # 动态特征
        if len(history) > 0:
            prev_zodiac = history.iloc[-1]['zodiac']
            features.append(prev_zodiac)
            features.append(0)  # 位置间隔（无法预知）
            features.append(1)  # 五行关系（默认相同）
            
            prev_attr = get_zodiac_attributes(prev_zodiac)
            features.extend([0, 0, 0, 0, 0, 0])  # 其他比较特征（无法预知）
        else:
            # 历史数据为空，使用默认值
            features.extend([0] * 9)  # 9个动态特征
        
        # 时序特征
        for z in range(1, self.n_zodiacs + 1):
            # 获取该生肖的历史出现位置
            appear_indices = []
            for i, row in history.iterrows():
                if row['zodiac'] == z:
                    appear_indices.append(i)
            
            # 计算间隔
            if len(appear_indices) >= 2:
                intervals = [appear_indices[i] - appear_indices[i-1] 
                           for i in range(1, len(appear_indices))]
                interval_mean = np.mean(intervals[-5:])  # 最近5次
                interval_std = np.std(intervals[-5:]) if len(intervals) >= 5 else 0
            else:
                interval_mean = 0
                interval_std = 0
            
            features.extend([interval_mean, interval_std, 0])  # 热度变化默认0
        
        return features
    
    def build_training_features(self, df):
        """
        为训练数据构建特征
        
        Args:
            df: 训练数据
        
        Returns:
            X: 特征矩阵
            y: 标签
            feature_names: 特征名称
        """
        n_samples = len(df)
        features_list = []
        labels = []
        
        # 特征名称
        feature_names = []
        
        # 基础统计特征
        for i in range(1, self.n_zodiacs + 1):
            feature_names.extend([
                f'zodiac_{i}_miss',           # 当前遗漏
                f'zodiac_{i}_miss_ratio',     # 遗漏比例
                f'zodiac_{i}_count_10',       # 近10期出现次数
                f'zodiac_{i}_count_20',       # 近20期出现次数
                f'zodiac_{i}_count_50',       # 近50期出现次数
                f'zodiac_{i}_freq_10',        # 近10期频率
                f'zodiac_{i}_freq_20',        # 近20期频率
                f'zodiac_{i}_rank',           # 热门排名
                f'zodiac_{i}_consecutive',    # 连开次数
                f'zodiac_{i}_break',          # 连断状态
            ])
        
        # 动态特征（与上期关联）
        feature_names.extend([
            'prev_zodiac',           # 上期生肖
            'position_gap',          # 位置间隔
            'element_relation',      # 五行关系
            'color_same',            # 波色相同
            'odd_even_same',         # 单双相同
            'big_small_same',        # 大小相同
            'zone_same',             # 区间相同
            'head_same',             # 头数相同
            'tail_same',             # 尾数相同
        ])
        
        # 时序特征
        for i in range(1, self.n_zodiacs + 1):
            feature_names.extend([
                f'zodiac_{i}_interval_mean',   # 间隔均值
                f'zodiac_{i}_interval_std',    # 间隔标准差
                f'zodiac_{i}_rank_change',     # 热度变化
            ])
        
        # 从第51期开始构建特征（确保有足够的历史数据）
        start_idx = 50
        
        for idx in range(start_idx, n_samples):
            # 当前期数据
            current_zodiac = df.iloc[idx]['zodiac']
            
            # 历史数据（当前期之前）
            history = df.iloc[:idx]
            
            features = []
            
            # 基础统计特征
            miss_counts = calculate_miss_counts(history, self.n_zodiacs)
            max_miss = calculate_max_miss(history, self.n_zodiacs)
            consecutive = calculate_consecutive(history, self.n_zodiacs)
            break_state = calculate_break_state(history, self.n_zodiacs)
            ranks = calculate_ranks(history, self.n_zodiacs, period=20)
            
            # 近N期统计
            recent_10 = history.tail(10)
            recent_20 = history.tail(20)
            recent_50 = history.tail(50)
            
            # 添加基础统计特征
            for z in range(1, self.n_zodiacs + 1):
                miss = miss_counts[z]
                max_m = max_miss[z] if max_miss[z] > 0 else 1
                
                features.extend([
                    miss,                                           # 当前遗漏
                    miss / max_m,                                   # 遗漏比例
                    (recent_10['zodiac'] == z).sum(),              # 近10期次数
                    (recent_20['zodiac'] == z).sum(),              # 近20期次数
                    (recent_50['zodiac'] == z).sum(),              # 近50期次数
                    (recent_10['zodiac'] == z).sum() / 10,         # 近10期频率
                    (recent_20['zodiac'] == z).sum() / 20,         # 近20期频率
                    ranks[z],                                       # 热门排名
                    consecutive[z],                                 # 连开次数
                    break_state[z],                                 # 连断状态
                ])
            
            # 动态特征
            prev_zodiac = history.iloc[-1]['zodiac']
            features.append(prev_zodiac)
            
            # 位置间隔
            position_gap = abs(current_zodiac - prev_zodiac)
            if position_gap > 6:
                position_gap = 12 - position_gap
            features.append(position_gap)
            
            # 五行关系
            prev_element = ZODIAC_ELEMENT_MAP[prev_zodiac]
            curr_element = ZODIAC_ELEMENT_MAP[current_zodiac]
            element_relation = get_element_relation(prev_element, curr_element)
            features.append(element_relation)
            
            # 其他属性比较
            prev_attr = get_zodiac_attributes(prev_zodiac)
            curr_attr = get_zodiac_attributes(current_zodiac)
            
            features.extend([
                1 if prev_attr['color'] == curr_attr['color'] else 0,      # 波色相同
                1 if prev_attr['odd_even'] == curr_attr['odd_even'] else 0, # 单双相同
                1 if prev_attr['big_small'] == curr_attr['big_small'] else 0, # 大小相同
                1 if prev_attr['zone'] == curr_attr['zone'] else 0,        # 区间相同
                1 if prev_attr['head'] == curr_attr['head'] else 0,        # 头数相同
                1 if prev_attr['tail'] == curr_attr['tail'] else 0,        # 尾数相同
            ])
            
            # 时序特征
            for z in range(1, self.n_zodiacs + 1):
                # 获取该生肖的历史出现位置
                appear_indices = []
                for i, row in history.iterrows():
                    if row['zodiac'] == z:
                        appear_indices.append(i)
                
                # 计算间隔
                if len(appear_indices) >= 2:
                    intervals = [appear_indices[i] - appear_indices[i-1] 
                               for i in range(1, len(appear_indices))]
                    interval_mean = np.mean(intervals[-5:])  # 最近5次
                    interval_std = np.std(intervals[-5:]) if len(intervals) >= 5 else 0
                else:
                    interval_mean = 0
                    interval_std = 0
                
                features.extend([interval_mean, interval_std])
                
                # 热度变化（排名变化）
                if len(history) >= 20:
                    recent_20_prev = history.iloc[-21:-1]
                    counts_20_prev = recent_20_prev['zodiac'].value_counts().to_dict()
                    rank_prev = 1
                    count_prev = counts_20_prev.get(z, 0)
                    for other_z in range(1, self.n_zodiacs + 1):
                        if counts_20_prev.get(other_z, 0) > count_prev:
                            rank_prev += 1
                    rank_change = rank_prev - ranks[z]
                else:
                    rank_change = 0
                
                features.append(rank_change)
            
            features_list.append(features)
            labels.append(current_zodiac - 1)  # 转换为0-11的标签
        
        X = np.array(features_list)
        y = np.array(labels)
        
        return X, y, feature_names


# 全局模型服务实例
model_service = ModelService()
