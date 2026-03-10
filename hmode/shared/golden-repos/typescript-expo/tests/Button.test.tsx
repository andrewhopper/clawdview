import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '@/components/ui/Button';
import { ThemeProvider, DefaultTheme } from '@/lib/theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider value={DefaultTheme}>{component}</ThemeProvider>
  );
};

describe('Button', () => {
  it('renders correctly with text', () => {
    const { getByText } = renderWithTheme(<Button>Click me</Button>);
    expect(getByText('Click me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByText } = renderWithTheme(
      <Button onPress={onPress}>Press me</Button>
    );

    fireEvent.press(getByText('Press me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('does not call onPress when disabled', () => {
    const onPress = jest.fn();
    const { getByText } = renderWithTheme(
      <Button onPress={onPress} disabled>
        Disabled
      </Button>
    );

    fireEvent.press(getByText('Disabled'));
    expect(onPress).not.toHaveBeenCalled();
  });

  it('shows loading indicator when loading', () => {
    const { queryByText, getByTestId } = renderWithTheme(
      <Button loading testID="button">
        Loading
      </Button>
    );

    // Text should not be visible when loading
    expect(queryByText('Loading')).toBeNull();
  });

  it('renders all variants', () => {
    const variants = ['default', 'secondary', 'outline', 'ghost', 'destructive', 'link'] as const;

    variants.forEach((variant) => {
      const { getByText } = renderWithTheme(
        <Button variant={variant}>{variant}</Button>
      );
      expect(getByText(variant)).toBeTruthy();
    });
  });
});
