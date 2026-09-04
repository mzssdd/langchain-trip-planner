<template>
  <div class="result-page">
    <div class="page-toolbar">
      <a-button size="large" @click="handleBackHome">
        返回首页
      </a-button>
      <a-button type="primary" ghost size="large" @click="handleRefreshPlan">
        查看缓存结果
      </a-button>
    </div>

    <template v-if="tripPlan">
      <section class="summary-section">
        <div class="summary-main">
          <div class="summary-kicker">Trip Summary</div>
          <h1 class="summary-title">{{ tripPlan.city }} 行程计划</h1>
          <p class="summary-description">
            {{ tripPlan.start_date }} 至 {{ tripPlan.end_date }}
          </p>
          <p class="summary-advice">
            {{ tripPlan.overall_suggestions }}
          </p>
        </div>

        <div class="summary-side">
          <div v-if="tripPlan.budget" class="budget-panel">
            <div class="budget-panel-title">预算概览</div>
            <div class="budget-total">¥{{ tripPlan.budget.total }}</div>
            <div class="budget-grid">
              <div class="budget-item">
                <span>景点</span>
                <strong>¥{{ tripPlan.budget.total_attractions }}</strong>
              </div>
              <div class="budget-item">
                <span>住宿</span>
                <strong>¥{{ tripPlan.budget.total_hotels }}</strong>
              </div>
              <div class="budget-item">
                <span>餐饮</span>
                <strong>¥{{ tripPlan.budget.total_meals }}</strong>
              </div>
              <div class="budget-item">
                <span>交通</span>
                <strong>¥{{ tripPlan.budget.total_transportation }}</strong>
              </div>
            </div>
          </div>

          <a-card
            v-if="tripPlan.weather_info.length"
            title="天气信息"
            :bordered="false"
            class="side-card"
          >
            <div class="weather-list">
              <div
                v-for="weather in tripPlan.weather_info"
                :key="weather.date"
                class="weather-card"
              >
                <div class="weather-date">{{ weather.date }}</div>
                <div class="weather-row">
                  <span>白天</span>
                  <strong>{{ weather.day_weather }} {{ weather.day_temp }}</strong>
                </div>
                <div class="weather-row">
                  <span>夜间</span>
                  <strong>{{ weather.night_weather }} {{ weather.night_temp }}</strong>
                </div>
                <div class="weather-wind">{{ weather.wind_direction }} {{ weather.wind_power }}</div>
              </div>
            </div>
          </a-card>
        </div>
      </section>

      <a-card title="每日行程" :bordered="false" class="content-card">
        <a-collapse v-model:activeKey="activeDayKey" accordion>
          <a-collapse-panel
            v-for="day in tripPlan.days"
            :key="String(day.day_index)"
          >
            <template #header>
              <div class="day-header">
                <span class="day-header-title">第 {{ day.day_index + 1 }} 天</span>
                <span class="day-header-date">{{ day.date }}</span>
              </div>
            </template>

            <div class="day-section">
              <div class="info-row">
                <span class="info-label">行程描述</span>
                <span class="info-value">{{ day.description }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">交通方式</span>
                <span class="info-value">{{ day.transportation }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">住宿说明</span>
                <span class="info-value">{{ day.accommodation }}</span>
              </div>
            </div>

            <div class="day-section">
              <div class="section-subtitle">景点安排</div>
              <div class="poi-grid">
                <div
                  v-for="attraction in day.attractions"
                  :key="`${day.day_index}-${attraction.name}`"
                  class="poi-card"
                >
                  <div v-if="attraction.image_url" class="poi-image-wrap">
                    <img
                      :src="attraction.image_url"
                      :alt="attraction.name"
                      class="poi-image"
                    />
                  </div>
                  <div class="poi-card-title">{{ attraction.name }}</div>
                  <div class="poi-card-text">{{ attraction.address }}</div>
                  <div class="poi-card-text">{{ attraction.description }}</div>
                  <div class="poi-card-meta">
                    游览 {{ attraction.visit_duration }} 分钟
                  </div>
                </div>
              </div>
            </div>

            <div v-if="day.hotel" class="day-section">
              <div class="section-subtitle">酒店推荐</div>
              <div class="hotel-card">
                <div class="poi-card-title">{{ day.hotel.name }}</div>
                <div class="poi-card-text">{{ day.hotel.address }}</div>
                <div class="hotel-meta">
                  <span>{{ day.hotel.type || '酒店' }}</span>
                  <span>{{ day.hotel.price_range || '价格待定' }}</span>
                  <span>{{ day.hotel.rating || '评分待定' }}</span>
                </div>
              </div>
            </div>

            <div class="day-section">
              <div class="section-subtitle">餐饮安排</div>
              <a-timeline>
                <a-timeline-item
                  v-for="meal in day.meals"
                  :key="`${day.day_index}-${meal.type}-${meal.name}`"
                >
                  <div class="meal-title">{{ getMealLabel(meal.type) }} · {{ meal.name }}</div>
                  <div class="poi-card-text">{{ meal.description || meal.address || '暂无补充说明' }}</div>
                </a-timeline-item>
              </a-timeline>
            </div>
          </a-collapse-panel>
        </a-collapse>
      </a-card>
    </template>

    <a-empty v-else description="没有找到旅行计划">
      <a-button type="primary" @click="handleBackHome">去创建行程</a-button>
    </a-empty>
  </div>
</template>

<script setup lang="ts">
// --------首先是模块不太清晰的一些内容--------
// 变量
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { TRIP_PLAN_STORAGE_KEY } from '@/utils/common'
import type { Meal, TripPlan } from '@/types'

const router = useRouter()
const tripPlan = ref<TripPlan | null>(null)
const activeDayKey = ref<string[]>(['0'])

// 定义props、emit

// 计算属性

// watch

// 生命周期
onMounted(() => {
  loadTripPlan()
})

// methods
function loadTripPlan() {
  const rawValue = sessionStorage.getItem(TRIP_PLAN_STORAGE_KEY)
  tripPlan.value = rawValue ? JSON.parse(rawValue) : null
}

function handleBackHome() {
  router.push('/')
}

function handleRefreshPlan() {
  loadTripPlan()
}

function getMealLabel(type: Meal['type']): string {
  const mealLabelMap: Record<Meal['type'], string> = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐',
    snack: '加餐',
  }

  return mealLabelMap[type]
}
</script>

<style scoped>
.result-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 28px 20px 56px;
}

