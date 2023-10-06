<script setup lang="ts">
import Centered from "./Centered.vue";

interface Props {
    center?: boolean;
}
const props = withDefaults(defineProps<Props>(), { center: false });
</script>

<template>
    <div class="fullscreen-container">
        <Centered v-if="center">
            <slot></slot>
        </Centered>
        <slot v-else></slot>
        <!-- <component :is="center ? Centered : 'div'" class="container">
            <slot></slot>
        </component> -->
    </div>
</template>

<style lang="scss" scoped>
.fullscreen-container {
    min-height: 100vh;
    min-width: 100vw;
}
</style>
