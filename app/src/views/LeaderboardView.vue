<script setup lang="ts">
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
</script>

<template>
    <Fullscreen>
        <Centered>
            <h1>Good job!</h1>
            <p>Here's how you compare to the top 10</p>
            <div>
                <RouterLink style="display: block" :to="{ name: 'home' }" class="button input-huge"
                    >Play Again!</RouterLink
                >
            </div>
        </Centered>
    </Fullscreen>
</template>

<style lang="scss" scoped>
@import "@/assets/components.scss";
</style>
