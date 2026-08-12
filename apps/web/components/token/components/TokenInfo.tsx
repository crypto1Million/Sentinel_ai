"use client";

import TokenHeader from "./components/TokenHeader";
import ContractCard from "./components/ContractCard";
import SocialLinks from "./components/SocialLinks";
import TokenStats from "./components/TokenStats";
import SecurityStatus from "./components/SecurityStatus";
import LaunchInfo from "./components/LaunchInfo";
import DeployerCard from "./components/DeployerCard";
import QuickActions from "./components/QuickActions";

export interface TokenInfoProps {
  logo: string;

  name: string;

  symbol: string;

  verified: boolean;

  contract: string;

  website?: string;

  telegram?: string;

  twitter?: string;

  github?: string;

  price: number;

  marketCap: number;

  holders: number;

  liquidity: number;

  volume24h: number;

  mintAuthority: boolean;

  freezeAuthority: boolean;

  lpLocked: boolean;

  lpBurned: boolean;

  verifiedContract: boolean;

  renounced: boolean;

  honeypot: boolean;

  securityScore: number;

  launchDate: string;

  tokenAge: string;

  blockchain: string;

  dex: string;

  pair: string;

  deployer: string;

  initialLiquidity: number;

  currentLiquidity: number;

  launchPrice: number;

  deployerVerified: boolean;

  reputationScore: number;

  totalTokens: number;

  successfulTokens: number;

  ruggedTokens: number;

  winRate: number;

  currentHoldings: number;

  soldPercentage: number;

  explorerUrl?: string;

  dexUrl?: string;
}

export default function TokenInfo({
  logo,
  name,
  symbol,
  verified,

  contract,

  website,
  telegram,
  twitter,
  github,

  price,
  marketCap,
  holders,
  liquidity,
  volume24h,

  mintAuthority,
  freezeAuthority,
  lpLocked,
  lpBurned,
  verifiedContract,
  renounced,
  honeypot,
  securityScore,

  launchDate,
  tokenAge,
  blockchain,
  dex,
  pair,
  deployer,
  initialLiquidity,
  currentLiquidity,
  launchPrice,

  deployerVerified,
  reputationScore,
  totalTokens,
  successfulTokens,
  ruggedTokens,
  winRate,
  currentHoldings,
  soldPercentage,

  explorerUrl,
  dexUrl,
}: TokenInfoProps) {
  return (
    <div className="space-y-6">

      {/* ================= HEADER ================= */}

      <div className="rounded-xl border border-zinc-800 bg-[#11161d] p-6">

        <div className="flex flex-col gap-6 xl:flex-row xl:items-center xl:justify-between">

          <TokenHeader
            logo={logo}
            name={name}
            symbol={symbol}
            verified={verified}
          />

          <SocialLinks
            website={website}
            telegram={telegram}
            twitter={twitter}
            github={github}
          />

        </div>

      </div>

      {/* ================= CONTRACT ================= */}

      <ContractCard
        contract={contract}
      />

      {/* ================= TOKEN STATS ================= */}

      <TokenStats
        price={price}
        marketCap={marketCap}
        holders={holders}
        liquidity={liquidity}
        volume24h={volume24h}
      />

      {/* ================= QUICK ACTIONS ================= */}

      <QuickActions
        contract={contract}
        explorerUrl={explorerUrl}
        dexUrl={dexUrl}
        onAIAnalysis={() =>
          console.log("AI Analysis")
        }
        onReplay={() =>
          console.log("Replay")
        }
        onWalletDNA={() =>
          console.log("Wallet DNA")
        }
        onRugRadar={() =>
          console.log("Rug Radar")
        }
      />

      {/* ================= SECURITY ================= */}

      <SecurityStatus
        mintAuthority={mintAuthority}
        freezeAuthority={freezeAuthority}
        lpLocked={lpLocked}
        lpBurned={lpBurned}
        verifiedContract={verifiedContract}
        renounced={renounced}
        honeypot={honeypot}
        securityScore={securityScore}
      />

      {/* ================= LAUNCH ================= */}

      <LaunchInfo
        launchDate={launchDate}
        tokenAge={tokenAge}
        blockchain={blockchain}
        dex={dex}
        pair={pair}
        deployer={deployer}
        initialLiquidity={initialLiquidity}
        currentLiquidity={currentLiquidity}
        launchPrice={launchPrice}
      />

      {/* ================= DEPLOYER ================= */}

      <DeployerCard
        address={deployer}
        verified={deployerVerified}
        reputationScore={reputationScore}
        totalTokens={totalTokens}
        successfulTokens={successfulTokens}
        ruggedTokens={ruggedTokens}
        winRate={winRate}
        currentHoldings={currentHoldings}
        soldPercentage={soldPercentage}
        explorerUrl={explorerUrl}
      />

    </div>
  );
}
```
