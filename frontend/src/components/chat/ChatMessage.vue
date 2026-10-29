<template>
  <div class="chat-message" :class="{ 'is-user': isUser }">
    <div class="message-avatar">
      <el-avatar v-if="isUser" :size="40" icon="UserFilled" />
      <div v-else class="ai-avatar">🤖</div>
    </div>
    <div class="message-content">
      <div class="message-bubble">
        <div class="message-text">{{ message.content }}</div>
      </div>
      <div class="message-time">{{ formatTime(message.time) }}</div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const isUser = props.message.role === 'user'

const formatTime = (time) => {
  if (!time) return ''
  return dayjs(time).format('HH:mm')
}
</script>

<style scoped>
.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  max-width: 80%;
}

.chat-message.is-user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.message-avatar {
  margin-right: 12px;
}

.chat-message.is-user .message-avatar {
  margin-right: 0;
  margin-left: 12px;
}

.ai-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.message-content {
  display: flex;
  flex-direction: column;
}

.chat-message.is-user .message-content {
  align-items: flex-end;
}

.message-bubble {
  background: #f5f7fa;
  padding: 12px 16px;
  border-radius: 12px;
  border-top-left-radius: 4px;
  max-width: 100%;
  word-break: break-word;
}

.chat-message.is-user .message-bubble {
  background: #409EFF;
  color: #fff;
  border-top-left-radius: 12px;
  border-top-right-radius: 4px;
}

.message-text {
  line-height: 1.6;
  white-space: pre-wrap;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
}

.chat-message.is-user .message-time {
  text-align: right;
}
</style>
