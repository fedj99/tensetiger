<script setup lang="ts"></script>

<template>
    <footer>
        &copy; 2023 <a href="mailto:federico.mantovani@hispeed.ch">Federico Mantovani</a>
        <span class="sep">&mdash;</span> <a href="https://gitlab.com/fettemanto/b3">Source Code</a>
        <span class="sep">&mdash;</span>
        <a href="https://gitlab.com/fettemanto/b3/-/issues/new">Report a bug</a>
        <span class="sep">&mdash;</span>
        <RouterLink :to="{ name: 'attributions' }">Attributions</RouterLink>
    </footer>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";

footer {
    opacity: 0.7;
    text-align: center;
    padding: var(--padding-lg);
}

@media screen and (max-width: $bp-mobile) {
    .sep {
        display: none;
    }

    footer {
        padding: var(--padding);

        * {
            display: block;
        }
    }
}
</style>
