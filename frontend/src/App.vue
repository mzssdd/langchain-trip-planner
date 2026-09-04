<template>
  <a-layout class="app-layout">
    <div class="app-backdrop app-backdrop--left"></div>
    <div class="app-backdrop app-backdrop--right"></div>

    <a-layout-header class="app-header">
      <div class="app-shell">
        <div class="app-brand">
          <span class="brand-mark">T</span>
          <div class="brand-copy">
            <div class="brand-title">LangChain 智能旅行助手</div>
          </div>
        </div>

        <div class="app-header-pill">
          <span class="pill-dot"></span>
          <span class="pill-text">AI 行程规划体验</span>
        </div>
      </div>
    </a-layout-header>

    <a-layout-content class="app-content">
      <div class="app-shell app-content-shell">
        <router-view v-slot="{ Component, route }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </transition>
        </router-view>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-layout {
  position: relative;
  min-height: 100vh;
  padding-top: 20px;
  overflow: hidden;
}

.app-backdrop {
  position: fixed;
  z-index: 0;
  pointer-events: none;
  filter: blur(8px);
  opacity: 0.9;
}

.app-backdrop--left {
  top: -120px;
  left: -120px;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.18), transparent 72%);
}

.app-backdrop--right {
  top: 160px;
  right: -140px;
  width: 380px;
  height: 380px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.16), transparent 70%);
}

.app-header {
  position: fixed;
  top: 20px;
  left: 50%;
  z-index: 10;
  width: calc(100% - 40px);
  max-width: 1240px;
  height: 64px;
  transform: translateX(-50%);
  padding: 0;
  border: 1px solid rgba(148, 163, 184, 0.14);
  border-radius: 20px;
  background: rgba(252, 249, 244, 0.82);
  box-shadow: 0 16px 40px rgba(31, 41, 55, 0.12);
  backdrop-filter: blur(18px);
}

.app-shell {
  display: flex;
  width: 100%;
  max-width: 1240px;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 0 auto;
  padding: 0 20px;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.brand-copy {
  min-width: 0;
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 11px;
  background: linear-gradient(135deg, #0f766e 0%, #f59e0b 100%);
  color: #fffaf0;
  font-size: 16px;
  font-weight: 700;
  box-shadow: 0 10px 22px rgba(15, 118, 110, 0.2);
}

.brand-title {
  color: #13202f;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
}

.brand-subtitle {
  margin-top: 1px;
  color: #6b7280;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.app-header-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  margin: 1px;
  padding: 0px 12px;
  border: 1px solid rgba(15, 118, 110, 0.12);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.52);
  color: #0f766e;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.pill-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12);
}

.app-content {
  position: relative;
  z-index: 1;
  padding: 84px 0 0;
}

.app-content-shell {
  display: block;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition:
    opacity 0.24s ease,
    transform 0.24s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 768px) {
  .app-layout {
    padding-top: 12px;
  }

  .app-shell {
    padding: 0 14px;
  }

  .app-header {
    top: 12px;
    width: calc(100% - 24px);
    border-radius: 16px;
  }

  .brand-subtitle {
    display: none;
  }

  .app-header-pill {
    display: none;
  }
}
</style>
