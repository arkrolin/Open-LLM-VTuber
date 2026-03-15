import os
import re
from datetime import datetime, timedelta
from loguru import logger


def _is_safe_filename(filename: str) -> bool:
    """Validate filename for safety and allowed characters"""
    if not filename or len(filename) > 255:
        return False
    pattern = re.compile(r"^[\w\-_\u0020-\u007E\u00A0-\uFFFF]+$")
    return bool(pattern.match(filename))


def _sanitize_path_component(component: str) -> str:
    """Sanitize and validate a path component"""
    sanitized = os.path.basename(component.strip())
    if not _is_safe_filename(sanitized):
        raise ValueError(f"Invalid characters in path component: {component}")
    return sanitized


def _ensure_memory_dir(conf_uid: str) -> str:
    """Ensure the directory for a specific conf exists and return its path"""
    if not conf_uid:
        raise ValueError("conf_uid cannot be empty")
    safe_conf_uid = _sanitize_path_component(conf_uid)
    base_dir = os.path.join("memory", safe_conf_uid)
    os.makedirs(base_dir, exist_ok=True)
    return base_dir


def append_memory(conf_uid: str, content: str) -> bool:
    """Append memory content to today's markdown file"""
    if not conf_uid or not content:
        return False

    try:
        conf_dir = _ensure_memory_dir(conf_uid)
        today_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(conf_dir, f"{today_str}.md")

        now_time = datetime.now().strftime("%H:%M:%S")
        memory_entry = f"\n## {now_time}\n\n{content.strip()}\n"

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(memory_entry)

        logger.debug(f"Successfully appended memory to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to append memory: {e}")
        return False


def clean_memory_content(raw_content: str) -> str:
    """
    清洗记忆内容：
    1. 将块状标题 ## 00:51:10 转换为行内标签 **[00:51:10]**
    2. 剔除没有任何内容的空时间戳
    3. 压缩多余换行，提升 Token 效率
    """
    if not raw_content:
        return ""

    # 1. 转换格式：## HH:MM:SS -> **[HH:MM:SS]**
    # re.MULTILINE 确保 ^ 匹配每一行的开头
    content = re.sub(
        r"^##\s+(\d{2}:\d{2}:\d{2})\s*", r"**[\1]** ", raw_content, flags=re.MULTILINE
    )

    # 2. 压缩换行：将连续的多个换行替换为单个换行
    content = re.sub(r"\n{2,}", "\n", content)

    # 3. 剔除空块：如果时间戳后面直接跟着另一个时间戳或字符串结束，说明该时间段无内容，直接删掉
    # 使用正向肯定断言 (?=...)
    content = re.sub(r"\*\*\[\d{2}:\d{2}:\d{2}\]\*\*\s*(?=\*\*\[|\Z)", "", content)

    return content.strip()


def get_recent_memories(conf_uid: str, days: int = 7) -> str:
    """
    获取最近 days 天的记忆文件，并返回格式化后的长字符串
    """
    if not conf_uid or days <= 0:
        return ""

    try:
        # 假设 _ensure_memory_dir 是你已有的工具函数，返回存储目录
        conf_dir = _ensure_memory_dir(conf_uid)
        if not os.path.exists(conf_dir):
            return ""

        memory_contents = []
        today = datetime.now().date()

        # 按日期从远到近读取
        for i in range(days - 1, -1, -1):
            target_date = today - timedelta(days=i)
            date_str = target_date.strftime("%Y-%m-%d")
            filepath = os.path.join(conf_dir, f"{date_str}.md")

            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        raw_text = f.read()
                        # 执行正则清洗
                        cleaned_text = clean_memory_content(raw_text)

                        if cleaned_text:
                            # 每一天的记忆给一个清晰的日期标题
                            memory_contents.append(
                                f"### Date: {date_str}\n{cleaned_text}"
                            )
                except Exception as e:
                    logger.error(f"Error reading memory file {filepath}: {e}")

        return "\n\n".join(memory_contents)
    except Exception as e:
        logger.error(f"Failed to get recent memories: {e}")
        return ""
