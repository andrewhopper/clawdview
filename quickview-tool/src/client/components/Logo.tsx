interface LogoProps {
  size?: number;
  className?: string;
}

export function Logo({ size = 24, className }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* top lid */}
      <path
        d="M2 26 Q24 6 46 26"
        stroke="currentColor"
        strokeWidth="2.8"
        strokeLinecap="round"
        fill="none"
      />
      {/* lash ticks */}
      <line x1="11" y1="14" x2="9" y2="7" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
      <line x1="24" y1="8" x2="24" y2="1" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
      <line x1="37" y1="14" x2="39" y2="7" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
      {/* wink */}
      <path
        d="M2 26 Q24 34 46 26"
        stroke="currentColor"
        strokeWidth="2.8"
        strokeLinecap="round"
        fill="none"
      />
      {/* check */}
      <path
        d="M17 23 L22 28 L31 16"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}
