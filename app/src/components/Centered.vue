<script setup lang="ts"></script>

<template>
    <div class="center-container">
        <div class="center-content">
            <slot></slot>
        </div>
    </div>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";

.center-container {
    width: 100%;
    height: 100%;
    flex: 1;

    display: flex;
    justify-content: center;
    align-items: center;

    text-align: center;
}

.center-content {
    width: 100%;
}

@media screen and (max-width: $bp-mobile) {
    .center-container {
        align-items: flex-start !important;
    }
}
</style>
