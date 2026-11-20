interface ComingSoonPanelProps {
  title: string;
  description: string;
}

export default function ComingSoonPanel({
  title,
  description,
}: ComingSoonPanelProps) {
  return (
    <section className="flex min-h-[60vh] flex-col items-center justify-center rounded-2xl border border-[#292929] bg-[#101010] p-8 text-center">

      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#D4AF37]">
        SENTINEL TERMINAL
      </p>

      <h1 className="mt-4 text-3xl font-bold text-white">
        {title}
      </h1>

      <p className="mt-3 max-w-lg text-sm leading-7 text-[#888]">
        {description}
      </p>

      <span className="mt-6 rounded-lg border border-[#433716] bg-[#17130A] px-4 py-2 text-xs font-semibold text-[#F5C84C]">
        WORKSPACE IN DEVELOPMENT
      </span>

    </section>
  );
}