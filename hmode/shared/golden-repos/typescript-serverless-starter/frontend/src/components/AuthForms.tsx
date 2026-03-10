import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/hooks/useAuth';

type AuthMode = 'signin' | 'signup' | 'confirm';

export function AuthForms() {
  const [mode, setMode] = useState<AuthMode>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmCode, setConfirmCode] = useState('');
  const [pendingUsername, setPendingUsername] = useState('');

  const { login, register, confirmRegistration, isLoading, error } = useAuth();

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login({ username: email, password });
    } catch {
      // Error is handled by the hook
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register({
        username: email,
        password,
        options: {
          userAttributes: { email },
        },
      });
      setPendingUsername(email);
      setMode('confirm');
    } catch {
      // Error is handled by the hook
    }
  };

  const handleConfirm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await confirmRegistration(pendingUsername, confirmCode);
      setMode('signin');
      setEmail(pendingUsername);
      setPassword('');
    } catch {
      // Error is handled by the hook
    }
  };

  if (mode === 'confirm') {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>Confirm Your Email</CardTitle>
          <CardDescription>
            We sent a verification code to {pendingUsername}
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleConfirm}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="code">Verification Code</Label>
              <Input
                id="code"
                type="text"
                value={confirmCode}
                onChange={(e) => setConfirmCode(e.target.value)}
                placeholder="Enter code"
                required
              />
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Confirming...' : 'Confirm'}
            </Button>
            <Button
              type="button"
              variant="ghost"
              onClick={() => setMode('signin')}
            >
              Back to Sign In
            </Button>
          </CardFooter>
        </form>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{mode === 'signin' ? 'Sign In' : 'Create Account'}</CardTitle>
        <CardDescription>
          {mode === 'signin'
            ? 'Enter your credentials to access your account'
            : 'Create a new account to get started'}
        </CardDescription>
      </CardHeader>
      <form onSubmit={mode === 'signin' ? handleSignIn : handleSignUp}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              minLength={8}
            />
          </div>
          {error && <p className="text-sm text-destructive">{error}</p>}
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading
              ? 'Loading...'
              : mode === 'signin'
              ? 'Sign In'
              : 'Create Account'}
          </Button>
          <Button
            type="button"
            variant="ghost"
            onClick={() => setMode(mode === 'signin' ? 'signup' : 'signin')}
          >
            {mode === 'signin'
              ? "Don't have an account? Sign up"
              : 'Already have an account? Sign in'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
