# 模型使用说明

## 📁 目录结构

```
models/
├── predict_model.py          # 通用预测脚本
├── README.md                  # 本文件
│
├── main/                      # 主模型
│   ├── zodiac_model.pkl
│   └── run.py
│
├── early80/                   # 前80期数据模型
│   ├── zodiac_model_前80期数据.pkl
│   └── run.py
│
├── later80/                   # 后80期数据模型
│   ├── zodiac_model_后80期数据.pkl
│   └── run.py
│
├── full/                      # 完整数据集模型
│   ├── zodiac_model_完整数据集.pkl
│   └── run.py
│
├── optimized/                 # 优化参数模型
│   ├── zodiac_model_完整数据-调整参数.pkl
│   └── run.py
│
└── legacy/                    # 遗留模型
    ├── best_zodiac_model.pkl
    └── run.py
```

## 🚀 使用方法

### 方式一：进入文件夹运行

```bash
# 运行主模型
cd main
python3 run.py

# 运行前80期数据模型
cd ../early80
python3 run.py

# 运行后80期数据模型
cd ../later80
python3 run.py

# 运行完整数据集模型
cd ../full
python3 run.py

# 运行优化参数模型
cd ../optimized
python3 run.py

# 运行遗留模型
cd ../legacy
python3 run.py
```

### 方式二：从根目录运行

```bash
# 在项目根目录执行
cd /path/to/project

# 运行主模型
python3 models/main/run.py

# 运行前80期数据模型
python3 models/early80/run.py

# 运行后80期数据模型
python3 models/later80/run.py

# 运行完整数据集模型
python3 models/full/run.py

# 运行优化参数模型
python3 models/optimized/run.py

# 运行遗留模型
python3 models/legacy/run.py
```

## 📊 模型说明

| 模型 | 文件 | 训练数据 | 说明 |
|------|------|----------|------|
| **主模型** | `main/zodiac_model.pkl` | 829期真实历史数据 | 当前使用的主要模型 |
| **前80期模型** | `early80/zodiac_model_前80期数据.pkl` | 前80期数据 | 历史数据前半部分训练 |
| **后80期模型** | `later80/zodiac_model_后80期数据.pkl` | 后80期数据 | 历史数据后半部分训练 |
| **完整数据集模型** | `full/zodiac_model_完整数据集.pkl` | 完整数据集 | 全部可用数据训练 |
| **优化参数模型** | `optimized/zodiac_model_完整数据-调整参数.pkl` | 完整数据+调整参数 | 优化后的参数设置 |
| **遗留最佳模型** | `legacy/best_zodiac_model.pkl` | 旧版数据 | 历史最佳模型 |

## ⚙️ 切换API服务使用的模型

如果需要在ML API服务中使用不同的模型，修改 `python/ml_api_server.py` 第73行：

```python
# 主模型
model_path = '../models/main/zodiac_model.pkl'

# 前80期模型
model_path = '../models/early80/zodiac_model_前80期数据.pkl'

# 后80期模型
model_path = '../models/later80/zodiac_model_后80期数据.pkl'

# 完整数据集模型
model_path = '../models/full/zodiac_model_完整数据集.pkl'

# 优化参数模型
model_path = '../models/optimized/zodiac_model_完整数据-调整参数.pkl'

# 遗留模型
model_path = '../models/legacy/best_zodiac_model.pkl'
```

修改后重启API服务即可生效。

## 🔧 批量运行所有模型

创建一个批量运行脚本（可选）：

```bash
#!/bin/bash
# 运行所有模型
echo "运行所有模型..."
python3 models/main/run.py
python3 models/early80/run.py
python3 models/later80/run.py
python3 models/full/run.py
python3 models/optimized/run.py
python3 models/legacy/run.py
```
