import { NextResponse } from 'next/server';
import { config } from '@/lib/config';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    version: '0.1.0',
    environment: config.NODE_ENV,
    timestamp: new Date().toISOString(),
  });
}
