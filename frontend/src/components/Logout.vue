<script setup>
import { onMounted } from 'vue';
import {useUserStore} from "@/Stores/UserStore.js";
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();

onMounted(() => {
  userStore.logout();       // clear token + user
  router.replace('/login'); // redirect after logout
});
</script>

<template>
  <div>Logging out...</div>
</template>
