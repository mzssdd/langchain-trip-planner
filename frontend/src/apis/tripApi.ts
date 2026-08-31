import httpRequest from '@/apis/request'
import type {
  HealthResponse,
  TripPlanResponse,
  TripRequest,
  TripTaskCreateResponse,
  TripTaskStatusResponse,
} from '@/types'

/**
 * @description 生成旅行计划
 * @link http://localhost:7000/docs#/default/plan_trip_api_trip_plan_post
 */
export async function fetchTripPlan(data: TripRequest): Promise<TripPlanResponse> {
  return httpRequest.post<TripPlanResponse>('/api/trip/plan', data)
}

/**
 * @description 创建异步旅行规划任务
 * @link http://localhost:7000/docs#/default/create_trip_plan_task_api_trip_plan_task_post
 */
export async function createTripPlanTask(
  data: TripRequest
): Promise<TripTaskCreateResponse> {
  return httpRequest.post<TripTaskCreateResponse>('/api/trip/plan-task', data)
}

/**
 * @description 查询异步旅行规划任务状态
 * @link http://localhost:7000/docs#/default/get_trip_plan_task_api_trip_plan_task__task_id__get
 */
export async function getTripPlanTask(taskId: string): Promise<TripTaskStatusResponse> {
  return httpRequest.get<TripTaskStatusResponse>(`/api/trip/plan-task/${taskId}`)
}

/**
 * @description 获取旅行规划健康状态
 * @link http://localhost:7000/docs#/default/health_check_api_trip_health_get
 */
export async function getTripHealth(): Promise<HealthResponse> {
  return httpRequest.get<HealthResponse>('/api/trip/health')
}
