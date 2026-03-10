import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { ThemeToggle } from '@/components/ThemeToggle';
import { AuthForms } from '@/components/AuthForms';
import { HomePage } from '@/pages/HomePage';
import { Button } from '@/components/ui/button';
import { LogOut, User } from 'lucide-react';

function Layout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, user, logout, isLoading } = useAuth();

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold">Serverless Starter</h1>
          </div>
          <div className="flex items-center gap-4">
            {isAuthenticated && user && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <User className="h-4 w-4" />
                <span>{user.email}</span>
              </div>
            )}
            <ThemeToggle />
            {isAuthenticated && (
              <Button
                variant="ghost"
                size="icon"
                onClick={logout}
                disabled={isLoading}
                title="Sign out"
              >
                <LogOut className="h-5 w-5" />
              </Button>
            )}
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

function LoginPage() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <AuthForms />
    </div>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <HomePage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
