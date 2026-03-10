import type { Preview } from "@storybook/react";
import { withThemeByClassName } from "@storybook/addon-themes";
import "../src/globals.css";

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    layout: "centered",
    backgrounds: {
      default: "dark",
      values: [
        { name: "light", value: "hsl(0 0% 100%)" },
        { name: "dark", value: "hsl(240 10% 3.9%)" },
      ],
    },
  },
  decorators: [
    withThemeByClassName({
      themes: {
        light: "",
        dark: "dark",
      },
      defaultTheme: "dark",
    }),
  ],
};

export default preview;
