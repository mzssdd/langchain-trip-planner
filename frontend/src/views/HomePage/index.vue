<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-copy">
        <div class="hero-copy-top">
          <div class="hero-kicker"><span class="live-dot"></span> AI 行程工作台</div>
          <span class="hero-index">01 / 04</span>
        </div>
        <div class="hero-route-art" aria-hidden="true">
          <span class="route-line"></span>
          <span class="route-node route-node--start"></span>
          <span class="route-node route-node--mid"></span>
          <span class="route-node route-node--end"></span>
          <span class="route-label route-label--start">出发</span>
          <span class="route-label route-label--end">目的地</span>
        </div>
        <h1 class="hero-title">把下一段旅程，<br /><em>交给路线。</em></h1>
        <p class="hero-description">
          告诉我你想去哪里、和谁出发，以及希望怎样抵达。我们把零散想法整理成一份可以直接出发的行程。
        </p>

        <div class="hero-actions">
          <a-button type="primary" size="large" @click="handleGoRequest">
            开始规划行程 <span class="button-arrow">↗</span>
          </a-button>
          <a-button size="large" @click="handleGoResult">查看已有行程</a-button>
        </div>
        <div class="hero-footnote"><span>⌁</span> 通常 30 秒内完成第一版路线</div>
      </div>

      <div class="hero-panel">
        <div class="hero-panel-header">
          <div>
            <div class="hero-panel-kicker">Planning system</div>
            <h2>出发前，先确认三件事</h2>
          </div>
          <a-tag :color="healthTagColor">{{ healthText }}</a-tag>
        </div>

        <div class="status-grid">
          <div class="status-card">
            <span class="status-number">01</span>
            <div><strong>目的地与日期</strong><small>从一个城市开始</small></div>
            <span class="status-check">→</span>
          </div>
          <div class="status-card">
            <span class="status-number">02</span>
            <div><strong>同行人与预算</strong><small>让路线贴合你的节奏</small></div>
            <span class="status-check">→</span>
          </div>
          <div class="status-card">
            <span class="status-number">03</span>
            <div><strong>偏好与风格</strong><small>把“想去”变成“会去”</small></div>
            <span class="status-check">→</span>
          </div>
        </div>
        <div class="system-strip"><span class="strip-dot"></span><span>规划服务</span><strong>{{ healthState.data?.planner_ready ? '运行正常' : '正在检查' }}</strong></div>
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

/* Route-led homepage */
.home-page { max-width: 1180px; padding: 42px 20px 64px; }
.hero-section { grid-template-columns: minmax(0, 1.18fr) minmax(340px, .82fr); gap: 18px; align-items: stretch; }
.hero-copy { position: relative; min-height: 560px; overflow: hidden; border: 0; border-radius: 24px; padding: 34px 38px; background: var(--ink); box-shadow: var(--shadow-md); }
.hero-copy::before { content: ''; position: absolute; inset: 0; opacity: .14; background: repeating-linear-gradient(0deg, transparent 0 35px, rgba(255,255,255,.22) 36px), repeating-linear-gradient(90deg, transparent 0 35px, rgba(255,255,255,.22) 36px); mask-image: linear-gradient(135deg, transparent 25%, #000 75%); }
.hero-copy::after { content: ''; position: absolute; width: 420px; height: 420px; right: -170px; bottom: -210px; border: 1px solid rgba(242,107,56,.55); border-radius: 50%; box-shadow: 0 0 0 36px rgba(242,107,56,.08), 0 0 0 72px rgba(242,107,56,.04); }
.hero-copy > * { position: relative; z-index: 1; }
.hero-copy-top, .hero-panel-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; }
.hero-kicker { display: flex; align-items: center; gap: 8px; color: var(--signal); font-size: 11px; letter-spacing: .12em; }
.live-dot, .strip-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--signal); box-shadow: 0 0 0 4px rgba(242,107,56,.15); }
.hero-index { color: rgba(255,255,255,.42); font-size: 11px; letter-spacing: .08em; }
.hero-route-art { position: relative; height: 92px; margin: 30px 0 12px; }
.route-line { position: absolute; top: 44px; left: 4%; width: 82%; height: 1px; background: linear-gradient(90deg, var(--signal), rgba(255,255,255,.24)); transform: rotate(-7deg); transform-origin: left; }
.route-node { position: absolute; width: 12px; height: 12px; border: 3px solid var(--ink); border-radius: 50%; background: var(--signal); box-shadow: 0 0 0 1px var(--signal); }
.route-node--start { top: 55px; left: 3%; }.route-node--mid { top: 30px; left: 46%; background: var(--tide); box-shadow: 0 0 0 1px var(--tide); }.route-node--end { top: 3px; right: 11%; }
.route-label { position: absolute; color: rgba(255,255,255,.52); font-size: 10px; }.route-label--start { top: 74px; left: 0; }.route-label--end { top: 22px; right: 4%; }
.hero-title { max-width: 580px; margin: 0; font-size: clamp(42px, 5.5vw, 68px); line-height: 1.03; letter-spacing: -.065em; }
.hero-title em { color: var(--signal); font-style: normal; }
.hero-description { max-width: 500px; margin-top: 22px; color: rgba(255,255,255,.7); font-size: 15px; line-height: 1.8; }
.hero-actions { margin-top: 30px; }.hero-actions .ant-btn-primary { min-width: 190px; }.button-arrow { margin-left: 10px; font-size: 18px; }.hero-actions .ant-btn-default { border-color: rgba(255,255,255,.26); background: transparent; color: #fff; }.hero-actions .ant-btn-default:hover { border-color: var(--signal); color: var(--signal); }
.hero-footnote { margin-top: 22px; color: rgba(255,255,255,.42); font-size: 11px; }.hero-footnote span { margin-right: 7px; color: var(--signal); font-size: 16px; }
.hero-panel { align-self: end; min-height: 430px; padding: 28px; border: 1px solid var(--mist); border-radius: 24px; background: var(--surface); box-shadow: var(--shadow-sm); }
.hero-panel-kicker { color: var(--tide); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; }.hero-panel h2 { margin: 9px 0 0; color: var(--ink); font-size: 22px; letter-spacing: -.035em; line-height: 1.25; }.status-grid { gap: 0; margin-top: 30px; }.status-card { display: grid; grid-template-columns: 32px 1fr 20px; align-items: center; gap: 10px; min-height: 78px; padding: 15px 0; border-bottom: 1px solid var(--mist); border-radius: 0; background: transparent; }.status-number { color: var(--signal); font-size: 11px; font-weight: 750; }.status-card strong { margin: 0; color: var(--ink); font-size: 14px; }.status-card small { display: block; margin-top: 4px; color: var(--muted); font-size: 11px; }.status-check { color: var(--tide); font-size: 18px; }.system-strip { display: flex; align-items: center; gap: 9px; margin-top: 24px; color: var(--muted); font-size: 11px; }.system-strip strong { margin-left: auto; color: var(--success); font-weight: 700; }
@media (max-width: 960px) { .hero-copy { min-height: 500px; } }
@media (max-width: 768px) { .home-page { padding: 20px 12px 40px; }.hero-copy { min-height: 540px; padding: 25px 22px; border-radius: 20px; }.hero-title { font-size: 43px; }.hero-panel { min-height: 0; padding: 22px; border-radius: 20px; }.hero-actions { flex-direction: column; }.hero-actions .ant-btn { width: 100%; } }
</style>
