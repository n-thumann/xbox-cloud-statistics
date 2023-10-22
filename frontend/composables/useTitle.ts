export const useTitle = async (gameId: string) => {
  const meta = await useMeta();
  return meta.games.find((game: any) => game.id === gameId).title;
};
