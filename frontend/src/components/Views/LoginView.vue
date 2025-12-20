<script setup>
import SimpleMenu from "@/components/SimpleMenu.vue";
import { ref } from 'vue';
import { useRouter } from "vue-router";
import { useUserStore } from "@/Stores/UserStore.js";

// PrimeVue Imports
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Message from 'primevue/message';
import FloatLabel from 'primevue/floatlabel';

const router = useRouter();
const login = ref('');
const password = ref('');
const errorMessage = ref('');
const loading = ref(false); // Added for button loading state

async function handleLogin() {
  loading.value = true;
  errorMessage.value = '';
  try {
    await useUserStore().login(login.value, password.value);
  }
  catch (error) {
    errorMessage.value = 'Invalid username or password';
    useUserStore().logout();
    loading.value = false;
  }
  // Simulate a small network delay for better UX feel
  setTimeout(() => {
    if (useUserStore().isLoggedIn()) {
      router.push('/home');
    } else {
      errorMessage.value = 'Invalid username or password';
      useUserStore().logout();
      loading.value = false;
    }
  }, 500);
}
</script>

<template>
  <div class="layout-wrapper">
    <SimpleMenu />

    <div class="login-body">
      <Card class="login-card">
        <template #title>
          <div class="header-text">Welcome Back</div>
        </template>
        <template #subtitle>
          <div class="sub-text">Please sign in to continue</div>
        </template>

        <template #content>
          <form @submit.prevent="handleLogin" class="form-content">

            <div class="field">
              <FloatLabel>
                <InputText id="username" v-model="login" class="w-full" />
                <label for="username">Username</label>
              </FloatLabel>
            </div>

            <div class="field">
              <FloatLabel>
                <Password
                    id="password"
                    v-model="password"
                    :feedback="false"
                    toggleMask
                    class="w-full"
                    inputClass="w-full"
                />
                <label for="password">Password</label>
              </FloatLabel>
            </div>

            <transition name="fade">
              <Message v-if="errorMessage" severity="error" :closable="false" class="mb-3">
                {{ errorMessage }}
              </Message>
            </transition>

            <Button
                type="submit"
                label="Login"
                icon="pi pi-sign-in"
                :loading="loading"
                class="w-full"
            />
          </form>
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
/* Main Layout wrapper to handle background and positioning */
.layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-ground); /* Uses PrimeVue theme color */
}

/* Center the login card vertically and horizontally */
.login-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  /* Adds a subtle shadow provided by PrimeVue styles, or you can add custom: */
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
  margin-bottom: 1.5rem;
  color: var(--text-color-secondary);
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 2rem; /* Spacing between inputs */
  padding-top: 1rem;
}

.field {
  width: 100%;
}

/* Helper to ensure inputs take full width */
.w-full {
  width: 100%;
}

/* Simple fade transition for the error message */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>