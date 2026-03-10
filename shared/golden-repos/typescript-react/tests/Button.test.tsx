import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../src/components/Button';

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('applies variant styles', () => {
    render(<Button variant="danger">Delete</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('bg-red');
  });

  it('renders with icons', () => {
    render(
      <Button leftIcon={<span data-testid="left-icon">L</span>}>
        With Icon
      </Button>
    );
    expect(screen.getByTestId('left-icon')).toBeInTheDocument();
  });
});
