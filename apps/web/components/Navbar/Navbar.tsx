export default function Navbar() {
  return (

    <div className="h-16 border-b border-zinc-800 flex items-center justify-between px-6">

      <div>

        <h1 className="text-xl font-bold text-green-400">
          Sentinel AI
        </h1>

      </div>

      <div>

        <input
          placeholder="Search Token..."
          className="bg-zinc-900 rounded px-4 py-2"
        />

      </div>

    </div>

  );
}