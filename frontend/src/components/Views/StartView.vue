<script setup>
import {Button} from "primevue";
import {useRouter} from "vue-router";
const router = useRouter();
</script>
<template>
  <div class="centered">
    <div>
      <Button label="Login" severity="primary" @click="router.push('/login')"/>
    </div>
    <div>
      <Button label="Register" severity="secondary" @click="router.push('/register')"/>
    </div>
  </div>
</template>

<style scoped>
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}
</style>