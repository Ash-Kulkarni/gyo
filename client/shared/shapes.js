export const SHAPES = {
  triangle: [
    [-10, 10],
    [10, 10],
    [0, -10],
  ],
  square: [
    [-10, -10],
    [10, -10],
    [10, 10],
    [-10, 10],
  ],
  hexagon: Array.from({ length: 6 }, (_, i) => {
    const angle = (Math.PI * 2 * i) / 6;
    return [Math.cos(angle) * 10, Math.sin(angle) * 10];
  }),
};
