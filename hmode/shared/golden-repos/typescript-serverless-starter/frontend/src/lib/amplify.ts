import { Amplify } from 'aws-amplify';

/**
 * Amplify configuration for Cognito authentication
 *
 * Integrates with the shared auth gateway at auth.b.lfg.new
 *
 * Required environment variables:
 * - VITE_USER_POOL_ID: Cognito User Pool ID (default: us-east-1_p0fQSZLEG)
 * - VITE_USER_POOL_CLIENT_ID: App Client ID for this application
 * - VITE_COGNITO_DOMAIN: Cognito hosted UI domain (default: auth.b.lfg.new)
 */

// Default to the shared auth.b.lfg.new user pool
const DEFAULT_USER_POOL_ID = 'us-east-1_p0fQSZLEG';
const DEFAULT_COGNITO_DOMAIN = 'auth.b.lfg.new';

const userPoolId = import.meta.env.VITE_USER_POOL_ID || DEFAULT_USER_POOL_ID;
const userPoolClientId = import.meta.env.VITE_USER_POOL_CLIENT_ID || '';
const cognitoDomain = import.meta.env.VITE_COGNITO_DOMAIN || DEFAULT_COGNITO_DOMAIN;

// Determine redirect URLs based on environment
const isDev = import.meta.env.DEV;
const baseUrl = isDev ? 'http://localhost:5173' : window.location.origin;

const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId,
      userPoolClientId,
      signUpVerificationMethod: 'code' as const,
      loginWith: {
        email: true,
        oauth: {
          domain: cognitoDomain,
          scopes: ['openid', 'email', 'profile'],
          redirectSignIn: [`${baseUrl}/callback`],
          redirectSignOut: [baseUrl],
          responseType: 'code' as const,
        },
      },
    },
  },
};

export function configureAmplify() {
  if (!userPoolClientId) {
    console.warn(
      'VITE_USER_POOL_CLIENT_ID not set. Authentication will not work.',
      'Please set VITE_USER_POOL_CLIENT_ID in your .env.local file.'
    );
  }
  Amplify.configure(amplifyConfig);
}

export { userPoolId, userPoolClientId, cognitoDomain };
export default amplifyConfig;
