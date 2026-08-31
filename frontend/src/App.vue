<template>
  <a-layout class="app-layout">
    <a-layout-header class="app-header">
      <div class="app-brand">
        <span class="brand-mark">T</span>
        <div>
          <div class="brand-title">LangChain 智能旅行助手</div>
          <div class="brand-subtitle">Trip Planner Workspace</div>
        </div>
      </div>
    </a-layout-header>

    <a-layout-content class="app-content">
      <router-view />
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(36, 99, 235, 0.14), transparent 30%),
    linear-gradient(180deg, #f8fbff 0%, #f3f7fb 100%);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  height: 72px;
  padding: 0 32px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(14px);
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0f766e 0%, #2563eb 100%);
  color: #ffffff;
  font-size: 20px;
  font-weight: 700;
}

.brand-title {
  color: #0f172a;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
}

.brand-subtitle {
  margin-top: 2px;
  color: #64748b;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.app-content {
  padding: 0;
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 16px;
  }

  .brand-subtitle {
    display: none;
  }
}
</style>
