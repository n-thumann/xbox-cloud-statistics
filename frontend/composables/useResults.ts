import { Point } from "chart.js";

const MAX_DAYS = 3;
const MS_PER_DAY = 1000 * 60 * 60 * 24;

export const useResults = async (gameId: string) => {
  const { data } = await useAsyncData("game" + gameId, () =>
    queryContent("games", gameId.toLowerCase()).find(),
  );

  const results: { [region: string]: { [subscription: string]: Point[] } } = {};

  data.value!.forEach((result) => {
    const region = result.path[3] as string;
    const subscription = result.title as string;

    const points: Point[] = Object.entries(result.body)
      .map(([serverTime, waitTime]) => [
        parseInt(serverTime) * 1000,
        waitTime as number,
      ])
      .filter(
        ([serverTime, _]) => serverTime >= Date.now() - MAX_DAYS * MS_PER_DAY,
      )
      .map(([serverTime, waitTime]) => {
        return { x: serverTime, y: waitTime as number };
      });

    results[region] = results[region] || {};
    results[region][subscription] = points;
  });

  return results;
};
