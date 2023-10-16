<script setup lang="ts">
import { login as apiLogin, logout as apiLogout } from "@/api";
import { bugpilotLogin, bugpilotLogout } from "@/bugpilot";
import Fullscreen from "@/components/Fullscreen.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import Logo from "@/components/Logo.vue";
import Modal from "@/components/Modal.vue";
import { useErrorsStore } from "@/stores/errors";
import { useGameStore } from "@/stores/game";
import type { AxiosError } from "axios";
import { computed, onMounted, ref } from "vue";
import { useCookies } from "vue3-cookies";

const cookies = useCookies().cookies;
const gameStore = useGameStore();
const errorStore = useErrorsStore();

const loading = ref(false);
const authErrorModal = ref<InstanceType<typeof Modal>>();

const username = ref("");
const password = ref("");
const userId = ref<number>(-1);
const loggedIn = computed(() => userId.value != -1);
const startText = computed(() =>
    gameStore.hasSavedGameState() ? "Keep Learning" : "Start Learning"
);

onMounted(() => {
    const loggedInUsername = decodeURI(cookies.get("username"));
    const loggedInUserId = parseInt(decodeURI(cookies.get("user_id")));
    if (loggedInUsername && loggedInUserId) {
        username.value = loggedInUsername;
        userId.value = loggedInUserId;
    }
});

async function login() {
    if (!username.value || !password.value) {
        alert("Please enter a username and password");
    }
    // Log in user, this will set the cookies
    loading.value = true;
    const ans = await apiLogin(username.value, password.value)
        .catch((e: AxiosError) => {
            console.error(e.response);
            if (e.response?.status == 401) {
                // Show error in popup
                authErrorModal.value?.open();
                password.value = "";
            } else {
                // Another error
                errorStore.setError(e);
            }
        })
        .finally(() => (loading.value = false));

    if (ans) {
        const user = ans.data.user;
        username.value = user.username;
        userId.value = user.id;

        bugpilotLogin(user.id, user.username, user.last_logon);
    }

    // Clear input fields
    password.value = "";
}

async function logout() {
    cookies.remove("username");
    cookies.remove("user_id");
    username.value = "";
    userId.value = -1;

    await apiLogout();

    bugpilotLogout();
}
</script>

<template>
    <Fullscreen :center="true">
        <main v-if="loading" class="loading">
            <LoadingSpinner>Please wait while we log you in...</LoadingSpinner>
        </main>
        <main v-else class="main">
            <Logo></Logo>

            <div v-if="!loggedIn">
                <form class="form" action="" @submit.prevent="login()">
                    <input
                        id="username"
                        v-model="username"
                        required
                        class="input-huge"
                        type="text"
                        placeholder="Username"
                        maxlength="32"
                    />
                    <input
                        id="password"
                        v-model="password"
                        type="password"
                        name="password"
                        required
                        class="input-huge"
                        placeholder="Password"
                    />
                    <button type="submit" class="button-huge">
                        <i class="ri-login-box-line"></i> Log in
                    </button>
                </form>

                <p class="sans">
                    Log in with a username and password. If this is your first time, you will be
                    registered automatically.
                </p>
            </div>

            <div v-else>
                <h2 class="greeting">
                    Welcome back, <span class="color-secondary">{{ username }}</span
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

    <Modal ref="authErrorModal" :buttons="[{ text: 'OK', role: 'confirm' }]">
        Wrong password
    </Modal>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";

.greeting {
    font-size: var(--font-size-large);
    font-family: var(--font-default-sans);
}

.main {
    width: min(100%, 50em);
    margin: auto;
    position: relative;
    padding: var(--padding-lg);
}

.form {
    width: 100%;

    gap: var(--gap);
    display: grid;
    grid-template-columns: auto max-content;
    grid-template-rows: 1fr 1fr;
    grid-auto-flow: column;

    [type="submit"] {
        grid-row: 1 / span 2;
    }
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
        display: flex;
        flex-direction: column;

        input {
            text-align: center;
        }
    }
}
</style>
