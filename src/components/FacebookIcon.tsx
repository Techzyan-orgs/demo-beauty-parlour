import React from 'react';

export default function FacebookIcon({ className = 'w-5 h-5' }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <circle cx="12" cy="12" r="12" fill="#1877F2" />
      <path
        d="M14.5 12.2H12.6V19H9.8V12.2H8.5V9.8H9.8V8.3C9.8 6.7 10.6 5 13.2 5H15.2V7.4H13.8C13.1 7.4 12.6 7.7 12.6 8.5V9.8H15.2L14.5 12.2Z"
        fill="white"
      />
    </svg>
  );
}
