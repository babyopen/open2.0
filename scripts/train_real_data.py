#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生肖预测2.0 - 真实数据训练脚本
使用真实历史数据进行训练
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss, classification_report
import json
import pickle
import warnings
import time
import os
warnings.filterwarnings('ignore')

# 生肖映射配置
ZODIAC_CONFIG = {
    # 生肖ID到名称的映射
    'id_to_name': {
        1: '马', 2: '蛇', 3: '龙', 4: '兔', 5: '虎', 6: '牛',
        7: '鼠', 8: '猪', 9: '狗', 10: '鸡', 11: '猴', 12: '羊'
    },
    # 生肖到五行的映射
    'zodiac_to_element': {
        1: '火',   # 马
        2: '火',   # 蛇
        3: '土',   # 龙
        4: '木',   # 兔
        5: '木',   # 虎
        6: '土',   # 牛
        7: '水',   # 鼠
        8: '水',   # 猪
        9: '土',   # 狗
        10: '金',  # 鸡
        11: '金',  # 猴
        12: '土'   # 羊
    },
    # 生肖到波色的映射
    'zodiac_to_color': {
        1: '红', 2: '红', 3: '红', 4: '绿', 5: '蓝', 6: '绿',
        7: '红', 8: '蓝', 9: '绿', 10: '红', 11: '蓝', 12: '绿'
    }
}

def get_element_relation(element1, element2):
    """
    获取两个五行元素之间的关系
    返回: 0=相克, 1=相同, 2=相生
    """
    element_generate = {
        '金': '水',
        '水': '木',
        '木': '火',
        '火': '土',
        '土': '金'
    }
    if element1 == element2:
        return 1  # 相同
    elif element_generate.get(element1) == element2:
        return 2  # 相生
    else:
        return 0  # 相克

def get_zodiac_attributes(zodiac_id):
    """
    获取生肖的各种属性
    """
    # 单双
    odd_even = zodiac_id % 2  # 0=双, 1=单
    
    # 大小 (1-6小, 7-12大)
    big_small = 1 if zodiac_id >= 7 else 0  # 0=小, 1=大
    
    # 区间 (1-4, 5-8, 9-12)
    if zodiac_id <= 4:
        zone = 0
    elif zodiac_id <= 8:
        zone = 1
    else:
        zone = 2
    
    # 头数 (1-9为0, 10-12为1)
    head = 1 if zodiac_id >= 10 else 0
    
    # 尾数
    tail = zodiac_id % 10
    
    # 五行
    element = ZODIAC_CONFIG['zodiac_to_element'][zodiac_id]
    element_map = {'金': 0, '水': 1, '木': 2, '火': 3, '土': 4}
    element_code = element_map.get(element, 2)
    
    # 波色
    color = ZODIAC_CONFIG['zodiac_to_color'][zodiac_id]
    color_map = {'红': 0, '绿': 1, '蓝': 2}
    color_code = color_map.get(color, 0)
    
    return {
        'odd_even': odd_even,
        'big_small': big_small,
        'zone': zone,
        'head': head,
        'tail': tail,
        'element': element_code,
        'color': color_code
    }

def load_data(file_path):
    """
    加载历史数据
    """
    try:
        df = pd.read_csv(file_path)
        df['period'] = df['period'].astype(int)
        df['zodiac'] = df['zodiac'].astype(int)
        df = df.sort_values('period').reset_index(drop=True)
        print(f"数据加载成功: {len(df)} 条记录")
        print(f"期号范围: {df['period'].min()} - {df['period'].max()}")
        
        print("\n生肖分布:")
        print(df['zodiac'].value_counts().sort_index())
        return df
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None

