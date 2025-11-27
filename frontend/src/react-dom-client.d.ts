// Temporary ambient declaration to satisfy TypeScript in build environments
// that can't resolve the 'react-dom/client' types. This keeps the
// build working on CI/Docker where @types/react-dom may not be
// available or mismatched.
declare module 'react-dom/client' {
  import * as React from 'react';
  export function createRoot(container: Element | DocumentFragment): any;
  export function hydrateRoot(container: Element, vdom: React.ReactNode): any;
  export * from 'react-dom';
}
declare module 'react-dom/client' {
  import { ReactNode } from 'react';

  export interface Root {
    render(children: ReactNode): void;
    unmount(): void;
  }

  export function createRoot(container: Element | DocumentFragment): Root;
  export function hydrateRoot(container: Element | DocumentFragment, initialChildren: ReactNode): Root;
}
