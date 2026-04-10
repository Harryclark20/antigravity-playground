import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import { ToastProvider } from "@/components/Toast";

export const metadata: Metadata = {
  title: "Revilo Store ERP",
  description: "Enterprise Resource Planning system for Revilo Store — manage inventory, sales, customers, finance, and more.",
  keywords: ["Revilo Store", "ERP", "inventory", "sales", "dashboard"],
  authors: [{ name: "Revilo Store" }],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </head>
      <body>
        <ToastProvider>
          <div className="app-shell">
            <Sidebar />
            <div className="main-wrapper">
              <Topbar />
              <main className="main-content">{children}</main>
            </div>
          </div>
        </ToastProvider>
      </body>
    </html>
  );
}
