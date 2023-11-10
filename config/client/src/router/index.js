import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/backup',
    name: 'Backup',
    component: () => import('../views/BackupView.vue')
  },
  {
    path: '/backupConfig',
    name: 'Backup Config',
    component: () => import('../components/gui/BackupConfig.vue')
  },
  {
    path: '/backupSources',
    name: 'Backup Sources',
    component: () => import('../components/gui/BackupSources.vue')
  },
  {
    path: '/other',
    name: 'Other',
    component: () => import('../views/BackupView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
