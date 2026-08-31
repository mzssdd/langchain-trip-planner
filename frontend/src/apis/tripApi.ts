import httpRequest from '@/apis/request'
import type { HealthResponse, TripPlanResponse, TripRequest } from '@/types'

/**
 * @description 生成旅行计划
 * @link http://localhost:7000/docs#/default/plan_trip_api_trip_plan_post
 */
export async function fetchTripPlan(data: TripRequest): Promise<TripPlanResponse> {
  return httpRequest.post<TripPlanResponse>('/api/trip/plan', data)
}

/**
 * @description 获取旅行规划健康状态
 * @link http://localhost:7000/docs#/default/health_check_api_trip_health_get
 */
export async function getTripHealth(): Promise<HealthResponse> {
  return httpRequest.get<HealthResponse>('/api/trip/health')
}
