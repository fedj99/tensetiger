<template>
    <div class="container">
        <div class="content">
            <slot></slot>
        </div>
    </div>
</template>

<script setup lang="ts">

</script>

<style lang="scss" scoped>
.container {
    width: 100%;
    height: 100%;

    display: flex;
    justify-content: center;
    align-items: center;
}

.content {
    text-align: center;
}
</style>
