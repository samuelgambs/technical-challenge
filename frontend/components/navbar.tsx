"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Home, Users, FileText } from "lucide-react";

export default function Navbar() {
  // Get the current pathname from Next.js navigation
  const pathname = usePathname();

  // Define the navigation items
  const navItems = [
    { href: "/", label: "Home", icon: Home },
    { href: "/users", label: "Users", icon: Users },
    { href: "/posts", label: "Posts", icon: FileText },
  ];

  return (
    <nav className="border-b">
      <div className="container mx-auto flex h-16 items-center px-4">
        {/* Application Logo/Title */}
        <Link href="/" className="font-bold text-xl flex items-center mr-8">
          SocialConnect
        </Link>

        {/* Navigation Links */}
        <div className="flex gap-6">
          {navItems.map((item) => {
            // Check if the current pathname matches the navigation item's href
            const isActive = pathname === item.href;

            // Dynamically render the icon component
            const Icon = item.icon;

            return (
              <Link key={item.href} href={item.href}>
                <Button
                  variant={isActive ? "default" : "ghost"}
                  className="flex items-center gap-2"
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Button>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}