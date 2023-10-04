<script setup lang="ts">
import "@/assets/components.scss";

import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import Logo from "@/components/Logo.vue";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const LS_USER_KEY = "username";

const router = useRouter();

const userName = ref("");

function startLearning() {
    console.log(`Logging in ${userName.value}`);
    localStorage.setItem(LS_USER_KEY, userName.value);
    router.push({
        name: "learn",
        query: {
            username: userName.value,
        },
    });
}

onMounted(() => {
    const cachedUserName = localStorage.getItem(LS_USER_KEY);
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
                <form class="form" action="" @submit.prevent="startLearning()">
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
