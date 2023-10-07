<script setup lang="ts">
import { computed } from "vue";

type SpinnerAnimationName = "circle-1" | "circle-2" | "circle-3";

interface Props {
    spinner?: SpinnerAnimationName;
    color?: string;
}

const props = withDefaults(defineProps<Props>(), {
    spinner: "circle-2",
    color: "var(--color-accent-secondary)",
});
const loaderStyle = computed(() => ({ "--spinner-color": props.color }));
</script>

<template>
    <span class="spinner-frame">
        <div class="spinner" :class="spinner" :style="loaderStyle"></div>
        <div>
            <slot></slot>
        </div>
    </span>
</template>

<style lang="scss" scoped>
@import "@/assets/spinners/circle-1.scss";
@import "@/assets/spinners/circle-2.scss";
@import "@/assets/spinners/circle-3.scss";
.spinner-frame {
    padding: var(--padding);
}
</style>
