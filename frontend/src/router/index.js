import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'friends',
        name: 'FriendList',
        component: () => import('@/views/FriendList.vue'),
        meta: { title: '亲友录' }
      },
      {
        path: 'friends/:id',
        name: 'FriendDetail',
        component: () => import('@/views/FriendDetail.vue'),
        meta: { title: '亲友详情' }
      },
      {
        path: 'notes',
        name: 'Notes',
        component: () => import('@/views/Notes.vue'),
        meta: { title: '便签记录' }
      },
      {
        path: 'chat',
        name: 'Chat',
        component: () => import('@/views/Chat.vue'),
        meta: { title: 'AI助手' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '首页'} - 亲友录信息智能记忆系统`
  next()
})

export default router