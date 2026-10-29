import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'
const AI_SERVICE_URL = import.meta.env.VITE_AI_URL || 'http://localhost:8000'

export const useChatStore = defineStore('chat', () => {
  // State
  const history = ref([])
  const sessionId = ref(localStorage.getItem('chat_session_id') || generateSessionId())
  const loading = ref(false)

  // 生成会话ID
  function generateSessionId() {
    const id = 'session_' + Date.now()
    localStorage.setItem('chat_session_id', id)
    return id
  }

  // Actions
  const loadHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/history`, {
        params: { sessionId: sessionId.value }
      })
      history.value = response.data.map(h => ({
        id: h.id,
        role: h.role,
        content: h.content,
        time: new Date(h.createdAt)
      }))
    } catch (error) {
      console.error('加载对话历史失败:', error)
      // 从localStorage加载
      const saved = localStorage.getItem(`chat_history_${sessionId.value}`)
      if (saved) {
        history.value = JSON.parse(saved)
      }
    }
  }

  const sendMessage = async (message) => {
    loading.value = true
    try {
      // 首先调用SpringBoot后端，后端转发给Python AI服务
      const response = await axios.post(`${API_BASE_URL}/chat/send`, {
        sessionId: sessionId.value,
        message: message
      })

      const aiResponse = response.data.response

      // 保存到本地历史
      const userMsg = {
        id: Date.now(),
        role: 'user',
        content: message,
        time: new Date()
      }
      const aiMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: aiResponse,
        time: new Date()
      }

      history.value.push(userMsg, aiMsg)
      saveHistory()

      return aiResponse
    } catch (error) {
      console.error('发送消息失败:', error)
      // 返回模拟响应
      return getMockResponse(message)
    } finally {
      loading.value = false
    }
  }

  const saveHistory = () => {
    localStorage.setItem(`chat_history_${sessionId.value}`, JSON.stringify(history.value))
  }

  const clearHistory = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/chat/history`, {
        params: { sessionId: sessionId.value }
      })
    } catch (error) {
      console.error('清空历史失败:', error)
    }
    history.value = []
    localStorage.removeItem(`chat_history_${sessionId.value}`)
    // 生成新会话ID
    sessionId.value = generateSessionId()
  }

  const getMockResponse = (message) => {
    const lowerMsg = message.toLowerCase()

    if (lowerMsg.includes('生日') || lowerMsg.includes('什么时候')) {
      return '根据记录，张三的生日是6月15日，李四是8月20日。'
    }

    if (lowerMsg.includes('喜欢') || lowerMsg.includes('爱好')) {
      return '张三喜欢吃火锅；李四喜欢粉色和喝奶茶。'
    }

    if (lowerMsg.includes('讨厌') || lowerMsg.includes('不喜欢') || lowerMsg.includes('忌讳')) {
      return '张三不喜欢吃香菜。'
    }

    if (lowerMsg.includes('总结') || lowerMsg.includes('信息')) {
      return '张三是男性，1995年出生，软件工程师，性格随和，喜欢吃火锅不喜欢吃香菜。李四是女性，1996年出生，设计师，很有创意，喜欢粉色和喝奶茶。'
    }

    return '抱歉，我暂时无法回答这个问题。请尝试询问亲友的生日、喜好或其他具体信息。'
  }

  return {
    history,
    sessionId,
    loading,
    loadHistory,
    sendMessage,
    clearHistory
  }
})
