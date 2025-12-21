import { defineStore } from 'pinia'
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user: null, //Object
    }),
    persist: true,
    getters: {
        getUser(state) {
            return state.user;
        }
    },
    actions: {
        async login(username, password) {
            try {
                const res = await axios.post('/api/auth/login', { 'username': username, 'password': password });
                this.user = res.data;
            } catch (error) {
                console.error("Login failed:", error);
                throw error;
            }
        },
        logout() {
            this.user = null;
        },
        isLoggedIn() {
            return !!this.user;
        },
        async changePassword(oldPassword, newPassword) {
            try {
                // Ensure we have a user ID from the state
                const userId = this.user?.id ?? 0;

                const res = await axios.post('/api/auth/change-password', {
                    user_id: userId,
                    old_password: oldPassword,
                    new_password: newPassword
                });

                return res.data;
            } catch (error) {
                console.error("Password change failed:", error);
                throw error; // Pass the error back to the component
            }
        },
        testEntry() {
            this.user = {
                username: "admin",
                password: "admin",
                userId: 0,
            };
        }
    }
})