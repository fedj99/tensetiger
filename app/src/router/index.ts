import AttributionsView from "@/views/AttributionsView.vue";
import LeaderboardView from "@/views/LeaderboardView.vue";
import LearnView from "@/views/LearnView.vue";
import LoginView from "@/views/LoginView.vue";
import BadRequestView from "@/views/errors/BadRequestView.vue";
import GenericErrorView from "@/views/errors/GenericErrorView.vue";
import InternalServerErrorView from "@/views/errors/InternalServerErrorView.vue";
import NotFoundView from "@/views/errors/NotFoundView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        // Main
        {
            path: "/",
            name: "home",
            component: LoginView,
        },
        {
            path: "/login",
            name: "login",
            redirect: { name: "home" },
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

        // Misc
        {
            path: "/attributions",
            name: "attributions",
            component: AttributionsView,
        },

        // Errors
        {
            path: "/not-found",
            name: "not-found",
            component: NotFoundView,
        },
        {
            path: "/bad-request",
            name: "bad-request",
            component: BadRequestView,
        },
        {
            path: "/internal-server-error",
            name: "internal-server-error",
            component: InternalServerErrorView,
        },
        {
            path: "/error",
            name: "generic-error",
            component: GenericErrorView,
        },
        {
            path: "/:catchAll(.*)",
            redirect: "/notfound",
        },
    ],
});

export default router;
