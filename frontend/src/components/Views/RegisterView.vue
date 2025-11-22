<script setup>
import SimpleMenu from "@/components/SimpleMenu.vue";
import { ref } from 'vue';
import {useRouter} from "vue-router";
const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');

function handleRegister() {
  if (!username.value || !email.value || !password.value || !confirmPassword.value) {
    errorMessage.value = 'All fields are required';
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match';
    return;
  }

  // Simple demo logic
  alert(`User ${username.value} registered successfully!`);
  errorMessage.value = '';

  // Reset fields
  username.value = '';
  email.value = '';
  password.value = '';
  confirmPassword.value = '';
  router.push('/home');
}
</script>

<template>
  <SimpleMenu />

  <div class="login-container">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister" class="login-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter your username"
            required
        />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Enter your email"
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

      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="Confirm your password"
            required
        />
      </div>

      <button type="submit">Register</button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p class="signup-link">
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>
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

.signup-link {
  margin-top: 1rem;
}
</style>
