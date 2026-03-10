import * as React from "react";
import { cn } from "../../lib/utils";

const Footer = React.forwardRef<
  HTMLElement,
  React.HTMLAttributes<HTMLElement>
>(({ className, ...props }, ref) => (
  <footer
    ref={ref}
    className={cn(
      "border-t bg-background px-4 py-6 sm:px-6 lg:px-8",
      className
    )}
    {...props}
  />
));
Footer.displayName = "Footer";

const FooterContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "mx-auto flex max-w-screen-lg flex-col items-center gap-4 sm:flex-row sm:justify-between",
      className
    )}
    {...props}
  />
));
FooterContent.displayName = "FooterContent";

const FooterText = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
FooterText.displayName = "FooterText";

const FooterLinks = React.forwardRef<
  HTMLElement,
  React.HTMLAttributes<HTMLElement>
>(({ className, ...props }, ref) => (
  <nav
    ref={ref}
    className={cn("flex gap-4", className)}
    {...props}
  />
));
FooterLinks.displayName = "FooterLinks";

const FooterLink = React.forwardRef<
  HTMLAnchorElement,
  React.AnchorHTMLAttributes<HTMLAnchorElement>
>(({ className, ...props }, ref) => (
  <a
    ref={ref}
    className={cn(
      "text-sm text-muted-foreground transition-colors hover:text-foreground",
      className
    )}
    {...props}
  />
));
FooterLink.displayName = "FooterLink";

export { Footer, FooterContent, FooterText, FooterLinks, FooterLink };
