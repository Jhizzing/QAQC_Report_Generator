import React, { type ReactElement } from 'react';
import { render, type RenderOptions } from '@testing-library/react';
import { vi } from 'vitest';
import userEvent from '@testing-library/user-event';

// Custom render function that includes any providers
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllTheProviders, ...options });

// Re-export everything
export * from '@testing-library/react';
export { customRender as render, userEvent };

// Helper to create mock file
export const createMockFile = (name: string, content: string, type: string = 'text/csv'): File => {
  const blob = new Blob([content], { type });
  return new File([blob], name, { type });
};

// Helper to create mock Excel file
export const createMockExcelFile = (name: string = 'test.xlsx'): File => {
  // Create a minimal Excel file structure
  const content = new Uint8Array([0x50, 0x4B, 0x03, 0x04]); // ZIP header (Excel is a ZIP file)
  return new File([content], name, { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
};

// Helper to wait for async operations
export const waitForAsync = () => new Promise(resolve => setTimeout(resolve, 0));

// Mock fetch helper
export const mockFetch = (response: any, ok: boolean = true) => {
  return vi.fn(() =>
    Promise.resolve({
      ok,
      json: () => Promise.resolve(response),
      text: () => Promise.resolve(JSON.stringify(response)),
      blob: () => Promise.resolve(new Blob([JSON.stringify(response)])),
      headers: new Headers(),
      status: ok ? 200 : 400,
      statusText: ok ? 'OK' : 'Bad Request',
    } as Response)
  );
};
