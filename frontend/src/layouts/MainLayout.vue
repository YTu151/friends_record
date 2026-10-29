<template>
  <el-container class="main-layout">
    <!-- 侧边栏 -->
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <span class="logo-icon">👨‍👩‍👧‍👦</span>
        <span class="logo-text">亲友录信息系统</span>
      </div>
      <el-menu
        :default-active="currentRoute"
        class="sidebar-menu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/friends">
          <el-icon><User /></el-icon>
          <span>亲友录</span>
        </el-menu-item>
        <el-menu-item index="/notes">
          <el-icon><Document /></el-icon>
          <span>便签记录</span>
        </el-menu-item>
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>AI助手</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-title">{{ pageTitle }}</div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-avatar">
              <el-avatar :size="32" icon="UserFilled" />
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人设置</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, User, Document, ChatDotRound, UserFilled } from '@element-plus/icons-vue'

const route = useRoute()

const currentRoute = computed(() => route.path)
const pageTitle = computed(() => route.meta.title || '首页')
</script>

<style lang="scss" scoped>
.main-layout {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  overflow: hidden;

  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 15px;
    border-bottom: 1px solid #263445;

    .logo-icon {
      font-size: 24px;
      margin-right: 8px;
    }

    .logo-text {
      font-size: 16px;
      color: #fff;
      font-weight: 500;
    }
  }

  .sidebar-menu {
    border-right: none;
    height: calc(100vh - 60px);
  }
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;

  .header-title {
    font-size: 18px;
    font-weight: 500;
    color: #303133;
  }

  .header-right {
    .user-avatar {
      cursor: pointer;
    }
  }
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>