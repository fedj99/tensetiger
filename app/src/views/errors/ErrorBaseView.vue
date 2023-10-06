<script setup lang="ts">
import Fullscreen from "@/components/Fullscreen.vue";

interface Props {
    imageName?: string;
    imageAlt?: string;
}

const props = withDefaults(defineProps<Props>(), {
    imageName: "sorry",
    imageAlt: "Error",
});

function makeImageURL(imageName: string) {
    return new URL(`../../assets/img/errors/${imageName}.svg`, import.meta.url).href;
}
</script>

<template>
    <Fullscreen :center="true">
        <main class="base">
            <img :src="makeImageURL(imageName)" :alt="props.imageAlt" />
            <p><slot>Aw, shucks! Something went wrong on our end.</slot></p>
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
