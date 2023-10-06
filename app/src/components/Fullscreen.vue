<script setup lang="ts">
import Centered from "./Centered.vue";

interface Props {
    center?: boolean;
}
const props = withDefaults(defineProps<Props>(), { center: false });
</script>

<template>
    <component :is="center ? Centered : 'div'" class="container">
        <slot></slot>
    </component>
</template>

<style lang="scss" scoped>
.container {
    width: 100vw;
    height: 100vh;
}
</style>
