<script setup lang="ts">
defineProps<{
  lastUpdate: number;
}>();
</script>

<template>
  <footer class="mt-auto pt-4">
    <div class="bg-neutral-950 text-neutral-300 text-center">
      <div class="max-w-6xl mx-auto relative p-6 lg:px-20 lg:py-6">
        <div>
          <div class="font-bold lg:text-lg">Want to change the region?</div>

          Check out
          <a
            href="https://github.com/n-thumann/xbox-cloud-server-selector"
            target="_blank"
          >
            Server Selector for Xbox Cloud Gaming
          </a>
          or
          <a href="https://github.com/redphx/better-xcloud" target="_blank">
            Better xCloud
          </a>
        </div>

        <div class="mt-8 text-xs mb-2 md:mt-10">
          Check out source code and raw data on
          <a
            href="https://github.com/n-thumann/xbox-cloud-statistics"
            target="_blank"
          >
            GitHub
          </a>
        </div>

        <div class="text-xs">
          Last update: {{ new Date(lastUpdate * 1000).toLocaleString() }}
        </div>
      </div>
    </div>
  </footer>
</template>
