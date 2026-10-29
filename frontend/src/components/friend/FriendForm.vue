<template>
  <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
    <!-- 头像 -->
    <div class="avatar-section">
      <div class="avatar-wrapper" @click="triggerUpload">
        <el-avatar :size="72" :src="form.avatar" icon="UserFilled" />
        <div class="avatar-overlay">
          <el-icon><Camera /></el-icon>
        </div>
        <input ref="fileInputRef" type="file" accept="image/*" hidden @change="handleAvatarUpload" />
      </div>
      <span class="avatar-hint">点击上传头像</span>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="form.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="生日" prop="birthday">
          <el-date-picker
            v-model="form.birthday"
            type="date"
            placeholder="选择生日"
            style="width: 100%"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="生日类型">
          <el-radio-group v-model="form.birthdayType">
            <el-radio label="solar">阳历</el-radio>
            <el-radio label="lunar">农历</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="身高(cm)">
          <el-input-number v-model="form.height" :min="50" :max="250" style="width: 100%" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="体重(kg)">
          <el-input-number v-model="form.weight" :min="20" :max="200" style="width: 100%" />
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="认识时间">
          <el-date-picker
            v-model="form.knowDate"
            type="date"
            placeholder="选择认识时间"
            style="width: 100%"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="职业">
          <el-input v-model="form.occupation" placeholder="请输入职业" />
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="家乡">
          <el-input v-model="form.hometown" placeholder="请输入家乡" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="联系方式">
          <el-input v-model="form.phone" placeholder="请输入联系方式" />
        </el-form-item>
      </el-col>
    </el-row>

    <el-form-item label="备注">
      <el-input
        v-model="form.remark"
        type="textarea"
        :rows="3"
        placeholder="对这个亲友的整体印象、初识故事等"
      />
    </el-form-item>

    <el-form-item>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Camera } from '@element-plus/icons-vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

const props = defineProps({
  friend: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formRef = ref(null)
const fileInputRef = ref(null)
const submitting = ref(false)
const uploading = ref(false)

const form = reactive({
  name: '',
  gender: '男',
  birthday: '',
  birthdayType: 'solar',
  height: null,
  weight: null,
  knowDate: '',
  occupation: '',
  hometown: '',
  phone: '',
  remark: '',
  avatar: ''
})

const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 1, max: 20, message: '长度在1-20个字符', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  birthday: [
    { required: true, message: '请选择生日', trigger: 'change' }
  ]
}

watch(() => props.friend, (newVal) => {
  if (newVal) {
    Object.assign(form, {
      name: newVal.name || '',
      gender: newVal.gender || '男',
      birthday: newVal.birthday || '',
      birthdayType: newVal.birthdayType || 'solar',
      height: newVal.height || null,
      weight: newVal.weight || null,
      knowDate: newVal.knowDate || '',
      occupation: newVal.occupation || '',
      hometown: newVal.hometown || '',
      phone: newVal.phone || '',
      remark: newVal.remark || '',
      avatar: newVal.avatar || ''
    })
  }
}, { immediate: true })

const triggerUpload = () => {
  fileInputRef.value?.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await axios.post(`${API_BASE_URL}/files/upload`, formData)
    form.avatar = res.data.url
    ElMessage.success('头像上传成功')
  } catch (e) {
    ElMessage.error('头像上传失败')
  }
  uploading.value = false
  event.target.value = ''
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const data = { ...form }
    emit('submit', data)
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.el-form {
  padding: 10px 0;
}

.avatar-section {
  display: flex;
  flex-direction: column;
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

  .avatar-hint {
    margin-top: 8px;
    font-size: 12px;
    color: #909399;
  }
}
</style>
