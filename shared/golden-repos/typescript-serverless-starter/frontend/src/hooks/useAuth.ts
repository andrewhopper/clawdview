import { useState, useEffect, useCallback } from 'react';
import {
  signIn,
  signUp,
  signOut,
  confirmSignUp,
  getCurrentUser,
  fetchUserAttributes,
  type SignInInput,
  type SignUpInput,
} from 'aws-amplify/auth';

interface User {
  username: string;
  email?: string;
  attributes?: Record<string, string>;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    error: null,
  });

  const checkAuth = useCallback(async () => {
    try {
      const user = await getCurrentUser();
      const attributes = await fetchUserAttributes();
      setState({
        user: {
          username: user.username,
          email: attributes.email,
          attributes: attributes as Record<string, string>,
        },
        isLoading: false,
        isAuthenticated: true,
        error: null,
      });
    } catch {
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: null,
      });
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = async (input: SignInInput) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      await signIn(input);
      await checkAuth();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Sign in failed';
      setState((prev) => ({ ...prev, isLoading: false, error: message }));
      throw error;
    }
  };

  const register = async (input: SignUpInput) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      const result = await signUp(input);
      setState((prev) => ({ ...prev, isLoading: false }));
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Sign up failed';
      setState((prev) => ({ ...prev, isLoading: false, error: message }));
      throw error;
    }
  };

  const confirmRegistration = async (username: string, code: string) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      await confirmSignUp({ username, confirmationCode: code });
      setState((prev) => ({ ...prev, isLoading: false }));
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Confirmation failed';
      setState((prev) => ({ ...prev, isLoading: false, error: message }));
      throw error;
    }
  };

  const logout = async () => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      await signOut();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: null,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Sign out failed';
      setState((prev) => ({ ...prev, isLoading: false, error: message }));
      throw error;
    }
  };

  return {
    ...state,
    login,
    register,
    confirmRegistration,
    logout,
    refreshAuth: checkAuth,
  };
}
