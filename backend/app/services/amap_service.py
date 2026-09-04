""" 高德地图MCP服务封装 """

from typing import List, Dict, Any, Optional

import httpx
from langchain_mcp_adapters.client import MultiServerMCPClient
from .mcp_env import build_amap_mcp_env
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo
from ..planner.pois import normalize_pois
from ..planner.weather import normalize_weather

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
        settings = get_settings()
        self.api_key = settings.amap_api_key
        self.mcp_tool = get_amap_map_tool()
        self.base_url = "https://restapi.amap.com/v3"

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
            if not self.api_key:
                raise ValueError("高德地图API Key未配置")

            response = httpx.get(
                f"{self.base_url}/place/text",
                params={
                    "keywords": keywords,
                    "city": city,
                    "citylimit": str(citylimit).lower(),
                    "extensions": "all",
                    "offset": 20,
                    "page": 1,
                    "key": self.api_key,
                },
                timeout=30,
            )
            response.raise_for_status()
            raw = response.json()
            pois = normalize_pois(raw, keywords, "scenic", True, "api")
            return [
                POIInfo(
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    type=item.get("type", ""),
                    address=item.get("address", ""),
                    location=Location(**item["location"]),
                    tel=None,
                )
                for item in pois
                if item.get("location")
            ]
        
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
            if not self.api_key:
                raise ValueError("高德地图API Key未配置")

            response = httpx.get(
                f"{self.base_url}/weather/weatherInfo",
                params={
                    "city": city,
                    "extensions": "all",
                    "key": self.api_key,
                },
                timeout=30,
            )
            response.raise_for_status()
            raw = response.json()
            return [
                WeatherInfo(**item)
                for item in normalize_weather(raw)
            ]

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
            if not self.api_key:
                raise ValueError("高德地图API Key未配置")

            if route_type == "driving":
                path = "/direction/driving"
            elif route_type == "transit":
                path = "/direction/transit/integrated"
            else:
                path = "/direction/walking"

            params = {
                "origin": origin_address,
                "destination": destination_address,
                "key": self.api_key,
            }
            response = httpx.get(f"{self.base_url}{path}", params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            print(f"路线规划结果: {str(result)[:200]}...")
            return result

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
            if not self.api_key:
                raise ValueError("高德地图API Key未配置")

            params = {"address": address, "key": self.api_key}
            if city:
                params["city"] = city

            response = httpx.get(f"{self.base_url}/geocode/geo", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            geocodes = data.get("geocodes") or []
            if not geocodes:
                return None

            location = geocodes[0].get("location", "")
            if not location or "," not in location:
                return None

            longitude, latitude = location.split(",", 1)
            return Location(longitude=float(longitude), latitude=float(latitude))

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
            if not self.api_key:
                raise ValueError("高德地图API Key未配置")

            response = httpx.get(
                f"{self.base_url}/place/detail",
                params={"id": poi_id, "key": self.api_key},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            print(f"POI详情结果: {str(data)[:200]}...")
            return data

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
