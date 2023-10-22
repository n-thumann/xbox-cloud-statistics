export const useMeta = async () => {
  const { data } = await useAsyncData("meta", () =>
    queryContent("meta").findOne(),
  );

  return data.value?.body as unknown as { games: any[]; last_update: number };
};
