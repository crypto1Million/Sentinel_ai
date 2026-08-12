type Props = {

  explanation: string;
};

export default function AIExplanation({

  explanation

}: Props) {

  return (

    <div className="bg-zinc-900 rounded-xl p-4">

      <h2 className="font-bold mb-3">

        Sentinel AI Analysis
      </h2>

      <p>

        {explanation}

      </p>

    </div>

  );
}