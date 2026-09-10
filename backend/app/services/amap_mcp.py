"""高德地图 MCP 客户端及同步调用适配。"""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Iterable

from langchain_mcp_adapters.client import MultiServerMCPClient

from ..config import get_settings
from .mcp_env import build_amap_mcp_env


class AmapMcpClient:
    """把高德 MCP 工具包装成现有服务可使用的同步客户端。"""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.amap_api_key:
            raise ValueError("高德地图 API Key 未配置，请在 .env 文件中设置 AMAP_API_KEY")

        self.client = MultiServerMCPClient(
            {
                "amap-maps": {
                    "transport": "stdio",
                    "command": "npx",
                    "args": ["-y", "@amap/amap-maps-mcp-server"],
                    "env": build_amap_mcp_env(settings.amap_api_key),
                }
            }
        )

    def call(self, tool_names: Iterable[str], arguments: Dict[str, Any]) -> Any:
        """查找并调用高德 MCP 工具。"""
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._call(tool_names, arguments))

        with ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(asyncio.run, self._call(tool_names, arguments)).result()

    async def get_tool_names(self) -> list[str]:
        """获取当前高德 MCP 服务暴露的工具名称。"""
        tools = await self.client.get_tools()
        return [tool.name for tool in tools]

    async def _call(self, tool_names: Iterable[str], arguments: Dict[str, Any]) -> Any:
        tools = await self.client.get_tools()
        requested_names = tuple(tool_names)
        tool = next(
            (
                item
                for item in tools
                if self._matches_tool_name(item.name, requested_names)
            ),
            None,
        )
        if tool is None:
            available_names = ", ".join(item.name for item in tools)
            raise RuntimeError(
                f"高德 MCP 工具未找到（需要: {', '.join(requested_names)}；"
                f"可用: {available_names}）"
            )

        filtered_arguments = self._filter_arguments(tool, arguments)
        result = await tool.ainvoke(filtered_arguments)
        return self._decode_result(result)

    def _matches_tool_name(self, actual_name: str, requested_names: tuple[str, ...]) -> bool:
        """兼容 MCP adapter 对服务名前缀的不同命名形式。"""
        return any(
            actual_name == name
            or actual_name.endswith(f"_{name}")
            or actual_name.endswith(f"-{name}")
            for name in requested_names
        )

    def _filter_arguments(self, tool: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """只传递工具 schema 接受的参数，避免 adapter 版本差异导致报错。"""
        args_schema = getattr(tool, "args_schema", None)
        model_fields = getattr(args_schema, "model_fields", None)
        if model_fields:
            return {key: value for key, value in arguments.items() if key in model_fields}
        if isinstance(args_schema, dict):
            properties = args_schema.get("properties", {})
            if properties:
                return {key: value for key, value in arguments.items() if key in properties}
        return arguments

    def _decode_result(self, result: Any) -> Any:
        """将 MCP ToolMessage 或文本结果还原为 Python 数据。"""
        if isinstance(result, dict):
            return result

        content = getattr(result, "content", result)
        if isinstance(content, list):
            content = "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )
        if not isinstance(content, str):
            return content

        decoded: Any = content.strip()
        for _ in range(2):
            if not isinstance(decoded, str):
                break
            try:
                decoded = json.loads(decoded)
            except json.JSONDecodeError:
                break
        return decoded


_amap_mcp_client: AmapMcpClient | None = None


def get_amap_mcp_client() -> AmapMcpClient:
    """获取进程内共享的高德 MCP 客户端。"""
    global _amap_mcp_client
    if _amap_mcp_client is None:
        _amap_mcp_client = AmapMcpClient()
    return _amap_mcp_client