def build_features(all_history, idx, n_zodiacs=12):
    """
    构建特征
    """
    features = []
    
    # 历史数据
    history = all_history.iloc[:idx]
    
    # 基础统计特征
    miss_counts = {i: 0 for i in range(1, n_zodiacs + 1)}
    max_miss = {i: 0 for i in range(1, n_zodiacs + 1)}
    
    for z in range(1, n_zodiacs + 1):
        last_appear = -1
        for i, row in history.iterrows():
            if row['zodiac'] == z:
                last_appear = i
        if last_appear == -1:
            miss_counts[z] = len(history)
        else:
            miss_counts[z] = idx - last_appear - 1
    
    for z in range(1, n_zodiacs + 1):
        current_miss = 0
        for i, row in history.iterrows():
            if row['zodiac'] == z:
                max_miss[z] = max(max_miss[z], current_miss)
                current_miss = 0
            else:
                current_miss += 1
    
    recent_10 = history.tail(10)
    recent_20 = history.tail(20)
    recent_50 = history.tail(50)
    
    counts_20 = recent_20['zodiac'].value_counts().to_dict()
    ranks = {}
    for z in range(1, n_zodiacs + 1):
        count = counts_20.get(z, 0)
        rank = 1
        for other_z in range(1, n_zodiacs + 1):
            if counts_20.get(other_z, 0) > count:
                rank += 1
        ranks[z] = rank
    
    consecutive = {i: 0 for i in range(1, n_zodiacs + 1)}
    break_state = {i: 0 for i in range(1, n_zodiacs + 1)}
    
    for z in range(1, n_zodiacs + 1):
        cons = 0
        for i in range(len(history) - 1, -1, -1):
            if history.iloc[i]['zodiac'] == z:
                cons += 1
            else:
                break
        consecutive[z] = cons
        
        if len(history) >= 2:
            last = history.iloc[-1]['zodiac']
            second_last = history.iloc[-2]['zodiac']
            break_state[z] = 1 if (last == z and second_last != z) else 0
    
    for z in range(1, n_zodiacs + 1):
        miss = miss_counts[z]
        max_m = max_miss[z] if max_miss[z] > 0 else 1
        
        features.extend([
            miss,
            miss / max_m,
            (recent_10['zodiac'] == z).sum(),
            (recent_20['zodiac'] == z).sum(),
            (recent_50['zodiac'] == z).sum(),
            (recent_10['zodiac'] == z).sum() / 10,
            (recent_20['zodiac'] == z).sum() / 20,
            ranks[z],
            consecutive[z],
            break_state[z],
        ])
    
    # 动态特征
    prev_zodiac = history.iloc[-1]['zodiac']
    features.append(prev_zodiac)
    features.append(0)  # 位置间隔（无法预知）
    features.append(1)  # 五行关系（默认相同）
    
    prev_attr = get_zodiac_attributes(prev_zodiac)
    features.extend([0, 0, 0, 0, 0, 0])  # 其他比较特征（无法预知）
    
    # 时序特征
    for z in range(1, n_zodiacs + 1):
        appear_indices = []
        for i, row in history.iterrows():
            if row['zodiac'] == z:
                appear_indices.append(i)
        
        if len(appear_indices) >= 2:
            intervals = [appear_indices[i] - appear_indices[i-1] 
                       for i in range(1, len(appear_indices))]
            interval_mean = np.mean(intervals[-5:])
            interval_std = np.std(intervals[-5:]) if len(intervals) >= 5 else 0
        else:
            interval_mean = 0
            interval_std = 0
        
        heat_change = 0
        if len(appear_indices) >= 3:
            recent_3 = appear_indices[-3:]
            if len(recent_3) >= 2:
                heat_change = (recent_3[-1] - recent_3[0]) / len(recent_3)
        
        features.extend([
            interval_mean,
            interval_std,
            heat_change,
        ])
    
    return features

def prepare_training_data(df):
    """
    准备训练数据
    """
    X = []
    y = []
    feature_names = []
    
    n_samples = len(df)
    min_samples = 50
    
    if n_samples < min_samples + 1:
        print(f"数据量不足，需要至少 {min_samples + 1} 条记录")
        return None, None, None
    
    # 生成特征名称
    for z in range(1, 13):
        feature_names.extend([
            f'zodiac_{z}_miss',
            f'zodiac_{z}_miss_ratio',
            f'zodiac_{z}_recent_10',
            f'zodiac_{z}_recent_20',
            f'zodiac_{z}_recent_50',
            f'zodiac_{z}_recent_10_ratio',
            f'zodiac_{z}_recent_20_ratio',
            f'zodiac_{z}_rank',
            f'zodiac_{z}_consecutive',
            f'zodiac_{z}_break',
        ])
    feature_names.extend([
        'prev_zodiac',
        'position_gap',
        'element_relation',
        'odd_even_same',
        'big_small_same',
        'zone_same',
        'head_same',
        'tail_same',
        'color_same',
    ])
    for z in range(1, 13):
        feature_names.extend([
            f'zodiac_{z}_interval_mean',
            f'zodiac_{z}_interval_std',
            f'zodiac_{z}_heat_change',
        ])
    
    # 构建训练数据
    for idx in range(min_samples, n_samples):
        features = build_features(df, idx)
        X.append(features)
        y.append(df.iloc[idx]['zodiac'])
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"特征维度: {X.shape[1]}")
    print(f"特征矩阵形状: {X.shape}")
    print(f"标签形状: {y.shape}")
    
    return X, y, feature_names

