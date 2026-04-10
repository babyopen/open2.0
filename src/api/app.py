#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API服务 - 处理HTTP请求和响应
"""

from flask import Flask, request, jsonify
import os
from src.services.model_service import model_service
from src.services.data_service import data_service
from src.config.zodiac_config import ZODIAC_MAP, ZODIAC_ELEMENT_MAP, ZODIAC_COLOR_MAP, API_CONFIG
from src.utils.cache_utils import file_cache

app = Flask(__name__)

# 模型加载标志
model_loaded = False


def load_model_once():
    """
    只加载模型一次
    """
    global model_loaded
    if not model_loaded:
        try:
            # 模型文件路径
            model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'zodiac_model.pkl')
            model = model_service.load_model(model_path)
            if model:
                model_loaded = True
                print("模型加载成功")
            else:
                print("模型加载失败")
        except Exception as e:
            print(f"模型加载失败: {str(e)}")


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({'status': 'ok', 'message': 'API is running'})


@app.route('/api/predict', methods=['POST'])
def predict():
    """预测下一期生肖"""
    try:
        # 加载模型
        load_model_once()
        if not model_loaded:
            return jsonify({'error': '模型加载失败'}), 500
        
        # 获取请求数据
        data = request.get_json()
        
        # 优先使用前端传递的历史数据
        if data and 'history' in data and data['history']:
            # 处理前端传递的历史数据
            df = data_service.process_frontend_data(data['history'])
            if df is None:
                # 前端数据无效，使用本地数据
                df = data_service.get_history_data()
                if df is None:
                    return jsonify({'error': '无法读取历史数据'}), 500
        else:
            # 没有前端数据，使用本地数据
            df = data_service.get_history_data()
            if df is None:
                return jsonify({'error': '无法读取历史数据'}), 500
        
        # 预测下一期
        if len(df) == 0:
            return jsonify({'error': '历史数据为空'}), 400
        
        # 检查数据量是否足够
        df = data_service.ensure_min_history_length(df)
        if df is None:
            return jsonify({'error': '历史数据不足'}), 400
        
        last_row = data_service.get_latest_period_data(df)
        if last_row is None:
            return jsonify({'error': '无法获取最新数据'}), 500
        
        predictions = model_service.predict_next(last_row, df)
        if predictions is None:
            return jsonify({'error': '预测失败'}), 500
        
        # 格式化结果
        results = []
        for i, prob in enumerate(predictions):
            zodiac_num = i + 1
            results.append({
                'name': ZODIAC_MAP.get(zodiac_num, f'未知{zodiac_num}'),
                'number': zodiac_num,
                'probability': float(prob),
                'element': ZODIAC_ELEMENT_MAP.get(zodiac_num, ''),
                'color': ZODIAC_COLOR_MAP.get(zodiac_num, '')
            })
        
        # 按概率排序
        results.sort(key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'predictions': results,
            'top3': results[:3],
            'recommendation': results[0] if results else None
        })
        
    except Exception as e:
        print(f"预测失败: {str(e)}")
        return jsonify({'error': '预测过程中发生错误'}), 500


@app.route('/api/zodiac-mapping', methods=['GET'])
def zodiac_mapping():
    """生肖映射表"""
    return jsonify({'zodiacs': ZODIAC_MAP})


@app.route('/', methods=['GET'])
def index():
    """根路径，返回前端页面"""
    try:
        # 检查缓存
        cache_key = 'index.html'
        cached_content = file_cache.get(cache_key)
        if cached_content is not None:
            return cached_content
        
        # 读取前端index.html文件
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 缓存文件内容
        file_cache.set(cache_key, html_content)
        return html_content
    except Exception as e:
        print(f"读取前端文件失败: {str(e)}")
        return jsonify({'error': '无法加载前端页面'}), 500


@app.route('/style.css', methods=['GET'])
def style_css():
    """返回前端样式文件"""
    try:
        # 检查缓存
        cache_key = 'style.css'
        cached_content = file_cache.get(cache_key)
        if cached_content is not None:
            return cached_content, 200, {'Content-Type': 'text/css'}
        
        # 读取前端style.css文件
        css_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'style.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # 缓存文件内容
        file_cache.set(cache_key, css_content)
        return css_content, 200, {'Content-Type': 'text/css'}
    except Exception as e:
        print(f"读取样式文件失败: {str(e)}")
        return jsonify({'error': '无法加载样式文件'}), 500


# 应用入口点
if __name__ == '__main__':
    app.run(
        debug=API_CONFIG['DEBUG'],
        host=API_CONFIG['HOST'],
        port=API_CONFIG['PORT']
    )
