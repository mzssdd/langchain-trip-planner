<template>
  <div class="process-page">
    <div class="page-toolbar">
      <a-button size="large" @click="handleBackRequest">
        返回填写页
      </a-button>
      <a-tag :color="taskStatusColor">{{ taskStatusText }}</a-tag>
    </div>

    <a-card :bordered="false" class="process-card">
      <div class="process-header">
        <div>
          <div class="process-kicker">Generation Process</div>
          <h1 class="process-title">生成过程</h1>
        </div>
        <div class="process-badge">实时轮询 · 阶段展示</div>
      </div>

      <div class="status-panel">
        <div class="status-row">
          <span class="status-label">状态</span>
          <span class="status-value">{{ taskStatusText }}</span>
        </div>
        <div class="status-row">
          <span class="status-label">任务 ID</span>
          <span class="status-value">{{ taskId || '未获取' }}</span>
        </div>
        <div class="status-row">
          <span class="status-label">说明</span>
          <span class="status-value">{{ taskMessage || '等待任务结果' }}</span>
        </div>
      </div>

      <div class="timeline-panel">
        <div class="timeline-title">生成过程</div>
        <div v-if="historyList.length" class="timeline-list">
          <div
            v-for="(item, index) in historyList"
            :key="`${index}-${item.status}-${item.message}`"
            class="timeline-item"
          >
            <span class="timeline-dot"></span>
            <div class="timeline-content">
              <div class="timeline-status">{{ getHistoryStatusLabel(item.status) }}</div>
              <div class="timeline-message">{{ item.message }}</div>
            </div>
          </div>
        </div>
        <a-empty v-else description="正在等待过程信息" />
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getTripPlanTask } from '@/apis/tripApi'
import { TRIP_PLAN_STORAGE_KEY, TRIP_TASK_ID_STORAGE_KEY } from '@/utils/common'
import type { TripTaskStatusResponse } from '@/types'

const router = useRouter()
const taskId = ref('')
const taskMessage = ref('正在等待任务开始')
const taskStatus = ref<'pending' | 'running' | 'success' | 'failed' | ''>('')
const historyList = ref<
  Array<{
    status: 'pending' | 'running' | 'success' | 'failed'
    message: string
  }>
>([])
let taskTimer: number | null = null

const taskStatusText = computed(() => {
  const statusMap: Record<string, string> = {
    pending: '等待中',
    running: '正在生成',
    success: '生成完成',
    failed: '生成失败',
  }

  return statusMap[taskStatus.value] || '未开始'
})

const taskStatusColor = computed(() => {
  if (taskStatus.value === 'success') {
    return 'success'
  }

  if (taskStatus.value === 'failed') {
    return 'error'
  }

  return 'processing'
})

onMounted(() => {
  taskId.value = sessionStorage.getItem(TRIP_TASK_ID_STORAGE_KEY) || ''

  if (!taskId.value) {
    router.replace('/request')
    return
  }

  taskStatus.value = 'pending'
  historyList.value = [
    {
      status: 'pending',
      message: '任务已创建，等待执行',
    },
  ]

  loadTaskStatus()
})

onBeforeUnmount(() => {
  clearTaskTimer()
})

async function loadTaskStatus() {
  try {
    const response = await getTripPlanTask(taskId.value)
    updateTaskStatus(response)

    if (response.status === 'success' && response.data) {
      sessionStorage.setItem(TRIP_PLAN_STORAGE_KEY, JSON.stringify(response.data))
      clearTaskTimer()
      router.replace('/result')
      return
    }

    if (response.status === 'failed') {
      clearTaskTimer()
      return
    }

    taskTimer = window.setTimeout(loadTaskStatus, 3000)
  } catch (error) {
    taskMessage.value = '查询任务状态失败，正在重试'
    taskTimer = window.setTimeout(loadTaskStatus, 3000)
  }
}

function updateTaskStatus(response: TripTaskStatusResponse) {
  taskStatus.value = response.status
  taskMessage.value = response.message
  historyList.value = response.history || []
}

function handleBackRequest() {
  clearTaskTimer()
  router.push('/request')
}

function clearTaskTimer() {
  if (taskTimer !== null) {
    window.clearTimeout(taskTimer)
    taskTimer = null
  }
}

function getHistoryStatusLabel(status: 'pending' | 'running' | 'success' | 'failed') {
  const statusMap = {
    pending: '等待中',
    running: '执行中',
    success: '已完成',
    failed: '失败',
  }

  return statusMap[status]
}
</script>

<style scoped>
.process-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 28px 20px 56px;
}

.page-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.process-card {
  padding: 28px;
  border: 1px solid rgba(255, 255, 255, 0.68);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 20px 50px rgba(31, 41, 55, 0.08);
  backdrop-filter: blur(16px);
}

.process-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.process-kicker {
  color: #0f766e;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.process-title {
  margin: 8px 0 0;
  color: #13202f;
  font-size: 28px;
}

.process-badge {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(245, 158, 11, 0.12);
  color: #9a6200;
  font-size: 13px;
  font-weight: 600;
}

.status-panel {
  padding: 18px 20px;
  border-radius: 20px;
  background: rgba(15, 118, 110, 0.06);
}

.status-row {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
}

.status-row:last-child {
  margin-bottom: 0;
}

.status-label {
  min-width: 64px;
  color: #6b7280;
  font-weight: 600;
}

.status-value {
  color: #13202f;
  line-height: 1.7;
  word-break: break-all;
}

.timeline-panel {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px solid rgba(148, 163, 184, 0.18);
}

.timeline-title {
  margin-bottom: 14px;
  color: #13202f;
  font-size: 18px;
  font-weight: 700;
}

.timeline-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.timeline-item {
  position: relative;
  display: flex;
  gap: 12px;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  margin-top: 5px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0f766e 0%, #f59e0b 100%);
  box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.08);
  flex-shrink: 0;
}

.timeline-content {
  min-width: 0;
}

.timeline-status {
  color: #0f766e;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.timeline-message {
  margin-top: 4px;
  color: #334155;
  line-height: 1.7;
}

@media (max-width: 768px) {
  .process-page {
    padding: 16px 12px 36px;
  }

  .process-card {
    padding: 22px;
    border-radius: 22px;
  }

  .process-header {
    flex-direction: column;
  }
}
</style>
