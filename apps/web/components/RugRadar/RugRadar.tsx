type Props = {

  bundle: number;

  sniper: number;

  insider: number;
};

export default function RugRadar({

  bundle,

  sniper,

  insider

}: Props) {

  return (

    <div className="bg-zinc-900 rounded-xl p-4">

      <h2 className="font-bold mb-4">

        Rug Radar
      </h2>

      <p>Bundles: {bundle}%</p>

      <p>Snipers: {sniper}%</p>

      <p>Insiders: {insider}%</p>

    </div>

  );
}