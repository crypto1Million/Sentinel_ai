"use client";

import {
  Globe2,
  MessageCircle,
  Send,
  ExternalLink,
} from "lucide-react";

interface SocialLinksProps {
  website?: string | null;
  twitter?: string | null;
  telegram?: string | null;
  discord?: string | null;
  github?: string | null;
}

export default function SocialLinks({
  website,
  twitter,
  telegram,
  discord,
  github,
}: SocialLinksProps) {
  const links = [
    {
      label: "Website",
      href: website,
      icon: Globe2,
    },
    {
      label: "X",
      href: twitter,
      icon: MessageCircle,
    },
    {
      label: "Telegram",
      href: telegram,
      icon: Send,
    },
    {
      label: "Discord",
      href: discord,
      icon: MessageCircle,
    },
    {
      label: "GitHub",
      href: github,
      icon: ExternalLink,
    },
  ].filter(
    (
      item
    ): item is {
      label: string;
      href: string;
      icon: typeof Globe2;
    } => Boolean(item.href)
  );

  if (links.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {links.map(
        ({
          label,
          href,
          icon: Icon,
        }) => (
          <a
            key={label}
            href={href}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-[#11161d] px-3 py-2 text-sm text-zinc-300 transition hover:border-amber-500/40 hover:text-white"
          >
            <Icon size={16} />

            <span>{label}</span>

            <ExternalLink
              size={13}
              className="text-zinc-500"
            />
          </a>
        )
      )}
    </div>
  );
}