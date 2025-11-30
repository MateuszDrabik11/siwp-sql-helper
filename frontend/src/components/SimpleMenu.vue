<script setup>
import { ref } from "vue";
import Menubar from 'primevue/menubar';

const items = ref([
  {
    label: 'Home',
    icon: 'pi pi-home', // Correct PrimeIcon class
    route: '/start'
  },
  {
    label: 'Login',
    icon: 'pi pi-sign-in',
    route: '/login'
  },
  {
    label: 'Register',
    icon: 'pi pi-user-plus',
    route: '/register'
  }
]);
</script>

<template>
  <div class="menu-wrapper">
    <Menubar :model="items" class="app-menubar">

      <template #start>
        <div class="brand-logo">
          <i class="pi pi-bolt" style="font-size: 1.5rem; color: var(--primary-color);"></i>
          <span class="brand-text">MyApp</span>
        </div>
      </template>

      <template #item="{ item, props }">
        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate" class="menu-link">
            <span :class="item.icon" />
            <span class="ml-2">{{ item.label }}</span>
          </a>
        </router-link>
      </template>

    </Menubar>
  </div>
</template>

<style scoped>
/* Remove default rounded corners for a full-width top bar look */
.app-menubar {
  border-radius: 0;
  border: none;
  border-bottom: 1px solid var(--surface-border);
  padding: 0.5rem 1rem;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-right: 1.5rem;
  font-weight: bold;
  font-size: 1.25rem;
  color: var(--text-color);
}

.brand-text {
  letter-spacing: -0.5px;
}
</style>