import "./globals.css";

import Navbar from "@/components/Navbar/Navbar";
import Sidebar from "@/components/Sidebar/Sidebar";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>

        <div className="flex h-screen bg-black text-white">

          <Sidebar />

          <div className="flex flex-col flex-1">

            <Navbar />

            <main className="p-6 overflow-y-auto flex-1">
              {children}
            </main>

          </div>

        </div>

      </body>
    </html>
  );
}