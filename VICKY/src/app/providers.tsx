import React from "react";

export default function Providers({ children }: { children: React.ReactNode }) {
  // You can add ThemeProvider, AuthProvider, QueryClientProvider here later
  return <>{children}</>;
}
