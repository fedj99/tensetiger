<script setup lang="ts">
import "@/assets/components.scss";

import { login } from "@/api";
import AxiosErrorWidget from "@/components/AxiosErrorWidget.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import Logo from "@/components/Logo.vue";
import type { AxiosError } from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useCookies } from "vue3-cookies";

const router = useRouter();
const cookies = useCookies().cookies;

const loading = ref(false);
const error = ref<AxiosError>();

const userName = ref("");

async function start() {
    if (!userName.value) {
        alert("Please enter a username");
    }
    // Log in user, this will set the cookies
    loading.value = true;
    await login(userName.value)
        .catch((e) => {
            error.value = e;
            throw e;
        })
        .finally(() => (loading.value = false));

    // Go to learning page
    router.push({ name: "learn" });
}

onMounted(() => {
    const cachedUserName = cookies.get("username");
    if (cachedUserName) {
        userName.value = cachedUserName;
    }
});
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
            <form class="form" action="" @submit.prevent="start()">
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
                    <i class="ri-arrow-right-double-line"></i> Start Learning
                </button>
            </form>

            <RouterLink
                :to="{ name: 'leaderboard' }"
                class="link-leaderboard button button-large button-accent-secondary"
                style="font-weight: normal"
            >
                See Leaderboard
            </RouterLink>
        </main>
    </Fullscreen>
</template>

<style lang="scss" scoped>
@import "@/assets/components.scss";
@import "@/assets/base.scss";

.main {
    width: min(90vw, 50em);
    position: relative;
}

.form {
    width: 100%;

    display: flex;
    align-items: stretch;
    gap: var(--gap);
}

.link-leaderboard {
    margin-top: 5em;
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
