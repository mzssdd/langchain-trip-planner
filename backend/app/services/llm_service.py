"""LLM服务模块"""

import os
from typing import Optional

from langchain.chat_models import BaseChatModel, init_chat_model

from ..config import get_settings

# 默认 LLM 和 Planner 专用 LLM 都做单例缓存，避免每次请求重复初始化客户端
_llm_instance: Optional[BaseChatModel] = None
# 已经把 use_personalized_planner 设置成 False，所以这个默认不会启用
_planner_llm_instance: Optional[BaseChatModel] = None


def _create_chat_model(
    model: str,
    api_key: str,
    base_url: str,
    provider: str,
) -> BaseChatModel:
    """统一创建聊天模型实例。"""
    return init_chat_model(
        model=model,
        api_key=api_key,
        base_url=base_url,
        model_provider=provider,
    )


def _get_model_provider(llm: BaseChatModel, fallback_provider: str) -> str:
    """兼容不同 LangChain provider 实现的模型提供商字段。"""
    provider = getattr(llm, 'provider', None)
    if provider:
        return str(provider)

    profile = getattr(llm, 'profile', None)
    if profile:
        profile_name = getattr(profile, 'name', None)
        if profile_name:
            return str(profile_name)

    return fallback_provider


def _get_model_name(llm: BaseChatModel, fallback_model: str) -> str:
    """兼容不同 LangChain provider 实现的模型名称字段。"""
    for attr_name in ('model', 'model_name'):
        model_name = getattr(llm, attr_name, None)
        if model_name:
            return str(model_name)

    return fallback_model


def _print_llm_info(title: str, llm: BaseChatModel, provider: str, model: str) -> None:
    """输出兼容不同模型实现的调试信息。"""
    print(title)
    print(f"   提供商: {_get_model_provider(llm, provider)}")
    print(f"   模型: {_get_model_name(llm, model)}")


def get_llm() -> BaseChatModel:
    """
    获取LLM实例(单例模式)

    Returns:
        HelloAgentsLLM实例
    """
    global _llm_instance

    if _llm_instance is None:
        settings = get_settings()
        _llm_instance = _create_chat_model(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            provider=settings.openai_provider,
        )
        _print_llm_info(
            "✅ LLM服务初始化成功",
            _llm_instance,
            settings.openai_provider,
            settings.openai_model,
        )

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

    if _planner_llm_instance is None:
        # 个性化 Planner 只替换最终生成模型，不影响工具查询和其他服务
        model = os.getenv('PERSONALIZED_LLM_MODEL_ID') or settings.personalized_llm_model
        base_url = settings.personalized_llm_base_url
        api_key = settings.personalized_llm_api_key or 'EMPTY'
        provider = settings.personalized_llm_provider or 'openai'

        if not model or not base_url:
            # 配置不完整时自动回退，保证服务可用性优先
            print('⚠️  个性化 Planner 配置不完整，将使用默认 LLM')
            return get_llm()

        _planner_llm_instance = _create_chat_model(
            model=model,
            api_key=api_key,
            base_url=base_url,
            provider=provider,
        )

        _print_llm_info(
            '✅ 个性化 Planner LLM 初始化成功',
            _planner_llm_instance,
            provider,
            model,
        )
        print(f'   Base URL: {base_url}')

    return _planner_llm_instance


def reset_llm() -> None:
    """重置 LLM 单例缓存，常用于测试或热重载后的重新初始化。"""
    global _llm_instance, _planner_llm_instance
    _llm_instance = None
    _planner_llm_instance = None
