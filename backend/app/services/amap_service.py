""" 高德地图MCP服务封装 """

from typing import Any, Dict, List, Optional

from ..config import get_settings
from ..models.schemas import Location, POIInfo, RouteInfo, WeatherInfo
from ..planner.pois import normalize_pois
from ..planner.weather import normalize_weather
from .amap_mcp import AmapMcpClient, get_amap_mcp_client

#全局mcp工具实例
def get_amap_map_tool() -> AmapMcpClient:
    """
    获取高德地图MCP工具实例(单例模式)

    Returns:
        MCPTool实例
    """

    return get_amap_mcp_client()

class AmapService:
    """高德地图服务封装类"""
    def __init__(self):
        """初始化服务"""
        settings = get_settings()
        self.api_key = settings.amap_api_key
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
            if not self.api_key:
                raise ValueError("高德地图API Key未配置")

            raw = self.mcp_tool.call(
                ("maps_text_search", "text_search"),
                {
                    "keywords": keywords,
                    "city": city,
                    "citylimit": str(citylimit).lower(),
                    "extensions": "all",
                    "offset": 20,
                    "page": 1,
                },
            )
            pois = normalize_pois(raw, keywords, "scenic", False, "mcp")
            return [
                POIInfo(
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    type=item.get("type", ""),
                    address=item.get("address", ""),
                    location=Location(**location),
                    tel=None,
                )
                for item in pois
                for location in [
                    item.get("location")
                    or self.mcp_tool.geocode_location(item.get("address", ""), city)
                ]
                if location
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

            raw = self.mcp_tool.call(
                ("maps_weather", "weather"),
                {
                    "city": city,
                    "extensions": "all",
                },
            )
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
    ) -> RouteInfo:
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

            origin_location = self.geocode(origin_address, origin_city)
            destination_location = self.geocode(destination_address, destination_city)
            if not origin_location:
                raise ValueError(f"起点地址无法解析为坐标: {origin_address}")
            if not destination_location:
                raise ValueError(f"终点地址无法解析为坐标: {destination_address}")

            origin = self._format_location(origin_location)
            destination = self._format_location(destination_location)
            direction_tool_names = {
                "walking": ("maps_direction_walking",),
                "driving": ("maps_direction_driving",),
                "transit": ("maps_direction_transit_integrated",),
            }
            result = self.mcp_tool.call(
                direction_tool_names.get(route_type, direction_tool_names["walking"]),
                {
                    "origin": origin,
                    "destination": destination,
                    "city": origin_city or destination_city or "",
                    "cityd": destination_city or origin_city or "",
                },
            )

            route = result.get("route") or {}
            if not route:
                raise ValueError(f"高德路线 MCP 返回失败: {result}")

            if route_type == "transit":
                transits = route.get("transits") or []
                if not transits:
                    raise ValueError("高德公交 MCP 未返回有效路径数据")
                distance = float(route.get("distance") or 0)
                duration = int(float(transits[0].get("duration") or 0))
            else:
                paths = route.get("paths") or []
                if not paths:
                    raise ValueError("高德路线 MCP 未返回有效路径数据")
                best_path = paths[0] or {}
                distance = float(best_path.get("distance") or 0)
                duration = int(float(best_path.get("duration") or 0))

            return RouteInfo(
                distance=distance,
                duration=duration,
                route_type=route_type,
                description=self._build_route_description(distance, duration, route_type),
            )

        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            raise

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

            location = self.mcp_tool.geocode_location(address, city)
            if not location:
                return None
            return Location(**location)

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

            data = self.mcp_tool.call(
                ("maps_search_detail",),
                {"id": poi_id},
            )
            print(f"POI详情结果: {str(data)[:200]}...")
            return data

        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}

    def _build_route_description(
        self,
        distance: float,
        duration: int,
        route_type: str,
    ) -> str:
        """生成给前端展示的路线描述。"""
        distance_km = round(distance / 1000, 1)
        duration_min = max(1, int(round(duration / 60)))
        return f"{route_type}路线约{distance_km}公里，预计{duration_min}分钟"

    def _format_location(self, location: Location) -> str:
        """把经纬度对象转换成高德路线接口需要的字符串。"""
        return f"{location.longitude:.6f},{location.latitude:.6f}"


#创建全局服务实例
_amap_servicer = None

def get_amap_service() -> AmapService:
    """获得高德地图服务实例"""
    global _amap_servicer

    if _amap_servicer is None:
        _amap_servicer = AmapService()

    return _amap_servicer
