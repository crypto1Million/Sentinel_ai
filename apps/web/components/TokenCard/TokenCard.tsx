type Props = {

  symbol: string;

  marketCap?: number;

  holders?: number;

  chain?: string;

  price?: number;

  mint?: string;

};


export default function TokenCard({

  symbol,

  marketCap,

  holders,

  chain,

  price,

  mint,

}: Props) {

  return (

    <article className="rounded-xl border border-[#292929] bg-zinc-900 p-4">

      <div className="flex items-start justify-between gap-3">

        <h2 className="truncate text-xl font-bold">

          {symbol}

        </h2>


        {chain ? (

          <span className="rounded-md bg-[#17130A] px-2 py-1 text-[10px] uppercase text-[#F5C84C]">

            {chain}

          </span>

        ) : null}

      </div>


      <div className="mt-3 space-y-1 text-sm text-[#B5B5B5]">

        <p>

          MC: {
            marketCap !== undefined
              ? `$${marketCap.toLocaleString()}`
              : "—"
          }

        </p>


        <p>

          Holders: {
            holders !== undefined
              ? holders.toLocaleString()
              : "—"
          }

        </p>


        {price !== undefined ? (

          <p>

            Price: ${price.toPrecision(6)}

          </p>

        ) : null}

      </div>


      {mint ? (

        <p

          className="mt-3 truncate font-mono text-[10px] text-[#666]"

          title={mint}

        >

          {mint}

        </p>

      ) : null}

    </article>

  );

}