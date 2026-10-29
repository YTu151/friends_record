<template>
  <el-tag
    :type="tagType"
    :closable="closable"
    @click="handleClick"
    @close="handleDelete"
    class="preference-tag"
    :class="{ clickable: !closable || true }"
  >
    <span v-if="item.tag" class="tag-label">[{{ item.tag }}]</span>
    {{ item.content }}
  </el-tag>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    default: 'like',
    validator: (value) => ['like', 'dislike'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['delete', 'click'])

const tagType = props.type === 'like' ? 'success' : 'danger'

const handleDelete = () => {
  emit('delete', props.item.id)
}

const handleClick = () => {
  emit('click', props.item)
}
</script>

<style scoped>
.preference-tag {
  font-size: 14px;
  padding: 0 10px;
  height: 32px;
  line-height: 30px;
  cursor: pointer;
}

.tag-label {
  font-size: 12px;
  margin-right: 4px;
  opacity: 0.8;
}
</style>
