<template>
  <a-layout class="app-layout">
    <div class="app-backdrop app-backdrop--left"></div>
    <div class="app-backdrop app-backdrop--right"></div>

    <a-layout-header class="app-header">
      <div class="app-shell">
        <div class="app-brand">
          <span class="brand-mark"><i></i><i></i><i></i></span>
          <div class="brand-copy">
            <div class="brand-title">Tripline</div>
            <div class="brand-subtitle">智能旅行规划</div>
          </div>
        </div>

        <div class="app-header-context">
          <span class="context-line"></span>
          <span>从想法到可执行路线</span>
        </div>

        <div class="app-header-pill">
          <span class="pill-dot"></span>
          <span class="pill-text">规划服务在线</span>
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
  padding-top: 16px;
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
  top: -160px;
  left: -100px;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(242, 107, 56, 0.14), transparent 72%);
}

.app-backdrop--right {
  top: 180px;
  right: -180px;
  width: 360px;
  height: 360px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(23, 107, 135, 0.12), transparent 70%);
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100%;
  height: 72px;
  padding: 0;
  border-bottom: 1px solid var(--mist);
  background: rgba(245, 247, 244, 0.94);
  box-shadow: 0 2px 16px rgba(16, 42, 67, 0.04);
  backdrop-filter: blur(14px);
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
  position: relative;
  width: 34px;
  height: 34px;
  border: 2px solid var(--signal);
  border-radius: 50%;
  background: var(--ink);
  box-shadow: 4px 4px 0 rgba(242, 107, 56, 0.18);
}

.brand-mark i {
  position: absolute;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--signal);
}

.brand-mark i:nth-child(1) { top: 7px; left: 8px; }
.brand-mark i:nth-child(2) { top: 15px; left: 18px; }
.brand-mark i:nth-child(3) { top: 22px; left: 9px; }

.brand-title {
  color: var(--ink);
  font-size: 16px;
  font-weight: 750;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.brand-title span {
  color: var(--slate);
  font-weight: 600;
}

.brand-subtitle {
  margin-top: 3px;
  color: var(--muted);
  font-size: 10px;
  letter-spacing: 0.08em;
}

.app-header-context {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
  margin-right: 24px;
  color: var(--muted);
  font-size: 12px;
}

.context-line {
  display: inline-block;
  width: 28px;
  height: 1px;
  background: var(--signal);
}

.app-header-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  margin: 1px;
  padding: 0px 12px;
  border: 1px solid rgba(23, 107, 135, 0.18);
  border-radius: 999px;
  background: var(--surface-muted);
  color: var(--tide);
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
  padding: 96px 0 0;
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
    padding-top: 0;
  }

  .app-shell {
    padding: 0 18px;
  }

  .app-header {
    top: 0;
    height: 64px;
  }

  .app-content {
    padding-top: 82px;
  }

  .app-header-context {
    display: none;
  }

  .brand-subtitle {
    display: none;
  }

  .app-header-pill {
    display: none;
  }
}
</style>
