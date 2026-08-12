type Props = {

  symbol: string;

  marketCap: number;

  holders: number;
};

export default function TokenCard({

  symbol,

  marketCap,

  holders

}: Props) {

  return (

    <div className="bg-zinc-900 p-4 rounded-xl">

      <h2 className="text-xl font-bold">

        {symbol}

      </h2>

      <p>

        MC: ${marketCap.toLocaleString()}

      </p>

      <p>

        Holders: {holders}

      </p>

    </div>

  );
}