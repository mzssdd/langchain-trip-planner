"""旅行规划API路由"""

import threading
import traceback
import uuid
from typing import Any, Dict, List, Optional, TypedDict

from fastapi import APIRouter, HTTPException
from ...models.schemas import (
    ErrorResponse,
    TripRequest,
    TripTaskCreateResponse,
    TripTaskStatusResponse,
    TripPlanResponse,
)
from ...agents.trip_planner_agent import get_trip_planner_agent

router = APIRouter(prefix="/trip", tags=["旅行规划"])


class TripTaskState(TypedDict):
    status: str
    message: str
    data: Optional[dict]
    error: Optional[str]
    history: List[Dict[str, Any]]


tripTaskMap: Dict[str, TripTaskState] = {}
tripTaskLock = threading.Lock()


def setTripTask(taskId: str, **kwargs) -> None:
    with tripTaskLock:
        currentTask = tripTaskMap.get(taskId, {
            'status': 'pending',
            'message': '',
            'data': None,
            'error': None,
            'history': [],
        })
        currentTask.update(kwargs)
        tripTaskMap[taskId] = currentTask


def appendTripTaskHistory(taskId: str, status: str, message: str) -> None:
    with tripTaskLock:
        currentTask = tripTaskMap.get(taskId, {
            'status': 'pending',
            'message': '',
            'data': None,
            'error': None,
            'history': [],
        })
        history = list(currentTask.get('history') or [])
        history.append({
            'status': status,
            'message': message,
        })
        currentTask['history'] = history
        currentTask['message'] = message
        currentTask['status'] = status
        tripTaskMap[taskId] = currentTask


def runTripTask(taskId: str, request: TripRequest) -> None:
    try:
        appendTripTaskHistory(taskId, 'running', '旅行计划生成中')

        print(f"\n{'=' * 60}")
        print(f"📥 收到旅行规划请求:")
        print(f"   task_id: {taskId}")
        print(f"   城市: {request.city}")
        print(f"   日期: {request.start_date} - {request.end_date}")
        print(f"   天数: {request.travel_days}")
        print(f"{'=' * 60}\n")

        print('🔄 获取多智能体系统实例...')
        appendTripTaskHistory(taskId, 'running', '正在获取规划器实例')
        agent = get_trip_planner_agent()

        print('🚀 开始生成旅行计划...')
        appendTripTaskHistory(taskId, 'running', '开始生成旅行计划')
        tripPlan = agent.plan_trip(
            request,
            progress_callback=lambda status, message: appendTripTaskHistory(taskId, status, message),
        )
        generationStatus = getattr(agent, 'last_generation_status', 'unknown')
        generationMessage = getattr(agent, 'last_generation_message', '') or '旅行计划生成完成'

        if generationStatus == 'fallback_success':
            print(f"⚠️  {generationMessage}, 准备返回fallback响应\n")
        else:
            print(f"✅ {generationMessage}, 准备返回响应\n")

        setTripTask(
            taskId,
            status='success',
            message=generationMessage,
            data=tripPlan.model_dump(),
            error=None,
        )
        appendTripTaskHistory(taskId, 'success', generationMessage)
    except Exception as error:
        print(f"❌ 生成旅行计划失败: {str(error)}")
        traceback.print_exc()
        setTripTask(
            taskId,
            status='failed',
            message='生成旅行计划失败',
            error=str(error),
            data=None,
        )
        appendTripTaskHistory(taskId, 'failed', f'生成旅行计划失败: {str(error)}')


@router.post(
    "/plan",
    response_model=TripPlanResponse,
    summary="生成旅行计划",
    description="根据用户输入的旅行需求,生成详细的旅行计划"
)
async def plan_trip(request: TripRequest):
    """
    生成旅行计划

    Args:
        request: 旅行请求参数

    Returns:
        旅行计划响应
    """
    try:
        print(f"\n{'='*60}")
        print(f"📥 收到旅行规划请求:")
        print(f"   城市: {request.city}")
        print(f"   日期: {request.start_date} - {request.end_date}")
        print(f"   天数: {request.travel_days}")
        print(f"{'='*60}\n")

        # 获取Agent实例
        print("🔄 获取多智能体系统实例...")
        agent = get_trip_planner_agent()

        # 生成旅行计划
        print("🚀 开始生成旅行计划...")
        trip_plan = agent.plan_trip(request)
        generation_status = getattr(agent, "last_generation_status", "unknown")
        generation_message = getattr(agent, "last_generation_message", "") or "旅行计划生成完成"

        if generation_status == "fallback_success":
            print(f"⚠️  {generation_message}, 准备返回fallback响应\n")
        else:
            print(f"✅ {generation_message}, 准备返回响应\n")

        return TripPlanResponse(
            success=True,
            message=generation_message,
            data=trip_plan
        )

    except Exception as e:
        print(f"❌ 生成旅行计划失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"生成旅行计划失败: {str(e)}"
        )


@router.post(
    '/plan-task',
    response_model=TripTaskCreateResponse,
    summary='创建旅行规划任务',
    description='创建异步旅行规划任务，立即返回 task_id'
)
async def create_trip_plan_task(request: TripRequest):
    """创建异步旅行规划任务"""
    taskId = uuid.uuid4().hex
    setTripTask(
        taskId,
        status='pending',
        message='任务已创建，等待执行',
        data=None,
        error=None,
        history=[],
    )
    appendTripTaskHistory(taskId, 'pending', '任务已创建，等待执行')

    workerThread = threading.Thread(
        target=runTripTask,
        args=(taskId, request),
        daemon=True,
    )
    workerThread.start()

    return TripTaskCreateResponse(
        success=True,
        message='任务创建成功',
        task_id=taskId,
        status='pending',
    )


@router.get(
    '/plan-task/{task_id}',
    response_model=TripTaskStatusResponse,
    summary='查询旅行规划任务状态',
    description='根据 task_id 查询异步旅行规划任务状态和结果'
)
async def get_trip_plan_task(task_id: str):
    """查询异步旅行规划任务状态"""
    with tripTaskLock:
        taskInfo = tripTaskMap.get(task_id)

    if taskInfo is None:
        raise HTTPException(
            status_code=404,
            detail='任务不存在'
        )

    return TripTaskStatusResponse(
        success=taskInfo['status'] != 'failed',
        message=taskInfo['message'],
        task_id=task_id,
        status=taskInfo['status'],
        data=taskInfo['data'],
        error=taskInfo['error'],
        history=taskInfo.get('history') or [],
    )


@router.get(
    "/health",
    summary="健康检查",
    description="检查旅行规划服务是否正常"
)
async def health_check():
    """健康检查"""
    try:
        # 检查Agent是否可用
        agent = get_trip_planner_agent()
        planner_agent = getattr(agent, 'planner_agent', None)
        fallback_planner_agent = getattr(agent, 'fallback_planner_agent', None)

        return {
            'status': 'healthy',
            'service': 'trip-planner',
            'agent_name': getattr(planner_agent, 'name', '行程规划专家'),
            'fallback_agent_name': getattr(fallback_planner_agent, 'name', '默认行程规划专家'),
            'planner_ready': planner_agent is not None,
            'fallback_ready': fallback_planner_agent is not None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"服务不可用: {str(e)}"
        )
