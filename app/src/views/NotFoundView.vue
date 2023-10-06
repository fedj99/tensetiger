<script setup lang="ts">
import Fullscreen from "@/components/Fullscreen.vue";
</script>

<template>
    <Fullscreen :center="true">
        <main class="base">
            <img src="@/assets/img/not-found.svg" alt="404 Not Found" />
            <p>You didn't break the internet, but we can't find what you're looking for.</p>
            <RouterLink :to="{ name: 'login' }" class="button"
                ><i class="ri-home-5-fill"></i> Return Home</RouterLink
            >
        </main>
    </Fullscreen>
</template>

<style lang="scss" scoped>
img {
    width: min(80vw, 20em);
}

p {
    margin: 3em 0;
    font-size: var(--font-size-large);
    font-family: var(--font-default-serif);
    font-weight: 500;
}

a {
    padding: var(--padding-huge);
    font-weight: 500;
}
</style>
