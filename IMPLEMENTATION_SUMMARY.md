# IndexTTS 集成实现总结

## 项目目标
为 Open-LLM-VTuber 添加对 IndexTTS（部署在 http://10.80.8.154:30413/）的完整支持。

## 实现完成清单

### 1. ✅ 核心引擎实现
**文件:** `src/open_llm_vtuber/tts/index_tts.py`

创建了 `IndexTTS` 类，继承自 `TTSInterface`，包含：
- 初始化方法，接受 API URL 和各种合成参数
- `generate_audio()` 方法用于同步音频生成
- `async_generate_audio()` 方法用于异步调用（继承自接口）
- 完整的 Google 风格文档字符串
- 使用 `gradio_client` 库与 Gradio API 通信
- 错误处理和日志记录（使用 loguru）

### 2. ✅ 工厂模式支持
**文件:** `src/open_llm_vtuber/tts/tts_factory.py`

在 `TTSFactory.get_tts_engine()` 方法中添加了 `index_tts` 分支：
```python
elif engine_type == "index_tts":
    from .index_tts import IndexTTS
    return IndexTTS(
        api_url=kwargs.get("api_url"),
        emotion=kwargs.get("emotion", "Same as the voice reference"),
        prompt_path=kwargs.get("prompt_path"),
        reference_audio_path=kwargs.get("reference_audio_path"),
        speed=kwargs.get("speed", 0.65),
        pitch=kwargs.get("pitch", 0.0),
        energy=kwargs.get("energy", 0.0),
        api_name=kwargs.get("api_name", "/gen_single"),
    )
```

### 3. ✅ 配置模型定义
**文件:** `src/open_llm_vtuber/config_manager/tts.py`

添加了 `IndexTTSConfig` 类：
- 8 个配置字段，均带有类型提示和别名
- 完整的中英文描述（通过 `DESCRIPTIONS` 类变量）
- 集成到 `TTSConfig` 主类中
- 在 `check_tts_config()` 验证方法中添加验证逻辑

参数包括：
- `api_url`: API 服务器地址
- `emotion`: 情感/风格模式
- `prompt_path`: 提示音频路径
- `reference_audio_path`: 参考音频路径
- `speed`: 语速倍数
- `pitch`: 音高调整
- `energy`: 能量/音量调整
- `api_name`: Gradio API 端点

### 4. ✅ 配置模板更新
**文件:** `config_templates/conf.default.yaml` 和 `config_templates/conf.ZH.default.yaml`

两个配置模板都已更新：
- 在 TTS 模型选项注释中添加了 `'index_tts'`
- 添加了完整的 IndexTTS 配置块
- 包含所有参数的默认值
- 英文和中文注释说明

示例配置：
```yaml
index_tts:
  api_url: "http://10.80.8.154:30413/"
  emotion: "Same as the voice reference"
  prompt_path: null
  reference_audio_path: null
  speed: 0.65
  pitch: 0.0
  energy: 0.0
  api_name: "/gen_single"
```

## 代码质量

### Ruff 检查结果
- ✅ `index_tts.py` - 所有检查通过
- ✅ `tts_factory.py` - 所有检查通过
- ✅ `config_manager/tts.py` - 所有检查通过

### 代码规范遵循
- ✅ 现代 Python 3.10+ 类型提示（使用 `|` 代替 `Optional`）
- ✅ Google 风格文档字符串（所有公共模块、类、函数）
- ✅ PEP 8 命名规范（`snake_case` 函数，`PascalCase` 类）
- ✅ 导入分组和排序
- ✅ 使用 loguru 进行日志记录
- ✅ 合理的错误处理

## 使用示例

### 配置文件方式
```yaml
tts_config:
  tts_model: 'index_tts'
  index_tts:
    api_url: "http://10.80.8.154:30413/"
    speed: 0.65
```

### 代码方式
```python
from src.open_llm_vtuber.tts.tts_factory import TTSFactory

tts_engine = TTSFactory.get_tts_engine(
    "index_tts",
    api_url="http://10.80.8.154:30413/",
    emotion="Same as the voice reference",
    speed=0.65,
)

audio_file = tts_engine.generate_audio("你好，我是兵智。")
```

## API 调用流程

1. **初始化**: IndexTTS 创建 gradio_client.Client 实例
2. **生成音频**: 调用 `client.predict()` 传入所有参数
3. **缓存**: 将生成的音频复制到本地缓存目录
4. **返回**: 返回本地缓存文件路径

## 依赖关系

项目原有依赖已包含 `gradio-client`（用于 Gradio API 通信）。

## 文档

新增：
- `INDEX_TTS_GUIDE.md` - 详细的集成和使用指南
- `test_index_tts.py` - 测试脚本示例

## 与 Gradio API 的兼容性

IndexTTS 实现基于提供的 `apitest.py` 示例，完全兼容其 API 签名：
- 支持情感/模式参数
- 支持提示和参考音频
- 支持速度、音高、能量调整
- 使用 `/gen_single` 端点

## 注意事项

1. **网络连接**: IndexTTS 需要网络连接到 Gradio 服务器
2. **异步支持**: 提供异步方法 `async_generate_audio()` 用于非阻塞调用
3. **错误处理**: 所有错误通过日志记录，失败时返回空字符串
4. **缓存管理**: 生成的文件保存到 `cache/` 目录

## 测试建议

```bash
# 运行测试脚本
python test_index_tts.py

# 运行代码检查
uv run ruff check src/open_llm_vtuber/tts/index_tts.py
uv run ruff format src/open_llm_vtuber/tts/index_tts.py
```

## 下一步（可选）

1. 添加单元测试
2. 添加与其他 TTS 引擎的性能对比
3. 添加更多预设的情感/风格选项
4. 实现流式音频生成支持

## 总结

IndexTTS 已完全集成到 Open-LLM-VTuber 中，可以通过配置文件或代码直接使用。实现遵循项目的所有代码规范和架构最佳实践。
