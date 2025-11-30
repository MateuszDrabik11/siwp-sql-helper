<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';

// If you haven't registered components globally, import them here:
import Card from 'primevue/card';
import Steps from 'primevue/steps';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import Password from 'primevue/password';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import ExtendedMenu from "@/components/ExtendedMenu.vue";

const router = useRouter();
const toast = useToast();

const activeStep = ref(0);
const isLoading = ref(false);

// 1. Wizard Steps
const items = ref([
  { label: 'Project Details' },
  { label: 'Database Connection' },
  { label: 'Review' }
]);

// 2. Form Data
const form = reactive({
  name: '',
  description: '',
  dbType: null,
  dbHost: 'localhost',
  dbPort: null,
  dbName: '',
  dbUser: '',
  dbPassword: ''
});

// 3. Database Options for Dropdown
const dbTypes = ref([
  { name: 'PostgreSQL', code: 'postgres', defaultPort: 5432 },
  { name: 'MySQL', code: 'mysql', defaultPort: 3306 },
  { name: 'SQL Server', code: 'mssql', defaultPort: 1433 },
  { name: 'MongoDB', code: 'mongo', defaultPort: 27017 },
  { name: 'Oracle', code: 'oracle', defaultPort: 1521 }
]);

// Helper: Auto-fill port when DB type changes
const onDbTypeChange = () => {
  if (form.dbType && form.dbType.defaultPort) {
    form.dbPort = form.dbType.defaultPort;
  }
};

// 4. Navigation Logic
const nextStep = () => {
  // Basic Validation for Step 0
  if (activeStep.value === 0) {
    if (!form.name) {
      toast.add({ severity: 'error', summary: 'Error', detail: 'Project Name is required.', life: 3000 });
      return;
    }
  }
  // Basic Validation for Step 1
  if (activeStep.value === 1) {
    if (!form.dbType || !form.dbHost || !form.dbUser) {
      toast.add({ severity: 'error', summary: 'Error', detail: 'Please fill in required DB fields.', life: 3000 });
      return;
    }
  }
  activeStep.value++;
};

const prevStep = () => {
  activeStep.value--;
};

// 5. Test Connection (Optional feature)
const testConnection = async () => {
  isLoading.value = true;
  // Simulate API ping
  setTimeout(() => {
    isLoading.value = false;
    toast.add({ severity: 'success', summary: 'Connected', detail: 'Database connection successful!', life: 3000 });
  }, 1000);
};

// 6. Submit Logic
const handleSubmit = async () => {
  isLoading.value = true;

  // Construct payload
  const payload = {
    ...form,
    dbType: form.dbType.code // Send only the code, not object
  };

  console.log("Submitting:", payload);

  // Simulate API Call
  setTimeout(() => {
    isLoading.value = false;
    toast.add({ severity: 'success', summary: 'Created', detail: 'Project created successfully', life: 3000 });
    router.push('/projects'); // Redirect to list
  }, 1500);
};
</script>

