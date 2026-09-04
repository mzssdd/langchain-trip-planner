export interface Location {
  longitude: number
  latitude: number
}

export interface Attraction {
  name: string
  address: string
  location: Location
  visit_duration: number
  description: string
  category?: string
  rating?: number | null
  photos?: string[]
  poi_id?: string
  image_url?: string | null
  ticket_price?: number
}

export interface Meal {
  type: 'breakfast' | 'lunch' | 'dinner' | 'snack'
  name: string
  address?: string | null
  location?: Location | null
  description?: string | null
  estimated_cost?: number
}

export interface Hotel {
  name: string
  address: string
  location?: Location | null
  price_range: string
  rating: string
  distance: string
  type: string
  estimated_cost?: number
}

export interface DayPlan {
  date: string
  day_index: number
  description: string
  transportation: string
  accommodation: string
  hotel?: Hotel | null
  attractions: Attraction[]
  meals: Meal[]
}

export interface WeatherInfo {
  date: string
  day_weather: string
  night_weather: string
  day_temp: number | string
  night_temp: number | string
  wind_direction: string
  wind_power: string
}

export interface Budget {
  total_attractions: number
  total_hotels: number
  total_meals: number
  total_transportation: number
  total: number
}

export interface TripPlan {
  city: string
  start_date: string
  end_date: string
  days: DayPlan[]
  weather_info: WeatherInfo[]
  overall_suggestions: string
  budget?: Budget | null
}

export interface PartyInfo {
  adults: number
  children: number
  elders: number
  total: number
  companion_type:
    | 'solo'
    | 'couple'
    | 'friends'
    | 'family_with_children'
    | 'family_with_elders'
    | 'business'
    | 'other'
}

export interface BudgetConstraint {
  amount: number | null
  scope: 'total'
  currency: 'CNY'
  budget_level: 'limited' | 'standard' | 'comfortable' | 'premium' | 'luxury'
  strictness: 'hard' | 'soft' | 'none'
}

export interface TripRequest {
  city: string
  start_date: string
  end_date: string
  travel_days: number
  transportation: string
  accommodation: string
  preferences: string[]
  free_text_input: string
  party: PartyInfo
  budget_constraint: BudgetConstraint
}

export interface TripPlanResponse {
  success: boolean
  message: string
  data?: TripPlan
}

export interface HealthResponse {
  status: string
  service: string
  agent_name?: string
  fallback_agent_name?: string
  planner_ready?: boolean
  fallback_ready?: boolean
}

export interface TripTaskCreateResponse {
  success: boolean
  message: string
  task_id: string
  status: string
}

export interface TripTaskStatusResponse {
  success: boolean
  message: string
  task_id: string
  status: 'pending' | 'running' | 'success' | 'failed'
  data?: TripPlan
  error?: string | null
  history?: Array<{
    status: 'pending' | 'running' | 'success' | 'failed'
    message: string
  }>
}
