""" 高德地图MCP服务封装 """

from typing import List, Dict, Any, Optional
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import MCPTool
from .mcp_env import build_amap_mcp_env
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo

#全局mcp工具实例
_amap_mcp_tool = None

def get_amap_map_tool() -> MultiServerMCPClient:
    """
    获取高德地图MCP工具实例(单例模式)

    Returns:
        MCPTool实例
    """

    global _amap_mcp_tool

    if _amap_mcp_tool is None:
        settings = get_settings()

        if not settings.amap_api_key:
            raise ValueError("高德地图API Key未配置,请在.env文件中设置AMAP_API_KEY")

        #创建MCP工具
        _amap_mcp_tool = MultiServerMCPClient(
            {
              "amap-maps": {
                "transport":"stdio",
                "args": [
                  "-y",
                  "@amap/amap-maps-mcp-server"
                ],
                "command": "npx",
                "env": {
                  "AMAP_MAPS_API_KEY": settings.amap_api_key
                }
              }
            }
        )

    return _amap_mcp_tool

class AmapService:
    """高德地图服务封装类"""
    def __init__(self):
        """初始化服务"""
        self.mcp_tool = get_amap_map_tool()

    def search_poi(self, keywords:str, city:str, citylimit:bool = True) -> List[POIInfo]:
        """
        搜索POI

        Args:
            keywords: 搜索关键词
            city: 城市
            citylimit: 是否限制在城市范围内

        Returns:
            POI信息列表
        """
        try:
            #调用mcp
            result = self.mcp_tool.run(
                {
                  "action": "call_tool",
                  "tool_name": "maps_text_search",
                  "arguments": {
                      "keywords": keywords,
                      "city": city,
                      "citylimit": str(citylimit).lower()
                }
                }
            )

            # 解析结果
            # 注意: MCP工具返回的是字符串,需要解析
            # 这里简化处理,实际应该解析JSON
            print(f"POI搜索结果: {result[:200]}...")  # 打印前200字符

            # TODO: 解析实际的POI数据
            return []
        
        except Exception as e:
            print(f"❌ POI搜索失败: {str(e)}")
            return []

    def get_weather(self, city: str) -> List[WeatherInfo]:
        """
        查询天气

        Args:
            city: 城市名称

        Returns:
            天气信息列表
        """
        try:
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_weather",
                "arguments": {
                    "city": city
                }
            })

            print(f"天气查询结果: {result[:200]}...")

            # TODO: 解析实际的天气数据
            return []

        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []

