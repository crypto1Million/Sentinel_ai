// apps/web/components/wallet/WalletModal.tsx

"use client";

import { useState } from "react";
import {
    X,
    Wallet,
    ShieldCheck,
    CheckCircle2,
    Loader2,
    Sparkles,
} from "lucide-react";

import WalletSelector from "./WalletSelector";
import { useWallet } from "./WalletProvider";

interface WalletModalProps {
    open: boolean;
    onClose: () => void;
}

export default function WalletModal({
    open,
    onClose,
}: WalletModalProps) {
    const {
        connected,
        address,
        balance,
        provider,
        disconnect,
    } = useWallet();

    const [disconnecting, setDisconnecting] =
        useState(false);

    if (!open) return null;

    const shortAddress = address
        ? `${address.slice(0, 4)}...${address.slice(-4)}`
        : "";

    const handleDisconnect = async () => {
        try {
            setDisconnecting(true);

            await disconnect();

            onClose();
        } finally {
            setDisconnecting(false);
        }
    };

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 backdrop-blur-sm">

            <div className="relative w-full max-w-xl overflow-hidden rounded-2xl border border-zinc-800 bg-[#0B0B0F] shadow-2xl">

                {/* Header */}

                <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-5">

                    <div className="flex items-center gap-3">

                        <div className="rounded-xl bg-indigo-500/20 p-3">

                            <Wallet className="text-indigo-400" />

                        </div>

                        <div>

                            <h2 className="text-xl font-bold">
                                Connect Wallet
                            </h2>

                            <p className="text-sm text-zinc-400">
                                Securely connect your Solana wallet to Sentinel AI.
                            </p>

                        </div>

                    </div>

                    <button
                        onClick={onClose}
                        className="rounded-lg p-2 transition hover:bg-zinc-800"
                    >
                        <X size={20} />
                    </button>

                </div>

                {/* Connected */}

                {connected && (

                    <div className="border-b border-zinc-800 bg-green-500/5 px-6 py-5">

                        <div className="flex items-center justify-between">

                            <div className="space-y-2">

                                <div className="flex items-center gap-2">

                                    <CheckCircle2
                                        className="text-green-400"
                                        size={20}
                                    />

                                    <span className="font-semibold text-green-400">
                                        Wallet Connected
                                    </span>

                                </div>

                                <div className="text-sm text-zinc-300">

                                    Address

                                    <div className="mt-1 font-mono">

                                        {shortAddress}

                                    </div>

                                </div>

                                <div className="text-sm text-zinc-300">

                                    Wallet

                                    <div className="mt-1 capitalize">

                                        {provider}

                                    </div>

                                </div>

                                <div className="text-sm text-zinc-300">

                                    Balance

                                    <div className="mt-1">

                                        ◎ {balance.toFixed(4)} SOL

                                    </div>

                                </div>

                            </div>

                            <button
                                onClick={handleDisconnect}
                                disabled={disconnecting}
                                className="rounded-lg bg-red-600 px-5 py-2 text-sm font-medium transition hover:bg-red-500 disabled:opacity-60"
                            >
                                {disconnecting ? (
                                    <Loader2
                                        size={18}
                                        className="animate-spin"
                                    />
                                ) : (
                                    "Disconnect"
                                )}
                            </button>

                        </div>

                    </div>

                )}

                {/* Wallet Selector */}

                {!connected && (

                    <div className="px-6 py-5">

                        <WalletSelector />

                    </div>

                )}

                {/* Features */}

                <div className="border-t border-zinc-800 bg-zinc-950 px-6 py-5">

                    <div className="mb-4 flex items-center gap-2">

                        <Sparkles
                            size={18}
                            className="text-indigo-400"
                        />

                        <span className="font-semibold">
                            Why connect?
                        </span>

                    </div>

                    <div className="grid grid-cols-2 gap-4">

                        <Feature
                            title="One-click Trading"
                            description="Buy & Sell instantly."
                        />

                        <Feature
                            title="AI Copilot"
                            description="Receive AI trading recommendations."
                        />

                        <Feature
                            title="Wallet DNA"
                            description="Analyze wallet reputation."
                        />

                        <Feature
                            title="Portfolio Tracking"
                            description="Monitor PnL in real-time."
                        />

                        <Feature
                            title="Jito Bundles"
                            description="MEV-protected execution."
                        />

                        <Feature
                            title="Replay Trading"
                            description="Replay historical opportunities."
                        />

                    </div>

                </div>

                {/* Security */}

                <div className="border-t border-zinc-800 px-6 py-4">

                    <div className="flex items-start gap-3">

                        <ShieldCheck
                            className="mt-1 text-green-400"
                            size={22}
                        />

                        <div>

                            <div className="font-medium">

                                Your wallet stays secure

                            </div>

                            <div className="mt-1 text-sm text-zinc-400">

                                Sentinel AI never stores your private keys.
                                All transaction approvals happen directly
                                inside your wallet.

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}

interface FeatureProps {
    title: string;
    description: string;
}

function Feature({
    title,
    description,
}: FeatureProps) {
    return (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">

            <div className="font-medium">

                {title}

            </div>

            <div className="mt-1 text-sm text-zinc-400">

                {description}

            </div>

        </div>
    );
}