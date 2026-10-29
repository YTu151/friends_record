<template>
  <div class="notes-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>便签记录</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        新增便签
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-bar">
      <el-select v-model="selectedFriend" placeholder="选择亲友" clearable @change="handleFilter">
        <el-option label="全部亲友" value="" />
        <el-option v-for="friend in friends" :key="friend.id" :label="friend.name" :value="friend.id" />
      </el-select>
      <el-input v-model="searchKeyword" placeholder="搜索关键词..." clearable style="max-width: 300px; margin-left: 15px" @input="handleSearch" />
    </div>

    <!-- 时间线视图 -->
    <div class="timeline-container">
      <div v-for="group in groupedNotes" :key="group.month" class="timeline-group">
        <div class="timeline-header">{{ group.month }}</div>
        <div class="timeline-items">
          <div v-for="note in group.notes" :key="note.id" class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-time">{{ note.time }}</div>
            <div class="timeline-card">
              <div class="note-content">{{ note.content }}</div>
              <div class="note-meta">
                <el-tag size="small" effect="plain">{{ note.friendName }}</el-tag>
                <div class="note-actions">
                  <el-button type="primary" link size="small" @click="editNote(note)">编辑</el-button>
                  <el-button type="danger" link size="small" @click="deleteNote(note)">删除</el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="filteredNotes.length === 0" description="暂无便签记录" />
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" destroy-on-close>
      <el-form :model="noteForm" label-width="80px">
        <el-form-item label="选择亲友" required>
          <el-select v-model="noteForm.friendId" placeholder="请选择亲友">
            <el-option v-for="friend in friends" :key="friend.id" :label="friend.name" :value="friend.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="便签内容" required>
          <el-input v-model="noteForm.content" type="textarea" :rows="4" placeholder="请输入便签内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNote">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useFriendStore } from '@/stores/friend'
import { useNoteStore } from '@/stores/note'
import dayjs from 'dayjs'

const friendStore = useFriendStore()
const noteStore = useNoteStore()

const friends = ref([])
const notes = ref([])
const selectedFriend = ref('')
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增便签')
const currentNote = ref(null)
const noteForm = ref({ friendId: '', content: '' })

const filteredNotes = computed(() => {
  let result = notes.value
  if (selectedFriend.value) {
    result = result.filter(n => n.friendId === selectedFriend.value)
  }
  if (searchKeyword.value) {
    result = result.filter(n =>
      n.content.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  return result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const groupedNotes = computed(() => {
  const groups = {}
  filteredNotes.value.forEach(note => {
    const month = dayjs(note.createdAt).format('YYYY年MM月')
    if (!groups[month]) {
      groups[month] = { month, notes: [] }
    }
    groups[month].notes.push({
      ...note,
      time: dayjs(note.createdAt).format('MM-DD HH:mm')
    })
  })
  return Object.values(groups)
})

const handleFilter = () => {}
const handleSearch = () => {}

const openAddDialog = () => {
  dialogTitle.value = '新增便签'
  currentNote.value = null
  noteForm.value = { friendId: '', content: '' }
  dialogVisible.value = true
}

const editNote = (note) => {
  dialogTitle.value = '编辑便签'
  currentNote.value = note
  noteForm.value = { friendId: note.friendId, content: note.content }
  dialogVisible.value = true
}

const deleteNote = async (note) => {
  try {
    await ElMessageBox.confirm('确定删除这条便签吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await noteStore.deleteNote(note.id)
    ElMessage.success('删除成功')
    loadNotes()
  } catch {
    // 用户取消
  }
}

const saveNote = async () => {
  if (!noteForm.value.friendId || !noteForm.value.content) {
    ElMessage.warning('请填写完整信息')
    return
  }
  try {
    if (currentNote.value) {
      await noteStore.updateNote(currentNote.value.id, noteForm.value)
      ElMessage.success('更新成功')
    } else {
      await noteStore.addNote(noteForm.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadNotes()
  } catch {
    ElMessage.error('操作失败')
  }
}

const loadFriends = async () => {
  await friendStore.loadFriends()
  friends.value = friendStore.friends
}

const loadNotes = async () => {
  await noteStore.loadNotes()
  notes.value = noteStore.notes.map(n => ({
    ...n,
    friendName: friends.value.find(f => f.id === n.friendId)?.name || '未知'
  }))
}

onMounted(async () => {
  await loadFriends()
  await loadNotes()
})
</script>

<style lang="scss" scoped>
.notes-page {
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

  .filter-bar {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
  }

  .timeline-container {
    .timeline-group {
      margin-bottom: 30px;

      .timeline-header {
        font-size: 16px;
        font-weight: 500;
        color: #606266;
        margin-bottom: 15px;
        padding-left: 20px;
        border-left: 3px solid #409EFF;
      }

      .timeline-items {
        .timeline-item {
          display: flex;
          align-items: flex-start;
          position: relative;
          padding-left: 30px;
          margin-bottom: 20px;

          &:last-child {
            margin-bottom: 0;
          }

          .timeline-dot {
            position: absolute;
            left: 8px;
            top: 5px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #409EFF;
            border: 2px solid #fff;
            box-shadow: 0 0 0 2px #409EFF;
          }

          .timeline-time {
            color: #909399;
            font-size: 12px;
            width: 80px;
          }

          .timeline-card {
            flex: 1;
            background: #fff;
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            margin-left: 15px;

            .note-content {
              color: #303133;
              margin-bottom: 10px;
            }

            .note-meta {
              display: flex;
              justify-content: space-between;
              align-items: center;

              .note-actions {
                display: flex;
                gap: 5px;
              }
            }
          }
        }
      }
    }
  }
}
</style>