<script setup>
import ExtendedMenu from "@/components/ExtendedMenu.vue";
import { Button } from "primevue";
import Drawer from 'primevue/drawer';
import { ref, onMounted } from "vue";
import ProjectItem from "@/components/ProjectItem.vue";
import { useUserStore } from "@/Stores/UserStore.js";

import {useRouter} from "vue-router";

const router = useRouter();

// Optional: Import Tooltip directive if not globally registered
import Tooltip from 'primevue/tooltip';
const vTooltip = Tooltip;

const userStore = useUserStore();
// Fallback if userStore is empty during dev
const user = userStore.getUser || { username: 'Guest' };

let visible = ref(false);
let projects = ref([
]);
const getProjects = async () => {
  try {
    // Replace with your actual backend endpoint
    let user = userStore.getUser.id;
    const response = await fetch(`/api/projects/${user}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 3. Update the reactive variable with the result
    const data = await response.json();
    projects.value = data;

  } catch (error) {
    console.error('Failed to fetch projects:', error);
  }
};

// 4. Trigger the fetch when the component mounts
onMounted(() => {
  getProjects();
});
</script>

<template>
  <div class="layout-wrapper">
    <ExtendedMenu class="top-nav" />

    <div class="layout-container">
      <aside class="sidebar-strip">
        <div class="sidebar-content">
          <Button
              icon="pi pi-bars"
              @click="visible = true"
              rounded
              text
              severity="secondary"
              size="large"
              v-tooltip.right="'View Projects'"
              aria-label="Open Projects"
          />
        </div>
      </aside>

      <main class="main-content">
        <div class="welcome-container">
          <h1>Hello, <span class="highlight">{{ user.username }}</span>!</h1>
          <p class="subtitle">Welcome to your dashboard.</p>
        </div>
      </main>

      <Drawer v-model:visible="visible" header="Your Projects" class="custom-drawer">
        <div class="project-list">
          <ProjectItem
              class="project-item"
              v-for="p in projects"
              :key="p.id"
              :project="p"
          />
        </div>
        <template #footer>
          <Button label="Create New Project" icon="pi pi-plus" class="w-full" outlined @click="router.push('/new_project')"/>
        </template>
      </Drawer>
    </div>
  </div>
</template>

<style scoped>
/* 1. Wrapper to ensure full screen height */
.layout-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--surface-ground); /* PrimeVue background color */
}

/* 2. Top Nav stays at top */
.top-nav {
  flex-shrink: 0;
  z-index: 100;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* 3. Container for Sidebar + Main Content */
.layout-container {
  display: flex;
  flex: 1; /* Fills remaining height */
  overflow: hidden;
}

/* 4. The Sidebar Strip (Left) */
.sidebar-strip {
  width: 60px; /* Fixed narrow width */
  background-color: var(--surface-card);
  border-right: 1px solid var(--surface-border);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 1rem;
  flex-shrink: 0;
}

/* 5. Main Content (Right) */
.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

.welcome-container {
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

h1 {
  font-size: 3rem;
  font-weight: 300;
  color: var(--text-color);
  margin: 0;
}

.highlight {
  font-weight: 700;
  color: var(--primary-color);
}

.subtitle {
  margin-top: 1rem;
  font-size: 1.2rem;
  color: var(--text-color-secondary);
}

/* 6. Drawer Styling */
.project-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 0.5rem;
}

/* Animation for smooth entry */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Utilities */
.w-full {
  width: 100%;
}
</style>