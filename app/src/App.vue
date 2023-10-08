<script setup lang="ts">
import { computed } from "vue";
import { RouterView, useRoute } from "vue-router";
import Footer from "./components/Footer.vue";
import NavBar from "./components/NavBar.vue";

const route = useRoute();

const showNavBar = computed(() => route.name != "home");
</script>

<template>
    <NavBar v-if="showNavBar"></NavBar>
    <RouterView />
    <Footer></Footer>
</template>

<style></style>
