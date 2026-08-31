import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage/index.vue'),
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('@/views/ResultPage/index.vue'),
    },
  ],
})

export default router
