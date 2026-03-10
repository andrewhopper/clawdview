import * as React from "react";
import { cn } from "../../lib/utils";

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl" | "full";
}

const Container = React.forwardRef<HTMLDivElement, ContainerProps>(
  ({ className, size = "lg", ...props }, ref) => {
    const sizes = {
      sm: "max-w-screen-sm",
      md: "max-w-screen-md",
      lg: "max-w-screen-lg",
      xl: "max-w-screen-xl",
      full: "max-w-full",
    };

    return (
      <div
        ref={ref}
        className={cn("mx-auto w-full px-4 sm:px-6 lg:px-8", sizes[size], className)}
        {...props}
      />
    );
  }
);
Container.displayName = "Container";

export { Container };
