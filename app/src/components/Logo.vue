<template>
    <!-- <h1 class="contrast">TenseTiger</h1> -->
    <img id="logo" src="/public/logo/Logo_Body_Fill_Text_Color.png" alt="TenseTiger Logo" />
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
@import "@/assets/base.scss";

#logo {
    margin-left: auto;
    margin-right: auto;
    width: min(80%, 20em);
}

@media screen and (max-width: $bp-mobile) {
    h1 {
        width: min-content;
        margin-left: auto;
        margin-right: auto;
        line-height: 1;
    }
}
</style>
