<script setup lang="ts">
import "chartjs-adapter-dayjs-4/dist/chartjs-adapter-dayjs-4.esm";
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  TimeScale,
  Title,
  Tooltip,
  type ChartDataset,
  type ChartOptions,
  type Point,
  type TooltipItem,
} from "chart.js";
import { Line } from "vue-chartjs";
import { useDate } from "~/composables/useDate";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
);

defineProps<{
  chartData: ChartDataset<"line", Point[]>[];
}>();

const chartOptions: ChartOptions<"line"> = {
  animation: false,
  elements: {
    point: {
      radius: 0,
      hitRadius: 5,
    },
    line: {
      borderWidth: 2,
    },
  },
  scales: {
    x: {
      type: "time",
      grid: {
        display: false,
      },
    },
    y: {
      beginAtZero: true,
      grid: {
        display: false,
      },
      ticks: {
        callback: (value) => useDate(value),
        count: 4,
      },
    },
  },
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      callbacks: {
        title: (tooltipItems: TooltipItem<"line">[]) =>
          new Date(tooltipItems[0].parsed.x).toLocaleString(),
        label: (tooltopItem: TooltipItem<"line">) =>
          `Wait time for ${tooltopItem.dataset.label}: ` +
          `${useDate(tooltopItem.parsed.y, true)}`,
      },
    },
  },
};
</script>

<template>
  <Line :data="{ datasets: chartData }" :options="chartOptions" />
</template>
