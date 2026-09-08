"use client";

import TokenHeader from "./TokenHeader";
import ContractCard from "./ContractCard";
import SocialLinks from "./SocialLinks";
import TokenStats from "./TokenStats";
import SecurityStatus from "./SecurityStatus";
import LaunchInfo from "./LaunchInfo";
import DeployerCard from "./DeployerCard";
import QuickActions from "./QuickActions";

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
      {/* Header */}

      <div className="rounded-xl border border-[#292929] bg-[#101010] p-6">
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

      {/* Contract */}

      <ContractCard
        contract={contract}
      />

      {/* Stats */}

      <TokenStats
        price={price}
        marketCap={marketCap}
        holders={holders}
        liquidity={liquidity}
        volume24h={volume24h}
      />

      {/* Quick Actions */}

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

      {/* Security */}

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

      {/* Launch */}

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

      {/* Deployer */}

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
