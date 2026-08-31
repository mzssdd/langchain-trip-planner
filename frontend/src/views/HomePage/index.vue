<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-copy">
        <div class="hero-kicker">AI Travel Workflow</div>
        <h1 class="hero-title">把出行需求整理成一份真正能执行的行程</h1>
        <p class="hero-description">
          参考你另一个项目的交互方式，这里直接对接当前后端服务，提交后生成每日行程、预算和天气建议。
        </p>
      </div>

      <div class="hero-status">
        <div class="hero-status-item">
          <span class="hero-status-label">目的地</span>
          <strong>{{ formState.city || '待填写' }}</strong>
        </div>
        <div class="hero-status-item">
          <span class="hero-status-label">天数</span>
          <strong>{{ formState.travel_days }} 天</strong>
        </div>
        <div class="hero-status-item">
          <span class="hero-status-label">同行</span>
          <strong>{{ formState.party.total }} 人</strong>
        </div>
      </div>
    </section>

    <a-card :bordered="false" class="planner-card">
      <div class="planner-header">
        <div>
          <div class="planner-kicker">Trip Request</div>
          <h2 class="planner-title">填写旅行需求</h2>
        </div>
        <a-tag :color="healthTagColor">{{ healthText }}</a-tag>
      </div>

      <a-form
        :model="formState"
        layout="vertical"
        @finish="handleSubmit"
      >
        <section class="form-section">
          <div class="section-title">基础信息</div>

          <a-row :gutter="[16, 0]">
            <a-col :xs="24" :md="8">
              <a-form-item
                label="目的地城市"
                name="city"
                :rules="[{ required: true, message: '请输入目的地城市' }]"
              >
                <a-input
                  v-model:value="formState.city"
                  placeholder="例如：北京"
                  size="large"
                />
              </a-form-item>
            </a-col>

            <a-col :xs="24" :md="8">
              <a-form-item
                label="开始日期"
                name="start_date"
                :rules="[{ required: true, message: '请选择开始日期' }]"
              >
                <a-date-picker
                  v-model:value="formState.start_date"
                  class="w100"
                  size="large"
                  value-format="YYYY-MM-DD"
                />
              </a-form-item>
            </a-col>

            <a-col :xs="24" :md="8">
              <a-form-item
                label="结束日期"
                name="end_date"
                :rules="[{ required: true, message: '请选择结束日期' }]"
              >
                <a-date-picker
                  v-model:value="formState.end_date"
                  class="w100"
                  size="large"
                  value-format="YYYY-MM-DD"
                />
              </a-form-item>
            </a-col>
          </a-row>
        </section>

        <section class="form-section">
          <div class="section-title">同行与预算</div>

          <a-row :gutter="[16, 0]">
            <a-col :xs="24" :sm="8" :md="4">
              <a-form-item label="成人">
                <a-input-number
                  v-model:value="formState.party.adults"
                  :min="0"
                  :max="20"
                  class="w100"
                  size="large"
                />
              </a-form-item>
            </a-col>

            <a-col :xs="24" :sm="8" :md="4">
              <a-form-item label="儿童">
                <a-input-number
                  v-model:value="formState.party.children"
                  :min="0"
                  :max="20"
                  class="w100"
                  size="large"
                />
              </a-form-item>
            </a-col>

            <a-col :xs="24" :sm="8" :md="4">
              <a-form-item label="老人">
                <a-input-number
                  v-model:value="formState.party.elders"
                  :min="0"
                  :max="20"
                  class="w100"
                  size="large"
                />
              </a-form-item>
            </a-col>

            <a-col :xs="24" :md="6">
              <a-form-item label="同行类型">
                <a-select
                  v-model:value="formState.party.companion_type"
                  size="large"
                >
                  <a-select-option
                    v-for="item in companionTypeList"
                    :key="item.value"
                    :value="item.value"
                  >
                    {{ item.label }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>

            <a-col :xs="24" :md="6">
              <a-form-item label="总预算">
                <a-input-number
                  v-model:value="formState.budget_constraint.amount"
                  :min="0"
                  :step="100"
                  class="w100"
                  size="large"
                  placeholder="可选"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="[16, 0]">
            <a-col :xs="24" :md="12">
              <a-form-item label="预算档位">
                <a-select
                  v-model:value="formState.budget_constraint.budget_level"
                  size="large"
                >
                  <a-select-option
                    v-for="item in budgetLevelList"
                    :key="item.value"
                    :value="item.value"
                  >
                    {{ item.label }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>

            <a-col :xs="24" :md="12">
              <a-form-item label="预算严格程度">
                <a-select
                  v-model:value="formState.budget_constraint.strictness"
                  size="large"
                >
                  <a-select-option value="none">不限制</a-select-option>
                  <a-select-option value="soft">尽量控制</a-select-option>
                  <a-select-option value="hard">严格限制</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
        </section>

        <section class="form-section">
          <div class="section-title">出行偏好</div>

          <a-row :gutter="[16, 0]">
            <a-col :xs="24" :md="12">
              <a-form-item label="交通方式">
                <a-select
                  v-model:value="formState.transportation"
                  size="large"
                >
                  <a-select-option
                    v-for="item in transportationList"
                    :key="item"
                    :value="item"
                  >
                    {{ item }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>

            <a-col :xs="24" :md="12">
              <a-form-item label="住宿偏好">
                <a-select
                  v-model:value="formState.accommodation"
                  size="large"
                >
                  <a-select-option
                    v-for="item in accommodationList"
                    :key="item"
                    :value="item"
                  >
                    {{ item }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>

          <a-form-item label="旅行偏好">
            <a-checkbox-group v-model:value="formState.preferences" class="preference-group">
              <a-checkbox
                v-for="item in preferenceList"
                :key="item.value"
                :value="item.value"
                class="preference-item"
              >
                {{ item.label }}
              </a-checkbox>
            </a-checkbox-group>
          </a-form-item>
        </section>

        <section class="form-section">
          <div class="section-title">补充说明</div>

          <a-form-item label="额外要求">
            <a-textarea
              v-model:value="formState.free_text_input"
              :rows="4"
              placeholder="例如：希望多安排博物馆、减少排队景点、适合带老人出行等"
            />
          </a-form-item>
        </section>

        <div class="submit-area">
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            :loading="isSubmitting"
            class="submit-button"
          >
            开始生成行程
          </a-button>
          <span class="submit-tip">提交后会创建异步任务并轮询结果</span>
        </div>

        <div v-if="taskState.status" class="task-status-panel">
          <div class="task-status-title">任务状态</div>
          <div class="task-status-row">
            <span class="task-status-label">状态</span>
            <span class="task-status-value">{{ taskStatusText }}</span>
          </div>
          <div v-if="taskState.taskId" class="task-status-row">
            <span class="task-status-label">任务 ID</span>
            <span class="task-status-value">{{ taskState.taskId }}</span>
          </div>
          <div v-if="taskState.message" class="task-status-row">
            <span class="task-status-label">说明</span>
            <span class="task-status-value">{{ taskState.message }}</span>
          </div>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
// --------首先是模块不太清晰的一些内容--------
// 变量
import dayjs from 'dayjs'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'

import { createTripPlanTask, getTripHealth, getTripPlanTask } from '@/apis/tripApi'
import { TRIP_PLAN_STORAGE_KEY, getDefaultCompanionType, getPartyTotal, getTravelDays } from '@/utils/common'
import type { HealthResponse, TripRequest, TripTaskStatusResponse } from '@/types'

interface TripFormState {
  city: string
  start_date: string
  end_date: string
  travel_days: number
  transportation: string
  accommodation: string
  preferences: string[]
  free_text_input: string
  party: {
    adults: number
    children: number
    elders: number
    total: number
    companion_type: TripRequest['party']['companion_type']
  }
  budget_constraint: TripRequest['budget_constraint']
}

const router = useRouter()
const isSubmitting = ref(false)
const healthState = reactive<{
  isLoading: boolean
  data: HealthResponse | null
  isError: boolean
}>({
  isLoading: false,
  data: null,
  isError: false,
})
const taskState = reactive<{
  taskId: string
  status: '' | 'pending' | 'running' | 'success' | 'failed'
  message: string
}>({
  taskId: '',
  status: '',
  message: '',
})
let taskTimer: number | null = null

const formState = reactive<TripFormState>({
  city: '',
  start_date: '',
  end_date: '',
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '经济型酒店',
  preferences: [],
  free_text_input: '',
  party: {
    adults: 1,
    children: 0,
    elders: 0,
    total: 1,
    companion_type: 'solo',
  },
  budget_constraint: {
    amount: null,
    scope: 'total',
    currency: 'CNY',
    budget_level: 'standard',
    strictness: 'none',
  },
})

const companionTypeList = [
  { label: '独行', value: 'solo' },
  { label: '情侣', value: 'couple' },
  { label: '朋友', value: 'friends' },
  { label: '亲子', value: 'family_with_children' },
  { label: '带长辈', value: 'family_with_elders' },
  { label: '商务', value: 'business' },
  { label: '其他', value: 'other' },
] as const

const budgetLevelList = [
  { label: '节省', value: 'limited' },
  { label: '标准', value: 'standard' },
  { label: '舒适', value: 'comfortable' },
  { label: '高端', value: 'premium' },
  { label: '奢华', value: 'luxury' },
] as const

const transportationList = [
  '公共交通',
  '地铁公交',
  '打车/网约车',
  '自驾',
  '租车自驾',
  '高铁+市内交通',
  '飞机+市内交通',
  '步行/骑行',
  '混合交通',
]

const accommodationList = [
  '经济型酒店',
  '舒适型酒店',
  '高端酒店',
  '豪华酒店',
  '民宿',
  '亲子酒店',
]

const preferenceList = [
  { label: '历史文化', value: '历史文化' },
  { label: '自然风光', value: '自然风光' },
  { label: '美食', value: '美食' },
  { label: '购物', value: '购物' },
  { label: '休闲', value: '休闲' },
  { label: '艺术', value: '艺术' },
  { label: '夜游', value: '夜游' },
  { label: '博物馆', value: '博物馆' },
  { label: '摄影打卡', value: '摄影打卡' },
  { label: '亲子友好', value: '亲子友好' },
  { label: '老人友好', value: '老人友好' },
  { label: '避开人群', value: '避开人群' },
]

// 定义props、emit

// 计算属性
const healthText = computed(() => {
  if (healthState.isLoading) {
    return '后端检测中'
  }

  if (healthState.isError) {
    return '后端异常'
  }

  if (healthState.data?.status === 'healthy') {
    return '后端可用'
  }

  return '未检测'
})

const healthTagColor = computed(() => {
  if (healthState.isError) {
    return 'error'
  }

  if (healthState.data?.status === 'healthy') {
    return 'success'
  }

  return 'processing'
})

const taskStatusText = computed(() => {
  const statusMap: Record<string, string> = {
    pending: '任务已创建',
    running: '正在生成',
    success: '生成完成',
    failed: '生成失败',
  }

  return statusMap[taskState.status] || '未开始'
})

// watch
watch(
  () => [formState.start_date, formState.end_date],
  ([startDate, endDate]) => {
    if (!startDate || !endDate) {
      formState.travel_days = 1
      return
    }

    const travelDays = getTravelDays(
      startDate ? dayjs(startDate) : null,
      endDate ? dayjs(endDate) : null
    )

    if (travelDays <= 0) {
      message.warning('结束日期不能早于开始日期')
      formState.end_date = ''
      formState.travel_days = 1
      return
    }

    if (travelDays > 30) {
      message.warning('旅行天数不能超过30天')
      formState.end_date = ''
      formState.travel_days = 1
      return
    }

    formState.travel_days = travelDays
  }
)

watch(
  () => [formState.party.adults, formState.party.children, formState.party.elders],
  ([adults, children, elders]) => {
    formState.party.total = getPartyTotal({
      adults: Number(adults || 0),
      children: Number(children || 0),
      elders: Number(elders || 0),
    })
    formState.party.companion_type = getDefaultCompanionType(formState.party)
  },
  {
    immediate: true,
  }
)

// 生命周期
onMounted(() => {
  loadTripHealth()
})

// methods
async function loadTripHealth() {
  healthState.isLoading = true
  healthState.isError = false

  try {
    healthState.data = await getTripHealth()
  } catch (error) {
    healthState.isError = true
  } finally {
    healthState.isLoading = false
  }
}

function validateFormState(): boolean {
  if (!formState.city.trim()) {
    message.error('请输入目的地城市')
    return false
  }

  if (!formState.start_date || !formState.end_date) {
    message.error('请选择完整日期')
    return false
  }

  if (formState.party.total <= 0) {
    message.error('同行人数至少为 1 人')
    return false
  }

  return true
}

async function handleSubmit() {
  if (!validateFormState()) {
    return
  }

  isSubmitting.value = true
  clearTaskTimer()
  taskState.taskId = ''
  taskState.status = 'pending'
  taskState.message = '正在创建任务'

  try {
    const strictness = formState.budget_constraint.amount ? formState.budget_constraint.strictness : 'none'
    const requestData: TripRequest = {
      city: formState.city.trim(),
      start_date: formState.start_date,
      end_date: formState.end_date,
      travel_days: formState.travel_days,
      transportation: formState.transportation,
      accommodation: formState.accommodation,
      preferences: formState.preferences,
      free_text_input: formState.free_text_input.trim(),
      party: {
        ...formState.party,
      },
      budget_constraint: {
        ...formState.budget_constraint,
        amount: formState.budget_constraint.amount ?? null,
        strictness,
      },
    }

    const createResponse = await createTripPlanTask(requestData)
    taskState.taskId = createResponse.task_id
    taskState.status = 'pending'
    taskState.message = createResponse.message || '任务已创建'

    await pollTripTask(createResponse.task_id)
  } finally {
    isSubmitting.value = false
  }
}

async function pollTripTask(taskId: string) {
  return new Promise<void>((resolve, reject) => {
    async function queryTask() {
      try {
        const response = await getTripPlanTask(taskId)
        updateTaskState(response)

        if (response.status === 'success' && response.data) {
          clearTaskTimer()
          sessionStorage.setItem(TRIP_PLAN_STORAGE_KEY, JSON.stringify(response.data))
          message.success(response.message || '旅行计划生成成功')
          router.push('/result')
          resolve()
          return
        }

        if (response.status === 'failed') {
          clearTaskTimer()
          const errorMessage = response.error || response.message || '生成旅行计划失败'
          message.error(errorMessage)
          reject(new Error(errorMessage))
          return
        }

        taskTimer = window.setTimeout(queryTask, 3000)
      } catch (error) {
        clearTaskTimer()
        message.error('查询任务状态失败')
        reject(error)
      }
    }

    queryTask()
  })
}

function updateTaskState(response: TripTaskStatusResponse) {
  taskState.taskId = response.task_id
  taskState.status = response.status
  taskState.message = response.message
}

function clearTaskTimer() {
  if (taskTimer !== null) {
    window.clearTimeout(taskTimer)
    taskTimer = null
  }
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 20px 48px;
}

.hero-section {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 20px;
  margin-bottom: 24px;
  padding: 36px;
  border-radius: 24px;
  background:
    linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 64, 175, 0.82)),
    linear-gradient(180deg, #0f172a, #1d4ed8);
  color: #ffffff;
  box-shadow: 0 20px 48px rgba(15, 23, 42, 0.18);
}

.hero-kicker {
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.hero-title {
  margin: 0;
  font-size: 38px;
  line-height: 1.18;
}

.hero-description {
  max-width: 640px;
  margin: 16px 0 0;
  color: rgba(255, 255, 255, 0.82);
  font-size: 16px;
  line-height: 1.8;
}

.hero-status {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1px;
  align-self: end;
  overflow: hidden;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.18);
}

.hero-status-item {
  padding: 18px 20px;
  background: rgba(255, 255, 255, 0.1);
}

.hero-status-label {
  display: block;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.hero-status-item strong {
  font-size: 22px;
  font-weight: 700;
}

.planner-card {
  border-radius: 24px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.1);
}

.planner-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}

.planner-kicker {
  color: #2563eb;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.planner-title {
  margin: 8px 0 0;
  color: #0f172a;
  font-size: 28px;
}

.form-section {
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.form-section:last-of-type {
  border-bottom: none;
}

.section-title {
  margin-bottom: 16px;
  color: #0f172a;
  font-size: 18px;
  font-weight: 700;
}

.preference-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.preference-item {
  margin-inline-start: 0 !important;
  padding: 8px 14px;
  border: 1px solid #dbe3ef;
  border-radius: 999px;
  background: #f8fbff;
}

.submit-area {
  display: flex;
  align-items: center;
  gap: 16px;
}

.submit-button {
  min-width: 220px;
  height: 48px;
  border-radius: 999px;
  background: linear-gradient(135deg, #0f766e 0%, #2563eb 100%);
  border: none;
  box-shadow: 0 14px 30px rgba(37, 99, 235, 0.24);
}

.submit-tip {
  color: #64748b;
  font-size: 13px;
}

.task-status-panel {
  margin-top: 20px;
  padding: 18px 20px;
  border: 1px solid #dbeafe;
  border-radius: 18px;
  background: #f8fbff;
}

.task-status-title {
  margin-bottom: 12px;
  color: #0f172a;
  font-size: 16px;
  font-weight: 700;
}

.task-status-row {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

.task-status-row:last-child {
  margin-bottom: 0;
}

.task-status-label {
  min-width: 64px;
  color: #64748b;
  font-weight: 600;
}

.task-status-value {
  color: #0f172a;
  line-height: 1.6;
  word-break: break-all;
}

@media (max-width: 900px) {
  .hero-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .home-page {
    padding: 16px 12px 32px;
  }

  .hero-section {
    padding: 24px 20px;
    border-radius: 20px;
  }

  .hero-title {
    font-size: 28px;
  }

  .planner-header {
    flex-direction: column;
  }

  .submit-area {
    align-items: stretch;
    flex-direction: column;
  }

  .submit-button {
    width: 100%;
  }
}
</style>