<template>
  <ExtendedMenu/>
  <div class="page-container">
    <Card class="project-card">

      <template #title>
        <div class="header-container">
          <h1>Create New Project</h1>
          <Steps :model="items" :readonly="true" v-model:activeStep="activeStep" class="custom-steps" />
        </div>
      </template>

      <template #content>
        <div class="form-content">

          <div v-if="activeStep === 0" class="step-panel fade-in">
            <div class="form-group">
              <label for="p_name">Project Name <span class="required">*</span></label>
              <InputText id="p_name" v-model="form.name" placeholder="My Analytics Dashboard" class="w-full" />
            </div>
            <div class="form-group">
              <label for="p_desc">Description</label>
              <Textarea id="p_desc" v-model="form.description" rows="5" placeholder="Brief description of the project..." class="w-full" />
            </div>
          </div>

          <div v-if="activeStep === 1" class="step-panel fade-in">
            <div class="form-grid">
              <div class="form-group span-full">
                <label>Database Type <span class="required">*</span></label>
                <Dropdown
                    v-model="form.dbType"
                    :options="dbTypes"
                    optionLabel="name"
                    placeholder="Select a Database"
                    class="w-full"
                    @change="onDbTypeChange"
                />
              </div>

              <div class="form-group span-2">
                <label>Host <span class="required">*</span></label>
                <InputText v-model="form.dbHost" placeholder="127.0.0.1 or db.example.com" class="w-full" />
              </div>

              <div class="form-group span-1">
                <label>Port</label>
                <InputNumber v-model="form.dbPort" :useGrouping="false" class="w-full" />
              </div>

              <div class="form-group span-full">
                <label>Database Name</label>
                <InputText v-model="form.dbName" placeholder="production_db" class="w-full" />
              </div>

              <div class="form-group span-full">
                <label>Username <span class="required">*</span></label>
                <InputText v-model="form.dbUser" class="w-full" />
              </div>

              <div class="form-group span-full">
                <label>Password</label>
                <Password
                    v-model="form.dbPassword"
                    :feedback="false"
                    toggleMask
                    class="w-full"
                    inputClass="w-full"
                />
              </div>
            </div>

            <div class="mt-3">
              <Button label="Test Connection" icon="pi pi-bolt" size="small" outlined @click="testConnection" :loading="isLoading" />
            </div>
          </div>

          <div v-if="activeStep === 2" class="step-panel fade-in">
            <div class="review-box">
              <h3>Summary</h3>
              <div class="review-item">
                <strong>Project:</strong> {{ form.name }}
              </div>
              <div class="review-item">
                <strong>Description:</strong> <span class="text-color-secondary">{{ form.description || 'None' }}</span>
              </div>
              <div class="divider"></div>
              <div class="review-item">
                <strong>Database:</strong> {{ form.dbType ? form.dbType.name : 'Not Selected' }}
              </div>
              <div class="review-item">
                <strong>Host:</strong> {{ form.dbHost }}:{{ form.dbPort }}
              </div>
              <div class="review-item">
                <strong>User:</strong> {{ form.dbUser }}
              </div>
            </div>
          </div>

        </div>
      </template>

      <template #footer>
        <div class="flex justify-content-between mt-4">
          <Button
              label="Back"
              icon="pi pi-arrow-left"
              severity="secondary"
              @click="prevStep"
              :disabled="activeStep === 0"
          />

          <Button
              v-if="activeStep < 2"
              label="Next"
              icon="pi pi-arrow-right"
              iconPos="right"
              @click="nextStep"
          />

          <Button
              v-else
              label="Create Project"
              icon="pi pi-check"
              severity="success"
              @click="handleSubmit"
              :loading="isLoading"
          />
        </div>
      </template>

    </Card>
  </div>
</template>

<style scoped>
/* Layout */
.page-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background-color: var(--surface-ground);
  min-height: calc(100vh - 4rem); /* Adjust based on your menubar height */
}

.project-card {
  width: 100%;
  max-width: 800px; /* Wider than login to fit grid */
  border-radius: 10px;
}

.header-container {
  margin-bottom: 2rem;
}
.header-container h1 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--text-color);
}

/* Form Styles */
.form-content {
  min-height: 350px; /* Prevents jumping height between steps */
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.required {
  color: var(--red-500);
}

/* Grid System for DB Config */
.form-grid {
  display: grid;
  grid-template-columns: 2fr 1fr; /* Host takes 2 parts, Port takes 1 */
  gap: 1rem;
}

.span-full {
  grid-column: 1 / -1;
}
.span-2 {
  grid-column: span 1; /* Actually span 1 in this 2-col layout means half, but we want auto logic */
}
/* On mobile, stack everything */
@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

/* Review Step */
.review-box {
  background-color: var(--surface-section);
  border: 1px solid var(--surface-border);
  padding: 1.5rem;
  border-radius: 8px;
}
.review-item {
  padding: 0.5rem 0;
  font-size: 1.1rem;
}
.divider {
  height: 1px;
  background-color: var(--surface-border);
  margin: 1rem 0;
}

/* PrimeVue Overrides */
:deep(.p-steps .p-steps-item .p-menuitem-link) {
  background: transparent;
}
:deep(.full-width-input), :deep(.p-inputtext), :deep(.p-dropdown), :deep(.p-inputnumber) {
  width: 100%;
}
/* Animation */
.fade-in {
  animation: fadeIn 0.4s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>