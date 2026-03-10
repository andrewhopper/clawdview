import type { Meta, StoryObj } from "@storybook/react";
import { Container } from "../src/components/layout/container";
import { Header, HeaderTitle, HeaderNav, HeaderActions } from "../src/components/layout/header";
import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarNav,
  SidebarNavItem,
} from "../src/components/layout/sidebar";
import { Footer, FooterContent, FooterText, FooterLinks, FooterLink } from "../src/components/layout/footer";
import { Button } from "../src/components/ui/button";

const meta = {
  title: "Layout/Components",
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta;

export default meta;

export const HeaderExample: StoryObj = {
  render: () => (
    <Header>
      <HeaderTitle>My App</HeaderTitle>
      <HeaderNav>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-foreground">
          Dashboard
        </a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-foreground">
          Projects
        </a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-foreground">
          Settings
        </a>
      </HeaderNav>
      <HeaderActions>
        <Button variant="outline" size="sm">
          Sign In
        </Button>
      </HeaderActions>
    </Header>
  ),
};

export const SidebarExample: StoryObj = {
  render: () => (
    <div className="h-[500px]">
      <Sidebar>
        <SidebarHeader>
          <span className="text-lg font-semibold">Navigation</span>
        </SidebarHeader>
        <SidebarContent>
          <SidebarNav>
            <SidebarNavItem href="#" active>
              Dashboard
            </SidebarNavItem>
            <SidebarNavItem href="#">Projects</SidebarNavItem>
            <SidebarNavItem href="#">Tasks</SidebarNavItem>
            <SidebarNavItem href="#">Analytics</SidebarNavItem>
            <SidebarNavItem href="#">Settings</SidebarNavItem>
          </SidebarNav>
        </SidebarContent>
        <SidebarFooter>
          <Button variant="outline" className="w-full">
            Logout
          </Button>
        </SidebarFooter>
      </Sidebar>
    </div>
  ),
};

export const FooterExample: StoryObj = {
  render: () => (
    <Footer>
      <FooterContent>
        <FooterText>&copy; 2024 My Company. All rights reserved.</FooterText>
        <FooterLinks>
          <FooterLink href="#">Privacy</FooterLink>
          <FooterLink href="#">Terms</FooterLink>
          <FooterLink href="#">Contact</FooterLink>
        </FooterLinks>
      </FooterContent>
    </Footer>
  ),
};

export const ContainerExample: StoryObj = {
  render: () => (
    <div className="space-y-4">
      <Container size="sm" className="border border-dashed border-border p-4">
        <p className="text-center text-muted-foreground">Small Container (max-w-screen-sm)</p>
      </Container>
      <Container size="md" className="border border-dashed border-border p-4">
        <p className="text-center text-muted-foreground">Medium Container (max-w-screen-md)</p>
      </Container>
      <Container size="lg" className="border border-dashed border-border p-4">
        <p className="text-center text-muted-foreground">Large Container (max-w-screen-lg)</p>
      </Container>
    </div>
  ),
};

export const FullLayout: StoryObj = {
  render: () => (
    <div className="flex h-screen flex-col">
      <Header sticky>
        <HeaderTitle>My App</HeaderTitle>
        <HeaderActions>
          <Button variant="ghost" size="sm">Profile</Button>
        </HeaderActions>
      </Header>
      <div className="flex flex-1 overflow-hidden">
        <Sidebar>
          <SidebarContent>
            <SidebarNav>
              <SidebarNavItem href="#" active>Dashboard</SidebarNavItem>
              <SidebarNavItem href="#">Projects</SidebarNavItem>
              <SidebarNavItem href="#">Settings</SidebarNavItem>
            </SidebarNav>
          </SidebarContent>
        </Sidebar>
        <main className="flex-1 overflow-auto p-6">
          <Container>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="mt-2 text-muted-foreground">
              Welcome to your dashboard. This is the main content area.
            </p>
          </Container>
        </main>
      </div>
      <Footer>
        <FooterContent>
          <FooterText>&copy; 2024 My Company</FooterText>
        </FooterContent>
      </Footer>
    </div>
  ),
};
