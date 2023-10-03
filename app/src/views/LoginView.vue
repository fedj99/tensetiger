<script setup lang="ts">
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import Logo from "@/components/Logo.vue";

</script>

<template>
    <Fullscreen>
        <Centered>
            <main>
                <Logo></Logo>
                <form>
                    <label for="username"><span>Benutzername</span> <input id="username" type="text"></label>
                    <input type="submit" value="OK!">
                </form>
            </main>
        </Centered>
    </Fullscreen>
</template>
