""" 高德地图MCP服务封装 """

from typing import List, Dict, Any, Optional
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
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


# async def get_amap_tools() -> list[BaseTool]:
#     client = get_amap_map_tool()
#     return await client.get_tools()

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

            tool_map = get_amap_map_tool()
            result = tool_map['maps_text_search'].invoke({
                'keywords':keywords,
                'city':city,
                'citylimit': True
            })

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
            tool_map = get_amap_map_tool()
            result = tool_map['maps_weather'].invoke({
                'city':city
            })

            print(f"天气查询结果: {result[:200]}...")

            # TODO: 解析实际的天气数据
            return []

        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []

    def plan_route(
        self,
        origin_address: str,
        destination_address: str,
        origin_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        route_type :str = 'walking'
    ) -> Dict[str, Any]:
        """
        规划路线

        Args:
            origin_address: 起点地址
            destination_address: 终点地址
            origin_city: 起点城市
            destination_city: 终点城市
            route_type: 路线类型 (walking/driving/transit)

        Returns:
            路线信息
        """
        try:
            tool_map = {
                'walking':'maps_direction_walking',
                'driving':'maps_direction_driving',
                'transit':'maps_direction_transit_integrated'
            }

            tool_name = tool_map.get(route_type, "maps_direction_walking_by_address")

            #构建参数
            arguments = {
                'origin_address': origin_address,
                'destination_address': destination_address
            }

            if route_type == 'route_type':
                if origin_city:
                    arguments['origin_city'] = origin_city

                if destination_city:
                    arguments['destination_city'] = destination_city

            #调用工具
            tool_mcp = get_amap_map_tool()
            result = tool_mcp[tool_name].incoke({
                arguments
            })

            print(f"路线规划结果: {result[:200]}...")

            # TODO: 解析实际的路线数据
            return {}

        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            return {}

    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        """
        地理编码(地址转坐标)

        Args:
            address: 地址
            city: 城市

        Returns:
            经纬度坐标
        """
        try:
            arguments = {"address": address}
            if city:
                arguments["city"] = city

            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_geo",
                "arguments": arguments
            })

            print(f"地理编码结果: {result[:200]}...")

            # TODO: 解析实际的坐标数据
            return None

        except Exception as e:
            print(f"❌ 地理编码失败: {str(e)}")
            return None

    def get_poi_detail(self, poi_id: str) -> Dict[str, Any]:
        """
        获取POI详情

        Args:
            poi_id: POI ID

        Returns:
            POI详情信息
        """
        try:
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_search_detail",
                "arguments": {
                    "id": poi_id
                }
            })

            print(f"POI详情结果: {result[:200]}...")

            # 解析结果并提取图片
            import json
            import re

            # 尝试从结果中提取JSON
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data

            return {"raw": result}

        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}

#创建全局服务实例
_amap_servicer = None

def get_amap_service() -> AmapService:
    """获得高德地图服务实例"""
    global _amap_servicer

    if _amap_servicer is None:
        _amap_servicer = AmapService()

    return _amap_servicer