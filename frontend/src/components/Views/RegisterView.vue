<script setup>
import SimpleMenu from "@/components/SimpleMenu.vue";
import { ref } from 'vue';
import { useRouter } from "vue-router";

// PrimeVue Imports
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Message from 'primevue/message';
import FloatLabel from 'primevue/floatlabel';

const router = useRouter();

// Form State
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const loading = ref(false);

function handleRegister() {
  loading.value = true;
  errorMessage.value = '';

  // Simulate network request
  setTimeout(() => {
    if (!username.value || !email.value || !password.value || !confirmPassword.value) {
      errorMessage.value = 'All fields are required';
      loading.value = false;
      return;
    }

    if (password.value !== confirmPassword.value) {
      errorMessage.value = 'Passwords do not match';
      loading.value = false;
      return;
    }

    // Success Simulation
    alert(`User ${username.value} registered successfully!`);

    // Reset
    username.value = '';
    email.value = '';
    password.value = '';
    confirmPassword.value = '';
    loading.value = false;

    router.push('/home');
  }, 500);
}
</script>

<template>
  <div class="layout-wrapper">
    <SimpleMenu />

    <div class="register-body">
      <Card class="register-card">
        <template #title>
          <div class="header-text">Create Account</div>
        </template>
        <template #subtitle>
          <div class="sub-text">Join us today!</div>
        </template>

        <template #content>
          <form @submit.prevent="handleRegister" class="form-content">

            <div class="field">
              <FloatLabel>
                <InputText id="username" v-model="username" class="w-full" />
                <label for="username">Username</label>
              </FloatLabel>
            </div>

            <div class="field">
              <FloatLabel>
                <InputText id="email" type="email" v-model="email" class="w-full" />
                <label for="email">Email Address</label>
              </FloatLabel>
            </div>

            <div class="field">
              <FloatLabel>
                <Password
                    id="password"
                    v-model="password"
                    toggleMask
                    class="w-full"
                    inputClass="w-full"
                >
                  <template #header>
                    <h6>Pick a password</h6>
                  </template>
                  <template #footer>
                    <div style="margin-top: 0.5rem;">Suggested: at least 8 characters</div>
                  </template>
                </Password>
                <label for="password">Password</label>
              </FloatLabel>
            </div>

            <div class="field">
              <FloatLabel>
                <Password
                    id="confirmPassword"
                    v-model="confirmPassword"
                    :feedback="false"
                    toggleMask
                    class="w-full"
                    inputClass="w-full"
                />
                <label for="confirmPassword">Confirm Password</label>
              </FloatLabel>
            </div>

            <transition name="fade">
              <Message v-if="errorMessage" severity="error" :closable="false" class="mb-3">
                {{ errorMessage }}
              </Message>
            </transition>

            <Button
                type="submit"
                label="Register"
                icon="pi pi-user-plus"
                :loading="loading"
                class="w-full"
            />

            <div class="footer-link">
              <span>Already have an account? </span>
              <router-link to="/login" class="link-text">Login</router-link>
            </div>

          </form>
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
/* Main Layout wrapper */
.layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-ground);
}

/* Center the card */
.register-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.register-card {
  width: 100%;
  max-width: 500px; /* Slightly wider than login to accommodate password hints if needed */
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.header-text {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-color);
}

.sub-text {
  text-align: center;
  margin-bottom: 1rem;
  color: var(--text-color-secondary);
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-top: 0.5rem;
}

.field {
  width: 100%;
}

.w-full {
  width: 100%;
}

.footer-link {
  text-align: center;
  margin-top: 0.5rem;
  color: var(--text-color-secondary);
}

.link-text {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.link-text:hover {
  text-decoration: underline;
}

/* Transition effects */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>