<script setup lang="ts">
import { RouterView } from "vue-router";
import Footer from "./components/Footer.vue";
import NavBar from "./components/NavBar.vue";
</script>

<template>
    <NavBar></NavBar>
    <RouterView />
    <Footer></Footer>
</template>

<style lang="scss" scoped></style>
