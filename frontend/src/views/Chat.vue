<template>
  <div class="chat-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>AI智能助手</h2>
      <el-button type="danger" plain @click="clearChat">
        <el-icon><Delete /></el-icon>
        清空对话
      </el-button>
    </div>

    <!-- 聊天容器 -->
    <div class="chat-container">
      <!-- 消息列表 -->
      <div class="message-list" ref="messageListRef">
        <ChatMessage
          v-for="message in messages"
          :key="message.id"
          :message="message"
        />
        <div v-if="isTyping" class="typing-indicator">
          <div class="typing-avatar">🤖</div>
          <div class="typing-text">
            <span></span><span></span><span></span>
          </div>
        </div>
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-icon">🤖</div>
          <div class="welcome-text">
            <p>你好！我是你的亲友记忆助手。</p>
            <p>我可以帮你回忆亲友的喜好、提醒生日、查询过往记录。</p>
            <p>试试问我：</p>
            <ul>
              <li @click="sendQuickQuestion('张三喜欢吃什么？')">张三喜欢吃什么？</li>
              <li @click="sendQuickQuestion('下周谁过生日？')">下周谁过生日？</li>
              <li @click="sendQuickQuestion('帮我总结一下李四的信息')">帮我总结一下李四的信息</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <el-input
          v-model="inputMessage"
          placeholder="请输入你的问题..."
          @keyup.enter="sendMessage"
          :disabled="isTyping"
        >
          <template #suffix>
            <el-button type="primary" :icon="isTyping ? '' : 'Position'" @click="sendMessage" :loading="isTyping">
              发送
            </el-button>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { useChatStore } from '@/stores/chat'
import ChatMessage from '@/components/chat/ChatMessage.vue'

const chatStore = useChatStore()

const messages = ref([])
const inputMessage = ref('')
const isTyping = ref(false)
const messageListRef = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isTyping.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  // 添加用户消息
  const userMsg = {
    id: Date.now(),
    role: 'user',
    content: userMessage,
    time: new Date()
  }
  messages.value.push(userMsg)
  scrollToBottom()

  // 模拟AI响应
  isTyping.value = true
  try {
    const response = await chatStore.sendMessage(userMessage)
    const aiMsg = {
      id: Date.now() + 1,
      role: 'assistant',
      content: response,
      time: new Date()
    }
    messages.value.push(aiMsg)
  } catch {
    ElMessage.error('AI服务暂时不可用')
  } finally {
    isTyping.value = false
    scrollToBottom()
  }
}

const sendQuickQuestion = (question) => {
  inputMessage.value = question
  sendMessage()
}

const clearChat = async () => {
  try {
    await ElMessageBox.confirm('确定清空所有对话记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    messages.value = []
    chatStore.clearHistory()
    ElMessage.success('已清空对话')
  } catch {
    // 用户取消
  }
}

const loadHistory = async () => {
  await chatStore.loadHistory()
  messages.value = [...chatStore.history]
  scrollToBottom()
}

onMounted(() => {
  loadHistory()
})
</script>

<style lang="scss" scoped>
.chat-page {
  height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;

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

  .chat-container {
    flex: 1;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    overflow: hidden;

    .message-list {
      flex: 1;
      padding: 20px;
      overflow-y: auto;

      .welcome-message {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        text-align: center;

        .welcome-icon {
          font-size: 48px;
          margin-bottom: 20px;
        }

        .welcome-text {
          color: #606266;

          p {
            margin-bottom: 10px;
          }

          ul {
            list-style: none;
            padding: 0;
            margin-top: 20px;

            li {
              color: #409EFF;
              cursor: pointer;
              margin-bottom: 8px;
              padding: 8px 16px;
              background: #f5f7fa;
              border-radius: 4px;
              transition: background-color 0.2s;

              &:hover {
                background: #e6f0ff;
              }
            }
          }
        }
      }

      .typing-indicator {
        display: flex;
        align-items: center;
        margin-top: 15px;

        .typing-avatar {
          font-size: 32px;
          margin-right: 10px;
        }

        .typing-text {
          display: flex;
          gap: 4px;

          span {
            width: 8px;
            height: 8px;
            background: #909399;
            border-radius: 50%;
            animation: typing 1s infinite;

            &:nth-child(2) {
              animation-delay: 0.2s;
            }

            &:nth-child(3) {
              animation-delay: 0.4s;
            }
          }
        }
      }
    }

    .input-area {
      padding: 20px;
      border-top: 1px solid #e4e7ed;

      .el-input {
        font-size: 14px;
      }
    }
  }
}

@keyframes typing {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 1;
  }
}
</style>