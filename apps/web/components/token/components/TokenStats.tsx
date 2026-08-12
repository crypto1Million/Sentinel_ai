"use client";

interface Props {

    price: number;

    marketCap: number;

    holders: number;

    liquidity: number;

    volume24h: number;

}

export default function TokenStats({

    price,

    marketCap,

    holders,

    liquidity,

    volume24h

}: Props) {

    const stats = [

        ["Price", `$${price}`],

        ["Market Cap", `$${marketCap.toLocaleString()}`],

        ["Holders", holders.toLocaleString()],

        ["Liquidity", `$${liquidity.toLocaleString()}`],

        ["24H Volume", `$${volume24h.toLocaleString()}`]

    ];

    return (

        <div className="grid grid-cols-5 gap-4">

            {

                stats.map(([title, value]) => (

                    <div

                        key={title}

                        className="rounded-lg bg-[#11161d] border border-zinc-800 p-4"

                    >

                        <div className="text-zinc-500 text-sm">

                            {title}

                        </div>

                        <div className="mt-2 font-semibold">

                            {value}

                        </div>

                    </div>

                ))

            }

        </div>

    );

}