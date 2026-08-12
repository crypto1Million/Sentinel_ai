import Link from "next/link";

export default function Sidebar() {

  return (

    <div className="w-64 bg-zinc-950 border-r border-zinc-800">

      <div className="p-6">

        <h2 className="font-bold text-green-400">
          Sentinel
        </h2>

      </div>

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

    </div>

  );
}