// frontend/src/components/kpi/KpiCard.tsx
import React from 'react';

interface KpiCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode; // To pass icons like <FiDollarSign />
  // Add more props for change, trend, etc. if needed
}

const KpiCard: React.FC<KpiCardProps> = ({ title, value, icon }) => {
  return (
    <div className="bg-dark-card p-6 rounded-lg shadow-md flex items-center space-x-4">
      {icon && <div className="p-3 rounded-full bg-brand-blue bg-opacity-20 text-brand-blue">{icon}</div>}
      <div>
        <p className="text-sm text-gray-400">{title}</p>
        <p className="text-2xl font-semibold text-gray-100">{value}</p>
      </div>
    </div>
  );
};
export default KpiCard;