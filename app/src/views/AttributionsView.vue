<script setup lang="ts">
import Fullscreen from "@/components/Fullscreen.vue";
</script>

<template>
    <Fullscreen center>
        <h1>Attributions</h1>

        <h2>Website Design</h2>
        <p>
            <a href="https://n.ethz.ch/~fmantova" target="_blank">Federico Mantovani</a>
        </p>

        <h2>Word List</h2>
        <p>
            <a href="https://github.com/mre/engldict" target="_blank">Matthias Endler</a>
        </p>

        <h2>Graphics</h2>
        <ul>
            <li>
                <a
                    href="https://www.freepik.com/free-vector/oops-404-error-with-broken-robot-concept-illustration_13315300.htm#query=not%20found&position=7&from_view=search&track=ais"
                    >Image by storyset</a
                >
                on Freepik
            </li>
            <li>
                <a
                    href="https://www.freepik.com/free-vector/400-error-bad-request-concept-illustration_7967799.htm#query=error%20400&position=39&from_view=search&track=ais"
                    >Image by storyset</a
                >
                on Freepik
            </li>
            <li>
                <a
                    href="https://www.freepik.com/free-vector/500-internal-server-error-concept-illustration_13416109.htm#query=server%20error&position=2&from_view=author"
                    >Image by storyset</a
                >
                on Freepik
            </li>
        </ul>
    </Fullscreen>
</template>

<style lang="scss" scoped>
h2 {
    font-size: var(--font-size-large);
    font-family: var(--font-default-serif);
}
</style>
