"""配置管理模块"""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


# 然后尝试加载HelloAgents的.env(如果存在)
agents_env = Path(__file__).parent.parent / ".env"
if agents_env.exists():
    load_dotenv(agents_env, override=False)  # 不覆盖已有的环境变量