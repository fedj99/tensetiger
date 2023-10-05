<script setup lang="ts">
import "@/assets/components.scss";

import { login } from "@/api";
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import Logo from "@/components/Logo.vue";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useCookies } from "vue3-cookies";

const router = useRouter();
const cookies = useCookies().cookies;

const userName = ref("");

async function start() {
    if (!userName.value) {
        alert("Please enter a username");
    }
    // Log in user, this will set the cookies
    await login(userName.value);

    // Go to learning page
    router.push({
        name: "learn",
    });
}

onMounted(() => {
    const cachedUserName = cookies.get("username");
    if (cachedUserName) {
        userName.value = cachedUserName;
    }
});
</script>

<template>
    <Fullscreen>
        <Centered>
            <main class="main">
                <Logo></Logo>
                <form class="form" action="" @submit.prevent="start()">
                    <input
                        v-model="userName"
                        required
                        class="input-huge"
                        style="flex: 1"
                        id="username"
                        type="text"
                        placeholder="Enter a username..."
                    />
                    <input class="input-huge" type="submit" value="Start Learning" />
                </form>
            </main>
        </Centered>
    </Fullscreen>
</template>

<style lang="scss" scoped>
@import "@/assets/components.scss";

.main {
    width: min(90vw, 50em);
}

.form {
    width: 100%;

    display: flex;
    align-items: stretch;
    gap: var(--gap);
}
</style>
