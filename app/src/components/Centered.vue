<template>
    <div class="center-container">
        <div class="center-content">
            <slot></slot>
        </div>
    </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.center-container {
    width: 100%;
    height: 100%;
    min-height: 100vh;

    display: flex;
    justify-content: center;
    align-items: center;

    text-align: center;
}
</style>
