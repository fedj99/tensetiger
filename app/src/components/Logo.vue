<template>
    <h1 class="contrast">TenseTiger</h1>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
@import "@/assets/base.scss";

@media screen and (max-width: $bp-mobile) {
    h1 {
        width: min-content;
        margin-left: auto;
        margin-right: auto;
        line-height: 1;
    }
}
</style>
