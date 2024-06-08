<script setup lang="ts">
import { computed, ref } from "vue";
import ThemeSwitcher from "./ThemeSwitcher.vue";

const navbarShown = ref<boolean>(false);
const navbarMobileClass = computed(() => (navbarShown.value ? "mobile-shown" : "mobile-hidden"));
</script>

<template>
    <nav class="navbar" :class="navbarMobileClass">
        <div class="navbar-mobile-topbar">
            <span class="name">TenseTiger</span>
            <button class="mobile-toggle-button" @click="navbarShown = !navbarShown">
                <i class="ri-menu-line"></i>
            </button>
        </div>
        <ul class="navbar-items" :class="navbarMobileClass">
            <li class="li-name">
                <RouterLink :to="{ name: 'home' }">
                    <span class="name">TenseTiger</span>
                </RouterLink>
            </li>

            <li>
                <RouterLink :to="{ name: 'home' }" @click="navbarShown = false"
                    ><i class="ri-home-line"></i> Home</RouterLink
                >
            </li>
            <li>
                <RouterLink :to="{ name: 'learn' }" @click="navbarShown = false"
                    ><i class="ri-play-line"></i> Resume Round</RouterLink
                >
            </li>
            <li>
                <RouterLink :to="{ name: 'leaderboard' }" @click="navbarShown = false"
                    ><i class="ri-vip-crown-line"></i> Leaderboard</RouterLink
                >
            </li>
            <span class="sep">|</span>
            <li class="theme-switcher">
                <ThemeSwitcher></ThemeSwitcher>
            </li>
        </ul>
    </nav>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";
@import "@/assets/main.scss";

.navbar {
    display: flex;
    align-items: center;
}

.navbar-items {
    padding: 0;
    margin: var(--padding-lg);
    list-style-type: none;
    display: flex;
    align-items: center;
    gap: var(--gap-lg);
    overflow: hidden;
    flex: 1;

    transition:
        max-height 200ms,
        background-color 200ms;
}

.name {
    font-family: var(--font-headings);
}

.li-name {
    flex: 1;
}

.navbar-mobile-topbar {
    display: none;
}

@media screen and (max-width: $bp-mobile) {
    .li-name {
        display: none;
    }

    .navbar-items {
        gap: var(--gap-sm);
    }

    .mobile-hidden .navbar-items {
        max-height: 0;
    }

    nav.navbar {
        display: block;
        text-align: center;
        transition:
            background-color 200ms,
            color 200ms;

        .theme-switcher {
            margin: 0;
        }
    }

    nav.mobile-shown {
        background-color: var(--color-accent-primary);
        color: var(--color-contrast-primary);

        a {
            color: var(--color-contrast-primary);
        }
    }

    .mobile-shown .navbar-items {
        max-height: 30em;
    }

    .mobile-toggle-button {
        --color: 0, 0, 0;
        @include button-style-outlined-inv(var(--color), var(--color-text), 0, #0003);
        padding: var(--padding-sm);
        line-height: 1;
    }

    .navbar-mobile-topbar {
        display: block;
        margin: var(--padding-lg);
        position: relative;
        text-align: center;

        button {
            position: absolute;
            right: 0;
            top: 0;
        }
    }

    .navbar-items {
        flex-direction: column;
    }

    .sep {
        display: none;
    }
}
</style>
