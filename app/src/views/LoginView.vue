<script setup lang="ts">
import "@/assets/components.scss";

import { login as apiLogin } from "@/api";
import AxiosErrorWidget from "@/components/AxiosErrorWidget.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import Logo from "@/components/Logo.vue";
import { useGameStore } from "@/stores/game";
import type { AxiosError } from "axios";
import { computed, onMounted, ref } from "vue";
import { useCookies } from "vue3-cookies";

const cookies = useCookies().cookies;
const gameStore = useGameStore();

const loading = ref(false);
const error = ref<AxiosError>();

const userName = ref("");
const userId = ref<number>(-1);
const loggedIn = computed(() => userId.value != -1);
const startText = computed(() =>
    gameStore.hasSavedGameState() ? "Keep Learning" : "Start Learning"
);

onMounted(() => {
    const loggedInUsername = decodeURI(cookies.get("username"));
    const loggedInUserId = parseInt(decodeURI(cookies.get("user_id")));
    if (loggedInUsername && loggedInUserId) {
        userName.value = loggedInUsername;
        userId.value = loggedInUserId;
    }
});

async function login() {
    if (!userName.value) {
        alert("Please enter a username");
    }
    // Log in user, this will set the cookies
    loading.value = true;
    const ans = await apiLogin(userName.value)
        .catch((e) => {
            error.value = e;
            throw e;
        })
        .finally(() => (loading.value = false));

    userName.value = ans.data.user.username;
    userId.value = ans.data.user.id;
}

function logout() {
    cookies.remove("username");
    cookies.remove("user_id");
    userName.value = "";
    userId.value = -1;
}
</script>

<template>
    <Fullscreen :center="true">
        <main v-if="error">
            <AxiosErrorWidget :error="error"></AxiosErrorWidget>
        </main>
        <main v-else-if="loading" class="loading">
            <LoadingSpinner>Please wait while we log you in...</LoadingSpinner>
        </main>
        <main v-else class="main">
            <Logo></Logo>
            <form v-if="!loggedIn" class="form" action="" @submit.prevent="login()">
                <input
                    id="username"
                    v-model="userName"
                    required
                    class="input-huge"
                    style="flex: 1"
                    type="text"
                    placeholder="Enter a username..."
                    maxlength="32"
                />
                <button type="submit" class="input-huge">
                    <i class="ri-login-box-line"></i> Log in
                </button>
            </form>

            <div v-else>
                <h2 class="greeting">
                    Welcome back, <span class="color-secondary">{{ userName }}</span
                    >!
                </h2>

                <div class="buttons">
                    <RouterLink :to="{ name: 'learn' }" class="button button-huge success">
                        <i class="ri-arrow-right-double-line"></i> {{ startText }}
                    </RouterLink>

                    <RouterLink
                        :to="{ name: 'leaderboard' }"
                        class="link-leaderboard button outlined"
                    >
                        <i class="ri-vip-crown-fill"></i> See Leaderboard
                    </RouterLink>

                    <button class="danger outlined" @click="logout()">
                        <i class="ri-logout-box-r-fill"></i> Logout
                    </button>
                </div>
            </div>
        </main>
    </Fullscreen>
</template>

<style lang="scss" scoped>
@import "@/assets/components.scss";
@import "@/assets/base.scss";

.greeting {
    font-size: var(--font-size-large);
    font-family: var(--font-default-sans);
}

.main {
    width: min(100%, 50em);
    margin: auto;
    position: relative;
}

.form {
    width: 100%;

    display: flex;
    align-items: stretch;
    gap: var(--gap);
}

.buttons {
    max-width: 16em;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: var(--gap-lg);
}

@media screen and (max-width: $bp-mobile) {
    .form {
        flex-direction: column;

        input {
            text-align: center;
        }
    }
}
</style>
