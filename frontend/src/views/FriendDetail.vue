<template>
  <div class="friend-detail-page">
    <!-- 返回和操作 -->
    <div class="page-header">
      <el-button link @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
      <div class="header-actions">
        <el-button type="primary" @click="editFriend">
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
        <el-button type="danger" @click="deleteFriend">
          <el-icon><Delete /></el-icon>
          删除
        </el-button>
      </div>
    </div>

    <!-- 基础信息卡片 -->
    <el-card class="info-card">
      <div class="friend-header">
        <div class="avatar-wrapper" @click="triggerUpload">
          <el-avatar :size="80" :src="friend.avatar" icon="UserFilled" />
          <div class="avatar-overlay">
            <el-icon><Camera /></el-icon>
          </div>
          <input ref="fileInputRef" type="file" accept="image/*" hidden @change="handleAvatarUpload" />
        </div>
        <div class="friend-title">
          <h2>{{ friend.name }}</h2>
          <div class="friend-tags">
            <el-tag v-if="friend.gender">{{ friend.gender }}</el-tag>
            <el-tag type="warning">{{ friend.zodiac }}</el-tag>
            <el-tag v-if="friend.specialCare" type="danger">❤️ 特别关心</el-tag>
          </div>
          <div class="special-care-toggle">
            <el-switch
              v-model="friend.specialCare"
              active-text="特别关心"
              inline-prompt
              @change="handleSpecialCareChange"
            />
          </div>
        </div>
      </div>

      <el-descriptions :column="2" border class="info-descriptions">
        <el-descriptions-item label="性别">{{ friend.gender }}</el-descriptions-item>
        <el-descriptions-item label="生日">
          {{ friend.birthday }}
          <span v-if="friend.lunarBirthday" class="lunar-text">({{ friend.lunarBirthday }})</span>
        </el-descriptions-item>
        <el-descriptions-item label="年龄">{{ friend.age }}岁</el-descriptions-item>
        <el-descriptions-item label="星座">{{ friend.zodiac }}</el-descriptions-item>
        <el-descriptions-item label="身高">{{ friend.height }}cm</el-descriptions-item>
        <el-descriptions-item label="体重">{{ friend.weight }}kg</el-descriptions-item>
        <el-descriptions-item label="认识时间">{{ friend.knowDate }} ({{ friend.knowYears }}年)</el-descriptions-item>
        <el-descriptions-item label="职业">{{ friend.occupation }}</el-descriptions-item>
        <el-descriptions-item label="家乡">{{ friend.hometown }}</el-descriptions-item>
        <el-descriptions-item label="联系方式">{{ friend.phone }}</el-descriptions-item>
      </el-descriptions>

      <div class="remark-section">
        <div class="remark-label">备注</div>
        <div class="remark-content">{{ friend.remark || '暂无备注' }}</div>
      </div>
    </el-card>

    <!-- 喜好卡片 -->
    <el-card class="preference-card">
      <template #header>
        <div class="card-header">
          <span>👍 喜好</span>
          <el-button type="primary" link size="small" @click="addPreference('like')">添加</el-button>
        </div>
      </template>
      <div class="preference-list">
        <PreferenceTag v-for="item in likes" :key="item.id" :item="item" type="like" @delete="deletePreference" @click="editTag(item)" />
        <el-empty v-if="likes.length === 0" description="暂无喜好记录" :image-size="60" />
      </div>
    </el-card>

    <!-- 厌恶卡片 -->
    <el-card class="preference-card">
      <template #header>
        <div class="card-header">
          <span>👎 厌恶</span>
          <el-button type="primary" link size="small" @click="addPreference('dislike')">添加</el-button>
        </div>
      </template>
      <div class="preference-list">
        <PreferenceTag v-for="item in dislikes" :key="item.id" :item="item" type="dislike" @delete="deletePreference" @click="editTag(item)" />
        <el-empty v-if="dislikes.length === 0" description="暂无厌恶记录" :image-size="60" />
      </div>
    </el-card>

    <!-- 便签卡片 -->
    <el-card class="notes-card">
      <template #header>
        <div class="card-header">
          <span>📝 便签记录</span>
          <el-button type="primary" link size="small" @click="goToNotes">查看全部便签</el-button>
        </div>
      </template>
      <div class="notes-preview">
        <div v-for="note in recentNotes" :key="note.id" class="note-item">
          <span class="note-time">{{ note.date }}</span>
          <span class="note-content">{{ note.content }}</span>
        </div>
        <el-empty v-if="recentNotes.length === 0" description="暂无便签记录" :image-size="60" />
      </div>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑亲友" width="600px" destroy-on-close>
      <FriendForm :friend="friend" @submit="handleUpdate" @cancel="editDialogVisible = false" />
    </el-dialog>

    <!-- 添加偏好对话框 -->
    <el-dialog v-model="preferenceDialogVisible" :title="preferenceDialogTitle" width="400px">
      <el-form :model="preferenceForm" label-width="60px">
        <el-form-item label="内容">
          <el-input v-model="preferenceForm.content" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="preferenceForm.tag" placeholder="选择标签" clearable style="width: 100%">
            <el-option v-for="t in tagOptions" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="preferenceDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePreference">确定</el-button>
      </template>
    </el-dialog>

    <!-- 编辑标签对话框 -->
    <el-dialog v-model="editTagDialogVisible" title="修改标签" width="400px">
      <el-form label-width="60px">
        <el-form-item label="内容">
          <el-input :model-value="editingPreference?.content" disabled />
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="editTagForm.tag" placeholder="选择标签" clearable style="width: 100%">
            <el-option v-for="t in tagOptions" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editTagDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTag">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Edit, Delete, UserFilled, Camera } from '@element-plus/icons-vue'
