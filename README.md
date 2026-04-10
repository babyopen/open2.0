# 生肖预测2.0

基于机器学习的生肖预测系统，使用RandomForest算法构建多分类模型，预测下一期生肖。

## 项目结构

```
新版2.0/
├── src/                # 源代码目录
│   ├── config/         # 配置文件
│   │   ├── __init__.py
│   │   └── zodiac_config.py  # 生肖配置
│   ├── utils/          # 工具函数
│   │   ├── __init__.py
│   │   ├── data_utils.py     # 数据处理工具
│   │   └── cache_utils.py    # 缓存工具
│   ├── services/       # 核心服务
│   │   ├── __init__.py
│   │   ├── model_service.py  # 模型服务
│   │   ├── data_service.py   # 数据服务
│   │   └── train_service.py  # 训练服务
│   ├── api/            # API服务
│   │   ├── __init__.py
│   │   └── app.py      # API主文件
│   └── tests/          # 测试文件
│       ├── __init__.py
│       ├── test_data_utils.py
│       ├── test_cache_utils.py
│       └── test_model_service.py
├── frontend/           # 前端文件
│   ├── index.html
│   └── style.css
├── python/             # 原有Python脚本
│   ├── fetch_real_history.py
│   ├── ml_api_server.py
│   ├── train_api_data.py
│   ├── train_systematic.py
│   └── zodiac_ml_predictor.py
├── data/               # 数据文件
│   ├── lottery_history.csv
│   └── real_lottery_history.csv
├── models/             # 模型文件
│   ├── zodiac_model.pkl
│   └── best_zodiac_model.pkl
├── train.py            # 主训练脚本
├── requirements.txt    # 依赖文件
└── README.md           # 项目说明
```

## 功能特性

- **机器学习预测**：使用RandomForest算法构建多分类模型
- **实时数据处理**：支持前端传递历史数据进行预测
- **缓存机制**：数据和文件缓存，提高响应速度
- **模块化设计**：清晰的职责划分，易于维护和扩展
- **完整的API**：提供预测、健康检查等接口
- **详细的测试**：确保功能正确性

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

### 训练模型

```bash
python train.py
```

### 启动API服务

```bash
python src/api/app.py
```

API服务默认运行在 `http://0.0.0.0:8000`

## API接口

### 健康检查

```
GET /api/health
```

### 生肖映射表

```
GET /api/zodiac-mapping
```

### 预测下一期生肖

```
POST /api/predict

请求体：
{
  "history": [
    {"period": 1, "zodiac": "马"},
    {"period": 2, "zodiac": "蛇"},
    ...
  ]
}
```

响应：
```json
{
  "status": "success",
  "predictions": [
    {"name": "马", "number": 1, "probability": 0.2, "element": "火", "color": "红"},
    ...
  ],
  "top3": [...],
  "recommendation": {...}
}
```

## 技术栈

- **后端**：Python 3.9+, Flask, scikit-learn, pandas, numpy
- **前端**：HTML, CSS, JavaScript
- **模型**：RandomForestClassifier
- **缓存**：内存缓存

## 项目优化

1. **模块化设计**：清晰的职责划分，易于维护和扩展
2. **缓存机制**：提高数据和文件访问速度
3. **性能优化**：向量化操作，减少计算时间
4. **代码规范**：遵循Python最佳实践
5. **测试覆盖**：确保功能正确性

## 注意事项

- 本项目仅供娱乐，非投注建议
- 模型预测结果仅供参考，不保证准确性
- 定期更新历史数据，提高模型预测能力
