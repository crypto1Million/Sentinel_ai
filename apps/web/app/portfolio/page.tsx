export default function PortfolioPage() {

  const portfolio = {
    totalValue: 12543,
    realizedPnL: 3210,
    unrealizedPnL: 1890,
    winRate: 67
  };

  return (
    <div className="p-6">

      <h1 className="text-3xl font-bold mb-6">
        Portfolio
      </h1>

      <div className="grid grid-cols-4 gap-4">

        <div className="border p-4 rounded">
          <h3>Total Value</h3>
          <p>${portfolio.totalValue}</p>
        </div>

        <div className="border p-4 rounded">
          <h3>Realized PnL</h3>
          <p>${portfolio.realizedPnL}</p>
        </div>

        <div className="border p-4 rounded">
          <h3>Unrealized PnL</h3>
          <p>${portfolio.unrealizedPnL}</p>
        </div>

        <div className="border p-4 rounded">
          <h3>Win Rate</h3>
          <p>{portfolio.winRate}%</p>
        </div>

      </div>

    </div>
  );
}