.page-toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.summary-section {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
  gap: 20px;
  margin-bottom: 20px;
}

.summary-main,
.budget-panel,
.side-card,
.content-card {
  border: 1px solid rgba(255, 255, 255, 0.68);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 20px 50px rgba(31, 41, 55, 0.08);
  backdrop-filter: blur(16px);
}

.summary-main {
  padding: 32px;
  background:
    linear-gradient(135deg, rgba(15, 118, 110, 0.95), rgba(17, 24, 39, 0.88)),
    linear-gradient(180deg, #0f172a, #134e4a);
  color: #fffaf3;
}

.summary-kicker {
  color: rgba(255, 255, 255, 0.68);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.summary-title {
  margin: 12px 0 0;
  font-size: 34px;
}

.summary-description {
  margin: 14px 0 0;
  color: rgba(255, 250, 243, 0.76);
  font-size: 15px;
}

.summary-advice {
  margin: 16px 0 0;
  line-height: 1.8;
}

.summary-side {
  display: grid;
  gap: 20px;
}

.budget-panel {
  padding: 24px;
}

.budget-panel-title {
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.budget-total {
  margin-top: 14px;
  color: #13202f;
  font-size: 36px;
  font-weight: 700;
}

.budget-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 18px;
}

.budget-item {
  padding: 14px;
  border-radius: 16px;
  background: #fbf9f4;
}

.budget-item span {
  display: block;
  color: #6b7280;
  font-size: 13px;
}

.budget-item strong {
  display: block;
  margin-top: 6px;
  color: #13202f;
  font-size: 18px;
}

.side-card,
.content-card {
  overflow: hidden;
}

.content-card {
  padding: 0;
}

.day-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 12px;
}

.day-header-title {
  color: #13202f;
  font-weight: 700;
}

.day-header-date {
  color: #6b7280;
  font-size: 13px;
}

.day-section + .day-section {
  margin-top: 24px;
}

.info-row {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
}

.info-label {
  min-width: 84px;
  color: #6b7280;
  font-weight: 600;
}

.info-value {
  color: #13202f;
  line-height: 1.7;
}

.section-subtitle {
  margin-bottom: 12px;
  color: #13202f;
  font-size: 16px;
  font-weight: 700;
}

.poi-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.poi-card,
.hotel-card,
.weather-card {
  padding: 16px;
  border: 1px solid #e3e8f0;
  border-radius: 18px;
  background: #fbf9f4;
}

.poi-image-wrap {
  overflow: hidden;
  margin-bottom: 12px;
  border-radius: 14px;
}

.poi-image {
  display: block;
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.poi-card-title,
.meal-title {
  color: #13202f;
  font-size: 15px;
  font-weight: 700;
}

.poi-card-text {
  margin-top: 8px;
  color: #475569;
  line-height: 1.7;
}

.poi-card-meta,
.hotel-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
  color: #0f766e;
  font-size: 12px;
}

.weather-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.weather-date {
  color: #13202f;
  font-size: 15px;
  font-weight: 700;
}

.weather-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 10px;
  color: #475569;
}

.weather-row strong {
  color: #13202f;
}

.weather-wind {
  margin-top: 10px;
  color: #6b7280;
  font-size: 13px;
}

:deep(.ant-card-head) {
  border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}

:deep(.ant-card-head-title) {
  color: #13202f;
  font-weight: 700;
}

:deep(.ant-collapse) {
  border: none;
  background: transparent;
}

:deep(.ant-collapse > .ant-collapse-item) {
  margin-bottom: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.72);
}

:deep(.ant-collapse > .ant-collapse-item:last-child) {
  margin-bottom: 0;
}

:deep(.ant-collapse > .ant-collapse-item > .ant-collapse-header) {
  align-items: center;
  padding: 16px 18px;
}

:deep(.ant-collapse-content) {
  border-top: 1px solid #edf2f7;
  background: rgba(255, 255, 255, 0.64);
}

:deep(.ant-collapse-content > .ant-collapse-content-box) {
  padding: 20px 18px 18px;
}

@media (max-width: 960px) {
  .summary-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .result-page {
    padding: 16px 12px 36px;
  }

  .page-toolbar {
    flex-wrap: wrap;
  }

  .summary-main,
  .budget-panel,
  .side-card,
  .content-card {
    border-radius: 22px;
  }

  .summary-main,
  .budget-panel {
    padding: 22px;
  }

  .summary-title {
    font-size: 28px;
  }

  .poi-grid {
    grid-template-columns: 1fr;
  }

  .info-row {
    flex-direction: column;
    gap: 4px;
  }
}
</style>
