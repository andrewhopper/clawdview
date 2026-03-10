// File UUID: d4e5f6a7-8b9c-0d1e-2f3a-4b5c6d7e8f9a
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
