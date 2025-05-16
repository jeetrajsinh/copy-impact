// frontend/src/pages/DashboardPage.tsx
import React, { useState } from 'react';
import Sidebar from '../components/layout/Sidebar';
import type { PerformanceAnalysisResponseData } from '../types';
import { fetchPerformanceAnalysis } from '../services/apiService';
import { FiDollarSign, FiActivity, FiTrendingDown, FiUsers } from 'react-icons/fi'; // Example icons
import KpiCard from '../components/kpi/KpiCard';

const DashboardPage: React.FC = () => {
  const [performanceData, setPerformanceData] = useState<PerformanceAnalysisResponseData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetchData = async (mainWallet: string, masterWallets: string[]) => {
    setIsLoading(true);
    setError(null);
    try {
      const req = { main_wallet_address: mainWallet, master_wallet_addresses: masterWallets };
      const data = await fetchPerformanceAnalysis(req);
      setPerformanceData(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to fetch performance data');
      setPerformanceData(null);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Helper to format currency
  const formatCurrency = (value?: number | null) => {
    if (value === null || typeof value === 'undefined') return '-';
    return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  return (
    <div className="flex h-screen">
      <Sidebar onFetchData={handleFetchData} isFetching={isLoading} />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        {error && (
          <div className="bg-red-800 text-white p-4 rounded mb-4">{error}</div>
        )}
        {!performanceData ? (
          <div className="text-gray-400 text-lg mt-16">Enter wallet addresses and click Analyze to view performance.</div>
        ) : (
          <>
            <section className="mb-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Example KPIs, replace with real data fields */}
              <KpiCard title="Total PnL" value={formatCurrency(performanceData.main_wallet_summary?.total_pnl)} icon={<FiDollarSign />} />
              <KpiCard title="Realized PnL" value={formatCurrency(performanceData.main_wallet_summary?.realized_pnl)} icon={<FiActivity />} />
              <KpiCard title="Unrealized PnL" value={formatCurrency(performanceData.main_wallet_summary?.unrealized_pnl)} icon={<FiTrendingDown />} />
              <KpiCard title="Tokens Traded" value={performanceData.main_wallet_summary?.tokens_traded_count ?? '-'} icon={<FiUsers />} />
            </section>
            {/* Placeholder for "Comparative Token P&L & MCap" Table */}
            <section className="mb-8">
              {/* DataTable or other components go here */}
            </section>
          </>
        )}
      </main>
    </div>
  );
};
export default DashboardPage;