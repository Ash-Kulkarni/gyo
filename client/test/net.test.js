import { describe, it, expect } from 'vitest';
import { sendInput } from '../net.js';

describe('network', () => {
  it('sendInput should be a function', () => {
    expect(typeof sendInput).toBe('function');
  });
});
