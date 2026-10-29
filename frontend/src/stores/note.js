import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

export const useNoteStore = defineStore('note', () => {
  // State
  const notes = ref([])
  const loading = ref(false)

  // Actions
  const loadNotes = async () => {
    loading.value = true
    try {
      const response = await axios.get(`${API_BASE_URL}/notes`)
      notes.value = response.data
    } catch (error) {
      console.error('加载便签失败:', error)
      // 使用模拟数据
      notes.value = getMockNotes()
    } finally {
      loading.value = false
    }
  }

  const loadNotesByFriendId = async (friendId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/friends/${friendId}/notes`)
      return response.data
    } catch (error) {
      console.error('加载朋友便签失败:', error)
      return notes.value.filter(n => n.friendId === friendId)
    }
  }

  const addNote = async (data) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/notes`, data)
      notes.value.unshift(response.data)
      return response.data
    } catch (error) {
      console.error('添加便签失败:', error)
      // 模拟添加
      const newNote = {
        id: Date.now().toString(),
        ...data,
        createdAt: new Date(),
        updatedAt: new Date()
      }
      notes.value.unshift(newNote)
      return newNote
    }
  }

  const updateNote = async (id, data) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/notes/${id}`, data)
      const index = notes.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notes.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('更新便签失败:', error)
      const index = notes.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notes.value[index] = { ...notes.value[index], ...data, updatedAt: new Date() }
      }
      return notes.value[index]
    }
  }

  const deleteNote = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/notes/${id}`)
      notes.value = notes.value.filter(n => n.id !== id)
    } catch (error) {
      console.error('删除便签失败:', error)
      notes.value = notes.value.filter(n => n.id !== id)
    }
  }

  const getMockNotes = () => {
    return [
      {
        id: '1',
        friendId: '1',
        content: '今天和张三一起去爬山了，天气很好',
        createdAt: '2024-05-01T10:00:00'
      },
      {
        id: '2',
        friendId: '2',
        content: '李四送了我一份生日礼物，很感谢',
        createdAt: '2024-04-15T18:30:00'
      },
      {
        id: '3',
        friendId: '1',
        content: '和张三一起吃火锅，聊了很多工作上的事情',
        createdAt: '2024-03-20T19:00:00'
      }
    ]
  }

  return {
    notes,
    loading,
    loadNotes,
    loadNotesByFriendId,
    addNote,
    updateNote,
    deleteNote
  }
})
