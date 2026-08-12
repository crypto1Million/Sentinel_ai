"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

interface CopyButtonProps {
  value: string;
}

export default function CopyButton({
  value,
}: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(value);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1500);

    } catch (error) {
      console.error(error);
    }
  }

  return (
    <button
      onClick={handleCopy}
      className="
        flex
        items-center
        gap-2
        rounded-lg
        bg-[#1B2330]
        px-3
        py-2
        hover:bg-[#263244]
        transition
      "
    >
      {copied ? (
        <Check
          size={16}
          className="text-green-400"
        />
      ) : (
        <Copy
          size={16}
        />
      )}

      <span className="text-sm">

        {copied ? "Copied" : "Copy"}

      </span>

    </button>
  );
}