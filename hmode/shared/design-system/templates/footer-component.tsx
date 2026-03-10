// File UUID: 7c8d9e0f-1a2b-3c4d-5e6f-7a8b9c0d1e2f
// Template: Standard Footer with buildinfo.json integration
// Usage: Copy to your project's components/layout/footer.tsx
//        Update copyright text and GitHub repo URL

'use client';

import { useState, useEffect } from 'react';

interface BuildInfo {
  build?: {
    gitHash?: string;
    gitHashFull?: string;
    gitBranch?: string;
    buildDate?: string;
    projectId?: string;
  };
  deployment?: {
    environment?: string;
    releaseId?: string;
  };
  infrastructure?: {
    [key: string]: string;
  };
}

/**
 * Standard Footer Component
 *
 * Displays:
 * - Copyright notice
 * - Project ID (from buildinfo.json)
 * - Environment badge (dev/stage/prod)
 * - Git commit hash (clickable link to GitHub)
 *
 * Fetches buildinfo.json at runtime (generated during build by shared/tools/generate-buildinfo.py)
 *
 * @example
 * ```tsx
 * import { Footer } from '@/components/layout/footer';
 *
 * export default function RootLayout({ children }) {
 *   return (
 *     <html>
 *       <body>
 *         {children}
 *         <Footer />
 *       </body>
 *     </html>
 *   );
 * }
 * ```
 */
export function Footer() {
  const [buildInfo, setBuildInfo] = useState<BuildInfo | null>(null);

  useEffect(() => {
    // Fetch buildinfo.json at runtime
    fetch('/buildinfo.json')
      .then((res) => res.json())
      .then((data) => setBuildInfo(data))
      .catch(() => {
        // Buildinfo not available, that's okay
        console.debug('Buildinfo not available');
      });
  }, []);

  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t bg-background px-4 py-6 sm:px-6 lg:px-8 mt-auto">
      <div className="mx-auto flex max-w-screen-lg flex-col items-center gap-4 sm:flex-row sm:justify-between">
        {/* TODO: Update copyright text for your project */}
        <p className="text-sm text-muted-foreground">
          © {currentYear} Your Project Name
        </p>

        <div className="flex gap-4 text-sm text-muted-foreground">
          {/* Project ID */}
          {buildInfo?.build?.projectId && (
            <span
              className="font-mono text-xs"
              title="Project ID"
            >
              {buildInfo.build.projectId}
            </span>
          )}

          {/* Environment Badge */}
          {buildInfo?.deployment?.environment && (
            <span
              className="font-mono"
              title={`Release: ${buildInfo.deployment.releaseId || 'unknown'}`}
            >
              {buildInfo.deployment.environment}
            </span>
          )}

          {/* Git Commit Hash (clickable) */}
          {buildInfo?.build?.gitHash && (
            <a
              href={`https://github.com/YOUR_USERNAME/YOUR_REPO/commit/${buildInfo.build.gitHashFull || buildInfo.build.gitHash}`}
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono hover:text-foreground transition-colors"
              title={`Build: ${buildInfo.build.buildDate || 'unknown'}`}
            >
              {buildInfo.build.gitHash.substring(0, 7)}
            </a>
          )}
        </div>
      </div>
    </footer>
  );
}
