<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
// Ensure these components are imported if not auto-imported
import DataView from 'primevue/dataview';
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import ExtendedMenu from "@/components/ExtendedMenu.vue";

const router = useRouter();
const layout = ref('grid');
const searchQuery = ref('');
const statusFilter = ref(null);
const projects = ref([]);
const isLoading = ref(true);

const statusOptions = [
  { label: 'All Statuses', value: null },
  { label: 'Active', value: 'active' },
  { label: 'Maintenance', value: 'maintenance' },
  { label: 'Offline', value: 'offline' }
];

// 1. Mock Data
onMounted(() => {
  setTimeout(() => {
    projects.value = [
      {
        id: 1,
        name: 'Marketing Analytics',
        description: 'Q4 Performance tracking for social media campaigns.',
        dbType: 'postgres',
        host: 'db-prod-01',
        status: 'active',
        lastAccessed: '2 hours ago'
      },
      {
        id: 2,
        name: 'User Inventory',
        description: 'Main warehouse database sync.',
        dbType: 'mysql',
        host: '192.168.1.50',
        status: 'active',
        lastAccessed: '1 day ago'
      },
      {
        id: 3,
        name: 'Legacy Logs',
        description: 'Archived logs from 2022.',
        dbType: 'mongo',
        host: 'mongo-cluster-x',
        status: 'offline',
        lastAccessed: '3 months ago'
      },
      {
        id: 4,
        name: 'HR Portal Data',
        description: 'Employee records and payroll sync.',
        dbType: 'mssql',
        host: 'corp-sql-09',
        status: 'maintenance',
        lastAccessed: '5 mins ago'
      }
    ];
    isLoading.value = false;
  }, 800);
});

// 2. Filter Logic
const filteredProjects = computed(() => {
  return projects.value.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        project.description.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesStatus = statusFilter.value ? project.status === statusFilter.value.value : true;
    return matchesSearch && matchesStatus;
  });
});

// 3. Icon Helper
const getDbIconClass = (type) => {
  const map = {
    'postgres': 'pi pi-database icon-blue',
    'mysql': 'pi pi-database icon-orange',
    'mongo': 'pi pi-server icon-green',
    'mssql': 'pi pi-microsoft icon-red',
    'oracle': 'pi pi-database icon-dark-red'
  };
  return map[type] || 'pi pi-database';
};

const getSeverity = (status) => {
  switch (status) {
    case 'active': return 'success';
    case 'maintenance': return 'warning';
    case 'offline': return 'danger';
    default: return null;
  }
};

// 4. Navigation Logic
const openProject = (id) => {
  // This performs the redirect to /project/1, /project/2, etc.
  router.push(`/project/${id}`);
};

const createNew = () => {
  router.push('/new_project');
};
</script>

