"use client";

interface TokenHeaderProps {

    logo: string;

    name: string;

    symbol: string;

    verified?: boolean;

}

export default function TokenHeader({

    logo,

    name,

    symbol,

    verified = false

}: TokenHeaderProps) {

    return (

        <div className="flex items-center gap-4">

            <img

                src={logo}

                alt={symbol}

                className="h-16 w-16 rounded-full border border-zinc-700"

            />

            <div>

                <div className="flex items-center gap-2">

                    <h2 className="text-3xl font-bold">

                        {name}

                    </h2>

                    {

                        verified && (

                            <span className="rounded bg-cyan-500 px-2 py-1 text-xs text-black">

                                VERIFIED

                            </span>

                        )

                    }

                </div>

                <p className="text-zinc-400">

                    ${symbol}

                </p>

            </div>

        </div>

    );

}