import * as React from "react";
import { cn } from "../../lib/utils";

interface SidebarProps extends React.HTMLAttributes<HTMLElement> {
  collapsed?: boolean;
}

const Sidebar = React.forwardRef<HTMLElement, SidebarProps>(
  ({ className, collapsed = false, ...props }, ref) => (
    <aside
      ref={ref}
      className={cn(
        "flex h-full flex-col border-r bg-background transition-all duration-300",
        collapsed ? "w-16" : "w-64",
        className
      )}
      {...props}
    />
  )
);
Sidebar.displayName = "Sidebar";

const SidebarHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex h-16 items-center border-b px-4", className)}
    {...props}
  />
));
SidebarHeader.displayName = "SidebarHeader";

const SidebarContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex-1 overflow-auto py-4", className)}
    {...props}
  />
));
SidebarContent.displayName = "SidebarContent";

const SidebarFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("border-t p-4", className)}
    {...props}
  />
));
SidebarFooter.displayName = "SidebarFooter";

const SidebarNav = React.forwardRef<
  HTMLElement,
  React.HTMLAttributes<HTMLElement>
>(({ className, ...props }, ref) => (
  <nav
    ref={ref}
    className={cn("flex flex-col gap-1 px-2", className)}
    {...props}
  />
));
SidebarNav.displayName = "SidebarNav";

interface SidebarNavItemProps extends React.HTMLAttributes<HTMLAnchorElement> {
  href?: string;
  active?: boolean;
  icon?: React.ReactNode;
}

const SidebarNavItem = React.forwardRef<HTMLAnchorElement, SidebarNavItemProps>(
  ({ className, active = false, icon, children, href = "#", ...props }, ref) => (
    <a
      ref={ref}
      href={href}
      className={cn(
        "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
        active
          ? "bg-accent text-accent-foreground"
          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
        className
      )}
      {...props}
    >
      {icon && <span className="h-4 w-4">{icon}</span>}
      {children}
    </a>
  )
);
SidebarNavItem.displayName = "SidebarNavItem";

export {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarNav,
  SidebarNavItem,
};
