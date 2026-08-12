// apps/web/components/wallet/ConnectButton.tsx

"use client";

import { useState } from "react";

import {
    Wallet,
    ChevronDown,
    Copy,
    LogOut,
    ExternalLink,
    RefreshCw,
    CheckCircle2,
} from "lucide-react";

import WalletModal from "./WalletModal";
import { useWallet } from "./WalletProvider";

export default function ConnectButton() {
    const {
        connected,
        connecting,
        address,
        balance,
        provider,
        disconnect,
        refresh,
    } = useWallet();

    const [openModal, setOpenModal] =
        useState(false);

    const [dropdown, setDropdown] =
        useState(false);

    const shortAddress = address
        ? `${address.slice(0, 4)}...${address.slice(-4)}`
        : "";

    const explorer =
        address &&
        `https://solscan.io/account/${address}`;

    const copyAddress = async () => {
        if (!address) return;

        await navigator.clipboard.writeText(
            address,
        );
    };

    return (
        <>
            {!connected ? (
                <>
                    <button
                        onClick={() =>
                            setOpenModal(true)
                        }
                        disabled={connecting}
                        className="flex items-center gap-2 rounded-xl bg-indigo-600 px-5 py-2.5 font-medium transition hover:bg-indigo-500 disabled:opacity-60"
                    >
                        <Wallet size={18} />

                        {connecting
                            ? "Connecting..."
                            : "Connect Wallet"}
                    </button>

                    <WalletModal
                        open={openModal}
                        onClose={() =>
                            setOpenModal(false)
                        }
                    />
                </>
            ) : (
                <div className="relative">

                    <button
                        onClick={() =>
                            setDropdown(
                                !dropdown,
                            )
                        }
                        className="flex items-center gap-3 rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 transition hover:bg-zinc-800"
                    >
                        <CheckCircle2
                            size={18}
                            className="text-green-500"
                        />

                        <div className="text-left">

                            <div className="text-sm font-semibold">
                                {shortAddress}
                            </div>

                            <div className="text-xs text-zinc-400">
                                ◎{" "}
                                {balance.toFixed(
                                    3,
                                )}{" "}
                                SOL
                            </div>

                        </div>

                        <ChevronDown
                            size={18}
                        />
                    </button>

                    {dropdown && (
                        <div className="absolute right-0 mt-3 w-72 overflow-hidden rounded-2xl border border-zinc-800 bg-[#0B0B0F] shadow-2xl">

                            {/* Header */}

                            <div className="border-b border-zinc-800 p-4">

                                <div className="font-semibold">
                                    Connected Wallet
                                </div>

                                <div className="mt-2 font-mono text-sm text-zinc-400">
                                    {shortAddress}
                                </div>

                                <div className="mt-2 text-xs uppercase text-indigo-400">
                                    {provider}
                                </div>

                            </div>

                            {/* Balance */}

                            <div className="border-b border-zinc-800 p-4">

                                <div className="text-sm text-zinc-400">
                                    Balance
                                </div>

                                <div className="mt-1 text-xl font-bold">
                                    ◎{" "}
                                    {balance.toFixed(
                                        4,
                                    )}{" "}
                                    SOL
                                </div>

                            </div>

                            {/* Actions */}

                            <button
                                onClick={
                                    copyAddress
                                }
                                className="flex w-full items-center gap-3 px-4 py-3 hover:bg-zinc-900"
                            >
                                <Copy size={18} />

                                Copy Address
                            </button>

                            <button
                                onClick={() =>
                                    window.open(
                                        explorer!,
                                        "_blank",
                                    )
                                }
                                className="flex w-full items-center gap-3 px-4 py-3 hover:bg-zinc-900"
                            >
                                <ExternalLink
                                    size={18}
                                />

                                View on Solscan
                            </button>

                            <button
                                onClick={
                                    refresh
                                }
                                className="flex w-full items-center gap-3 px-4 py-3 hover:bg-zinc-900"
                            >
                                <RefreshCw
                                    size={18}
                                />

                                Refresh Balance
                            </button>

                            <button
                                onClick={async () => {
                                    await disconnect();

                                    setDropdown(
                                        false,
                                    );
                                }}
                                className="flex w-full items-center gap-3 border-t border-zinc-800 px-4 py-3 text-red-400 hover:bg-red-500/10"
                            >
                                <LogOut
                                    size={18}
                                />

                                Disconnect Wallet
                            </button>
                        </div>
                    )}
                </div>
            )}
        </>
    );
}