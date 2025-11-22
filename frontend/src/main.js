import { createApp } from 'vue'
import App from './App.vue'
import LoginView from "@/components/Views/LoginView.vue";
import HomeView from "@/components/Views/HomeView.vue";
import PrimeVue from 'primevue/config';
import { createWebHashHistory, createRouter } from 'vue-router'
import StartView from "@/components/Views/StartView.vue";
import RegisterView from "@/components/Views/RegisterView.vue";
import NewProjectView from "@/components/Views/NewProjectView.vue";
import NewPasswordView from "@/components/Views/NewPasswordView.vue";
import ProjectView from "@/components/Views/ProjectView.vue";
import { createPinia } from 'pinia'
import darkBlue from "@/darkBlue.js";
import 'primeicons/primeicons.css'
import {useUserStore} from "@/Stores/UserStore.js";
import Logout from "@/components/Logout.vue";
const AuthGuard = (to, from) => {
    return useUserStore().isLoggedIn();
}

const routes = [
    { path: '/', component: App, redirect: '/start', },
    { path: '/start', component: StartView },
    { path: '/login', component: LoginView },
    { path: '/home', component: HomeView, beforeEnter: AuthGuard },
    { path: '/register', component: RegisterView },
    { path: '/new_project', component: NewProjectView, beforeEnter: AuthGuard },
    { path: '/new_password', component: NewPasswordView, beforeEnter: AuthGuard },
    { path: '/project/:id', component: ProjectView, beforeEnter: AuthGuard, props: true },
    { path: '/logout', component: Logout, beforeEnter: AuthGuard },
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes,
});
const pinia = createPinia();
const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: darkBlue,
    }
});
app.use(router);
app.use(pinia);
app.mount('#app');