def train_model(X_train, y_train, params=None):
    """
    训练模型
    """
    if params is None:
        params = {
            'n_estimators': 200,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'class_weight': 'balanced',
            'n_jobs': -1
        }
    
    print(f"模型参数: {params}")
    
    # 处理类别权重
    from sklearn.utils.class_weight import compute_class_weight
    classes = np.unique(y_train)
    class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = dict(zip(classes, class_weights))
    print(f"类别权重: {class_weight_dict}")
    
    model = RandomForestClassifier(**params)
    
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    print(f"模型训练完成，耗时: {train_time:.2f}秒")
    return model

def evaluate_model(model, X_test, y_test):
    """
    评估模型
    """
    print("\n========== 模型评估 ==========")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"准确率: {accuracy:.4f}")
    
    # 计算Top-3准确率
    y_proba = model.predict_proba(X_test)
    top3_correct = 0
    for i in range(len(y_test)):
        true_label = y_test[i]
        probs = y_proba[i]
        top3_indices = np.argsort(probs)[-3:][::-1]
        top3_classes = [model.classes_[idx] for idx in top3_indices]
        if true_label in top3_classes:
            top3_correct += 1
    top3_accuracy = top3_correct / len(y_test)
    print(f"Top-3 准确率: {top3_accuracy:.4f}")
    
    # 计算对数损失
    loss = log_loss(y_test, y_proba)
    print(f"对数损失: {loss:.4f}")
    
    print("\n分类报告:")
    target_names = [ZODIAC_CONFIG['id_to_name'][c] for c in sorted(model.classes_)]
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    return {
        'accuracy': accuracy,
        'top3_accuracy': top3_accuracy,
        'log_loss': loss
    }

def predict_next(model, df):
    """
    预测下一期
    """
    print("\n========== 下一期预测 ==========")
    
    X_next = build_features(df, len(df))
    X_next = np.array(X_next).reshape(1, -1)
    
    probabilities = model.predict_proba(X_next)[0]
    
    # 构建预测结果
    pred_list = []
    for i, class_idx in enumerate(model.classes_):
        pred_list.append({
            'zodiac': class_idx,
            'name': ZODIAC_CONFIG['id_to_name'][class_idx],
            'probability': float(probabilities[i])
        })
    
    # 按概率排序
    pred_list_sorted = sorted(pred_list, key=lambda x: x['probability'], reverse=True)
    
    print("\n生肖预测概率（按概率排序）:")
    print("-" * 40)
    for item in pred_list_sorted:
        prob = item['probability']
        bar_length = int(prob * 50)
        bar = '█' * bar_length
        print(f"{item['zodiac']:2d}. {item['name']}: {prob:.4f} {bar}")
    
    # 推荐
    print(f"\n推荐生肖: {pred_list_sorted[0]['name']} (概率: {pred_list_sorted[0]['probability']:.4f})")
    print(f"次选生肖: {pred_list_sorted[1]['name']} (概率: {pred_list_sorted[1]['probability']:.4f})")
    print(f"备选生肖: {pred_list_sorted[2]['name']} (概率: {pred_list_sorted[2]['probability']:.4f})")
    
    return pred_list_sorted

def save_model(model, file_path):
    """
    保存模型
    """
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n模型已保存: {file_path}")

def main():
    """
    主程序
    """
    print("=" * 80)
    print("生肖预测2.0 - 真实数据训练")
    print("=" * 80)
    
    # 1. 加载真实数据
    df = load_data('../data/real_lottery_history.csv')
    if df is None:
        print("请确保 real_lottery_history.csv 文件存在")
        return
    
    # 2. 准备训练数据
    print("\n" + "=" * 80)
    print("准备训练数据")
    print("=" * 80)
    X, y, feature_names = prepare_training_data(df)
    if X is None:
        return
    
    # 3. 划分训练集和测试集
    print("\n" + "=" * 80)
    print("划分数据集")
    print("=" * 80)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    print(f"训练集大小: {len(X_train)}")
    print(f"测试集大小: {len(X_test)}")
    
    # 4. 训练模型
    print("\n" + "=" * 80)
    print("开始训练模型...")
    print("=" * 80)
    model = train_model(X_train, y_train)
    
    # 5. 评估模型
    metrics = evaluate_model(model, X_test, y_test)
    
    # 6. 预测下一期
    pred_list = predict_next(model, df)
    
    # 7. 保存模型
    save_model(model, '../models/zodiac_model.pkl')
    
    print("\n" + "=" * 80)
    print("训练完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()
