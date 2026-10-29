<template>
  <div class="friend-list-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>亲友录</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        新增亲友
      </el-button>
    </div>

    <!-- 搜索框 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索亲友姓名..."
        prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
    </div>

    <!-- 朋友列表 -->
    <div class="friend-grid">
      <div v-for="friend in filteredFriends" :key="friend.id" class="friend-card" @click="goToDetail(friend.id)">
        <div class="friend-avatar">
          <el-avatar :size="60" :src="friend.avatar" icon="UserFilled" />
          <el-tag v-if="friend.specialCare" type="danger" size="small" class="special-badge">特别关心</el-tag>
        </div>
        <div class="friend-info">
          <div class="friend-name">{{ friend.name }}</div>
          <div class="friend-meta">
            <span>生日: {{ friend.birthday }}</span>
            <span>认识: {{ friend.knowYears }}年</span>
          </div>
        </div>
        <div class="friend-actions">
          <el-button type="primary" link size="small" @click.stop="goToDetail(friend.id)">查看</el-button>
          <el-button type="primary" link size="small" @click.stop="editFriend(friend)">编辑</el-button>
          <el-button type="danger" link size="small" @click.stop="deleteFriend(friend)">删除</el-button>
        </div>
      </div>

      <!-- 空状态 -->
      <el-empty v-if="filteredFriends.length === 0" description="暂无亲友记录，点击上方按钮添加" />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
      <FriendForm :friend="currentFriend" @submit="handleSubmit" @cancel="dialogVisible = false" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, UserFilled } from '@element-plus/icons-vue'
import { useFriendStore } from '@/stores/friend'
import FriendForm from '@/components/friend/FriendForm.vue'

const router = useRouter()
const friendStore = useFriendStore()

const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增亲友')
const currentFriend = ref(null)

const filteredFriends = computed(() => {
  if (!searchKeyword.value) return friendStore.friends
  return friendStore.friends.filter(f =>
    f.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

const handleSearch = () => {
  // 搜索处理
}

const goToDetail = (id) => {
  router.push(`/friends/${id}`)
}

const openAddDialog = () => {
  dialogTitle.value = '新增亲友'
  currentFriend.value = null
  dialogVisible.value = true
}

const editFriend = (friend) => {
  dialogTitle.value = '编辑亲友'
  currentFriend.value = { ...friend }
  dialogVisible.value = true
}

const deleteFriend = async (friend) => {
  try {
    await ElMessageBox.confirm(`确定删除亲友"${friend.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await friendStore.deleteFriend(friend.id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

const handleSubmit = async (data) => {
  try {
    if (currentFriend.value) {
      await friendStore.updateFriend(currentFriend.value.id, data)
      ElMessage.success('更新成功')
    } else {
      await friendStore.addFriend(data)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
  } catch {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  friendStore.loadFriends()
})
</script>

<style lang="scss" scoped>
.friend-list-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      font-size: 20px;
      font-weight: 500;
      margin: 0;
    }
  }

  .search-bar {
    margin-bottom: 20px;
    max-width: 400px;
  }

  .friend-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;

    .friend-card {
      background: #fff;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
      }

      .friend-avatar {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
        position: relative;

        .special-badge {
          position: absolute;
          top: -4px;
          right: -4px;
        }
      }

      .friend-info {
        text-align: center;
        margin-bottom: 15px;

        .friend-name {
          font-size: 18px;
          font-weight: 500;
          margin-bottom: 8px;
        }

        .friend-meta {
          font-size: 14px;
          color: #909399;
          display: flex;
          justify-content: center;
          gap: 15px;
        }
      }

      .friend-actions {
        display: flex;
        justify-content: center;
        gap: 10px;
      }
    }
  }
}
</style>