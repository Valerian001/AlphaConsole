import type { Metadata } from "next";
import { Geist, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { ConsoleProvider } from "@/context/ConsoleContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AlphaConsole | Multi-Agent Orchestration",
  description: "Advanced control plane for autonomous multi-agent systems",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${jetbrainsMono.variable}`}>
      <body>
        <ConsoleProvider>
          {children}
        </ConsoleProvider>
      </body>
    </html>
  );
}
