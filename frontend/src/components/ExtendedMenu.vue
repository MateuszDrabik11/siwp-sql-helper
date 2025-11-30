<script setup>
import { ref } from "vue";
import Menubar from 'primevue/menubar';
import Avatar from 'primevue/avatar';
import Badge from 'primevue/badge';
import Button from "primevue/button";
import {useRouter} from "vue-router";
const router = useRouter();

const items = ref([
  {
    label: 'Dashboard',
    icon: 'pi pi-home',
    route: '/home'
  },
  {
    label: 'Projects',
    icon: 'pi pi-folder',
    items: [ // Example of a dropdown submenu
      {
        label: 'Create New',
        icon: 'pi pi-plus',
        route: '/new_project'
      },
      {
        label: 'View All',
        icon: 'pi pi-list',
        route: '/projects'
      }
    ]
  }
]);

// Items that appear on the far right
const userItems = ref([
  {
    label: 'Settings',
    icon: 'pi pi-cog',
    route: '/new_password'
  },
  {
    label: 'Logout',
    icon: 'pi pi-power-off',
    route: '/logout'
  }
]);
</script>

<template>
  <div>
    <Menubar :model="items" class="app-menubar">

      <template #start>
        <div class="brand-logo">
          <i class="pi pi-box" style="font-size: 1.5rem; color: var(--primary-color);"></i>
          <span class="brand-text">Dashboard</span>
        </div>
      </template>

      <template #item="{ item, props, hasSubmenu }">
        <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate">
            <span :class="item.icon" />
            <span class="ml-2">{{ item.label }}</span>
          </a>
        </router-link>
        <a v-else :href="item.url" v-bind="props.action" :target="item.target">
          <span :class="item.icon" />
          <span class="ml-2">{{ item.label }}</span>
          <span v-if="hasSubmenu" class="pi pi-angle-down ml-2" />
        </a>
      </template>

      <template #end>
        <div class="flex align-items-center gap-2 relative z-5">

          <Button
              icon="pi pi-cog"
              text
              rounded
              aria-label="Settings"
              v-tooltip.bottom="'Settings'"
              @click="router.push('/new_password')"
              style="color: var(--text-color);"
          />

          <Button
              icon="pi pi-power-off"
              text
              rounded
              severity="danger"
              aria-label="Logout"
              v-tooltip.bottom="'Logout'"
              @click="router.push('/logout')"
          />

          <Avatar icon="pi pi-user" shape="circle" style="background-color: var(--primary-color); color: #fff" />

        </div>
      </template>

    </Menubar>
  </div>
</template>

<style scoped>
.app-menubar {
  border-radius: 0;
  border: none;
  border-bottom: 1px solid var(--surface-border);
  padding: 0.5rem 1.5rem;
  background: var(--surface-card);
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-right: 1rem;
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--text-color);
}

/* Flex utility for the end slot */
.flex {
  display: flex;
}
.align-items-center {
  align-items: center;
}
.gap-2 {
  gap: 1rem;
}

/* Custom styling for the icon-only links in the end slot */
.custom-icon-link {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  color: var(--text-color-secondary);
  text-decoration: none;
  transition: color 0.2s;
  cursor: pointer;
}

.custom-icon-link:hover {
  color: var(--primary-color);
}
</style>