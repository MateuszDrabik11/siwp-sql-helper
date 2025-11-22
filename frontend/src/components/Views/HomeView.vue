<script setup>
import ExtendedMenu from "@/components/ExtendedMenu.vue";
import {Button} from "primevue";
import Drawer from 'primevue/drawer';
import {ref} from "vue";
import ProjectItem from "@/components/ProjectItem.vue";
import {useUserStore} from "@/Stores/UserStore.js";
const userStore = useUserStore();
const user = userStore.getUser;
let visible = ref(false);
let projects = ref([
    {
      id: 1,
      name: "abc"
    },
  {
    id: 2,
    name: "def"
  },
  {
    id: 3,
    name: "ghi"
  },
  {
    id: 4,
    name: "jkl"
  }
]);
</script>

<template>
  <ExtendedMenu/>
  <div class="drawer">
    <div class="container">
      <div>
        <Drawer v-model:visible="visible" header="Your projects">
          <div class="project-list">
            <ProjectItem class="items"
                v-for="p in projects"
                :key="p.id"
                :project="p"
            />
          </div>
        </Drawer>
      </div>
      <Button icon="pi pi-arrow-right" @click="visible = true" />
    </div>
  </div>
  <div class="fullscreen">
    Hello {{user.username}}!
  </div>
</template>

<style scoped>
.drawer {
  display: block;
  margin-top: 10px;
  gap: 10rem;
}
.container {
  display: flex;
  margin: 10px;
  flex-direction: column;
  gap: 0.3rem;
  justify-content: space-between;
  align-items: flex-start;
}
.project-list {
  padding: 10px;
}
.fullscreen {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  padding: 1rem;
}
</style>