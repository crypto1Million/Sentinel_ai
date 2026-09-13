"use client";

import TokenHeader from "./TokenHeader";
import ContractCard from "./ContractCard";
import SocialLinks from "./SocialLinks";
import TokenStats from "./TokenStats";
import SecurityStatus from "./SecurityStatus";
import LaunchInfo from "./LaunchInfo";
import DeployerCard from "./DeployerCard";
import QuickActions from "./QuickActions";
import LiquidityPanel from "./LiquidityPanel";
import HolderDistribution from "./HolderDistribution";
import TokenMetrics from "./TokenMetrics";

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

  // Extended metrics.
  // Optional so existing TokenInfo callers do not break.
  fdv?: number;

  volume5m?: number;
  volume1h?: number;

  buys?: number;
  sells?: number;

  buyVolume?: number;
  sellVolume?: number;

  uniqueBuyers?: number;
  uniqueSellers?: number;

  smartMoneyPercent?: number;
  freshWalletPercent?: number;
  whalePercent?: number;
  insiderPercent?: number;
  sniperPercent?: number;
  bundledPercent?: number;

  top10Percent?: number;
  top25Percent?: number;

  devHolding?: number;

  lpLockedPercent?: number;
  lpBurnedPercent?: number;

  ath?: number;
  atl?: number;

  change5m?: number;
  change1h?: number;
  change24h?: number;

  // Holder distribution.
  exchangePercent?: number;
  othersPercent?: number;
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

  fdv = marketCap,

  volume5m = 0,
  volume1h = 0,

  buys = 0,
  sells = 0,

  buyVolume = 0,
  sellVolume = 0,

  uniqueBuyers = 0,
  uniqueSellers = 0,

  smartMoneyPercent = 0,
  freshWalletPercent = 0,
  whalePercent = 0,
  insiderPercent = 0,
  sniperPercent = 0,
  bundledPercent = 0,

  top10Percent = 0,
  top25Percent = 0,

  devHolding = 0,

  lpLockedPercent = lpLocked ? 100 : 0,
  lpBurnedPercent = lpBurned ? 100 : 0,

  ath = price,
  atl = price,

  change5m = 0,
  change1h = 0,
  change24h = 0,

  exchangePercent = 0,
  othersPercent = 100,
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

      {/* Summary stats */}

      <TokenStats
        price={price}
        marketCap={marketCap}
        holders={holders}
        liquidity={liquidity}
        volume24h={volume24h}
      />

      {/* Detailed token metrics */}

      <TokenMetrics
        price={price}
        marketCap={marketCap}
        fdv={fdv}
        liquidity={liquidity}
        volume5m={volume5m}
        volume1h={volume1h}
        volume24h={volume24h}
        buys={buys}
        sells={sells}
        buyVolume={buyVolume}
        sellVolume={sellVolume}
        holders={holders}
        uniqueBuyers={uniqueBuyers}
        uniqueSellers={uniqueSellers}
        smartMoneyPercent={smartMoneyPercent}
        freshWalletPercent={freshWalletPercent}
        whalePercent={whalePercent}
        insiderPercent={insiderPercent}
        sniperPercent={sniperPercent}
        bundledPercent={bundledPercent}
        top10Percent={top10Percent}
        top25Percent={top25Percent}
        devHolding={devHolding}
        lpLockedPercent={lpLockedPercent}
        lpBurnedPercent={lpBurnedPercent}
        ath={ath}
        atl={atl}
        change5m={change5m}
        change1h={change1h}
        change24h={change24h}
      />

      {/* Liquidity */}

      <LiquidityPanel
        currentLiquidity={currentLiquidity}
        initialLiquidity={initialLiquidity}
        liquidityLocked={lpLocked ? 100 : 0}
        liquidityBurned={lpBurned ? 100 : 0}
        liquidityAdded24h={0}
        liquidityRemoved24h={0}
        buyWall={0}
        sellWall={0}
        liquidityHealth={securityScore}
        exitLiquidityScore={securityScore}
        migrationDetected={false}
        liquidityProviders={0}
        lpHolders={0}
        topLPHolder={0}
        rugRisk={Math.max(0, 100 - securityScore)}
      />

      {/* Holder distribution */}

      <HolderDistribution
        totalHolders={holders}
        top10Percent={top10Percent}
        top25Percent={top25Percent}
        smartMoneyPercent={smartMoneyPercent}
        whalePercent={whalePercent}
        freshWalletPercent={freshWalletPercent}
        insiderPercent={insiderPercent}
        sniperPercent={sniperPercent}
        deployerPercent={devHolding}
        lpPercent={0}
        burnedPercent={0}
        exchangePercent={exchangePercent}
        othersPercent={othersPercent}
      />

      {/* Quick actions */}

      <QuickActions
        contract={contract}
        explorerUrl={explorerUrl}
        dexUrl={dexUrl}
        onAIAnalysis={() => {
          console.log("AI Analysis");
        }}
        onReplay={() => {
          console.log("Replay");
        }}
        onWalletDNA={() => {
          console.log("Wallet DNA");
        }}
        onRugRadar={() => {
          console.log("Rug Radar");
        }}
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