import { useFriendStore } from '@/stores/friend'
import FriendForm from '@/components/friend/FriendForm.vue'
import PreferenceTag from '@/components/preference/PreferenceTag.vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

const router = useRouter()
const route = useRoute()
const friendStore = useFriendStore()

const friendId = route.params.id
const friend = ref({})
const likes = ref([])
const dislikes = ref([])
const recentNotes = ref([])
const fileInputRef = ref(null)

const tagOptions = ['食物', '水果', '蔬菜', '饮品', '零食', '颜色', '运动', '音乐', '明星', '动物', '技能', '电影', '游戏', '服装', '娱乐']

const editDialogVisible = ref(false)
const preferenceDialogVisible = ref(false)
const preferenceType = ref('like')
const preferenceForm = ref({ content: '', tag: '' })

const editTagDialogVisible = ref(false)
const editingPreference = ref(null)
const editTagForm = ref({ tag: '' })

const preferenceDialogTitle = computed(() =>
  preferenceType.value === 'like' ? '添加喜好' : '添加厌恶'
)

const goBack = () => {
  router.push('/friends')
}

const goToNotes = () => {
  router.push('/notes')
}

const editFriend = () => {
  editDialogVisible.value = true
}

const deleteFriend = async () => {
  try {
    await ElMessageBox.confirm(`确定删除亲友"${friend.value.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await friendStore.deleteFriend(friendId)
    ElMessage.success('删除成功')
    router.push('/friends')
  } catch {
    // 用户取消
  }
}

const handleUpdate = async (data) => {
  try {
    await friendStore.updateFriend(friendId, data)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadFriendDetail()
  } catch {
    ElMessage.error('更新失败')
  }
}

const addPreference = (type) => {
  preferenceType.value = type
  preferenceForm.value = { content: '', tag: '' }
  preferenceDialogVisible.value = true
}

const savePreference = async () => {
  if (!preferenceForm.value.content) {
    ElMessage.warning('请输入内容')
    return
  }
  try {
    await friendStore.addPreference(friendId, {
      type: preferenceType.value,
      content: preferenceForm.value.content,
      tag: preferenceForm.value.tag
    })
    ElMessage.success('添加成功')
    preferenceDialogVisible.value = false
    loadFriendDetail()
  } catch {
    ElMessage.error('添加失败')
  }
}

const deletePreference = async (itemId) => {
  try {
    await friendStore.deletePreference(friendId, itemId)
    ElMessage.success('删除成功')
    loadFriendDetail()
  } catch {
    ElMessage.error('删除失败')
  }
}

const editTag = (item) => {
  editingPreference.value = item
  editTagForm.value = { tag: item.tag || '' }
  editTagDialogVisible.value = true
}

const saveTag = async () => {
  if (!editingPreference.value) return
  try {
    await friendStore.updatePreferenceTag(friendId, editingPreference.value.id, editTagForm.value.tag)
    ElMessage.success('标签修改成功')
    editTagDialogVisible.value = false
    loadFriendDetail()
  } catch {
    ElMessage.error('标签修改失败')
  }
}

const loadFriendDetail = async () => {
  const data = await friendStore.getFriendById(friendId)
  if (data) {
    friend.value = data
    likes.value = data.preferences?.filter(p => p.type === 'like') || []
    dislikes.value = data.preferences?.filter(p => p.type === 'dislike') || []
    recentNotes.value = data.notes?.slice(0, 3) || []
  }
}

const handleSpecialCareChange = async (value) => {
  await friendStore.toggleSpecialCare(friendId)
}

const triggerUpload = () => {
  fileInputRef.value?.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await axios.post(`${API_BASE_URL}/files/upload`, formData)
    const url = res.data.url
    await axios.put(`${API_BASE_URL}/friends/${friendId}/avatar`, { avatar: url })
    friend.value.avatar = url
    ElMessage.success('头像上传成功')
  } catch (e) {
    ElMessage.error('头像上传失败')
  }
  event.target.value = ''
}

onMounted(() => {
  loadFriendDetail()
})
</script>

<style lang="scss" scoped>
.friend-detail-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .info-card {
    margin-bottom: 20px;

    .friend-header {
      display: flex;
      align-items: center;
      margin-bottom: 20px;

      .avatar-wrapper {
        position: relative;
        cursor: pointer;
        border-radius: 50%;
        overflow: hidden;

        &:hover .avatar-overlay {
          opacity: 1;
        }

        .avatar-overlay {
          position: absolute;
          inset: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          opacity: 0;
          transition: opacity 0.2s;
          color: #fff;
          font-size: 20px;
          border-radius: 50%;
        }
      }

      .friend-title {
        margin-left: 20px;

        h2 {
          margin: 0 0 10px 0;
          font-size: 24px;
        }

        .friend-tags {
          display: flex;
          gap: 8px;
          margin-bottom: 8px;
        }

        .special-care-toggle {
          display: flex;
          align-items: center;
        }
      }
    }

    .info-descriptions {
      margin-bottom: 20px;
    }

    .lunar-text {
      color: #909399;
      font-size: 12px;
    }

    .remark-section {
      padding: 15px;
      background: #f5f7fa;
      border-radius: 4px;

      .remark-label {
        font-weight: 500;
        margin-bottom: 8px;
      }

      .remark-content {
        color: #606266;
      }
    }
  }

  .preference-card, .notes-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 16px;
      font-weight: 500;
    }

    .preference-list {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
  }

  .notes-preview {
    .note-item {
      padding: 12px 0;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }

      .note-time {
        color: #909399;
        font-size: 12px;
        margin-right: 15px;
      }

      .note-content {
        color: #606266;
      }
    }
  }
}
</style>