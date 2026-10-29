<template>
  <div class="home-page">
    <!-- 统计卡片 -->
    <div class="stats-row">
      <el-card class="stat-card">
        <div class="stat-icon friends-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.friendsCount }}</div>
          <div class="stat-label">亲友总数</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon recent-icon">📅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.recentRecords }}</div>
          <div class="stat-label">最近记录</div>
        </div>
      </el-card>
    </div>

    <!-- 双列布局 -->
    <div class="content-row">
      <!-- 特别关心 -->
      <el-card class="special-card">
        <template #header>
          <div class="card-header">
            <span>❤️ 特别关心</span>
            <el-button type="primary" link @click="showAddSpecialDialog = true">添加</el-button>
          </div>
        </template>
        <div class="special-list">
          <div v-for="friend in specialCareFriends" :key="friend.id" class="special-item" @click="goToFriend(friend.id)">
            <el-avatar :size="40" :src="friend.avatar" icon="UserFilled" />
            <div class="special-info">
              <div class="special-name">{{ friend.name }}</div>
              <div class="special-time">{{ friend.addedTime }}</div>
            </div>
            <el-button text circle @click.stop="removeSpecialCare(friend.id)">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          <el-empty v-if="specialCareFriends.length === 0" description="暂无特别关心" :image-size="80" />
        </div>
      </el-card>

      <!-- 最近添加的朋友 -->
      <el-card class="recent-card">
        <template #header>
          <div class="card-header">
            <span>👤 最近添加的亲友</span>
            <el-button type="primary" link @click="goToFriends">查看全部</el-button>
          </div>
        </template>
        <div class="recent-list">
          <div v-for="friend in recentFriends" :key="friend.id" class="recent-item" @click="goToFriend(friend.id)">
            <el-avatar :size="40" :src="friend.avatar" icon="UserFilled" />
            <div class="recent-info">
              <div class="recent-name">{{ friend.name }}</div>
              <div class="recent-time">{{ friend.addedTime }}</div>
            </div>
          </div>
          <el-empty v-if="recentFriends.length === 0" description="暂无亲友记录" :image-size="80" />
        </div>
      </el-card>
    </div>

    <!-- 添加特别关心对话框 -->
    <el-dialog v-model="showAddSpecialDialog" title="添加特别关心" width="400px">
      <div class="add-special-list">
        <div
          v-for="friend in availableFriends"
          :key="friend.id"
          class="add-special-item"
          :class="{ selected: selectedSpecialIds.includes(friend.id) }"
          @click="toggleSelect(friend.id)"
        >
          <el-avatar :size="36" :src="friend.avatar" icon="UserFilled" />
          <span class="add-special-name">{{ friend.name }}</span>
          <el-checkbox :checked="selectedSpecialIds.includes(friend.id)" @click.stop="toggleSelect(friend.id)" />
        </div>
        <el-empty v-if="availableFriends.length === 0" description="所有亲友已在特别关心列表中" :image-size="60" />
      </div>
      <template #footer>
        <el-button @click="showAddSpecialDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmAddSpecial">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFriendStore } from '@/stores/friend'
import { UserFilled, Close } from '@element-plus/icons-vue'

const router = useRouter()
const friendStore = useFriendStore()

// 统计数据
const stats = ref({
  friendsCount: 0,
  recentRecords: 0
})

// 最近添加的朋友
const recentFriends = ref([])

// 特别关心
const specialCareFriends = computed(() => friendStore.specialCareFriends)

// 添加特别关心对话框
const showAddSpecialDialog = ref(false)
const selectedSpecialIds = ref([])

const goToFriends = () => {
  router.push('/friends')
}

const goToFriend = (id) => {
  router.push(`/friends/${id}`)
}

// 可添加为特别关心的朋友（未勾选的）
const availableFriends = computed(() => {
  const specialIds = new Set(specialCareFriends.value.map(f => f.id))
  return friendStore.friends
    .filter(f => !specialIds.has(f.id))
    .map(f => ({ id: f.id, name: f.name, avatar: f.avatar }))
})

const toggleSelect = (id) => {
  const idx = selectedSpecialIds.value.indexOf(id)
  if (idx === -1) {
    selectedSpecialIds.value.push(id)
  } else {
    selectedSpecialIds.value.splice(idx, 1)
  }
}

const removeSpecialCare = async (id) => {
  await friendStore.toggleSpecialCare(id)
}

const confirmAddSpecial = async () => {
  for (const id of selectedSpecialIds.value) {
    await friendStore.toggleSpecialCare(id)
  }
  selectedSpecialIds.value = []
  showAddSpecialDialog.value = false
}

onMounted(async () => {
  await friendStore.loadFriends()

  stats.value = friendStore.getStats
  recentFriends.value = friendStore.getRecentFriends
})
</script>

<style lang="scss" scoped>
.home-page {
  .stats-row {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;

    .stat-card {
      flex: 1;
      display: flex;
      align-items: center;
      padding: 10px 20px;

      .stat-icon {
        font-size: 36px;
        margin-right: 15px;
      }

      .stat-info {
        .stat-value {
          font-size: 28px;
          font-weight: 600;
          color: #303133;
        }

        .stat-label {
          font-size: 14px;
          color: #909399;
          margin-top: 5px;
        }
      }
    }
  }

  .content-row {
    display: flex;
    gap: 20px;

    .special-card, .recent-card {
      flex: 1;
      min-height: 300px;

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 16px;
        font-weight: 500;
      }
    }

    .special-list, .recent-list {
      .special-item, .recent-item {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;
        cursor: pointer;
        transition: background-color 0.2s;

        &:hover {
          background-color: #f5f7fa;
        }

        &:last-child {
          border-bottom: none;
        }

        .special-info, .recent-info {
          margin-left: 15px;
          flex: 1;

          .special-name, .recent-name {
            font-weight: 500;
          }

          .special-time, .recent-time {
            font-size: 12px;
            color: #909399;
            margin-top: 4px;
          }
        }
      }

      .recent-item {
        cursor: pointer;
        transition: background-color 0.2s;

        &:hover {
          background-color: #f5f7fa;
        }
      }
    }
  }

  .add-special-list {
    max-height: 400px;
    overflow-y: auto;

    .add-special-item {
      display: flex;
      align-items: center;
      padding: 10px 12px;
      border-radius: 6px;
      cursor: pointer;
      transition: background-color 0.2s;

      &:hover {
        background-color: #f5f7fa;
      }

      &.selected {
        background-color: #ecf5ff;
      }

      .add-special-name {
        flex: 1;
        margin: 0 12px;
        font-size: 14px;
      }
    }
  }
}
</style>
