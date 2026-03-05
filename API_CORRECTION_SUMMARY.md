# IndexTTS API 参数修正总结

## 问题描述
初期实现使用了不正确的 API 参数名称。现在根据提供的 `apitest.py` 进行了完整的修正。

## 修改的文件

### 1. [src/open_llm_vtuber/tts/index_tts.py](src/open_llm_vtuber/tts/index_tts.py)
**修改内容:**
- 更新 `__init__` 方法的所有参数，改为与 Gradio API 完全匹配的参数名称

**旧参数 → 新参数:**
```
emotion → emo_control_method
prompt_path → prompt
reference_audio_path → emo_ref_path
speed → emo_weight
pitch, energy → vec1-vec8（新增）
```

**新增参数:**
- `vec1` 到 `vec8`: 8个情感向量参数（整数）
- `emo_text`: 情感文本描述（字符串）
- `emo_random`: 随机情感变化（布尔值）
- `max_text_tokens_per_segment`: 最大文本令牌数（整数）
- `param_16` 到 `param_23`: 其他微调参数（浮点/整数混合）

**更新 `generate_audio()` 方法:**
- 现在调用 `client.predict()` 时传递所有26个参数
- 完全对应 Gradio API 的实际签名

### 2. [src/open_llm_vtuber/config_manager/tts.py](src/open_llm_vtuber/config_manager/tts.py)
**修改内容:**
- 重构 `IndexTTSConfig` 类，包含所有新参数字段
- 添加每个参数的中英文描述

**字段定义:**
```python
# 核心参数
api_url: str
emo_control_method: str = "Same as the voice reference"
prompt: str | None = None
emo_ref_path: str | None = None

# 情感相关
emo_weight: float = 0.65
vec1-vec8: int = 0
emo_text: str = ""
emo_random: bool = False

# 分段和优化参数
max_text_tokens_per_segment: int = 120
param_16: bool = True
param_17: float = 0.8
param_18: int = 30
param_19: float = 0.8
param_20: int = 0
param_21: int = 3
param_22: int = 10
param_23: int = 1500

# API 端点
api_name: str = "/gen_single"
```

### 3. [src/open_llm_vtuber/tts/tts_factory.py](src/open_llm_vtuber/tts/tts_factory.py)
**修改内容:**
- 更新 `get_tts_engine()` 方法中的 `index_tts` 分支
- 现在正确传递所有26个参数给 IndexTTS 构造函数

### 4. [config_templates/conf.default.yaml](config_templates/conf.default.yaml)
**修改内容:**
- 更新 index_tts 配置块，包含所有新参数
- 添加英文注释说明

### 5. [config_templates/conf.ZH.default.yaml](config_templates/conf.ZH.default.yaml)
**修改内容:**
- 更新 index_tts 配置块，包含所有新参数
- 添加中文注释说明

### 6. [conf.yaml](conf.yaml)
**修改内容:**
- 同步用户配置文件中的 index_tts 参数

## API 参数详解

根据 `apitest.py` 的实际调用：

```python
client.predict(
    emo_control_method="Same as the voice reference",  # 情感控制模式
    prompt=None,                                        # 提示音频
    text="Hello!!",                                     # 输入文本（由 generate_audio 提供）
    emo_ref_path=None,                                  # 情感参考音频
    emo_weight=0.65,                                    # 情感权重
    vec1=0, vec2=0, vec3=0, vec4=0,                    # 情感向量1-4
    vec5=0, vec6=0, vec7=0, vec8=0,                    # 情感向量5-8
    emo_text="",                                        # 情感文本描述
    emo_random=False,                                   # 随机情感变化
    max_text_tokens_per_segment=120,                    # 最大文本令牌数
    param_16=True,                                      # 参数16
    param_17=0.8,                                       # 参数17
    param_18=30,                                        # 参数18
    param_19=0.8,                                       # 参数19
    param_20=0,                                         # 参数20
    param_21=3,                                         # 参数21
    param_22=10,                                        # 参数22
    param_23=1500,                                      # 参数23
    api_name="/gen_single",                             # API 端点
)
```

## 使用示例

### 配置文件方式
```yaml
tts_config:
  tts_model: 'index_tts'
  index_tts:
    api_url: "http://10.80.8.154:30413/"
    emo_control_method: "Same as the voice reference"
    emo_weight: 0.65
    # ... 其他参数保持默认值
```

### 代码方式
```python
from src.open_llm_vtuber.tts.tts_factory import TTSFactory

tts_engine = TTSFactory.get_tts_engine(
    "index_tts",
    api_url="http://10.80.8.154:30413/",
    emo_control_method="Same as the voice reference",
    emo_weight=0.65,
)

audio_file = tts_engine.generate_audio("Hello, this is IndexTTS!")
```

## 代码质量验证

✅ **Ruff 检查**: 所有文件通过

```
src/open_llm_vtuber/tts/index_tts.py     All checks passed!
src/open_llm_vtuber/config_manager/tts.py All checks passed!
src/open_llm_vtuber/tts/tts_factory.py     All checks passed!
```

✅ **代码规范**:
- 现代 Python 3.10+ 类型提示
- Google 风格文档字符串
- 完整的中英文配置描述
- 正确的参数验证

## 关键改进

| 方面     | 之前           | 之后                 |
| -------- | -------------- | -------------------- |
| 参数对应 | ❌ 不匹配 API   | ✅ 完全匹配           |
| 参数数量 | 7 个           | 26 个                |
| 情感控制 | 简化的三个参数 | 完整的8维向量 + 权重 |
| 微调能力 | 有限           | 丰富（param_16-23）  |
| 配置覆盖 | 基础           | 完整                 |

## 现在 IndexTTS 已准备就绪！🎉

所有参数现在完全对应真实的 Gradio API，可以进行完整的音色和情感控制。
