import { describe, it, expect } from 'vitest';
import { input } from '../input.js';

describe('input system', () => {
  it('should have default input state', () => {
    expect(input).toEqual({ vx: 0, vy: 0, angle: 0 });
  });
});
