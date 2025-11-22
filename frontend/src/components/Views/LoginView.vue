<script setup>
import SimpleMenu from "@/components/SimpleMenu.vue";
import { ref } from 'vue';
import { useRouter } from "vue-router";
import {useUserStore} from "@/Stores/UserStore.js";
const router = useRouter();
const login = ref('');
const password = ref('');
const errorMessage = ref('');
function handleLogin() {
  if (login.value === 'admin' && password.value === 'admin') {
    errorMessage.value = '';
    useUserStore().testEntry();
    router.push('/home');
  } else {
    errorMessage.value = 'Invalid email or password';
    useUserStore().logout();
  }
}
</script>

<template>
  <SimpleMenu />
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="login">Username:</label>
        <input
            type="text"
            id="login"
            v-model="login"
            placeholder="Enter your username"
            required
        />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
        />
      </div>

      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 12px;
  background-color: #03023a;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

input {
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 0.25rem;
}

button {
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
