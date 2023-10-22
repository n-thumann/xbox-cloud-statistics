export const useDate = (
  seconds: string | number,
  fullTime: boolean = false,
) => {
  if (typeof seconds === "string") {
    seconds = parseInt(seconds);
  }
  return new Date(seconds * 1000)
    .toISOString()
    .slice(seconds >= 3600 || fullTime ? 11 : 14, 19);
};
