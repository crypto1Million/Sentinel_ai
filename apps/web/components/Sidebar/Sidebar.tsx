import Image from "next/image";
import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 shrink-0 border-r border-zinc-800 bg-zinc-950">

      { /* Sentinel brand */}
      <div className="p-6">
        <Link
          href="/"
          aria-label="Sentinel Home"
          className="relative block h-14 w-full"
        >
          <Image
            src="/brand/sentinel-logo.svg"
            alt="Sentinel"
            fill
            priority
            sizes="224px"
            className="object-contain object-left"
          />
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-3 px-4">

        <Link href="/">
          Dashboard
        </Link>

        <Link href="/discover">
          Discover
        </Link>

        <Link href="/wallets">
          Wallet DNA
        </Link>

        <Link href="/narratives">
          Narratives
        </Link>

        <Link href="/portfolio">
          Portfolio
        </Link>

        <Link href="/settings">
          Settings
        </Link>

      </nav>

    </aside>
  );
}