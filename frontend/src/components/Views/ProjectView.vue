<script setup>
import ExtendedMenu from "@/components/ExtendedMenu.vue";

defineProps({
  id: Number,
})
</script>

<template>
  <ExtendedMenu/>
  <div>
    Project {{ id }}
  </div>
</template>

<style scoped>

</style>