"""多智能体旅行规划系统"""

import os
import time
from typing import Dict, Any, List, Optional


from ..config import get_settings
from ..planner




#最大尝试次数
PLANNER_MAX_ATTEMPTS = 5
#单次请求超时时间
PLANNER_REQUEST_TIMEOUT = int(os.getenv("PLANNER_REQUEST_TIMEOUT", "600"))
#LLM生成温度
PLANNER_TEMPERATURE = float(os.getenv("PLANNER_TEMPERATURE", "0.2"))
#主模型调用失败容忍次数
PLANNER_PRIMARY_CALL_FAILURE_LIMIT = int(os.getenv("PLANNER_PRIMARY_CALL_FAILURE_LIMIT", "3"))
#备用模型调用失败容忍次数
PLANNER_FALLBACK_CALL_FAILURE_LIMIT = int(os.getenv("PLANNER_FALLBACK_CALL_FAILURE_LIMIT", "3"))
#是否启用重排序
PLANNER_ENABLE_RERANK = os.getenv("PLANNER_ENABLE_RERANK", "1") == "1"
#重排序候选数
PLANNER_RERANK_CANDIDATE_COUNT = max(1, int(os.getenv("PLANNER_RERANK_CANDIDATE_COUNT", "3")))
#重排序温度步长
PLANNER_RERANK_TEMPERATURE_STEP = float(os.getenv("PLANNER_RERANK_TEMPERATURE_STEP", "0.08"))


class MultAgentTripPlanner:
    """多智能体旅行规划系统"""

    def __init__(self):
        """初始化多智能体系统"""
        print("开始启用")
        self.last_generation_status = "idle"
        self.last_generation_message = ''

        try:
            settings = get_settings()
            self.settings = settings
            self.amap_api_key = settings.amap_api_key or os.getenv("AMAP_MAPS_API_KEY") or os.getenv("AMAP_API_KEY")
            self.planner_context_builder = PlannerContextBuilder(self.amap_api_key)
            self.tool_llm = get_llm()
            self.planner_llm = get_planner_llm()
            self.llm = self.tool_llm


        except Exception as e:
            print(f"❌ 多智能体系统初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

