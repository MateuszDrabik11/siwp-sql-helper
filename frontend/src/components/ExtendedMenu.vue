<script setup>
import {ref} from "vue";
import Menubar from 'primevue/menubar';
const items = ref([
  {
    label: 'Home',
    icon: 'home',
    route: '/home'
  },
  {
    label: 'Logout',
    icon: 'logout',
    route: '/logout'
  },
  {
    label: 'Create new project',
    icon: 'new_project',
    route: '/new_project'
  },
  {
    label: 'Change password',
    icon: 'new_password',
    route: '/new_password'
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