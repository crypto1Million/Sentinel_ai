// apps/web/components/wallet/WalletSelector.tsx

"use client";

import React from "react";
import {
    Wallet,
    CheckCircle2,
    AlertCircle,
    ExternalLink,
} from "lucide-react";

import { WalletType } from "@/lib/wallet/WalletManager";
import { useWallet } from "./WalletProvider";

interface WalletOption {
    id: WalletType;
    name: string;
    icon: string;
    website: string;
}

const wallets: WalletOption[] = [
    {
        id: "phantom",
        name: "Phantom",
        icon: "/wallets/phantom.png",
        website: "https://phantom.app",
    },
    {
        id: "backpack",
        name: "Backpack",
        icon: "/wallets/backpack.png",
        website: "https://backpack.app",
    },
    {
        id: "solflare",
        name: "Solflare",
        icon: "/wallets/solflare.png",
        website: "https://solflare.com",
    },
];

export default function WalletSelector() {
    const {
        connect,
        connecting,
        walletManager,
    } = useWallet();

    const installed =
        walletManager.installedWallets();

    const connectWallet = async (
        wallet: WalletType,
    ) => {
        try {
            await connect(wallet);
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="space-y-4">

            <div>
                <h2 className="text-xl font-bold">
                    Connect Wallet
                </h2>

                <p className="text-sm text-zinc-400">
                    Choose a Solana wallet to connect with Sentinel.
                </p>
            </div>

            <div className="space-y-3">

                {wallets.map((wallet) => {

                    const isInstalled =
                        installed[wallet.id];

                    return (

                        <div
                            key={wallet.id}
                            className="rounded-xl border border-zinc-800 bg-zinc-900 p-4"
                        >

                            <div className="flex items-center justify-between">

                                <div className="flex items-center gap-4">

                                    <img
                                        src={wallet.icon}
                                        alt={wallet.name}
                                        className="h-12 w-12 rounded-lg"
                                    />

                                    <div>

                                        <div className="flex items-center gap-2">

                                            <h3 className="font-semibold">
                                                {wallet.name}
                                            </h3>

                                            {isInstalled ? (
                                                <CheckCircle2
                                                    className="text-green-500"
                                                    size={18}
                                                />
                                            ) : (
                                                <AlertCircle
                                                    className="text-yellow-500"
                                                    size={18}
                                                />
                                            )}

                                        </div>

                                        <p className="text-sm text-zinc-400">

                                            {isInstalled
                                                ? "Installed"
                                                : "Not Installed"}

                                        </p>

                                    </div>

                                </div>

                                <div className="flex gap-2">

                                    {isInstalled ? (

                                        <button
                                            disabled={connecting}
                                            onClick={() =>
                                                connectWallet(
                                                    wallet.id,
                                                )
                                            }
                                            className="rounded-lg bg-green-600 px-5 py-2 text-sm font-medium hover:bg-green-500 disabled:opacity-50"
                                        >

                                            {connecting
                                                ? "Connecting..."
                                                : "Connect"}

                                        </button>

                                    ) : (

                                        <a
                                            href={
                                                wallet.website
                                            }
                                            target="_blank"
                                            rel="noreferrer"
                                            className="flex items-center gap-2 rounded-lg bg-zinc-800 px-5 py-2 text-sm hover:bg-zinc-700"
                                        >
                                            Install

                                            <ExternalLink
                                                size={16}
                                            />

                                        </a>

                                    )}

                                </div>

                            </div>

                        </div>

                    );

                })}

            </div>

            <div className="rounded-lg border border-indigo-500/30 bg-indigo-500/10 p-4">

                <div className="flex items-center gap-3">

                    <Wallet
                        className="text-indigo-400"
                    />

                    <div>

                        <div className="font-semibold">

                            Recommended

                        </div>

                        <div className="text-sm text-zinc-400">

                            Phantom offers the smoothest experience
                            for Sentinel AI Trading Terminal.

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}