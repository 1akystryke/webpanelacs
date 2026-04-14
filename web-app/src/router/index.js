import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SessionView from '@/views/SessionView.vue'

import PlayersView from '@/views/PlayersView.vue'
import ContentView from '@/views/ContentView.vue'
import PresetsView from '@/views/PresetsView.vue'
import LogsView from '@/views/LogsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/session',
    name: "session",
    component: SessionView
  },
  {
    path: '/players',
    name: "players",
    component: PlayersView
  },
  {
    path: '/content',
    name: "content",
    component: ContentView
  },
  {
    path: '/presets',
    name: "presets",
    component: PresetsView
  },
  {
    path: '/logs',
    name: "logs",
    component: LogsView
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
