import { defineStore } from 'pinia'
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user: null, //Object
        token: null,
    }),
    getters: {
        getToken(state) {
            return state.token;
        },
        getUser(state) {
            return state.user;
        }
    },
    actions: {
        async login(username, password) {
            try {
                const res = await axios.post('/login', { username, password });

                this.token = res.data.token;
                this.user = res.data.user;
            } catch (error) {
                console.error("Login failed:", error);
                throw error;
            }
        },
        logout() {
            this.token = null;
            this.user = null;
        },
        isLoggedIn() {
            return !!this.token;
        },
        testEntry() {
            this.token = 123;
            this.user = {
                username: "admin",
                password: "admin",
                userId: 0,
            };
        }
    }
})