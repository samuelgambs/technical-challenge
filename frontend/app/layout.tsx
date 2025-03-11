import type React from "react";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "sonner";
import Navbar from "@/components/navbar";
import "@/app/globals.css";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {/* ThemeProvider for managing light/dark mode */}
        <ThemeProvider attribute="class" defaultTheme="light">
          {/* Navigation bar component */}
          <Navbar />

          {/* Main content container */}
          <main className="container mx-auto py-6 px-4">
            {/* Render child components */}
            {children}
          </main>

          {/* Toaster for displaying notifications */}
          <Toaster position="top-right" />
        </ThemeProvider>
      </body>
    </html>
  );
}