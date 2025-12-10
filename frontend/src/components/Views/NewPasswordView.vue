<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';

// Components (Make sure these are registered globally or import them)
import Card from 'primevue/card';
import Button from 'primevue/button';
import Password from 'primevue/password';
import Toast from 'primevue/toast';

const router = useRouter();
const toast = useToast();

const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);

const handleSubmit = async () => {
  // 1. Basic Validation
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    toast.add({ severity: 'warn', summary: 'Missing Data', detail: 'Please fill in all fields.', life: 3000 });
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'New passwords do not match.', life: 3000 });
    return;
  }

  // 2. Mock API Call
  isLoading.value = true;

  // Simulate network delay (Replace this with your actual axios/fetch call)
  setTimeout(() => {
    isLoading.value = false;

    // Success scenario
    toast.add({ severity: 'success', summary: 'Success', detail: 'Password updated successfully', life: 3000 });

    // Optional: Reset form or redirect
    currentPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';

    // Redirect back to dashboard after a short delay?
    // setTimeout(() => router.push('/home'), 1000);

  }, 1500);
};

const handleCancel = () => {
  router.back(); // Go back to previous page
};
</script>

<template>
  <div class="password-container">
    <Toast />

    <Card class="password-card">
      <template #title>
        <h1 class="card-title">Change Password</h1>
      </template>
      <template #subtitle>
        <p class="card-subtitle">Update your account security</p>
      </template>

      <template #content>
        <form @submit.prevent="handleSubmit" class="password-form">

          <div class="form-group">
            <label for="current_pwd" class="form-label">Current Password</label>
            <Password
                id="current_pwd"
                v-model="currentPassword"
                :feedback="false"
                toggleMask
                placeholder="Enter current password"
                class="full-width-input"
            />
          </div>

          <div class="form-group">
            <label for="new_pwd" class="form-label">New Password</label>
            <Password
                id="new_pwd"
                v-model="newPassword"
                toggleMask
                placeholder="Enter new password"
                promptLabel="Choose a strong password"
                weakLabel="Weak"
                mediumLabel="Medium"
                strongLabel="Strong"
                class="full-width-input"
            >
              <template #footer>
                <div class="password-requirements">
                  <div class="divider"></div>
                  <ul>
                    <li>At least one lowercase</li>
                    <li>At least one uppercase</li>
                    <li>At least one numeric</li>
                    <li>Minimum 8 characters</li>
                  </ul>
                </div>
              </template>
            </Password>
          </div>

          <div class="form-group">
            <label for="confirm_pwd" class="form-label">Confirm Password</label>
            <Password
                id="confirm_pwd"
                v-model="confirmPassword"
                :feedback="false"
                toggleMask
                placeholder="Confirm new password"
                class="full-width-input"
                :class="{ 'p-invalid': newPassword && confirmPassword && newPassword !== confirmPassword }"
            />
            <small v-if="newPassword && confirmPassword && newPassword !== confirmPassword" class="error-msg">
              Passwords do not match.
            </small>
          </div>

          <div class="button-group">
            <Button
                type="submit"
                label="Update Password"
                icon="pi pi-check"
                :loading="isLoading"
                class="w-full"
            />
            <Button
                type="button"
                label="Cancel"
                icon="pi pi-times"
                severity="secondary"
                text
                @click="handleCancel"
                class="w-full"
            />
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<style scoped>
/* 1. Main Layout */
.password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--surface-ground); /* Uses PrimeVue var or fallback */
  padding: 1rem;
}

/* 2. Card Styling */
.password-card {
  width: 100%;
  max-width: 450px;
  border-radius: 12px;
  /* Adds a subtle shadow if PrimeVue card doesn't have one */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* 3. Typography */
.card-title {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
}

.card-subtitle {
  text-align: center;
  margin: 0 0 2rem 0;
  color: var(--text-color-secondary);
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--text-color);
}

/* 4. Form Layout */
.password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Space between input groups */
}

.form-group {
  display: flex;
  flex-direction: column;
}

/* 5. PrimeVue Overrides (Crucial for full width) */
/* This targets the internal structure of the PrimeVue Password component */
:deep(.full-width-input),
:deep(.p-password-input) {
  width: 100%;
}

:deep(.p-password) {
  width: 100%;
  display: inline-flex;
}

/* 6. Validation & Extras */
.error-msg {
  color: var(--red-500, #ef4444);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

/* Password Hint Styling */
.password-requirements {
  padding: 0 0.5rem;
}

.divider {
  height: 1px;
  background-color: var(--surface-border, #dee2e6);
  margin: 0.5rem 0;
}

.password-requirements ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-color-secondary);
  line-height: 1.5;
}
</style>