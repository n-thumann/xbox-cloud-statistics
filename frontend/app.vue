<script setup lang="ts">
useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk
      ? `${titleChunk} - Xbox Cloud Statistics`
      : "Xbox Cloud Statistics";
  },
});
</script>

<template>
  <div>
    <NuxtPage />
  </div>
</template>
