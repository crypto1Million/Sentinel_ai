"use client";

import CopyButton from "./CopyButton";

interface Props {

    contract: string;

}

export default function ContractCard({

    contract

}: Props) {

    return (

        <div className="rounded-xl bg-[#11161d] border border-zinc-800 p-4">

            <div className="text-sm text-zinc-400 mb-2">

                Contract Address

            </div>

            <div className="flex items-center justify-between gap-4">

                <code className="text-cyan-400 break-all">

                    {contract}

                </code>

                <CopyButton value={contract} />

            </div>

        </div>

    );

}


