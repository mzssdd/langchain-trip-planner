<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-copy">
        <div class="hero-kicker">AI Travel Workflow</div>
        <h1 class="hero-title">旅行计划生成器</h1>
        <p class="hero-description">
          先确认服务状态，再进入需求填写页，最后查看自动生成的行程结果。
        </p>

        <div class="hero-actions">
          <a-button type="primary" size="large" @click="handleGoRequest">
            开始填写需求
          </a-button>
          <a-button size="large" @click="handleGoResult">
            查看结果页
          </a-button>
        </div>
      </div>

      <div class="hero-panel">
        <div class="hero-panel-header">
          <span class="hero-panel-kicker">System Status</span>
          <a-tag :color="healthTagColor">{{ healthText }}</a-tag>
        </div>

        <div class="status-grid">
          <div class="status-card">
            <span>后端</span>
            <strong>{{ healthState.data?.service || 'Trip API' }}</strong>
          </div>
          <div class="status-card">
            <span>规划器</span>
            <strong>{{ healthState.data?.planner_ready ? 'Ready' : 'Checking' }}</strong>
          </div>
          <div class="status-card">
            <span>兜底 Agent</span>
            <strong>{{ healthState.data?.fallback_ready ? 'Ready' : 'Checking' }}</strong>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'

import { getTripHealth } from '@/apis/tripApi'
import type { HealthResponse } from '@/types'

const router = useRouter()
const healthState = reactive<{
  isLoading: boolean
  data: HealthResponse | null
  isError: boolean
}>({
  isLoading: false,
  data: null,
  isError: false,
})

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

onMounted(() => {
  loadTripHealth()
})

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

function handleGoRequest() {
  router.push('/request')
}

function handleGoResult() {
  router.push('/result')
}
</script>

<style scoped>
.home-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 28px 20px 56px;
}

.hero-section {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  gap: 20px;
}

.hero-copy,
.hero-panel {
  border: 1px solid rgba(255, 255, 255, 0.68);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 20px 50px rgba(31, 41, 55, 0.08);
  backdrop-filter: blur(16px);
}

.hero-copy {
  padding: 42px;
  background:
    linear-gradient(135deg, rgba(15, 118, 110, 0.95), rgba(17, 24, 39, 0.88)),
    linear-gradient(180deg, #0f172a, #134e4a);
  color: #fffaf3;
}

.hero-kicker,
.hero-panel-kicker {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.hero-kicker {
  color: rgba(255, 255, 255, 0.68);
}

.hero-title {
  margin: 14px 0 0;
  font-size: 44px;
  line-height: 1.08;
}

.hero-description {
  max-width: 520px;
  margin: 16px 0 0;
  color: rgba(255, 250, 243, 0.8);
  font-size: 16px;
  line-height: 1.85;
}

.hero-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
}

.hero-panel {
  padding: 24px;
}

.hero-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hero-panel-kicker {
  color: #0f766e;
}

.status-grid {
  display: grid;
  gap: 12px;
  margin-top: 18px;
}

.status-card {
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, #fffefb, #f7f4ee);
}

.status-card span {
  color: #6b7280;
  font-size: 13px;
}

.status-card strong {
  display: block;
  margin-top: 8px;
  color: #13202f;
  font-size: 18px;
}

@media (max-width: 960px) {
  .hero-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .home-page {
    padding: 16px 12px 36px;
  }

  .hero-copy,
  .hero-panel {
    border-radius: 22px;
  }

  .hero-copy {
    padding: 22px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-actions {
    flex-direction: column;
  }
}
</style>
