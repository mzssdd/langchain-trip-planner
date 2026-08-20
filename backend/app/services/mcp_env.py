""" MCP服务器子进程环境的辅助工具。 """

import os
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parents[3]

#print(PROJECT_ROOT)

def build_amap_mcp_env(amap_api_key:str) -> Dict[str, str]:
  """构建传递给 amap MCP stdio 服务器的显式环境。"""
  env = {
    "AMAP_MAPS_API_KEY": amap_api_key,
    "UV_CACHE_DIR":os.getenv("UV_CACHE_DIR",str(PROJECT_ROOT / ".uv-cache"))
  }
  for key in ("http_proxy", "https_proxy", "all_proxy", "NO_PROXY", "no_proxy"):
    value = os.getenv(key)
    if value:
      env[key] = value
  return env