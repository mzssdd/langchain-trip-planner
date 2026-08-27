""" LLM服务模块 """

import os
from typing import List, Optional, Iterator

from langchain.chat_models import init_chat_model,BaseChatModel
from ..config import get_settings

# 默认 LLM 和 Planner 专用 LLM 都做单例缓存，避免每次请求重复初始化客户端
_llm_instance = None
#已经把use_personalized_planner设置成False，所以这个没啥用
_planner_llm_instance = None

def get_llm() -> BaseChatModel:
    """
    获取LLM实例(单例模式)

    Returns:
        HelloAgentsLLM实例
    """
    global _llm_instance


    if _llm_instance is None:
      settings = get_settings()

      _llm_instance = init_chat_model(
          model= settings.openai_model,
          api_key = settings.openai_api_key,
          base_url = settings.openai_base_url
      )

      print(f"✅ LLM服务初始化成功")
      print(f"   提供商: {_llm_instance.provider}")
      print(f"   模型: {_llm_instance.model}")

    return _llm_instance


def get_planner_llm() -> BaseChatModel:
    """
    获取最终行程规划 LLM。

    默认返回通用 LLM；当 USE_PERSONALIZED_PLANNER=true 且配置完整时，
    仅 planner agent 使用个性化微调模型。
    """
    global _planner_llm_instance

    settings = get_settings()
    if not settings.use_personalized_planner:
        # 未开启个性化模式时，Planner 直接复用默认模型
        return get_llm()
    #下面没有起过作用
    if _planner_llm_instance is None:
        # 个性化 Planner 只替换最终生成模型，不影响工具查询和其他服务
        model = os.getenv("PERSONALIZED_LLM_MODEL_ID") or settings.personalized_llm_model
        base_url = settings.personalized_llm_base_url
        api_key = settings.personalized_llm_api_key or "EMPTY"
        provider = settings.personalized_llm_provider or "openai"

        if not model or not base_url:
            # 配置不完整时自动回退，保证服务可用性优先
            print("⚠️  个性化 Planner 配置不完整，将使用默认 LLM")
            return get_llm()

        # 通过临时环境变量构造第二套 LLM 配置，避免污染全局默认实例
        overrides = {
            "LLM_API_KEY": api_key,
            "OPENAI_API_KEY": api_key,
            "LLM_BASE_URL": base_url,
            "OPENAI_BASE_URL": base_url,
            "LLM_MODEL_ID": model,
            "OPENAI_MODEL": model,
            "LLM_PROVIDER": provider,
        }
        with _temporary_env(overrides):
            _planner_llm_instance = BaseChatModel()

        print("✅ 个性化 Planner LLM 初始化成功")
        print(f"   提供商: {_planner_llm_instance.provider}")
        print(f"   模型: {_planner_llm_instance.model}")
        print(f"   Base URL: {base_url}")

    return _planner_llm_instance

def reset_llm():
    """重置 LLM 单例缓存，常用于测试或热重载后的重新初始化。"""
    global _llm_instance, _planner_llm_instance
    _llm_instance = None
    _planner_llm_instance = None