import '@testing-library/jest-dom';
import React from 'react';
import { vi } from 'vitest';

// Make React available globally in tests
globalThis.React = React;

// Mock Next.js Image component
vi.mock('next/image', () => ({
  default: (props: Record<string, unknown>) => React.createElement('img', { ...props, src: props.src, alt: props.alt }),
}));