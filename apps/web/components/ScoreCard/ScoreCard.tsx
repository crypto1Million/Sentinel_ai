type Props = {

  title: string;

  score: number;
};

export default function ScoreCard({

  title,

  score

}: Props) {

  return (

    <div className="bg-zinc-900 rounded-xl p-4">

      <h3 className="text-sm text-zinc-400">

        {title}

      </h3>

      <div className="text-3xl font-bold text-green-400">

        {score}

      </div>

    </div>

  );
}