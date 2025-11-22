<script setup>
import {ref} from "vue";
import Menubar from 'primevue/menubar';
const items = ref([
  {
    label: 'Home',
    icon: 'home',
    route: '/start'
  },
  {
    label: 'Login',
    icon: 'login',
    route: '/login'
  },
  {
    label: 'Register',
    icon: 'register',
    route: '/register'
  }
]);
</script>

<template>
  <div>
    <Menubar :model="items">
      <template #item="{ item, props }">
        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate">
            <span :class="item.icon" />
            <span class="ml-2">{{ item.label }}</span>
          </a>
        </router-link>
      </template>
    </Menubar>
  </div>
</template>

<style scoped>

</style>