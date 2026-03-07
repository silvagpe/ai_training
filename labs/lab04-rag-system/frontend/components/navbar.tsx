"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="border-b border-border bg-white">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="text-xl font-bold text-primary">
          RAG System
        </Link>
        <div className="flex gap-2">
          <Link href="/">
            <Button
              variant={pathname === "/" ? "default" : "ghost"}
              className={pathname === "/" ? "bg-rag-cyan text-white hover:bg-rag-cyan/90" : ""}
            >
              Query
            </Button>
          </Link>
          <Link href="/index-files">
            <Button
              variant={pathname === "/index-files" ? "default" : "ghost"}
              className={pathname === "/index-files" ? "bg-rag-cyan text-white hover:bg-rag-cyan/90" : ""}
            >
              Index Files
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  );
}
