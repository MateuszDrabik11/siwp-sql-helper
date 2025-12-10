<script setup>
import {useRouter} from "vue-router";
const router = useRouter();
defineProps({
  project: {
    type: Object,
    required: true
  }
});
</script>
<template>
  <div class="project-item" @click="router.push(`/project/${project.id}`)">
    <div class="project-name">{{ project.name }}</div>
  </div>
</template>

<style scoped>
.project-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  margin: 6px 0;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
  transition: 0.2s ease-in-out;
  cursor: pointer;
}

.project-item:hover {
  background: #f0f0f0;
  transform: translateY(-1px);
}
.project-name {
  font-size: 1rem;
  font-weight: 500;
  color: #666;
}
</style>