<script setup lang="ts">
const meta = await useMeta();
const lastUpdate = meta.last_update;
const games = meta.games;
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <div class="max-w-6xl mx-auto p-6 lg:p-20">
      <h1 class="text-3xl font-bold uppercase text-center pb-2 lg:text-4xl">
        Xbox Cloud Statistics
      </h1>

      <div class="w-28 mx-auto bg-xbox pb-1 mb-10 lg:mb-12" />

      <div
        class="grid gap-4 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:gap-6"
      >
        <NuxtLink
          v-for="game in games"
          :key="game.id"
          :to="`/games/${game.id}/`"
          :title="game.title"
          class="overflow-hidden relative group/game"
        >
          <img
            :src="game.image_url"
            :alt="game.title"
            class="transition-transform duration-700 group-hover/game:scale-110 group-hover/game:rotate-2"
          />

          <div
            class="absolute inset-0 bg-xbox h-full w-full transition-opacity duration-700 opacity-0 group-hover/game:opacity-50"
          />
        </NuxtLink>
      </div>
    </div>

    <Footer :last-update="lastUpdate" />
  </div>
</template>