<template>

  <ExtendedMenu/>

  <div class="projects-container">

    <div class="view-header">
      <div class="header-text">
        <h1>My Projects</h1>
        <span class="subtitle">Manage and monitor your database connections</span>
      </div>
      <Button label="New Project" icon="pi pi-plus" @click="createNew" />
    </div>

    <div class="toolbar-card">
      <div class="search-wrapper">
        <i class="pi pi-search search-icon" />
        <InputText v-model="searchQuery" placeholder="Search projects..." class="search-input" />
      </div>

      <div class="controls-wrapper">
        <Dropdown
            v-model="statusFilter"
            :options="statusOptions"
            optionLabel="label"
            placeholder="Filter Status"
            showClear
            class="status-dropdown"
        />
        <DataViewLayoutOptions v-model="layout" />
      </div>
    </div>

    <DataView :value="filteredProjects" :layout="layout" :paginator="true" :rows="9" :loading="isLoading">

      <template #grid="slotProps">
        <div class="grid-layout">
          <div v-for="(item, index) in slotProps.items" :key="index" class="grid-item">
            <div class="project-card" @click="openProject(item.id)">

              <div class="card-header">
                <div class="db-badge">
                  <i :class="getDbIconClass(item.dbType)"></i>
                  <span class="db-name">{{ item.dbType }}</span>
                </div>
                <Tag :value="item.status" :severity="getSeverity(item.status)" />
              </div>

              <div class="card-body">
                <h3 class="project-title">{{ item.name }}</h3>
                <p class="project-desc">{{ item.description }}</p>
              </div>

              <div class="card-footer">
                <span class="timestamp"><i class="pi pi-clock"></i> {{ item.lastAccessed }}</span>
                <Button icon="pi pi-arrow-right" rounded text severity="secondary" class="action-btn" />
              </div>

            </div>
          </div>
        </div>
      </template>

      <template #list="slotProps">
        <div class="list-layout">
          <div v-for="(item, index) in slotProps.items" :key="index" class="list-item" @click="openProject(item.id)">

            <div class="list-icon">
              <i :class="getDbIconClass(item.dbType)"></i>
            </div>

            <div class="list-content">
              <div class="project-title">{{ item.name }}</div>
              <div class="project-desc">{{ item.description }}</div>
            </div>

            <div class="list-meta">
              <span class="host-info"><i class="pi pi-server"></i> {{ item.host }}</span>
              <Tag :value="item.status" :severity="getSeverity(item.status)" />
              <Button icon="pi pi-chevron-right" text rounded severity="secondary" />
            </div>

          </div>
        </div>
      </template>

      <template #empty>
        <div class="empty-state">
          <i class="pi pi-folder-open empty-icon"></i>
          <h3>No projects found</h3>
          <p>Create a new project to get started.</p>
          <Button label="Create Project" text @click="createNew" />
        </div>
      </template>

    </DataView>
  </div>
</template>

<style scoped>
/* 1. Main Container */
.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 2. Header */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.header-text h1 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}
.subtitle {
  color: var(--text-color-secondary);
}

/* 3. Toolbar */
.toolbar-card {
  background: var(--surface-card, );
  border: 1px solid var(--surface-border, #dfe7ef);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-wrapper {
  position: relative;
  flex: 1;
  min-width: 250px;
}
.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-color-secondary);
}
:deep(.search-input) {
  width: 100%;
  padding-left: 2.5rem;
}

.controls-wrapper {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.status-dropdown {
  width: 12rem;
}

/* 4. GRID View Styles */
.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: var(--surface-card);
  border: 1px solid var(--surface-border, #dfe7ef);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.db-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.db-name {
  font-weight: 600;
  color: var(--text-color-secondary);
  text-transform: capitalize;
}

.card-body {
  flex-grow: 1;
  margin-bottom: 1.5rem;
}

.project-title {
  font-size: 1.25rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}
.project-desc {
  color: var(--text-color-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
  /* Truncate text after 2 lines */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--surface-border);
  padding-top: 1rem;
}
.timestamp {
  font-size: 0.85rem;
  color: var(--text-color-secondary);
}
.timestamp i {
  margin-right: 0.25rem;
}

/* 5. LIST View Styles */
.list-layout {
  display: flex;
  flex-direction: column;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--surface-border);
  background: var(--surface-card);
  cursor: pointer;
  transition: background-color 0.2s;
}
.list-item:hover {
  background-color: var(--surface-hover);
}
.list-icon {
  font-size: 1.5rem;
  margin-right: 1.5rem;
  display: flex;
  align-items: center;
}
.list-content {
  flex: 1;
}
.list-meta {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.host-info {
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

/* 6. Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 1rem;
}
.empty-icon {
  font-size: 3rem;
  color: var(--text-color-secondary);
  margin-bottom: 1rem;
}

/* 7. Icon Colors */
.icon-blue { color: #3b82f6; }
.icon-orange { color: #f97316; }
.icon-green { color: #22c55e; }
.icon-red { color: #ef4444; }
.icon-dark-red { color: #b91c1c; }

/* 8. Mobile Responsiveness */
@media (max-width: 768px) {
  .list-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .list-meta {
    width: 100%;
    justify-content: space-between;
  }
  .view-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .controls-wrapper {
    width: 100%;
    justify-content: space-between;
  }
  .status-dropdown {
    flex: 1;
  }
}
</style>