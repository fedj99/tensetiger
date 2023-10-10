<script setup lang="ts">
import Fullscreen from "@/components/Fullscreen.vue";
</script>

<template>
    <Fullscreen center>
        <main>
            <h1>Attributions</h1>

            <h2>Website Design</h2>
            <p>
                <a href="https://n.ethz.ch/~fmantova" target="_blank">Federico Mantovani</a>
            </p>

            <h2>Lesson Content</h2>
            <p>
                <a href="mailto:cristina.comino@hispeed.ch" target="_blank">Cristina Comino</a>
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
                <li>
                    <a
                        href="https://www.freepik.com/free-vector/feeling-sorry-concept-illustration_10386553.htm#page=3&query=error&position=42&from_view=author"
                        >Image by storyset</a
                    >
                    on Freepik
                </li>
                <li>Using the <a href="https://remixicon.com/">Remix Icon</a> icon pack</li>
            </ul>
        </main>
    </Fullscreen>
</template>

<style lang="scss" scoped>
main {
    max-width: min(100%, 50em);
    padding: var(--padding-lg);
}

h1 {
    max-width: 100%;
    overflow-wrap: break-word;
    font-size: var(--font-size-huge);
}

h2 {
    font-size: var(--font-size-large);
    font-family: var(--font-default-serif);
}

ul {
    list-style-type: "⭐   ";
    list-style-position: inside;
    padding: 0;
}

main {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
