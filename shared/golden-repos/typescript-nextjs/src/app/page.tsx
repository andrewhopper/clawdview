import { config } from '@/lib/config';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-4">{config.NEXT_PUBLIC_APP_NAME}</h1>
      <p className="text-gray-600">
        Gold standard Next.js template with TypeScript
      </p>
      <div className="mt-8 grid grid-cols-2 gap-4">
        <FeatureCard
          title="Type Safety"
          description="Strict TypeScript with Zod validation"
        />
        <FeatureCard
          title="Testing"
          description="Vitest with React Testing Library"
        />
        <FeatureCard
          title="Logging"
          description="Structured JSON logging"
        />
        <FeatureCard
          title="Config"
          description="Environment variable validation"
        />
      </div>
    </main>
  );
}

function FeatureCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="p-4 border rounded-lg hover:border-gray-400 transition-colors">
      <h3 className="font-semibold">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );
}
