// File UUID: a2b3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d

/**
 * Shared Auth Client - SSO library for Hopper Labs apps
 *
 * Provides cross-subdomain authentication via the shared auth gateway.
 * Works with both personal (*.b.lfg.new) and work (*.b.aws.demo1983.com) contexts.
 */

export {
  initSSO,
  getSSOToken,
  clearSSO,
  redirectToLauncher,
  type SSOTokenData,
} from './sso';
