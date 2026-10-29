import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import dayjs from 'dayjs'
import { Lunar } from 'lunar-javascript'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

export const useFriendStore = defineStore('friend', () => {
  // State
  const friends = ref([])
  const loading = ref(false)

  // Getters
  const getStats = computed(() => {
    const now = dayjs()
    const friendsCount = friends.value.length
    const recentRecords = friends.value.filter(f => {
      if (!f.createdAt) return false
      return dayjs(f.createdAt).isAfter(now.subtract(7, 'day'))
    }).length

    return { friendsCount, recentRecords }
  })

  const getRecentFriends = computed(() => {
    return [...friends.value]
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      .slice(0, 5)
      .map(f => ({
        id: f.id,
        name: f.name,
        avatar: f.avatar,
        addedTime: dayjs(f.createdAt).format('YYYY-MM-DD')
      }))
  })

  const specialCareFriends = computed(() => {
    return friends.value
      .filter(f => f.specialCare)
      .map(f => ({
        id: f.id,
        name: f.name,
        avatar: f.avatar,
        addedTime: dayjs(f.createdAt).format('YYYY-MM-DD')
      }))
  })

  // Actions
  const loadFriends = async () => {
    loading.value = true
    try {
      const response = await axios.get(`${API_BASE_URL}/friends`)
      friends.value = response.data.map(f => processFriendData(f))
    } catch (error) {
      console.error('加载朋友列表失败:', error)
      // 只在首次加载且无数据时使用模拟数据
      if (friends.value.length === 0) {
        friends.value = getMockFriends()
      }
    } finally {
      loading.value = false
    }
  }

  const getFriendById = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/friends/${id}`)
      return processFriendData(response.data)
    } catch (error) {
      console.error('加载朋友详情失败:', error)
      // 从本地查找
      const friend = friends.value.find(f => f.id === id)
      return friend || null
    }
  }

  const addFriend = async (data) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/friends`, data)
      const newFriend = processFriendData(response.data)
      friends.value.unshift(newFriend)
      return newFriend
    } catch (error) {
      console.error('添加亲友失败:', error)
      // 模拟添加
      const newFriend = {
        id: Date.now().toString(),
        ...data,
        createdAt: new Date(),
        updatedAt: new Date()
      }
      friends.value.unshift(processFriendData(newFriend))
      return newFriend
    }
  }

  const updateFriend = async (id, data) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/friends/${id}`, data)
      const updated = processFriendData(response.data)
      const index = friends.value.findIndex(f => f.id === id)
      if (index !== -1) {
        friends.value[index] = updated
      }
      return updated
    } catch (error) {
      console.error('更新朋友失败:', error)
      const index = friends.value.findIndex(f => f.id === id)
      if (index !== -1) {
        friends.value[index] = { ...friends.value[index], ...data, updatedAt: new Date() }
        friends.value[index] = processFriendData(friends.value[index])
      }
      return friends.value[index]
    }
  }

  const deleteFriend = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/friends/${id}`)
      friends.value = friends.value.filter(f => f.id !== id)
    } catch (error) {
      console.error('删除朋友失败:', error)
      friends.value = friends.value.filter(f => f.id !== id)
    }
  }

  const addPreference = async (friendId, data) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/friends/${friendId}/preferences`, data)
      const index = friends.value.findIndex(f => f.id === friendId)
      if (index !== -1) {
        friends.value[index].preferences = response.data
      }
      return response.data
    } catch (error) {
      console.error('添加偏好失败:', error)
      // 模拟添加
      const friend = friends.value.find(f => f.id === friendId)
      if (friend) {
        if (!friend.preferences) friend.preferences = []
        friend.preferences.push({
          id: Date.now().toString(),
          ...data,
          createdAt: new Date()
        })
      }
    }
  }

  const deletePreference = async (friendId, preferenceId) => {
    try {
      await axios.delete(`${API_BASE_URL}/friends/${friendId}/preferences/${preferenceId}`)
      const friend = friends.value.find(f => f.id === friendId)
      if (friend && friend.preferences) {
        friend.preferences = friend.preferences.filter(p => p.id !== preferenceId)
      }
    } catch (error) {
      console.error('删除偏好失败:', error)
      const friend = friends.value.find(f => f.id === friendId)
      if (friend && friend.preferences) {
        friend.preferences = friend.preferences.filter(p => p.id !== preferenceId)
      }
    }
  }

  const updatePreferenceTag = async (friendId, preferenceId, tag) => {
    try {
      await axios.put(`${API_BASE_URL}/friends/${friendId}/preferences/${preferenceId}/tag`, { tag })
      const friend = friends.value.find(f => f.id === friendId)
      if (friend && friend.preferences) {
        const pref = friend.preferences.find(p => p.id === preferenceId)
        if (pref) pref.tag = tag
      }
    } catch (error) {
      console.error('更新标签失败:', error)
      throw error
    }
  }

  const toggleSpecialCare = async (id) => {
    const friend = friends.value.find(f => f.id === id)
    if (!friend) return
    const newValue = !friend.specialCare
    try {
      await axios.put(`${API_BASE_URL}/friends/${id}/special-care`, { specialCare: newValue })
      friend.specialCare = newValue
    } catch (error) {
      console.error('更新特别关心状态失败:', error)
      friend.specialCare = newValue
    }
  }

  // Helper functions
  const processFriendData = (friend) => {
    if (!friend) return null

    // 计算年龄
    let age = null
    if (friend.birthday) {
      age = dayjs().diff(dayjs(friend.birthday), 'year')
    }

    // 计算星座
    let zodiac = ''
    if (friend.birthday) {
      zodiac = getZodiac(friend.birthday)
    }

    // 计算认识年限
    let knowYears = 0
    if (friend.knowDate) {
      knowYears = dayjs().diff(dayjs(friend.knowDate), 'year')
    }

    // 农历生日
    let lunarBirthday = ''
    let nextBirthday = ''
    if (friend.birthday) {
      const today = dayjs()
      const birthDate = dayjs(friend.birthday)

      if (friend.birthdayType === 'lunar') {
        try {
          // 从存储的公历生日反推农历月日
          const lunar = Lunar.fromDate(birthDate.toDate())
          const lunarMonth = lunar.getMonth()
          const lunarDay = lunar.getDay()
          const thisYear = today.year()

          // 今年农历生日对应的公历日期
          const thisYearLunar = Lunar.fromYmd(thisYear, lunarMonth, lunarDay)
          const thisSolar = thisYearLunar.getSolar()
          let next = dayjs(`${thisSolar.getYear()}-${String(thisSolar.getMonth()).padStart(2, '0')}-${String(thisSolar.getDay()).padStart(2, '0')}`)

          if (next.isBefore(today, 'day')) {
            // 今年已过，算明年
            const nextYearLunar = Lunar.fromYmd(thisYear + 1, lunarMonth, lunarDay)
            const nextSolar = nextYearLunar.getSolar()
            next = dayjs(`${nextSolar.getYear()}-${String(nextSolar.getMonth()).padStart(2, '0')}-${String(nextSolar.getDay()).padStart(2, '0')}`)
          }
          nextBirthday = next.format('YYYY-MM-DD')
          lunarBirthday = `${lunar.getMonthInChinese()}月${lunar.getDayInChinese()}`
        } catch (e) {
          console.error('农历生日计算失败:', e)
        }
      } else {
        // 公历生日
        let next = birthDate.year(today.year())
        if (next.isBefore(today, 'day')) {
          next = next.add(1, 'year')
        }
        nextBirthday = next.format('YYYY-MM-DD')
      }
    }

    return {
      ...friend,
      age,
      zodiac,
      knowYears,
      lunarBirthday,
      nextBirthday
    }
  }

  const getZodiac = (birthday) => {
    const date = dayjs(birthday)
    const month = date.month() + 1
    const day = date.date()

    const zodiacDates = [
      { name: '摩羯座', start: [1, 1], end: [1, 19] },
      { name: '水瓶座', start: [1, 20], end: [2, 18] },
      { name: '双鱼座', start: [2, 19], end: [3, 20] },
      { name: '白羊座', start: [3, 21], end: [4, 19] },
      { name: '金牛座', start: [4, 20], end: [5, 20] },
      { name: '双子座', start: [5, 21], end: [6, 21] },
      { name: '巨蟹座', start: [6, 22], end: [7, 22] },
      { name: '狮子座', start: [7, 23], end: [8, 22] },
      { name: '处女座', start: [8, 23], end: [9, 22] },
      { name: '天秤座', start: [9, 23], end: [10, 23] },
      { name: '天蝎座', start: [10, 24], end: [11, 22] },
      { name: '射手座', start: [11, 23], end: [12, 21] },
      { name: '摩羯座', start: [12, 22], end: [12, 31] }
    ]

    for (const z of zodiacDates) {
      const [startMonth, startDay] = z.start
      const [endMonth, endDay] = z.end

      if (month === startMonth && day >= startDay) return z.name
      if (month === endMonth && day <= endDay) return z.name
    }

    return ''
  }

  const getMockFriends = () => {
    return [
      {
        id: '1',
        name: '张三',
        gender: '男',
        birthday: '1995-06-15',
        birthdayType: 'solar',
        height: 175,
        weight: 70,
        knowDate: '2018-03-10',
        occupation: '软件工程师',
        hometown: '北京',
        phone: '13800138000',
        remark: '大学室友，性格随和',
        createdAt: '2024-01-15T10:00:00',
        specialCare: true,
        preferences: [
          { id: '1', type: 'like', content: '喜欢吃火锅', tag: '饮食' },
          { id: '2', type: 'dislike', content: '不喜欢吃香菜', tag: '饮食' }
        ],
        notes: [
          { id: '1', content: '今天一起去爬山了', createdAt: '2024-05-01T10:00:00' }
        ]
      },
      {
        id: '2',
        name: '李四',
        gender: '女',
        birthday: '1996-08-20',
        birthdayType: 'solar',
        height: 162,
        weight: 50,
        knowDate: '2019-07-22',
        occupation: '设计师',
        hometown: '上海',
        phone: '13900139000',
        remark: '同事，很有创意',
        createdAt: '2024-02-20T14:30:00',
        preferences: [
          { id: '3', type: 'like', content: '喜欢粉色', tag: '颜色' },
          { id: '4', type: 'like', content: '喜欢喝奶茶', tag: '饮食' }
        ],
        notes: []
      }
    ].map(f => processFriendData(f))
  }

  return {
    friends,
    loading,
    getStats,
    getRecentFriends,
    specialCareFriends,
    loadFriends,
    getFriendById,
    addFriend,
    updateFriend,
    deleteFriend,
    addPreference,
    deletePreference,
    updatePreferenceTag,
    toggleSpecialCare
  }
})
