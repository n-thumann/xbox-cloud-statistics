<script setup lang="ts">
import { ChartDataset, Point } from "chart.js";
import colors from "#tailwind-config/theme/colors";

const gameId = useRoute().params.game as string;

const meta = await useMeta();
const lastUpdate = meta.last_update;

const title = await useTitle(gameId);
const results = await useResults(gameId);

useSeoMeta({
  title,
  description: `View the current wait times for ${title} on Xbox Cloud.`,
});

const getDatasets = (subscriptions: any) => {
  return Object.entries(subscriptions).map(([subscription, points]) => {
    const color = subscription === "F2P" ? colors.green : colors.purple;
    return {
      label: subscription,
      data: points,
      borderColor: color,
      backgroundColor: color,
    };
  }) as ChartDataset<"line", Point[]>[];
};

const getWaitTimes = (subscriptions: { [subscription: string]: Point[] }) => {
  const waitTimes: { [subscription: string]: number } = {};

  Object.entries(subscriptions).forEach(([subscription, points]) => {
    waitTimes[subscription] = points.at(-1)!.y;
  });

  return waitTimes;
};
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <div class="max-w-6xl p-8 lg:self-center lg:w-[72rem]">
      <NuxtLink to="/" title="homepage" class="mb-6 text-5xl">
        &lsaquo;
      </NuxtLink>
      <h1 class="text-3xl font-bold uppercase text-center pb-2 lg:text-4xl">
        {{ title }}
      </h1>

      <div class="w-28 mx-auto bg-xbox pb-1 mb-10 lg:mb-12" />

      <div class="grid gap-6 lg:grid-cols-2">
        <div
          v-for="(subscriptions, region) in results"
          :key="region"
          class="relative shadow-xl rounded-md m-4"
        >
          <h2 class="text-2xl font-bold mb-1">
            {{ region }}
          </h2>

          <div class="text-neutral-300 text-xs mb-6">
            <div class="font-bold">Current wait time:</div>

            <div
              v-for="(waitTime, subscription) in getWaitTimes(subscriptions)"
              :key="subscription"
            >
              {{ useDate(waitTime) }} ({{ subscription }})
            </div>
          </div>

          <Chart :chart-data="getDatasets(subscriptions)" />
        </div>
      </div>
    </div>

    <Footer :last-update="lastUpdate" />
  </div>
</template>
