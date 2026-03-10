import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from 'ink-testing-library';
import { GreetCommand } from '../src/commands/Greet.js';

describe('GreetCommand', () => {
  it('renders greeting with name', () => {
    const { lastFrame } = render(<GreetCommand name="World" />);
    expect(lastFrame()).toContain('Hello, World!');
  });

  it('renders loud greeting in uppercase', () => {
    const { lastFrame } = render(<GreetCommand name="World" loud />);
    expect(lastFrame()).toContain('HELLO, WORLD!');
  });
});
