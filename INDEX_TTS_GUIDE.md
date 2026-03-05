# IndexTTS 集成指南

## 概述

IndexTTS 是一个支持低延迟语音合成的 TTS 引擎，现已集成到 Open-LLM-VTuber 项目中。它通过 Gradio 客户端与服务器通信，支持灵活的情感和音色控制。

## 文件结构

新增文件：
- `src/open_llm_vtuber/tts/index_tts.py` - IndexTTS 引擎实现
- `test_index_tts.py` - 测试脚本

修改文件：
- `src/open_llm_vtuber/tts/tts_factory.py` - 添加 IndexTTS 工厂方法
- `src/open_llm_vtuber/config_manager/tts.py` - 添加 IndexTTSConfig 配置类
- `config_templates/conf.default.yaml` - 英文配置模板
- `config_templates/conf.ZH.default.yaml` - 中文配置模板

## 配置说明

### 配置文件示例

在 `conf.yaml` 中配置 IndexTTS：

```yaml
tts_config:
  tts_model: 'index_tts'
  
  index_tts:
    api_url: "http://10.80.8.154:30413/"  # IndexTTS 服务器 URL
    emotion: "Same as the voice reference"  # 情感模式
    prompt_path: null                        # 提示音频路径（null 为默认）
    reference_audio_path: null               # 参考音频路径（null 为默认）
    speed: 0.65                              # 语速倍数（0.5-2.0）
    pitch: 0.0                               # 音高调整（-12 到 12 半音）
    energy: 0.0                              # 能量/音量调整
    api_name: "/gen_single"                  # API 端点名称
```

### 参数说明

| 参数                   | 类型        | 默认值                        | 说明                                         |
| ---------------------- | ----------- | ----------------------------- | -------------------------------------------- |
| `api_url`              | str         | 必填                          | IndexTTS Gradio API 服务器地址               |
| `emotion`              | str         | "Same as the voice reference" | 情感/风格模式                                |
| `prompt_path`          | str \| None | None                          | 提示音频文件路径（为 None 时使用服务器默认） |
| `reference_audio_path` | str \| None | None                          | 参考音频文件路径用于风格转移                 |
| `speed`                | float       | 0.65                          | 语速倍数，范围 0.5-2.0                       |
| `pitch`                | float       | 0.0                           | 音高调整，范围 -12 到 12 半音                |
| `energy`               | float       | 0.0                           | 能量/音量调整                                |
| `api_name`             | str         | "/gen_single"                 | Gradio API 端点名称                          |

## 使用示例

### 基础使用

```python
from src.open_llm_vtuber.tts.tts_factory import TTSFactory

# 创建 IndexTTS 引擎
tts_engine = TTSFactory.get_tts_engine(
    "index_tts",
    api_url="http://10.80.8.154:30413/",
    emotion="Same as the voice reference",
    speed=0.65,
)

# 生成语音
audio_file = tts_engine.generate_audio("你好，我是 IndexTTS")
print(f"音频文件保存到: {audio_file}")
```

### 高级使用

```python
# 使用自定义提示音频和参考音频
tts_engine = TTSFactory.get_tts_engine(
    "index_tts",
    api_url="http://10.80.8.154:30413/",
    emotion="happy",
    prompt_path="/path/to/prompt.wav",
    reference_audio_path="/path/to/reference.wav",
    speed=0.8,
    pitch=2.0,
    energy=1.0,
)

audio_file = tts_engine.generate_audio("这是一个高度定制的语音合成示例")
```

### 异步使用

```python
import asyncio

async def generate_audio_async():
    tts_engine = TTSFactory.get_tts_engine(
        "index_tts",
        api_url="http://10.80.8.154:30413/",
    )
    
    # 使用异步方法（在后台线程中运行）
    audio_file = await tts_engine.async_generate_audio("你好")
    return audio_file

# 运行异步函数
result = asyncio.run(generate_audio_async())
```

## 集成检查清单

✅ IndexTTS 类实现  
✅ TTSFactory 工厂方法添加  
✅ 配置模型定义  
✅ 英文和中文配置模板更新  
✅ 代码符合项目规范（ruff 检查通过）  
✅ 完整的 Google 风格文档字符串  

## 错误处理

IndexTTS 会在以下情况下返回空字符串 (`""`):

1. API URL 未配置
2. 无法连接到 Gradio 服务器
3. API 调用失败
4. 返回响应格式不正确

所有错误都会通过 `loguru` 记录，包含详细的错误信息。

## 缓存管理

生成的音频文件默认保存到 `cache/` 目录。可以使用 `remove_file()` 方法清理缓存：

```python
tts_engine.remove_file("cache/your_audio.wav")
```

## 性能考虑

- IndexTTS 通过网络与 Gradio 服务器通信，确保服务器在线
- 异步调用 `async_generate_audio()` 不会阻塞主线程
- 生成的音频缓存在本地，可重复使用

## 与 SiliconFlow TTS 的对比

| 特性     | IndexTTS           | SiliconFlow TTS  |
| -------- | ------------------ | ---------------- |
| 部署方式 | 本地 Gradio 服务器 | 云 API（需网络） |
| 离线支持 | ✅ 支持             | ❌ 不支持         |
| 情感控制 | ✅ 灵活             | ✅ 有             |
| 风格转移 | ✅ 支持参考音频     | ✅ 支持           |
| 延迟     | ⚡ 低（局域网）     | 📡 取决于网络     |

## 故障排查

### 问题：无法连接到 API

**解决方案：**
- 检查 `api_url` 是否正确
- 确保 IndexTTS Gradio 服务器正在运行
- 检查网络连接和防火墙设置

### 问题：音频生成失败

**解决方案：**
- 查看日志中的详细错误信息
- 验证 `text` 参数是否为空
- 检查 `prompt_path` 和 `reference_audio_path` 是否存在

### 问题：音频质量差

**调整以下参数：**
- `speed`: 降低速度可能会改善清晰度
- `pitch`: 调整音高以匹配参考音频
- `energy`: 增加能量以提高音量

## 相关文档

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Pydantic v2 文档](https://docs.pydantic.dev/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [loguru 文档](https://loguru.readthedocs.io/)
