import LeaderboardView from "@/views/LeaderboardView.vue";
import LearnView from "@/views/LearnView.vue";
import LoginView from "@/views/LoginView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            redirect: { name: "login" },
        },
        {
            path: "/login",
            name: "login",
            component: LoginView,
        },
        {
            path: "/learn",
            name: "learn",
            component: LearnView,
        },
        {
            path: "/leaderboard",
            name: "leaderboard",
            component: LeaderboardView,
        },
    ],
});

export default router;
