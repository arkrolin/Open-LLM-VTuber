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


def get_recent_memories(conf_uid: str, days: int = 7) -> str:
    """Get the memory contents from the last `days` days"""
    if not conf_uid or days <= 0:
        return ""

    try:
        conf_dir = _ensure_memory_dir(conf_uid)

        if not os.path.exists(conf_dir):
            return ""

        memory_contents = []
        today = datetime.now().date()

        for i in range(days - 1, -1, -1):
            target_date = today - timedelta(days=i)
            target_file = f"{target_date.strftime('%Y-%m-%d')}.md"
            filepath = os.path.join(conf_dir, target_file)

            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            memory_contents.append(
                                f"# {target_date.strftime('%Y-%m-%d')} Memory:\n{content}"
                            )
                except Exception as e:
                    logger.error(f"Error reading memory file {filepath}: {e}")

        return "\n\n".join(memory_contents)
    except Exception as e:
        logger.error(f"Failed to get recent memories: {e}")
        return ""
