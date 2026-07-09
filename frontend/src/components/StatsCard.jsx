function StatsCard({ title, value, change, icon: Icon, gradient }) {
  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg ${gradient} flex items-center justify-center`}>
          <Icon className="text-white" size={24} />
        </div>
      </div>

      <div>
        <p className="text-gray-400 text-sm mb-1">{title}</p>
        <h3 className="text-white text-3xl font-bold mb-2">{value}</h3>
        {change ? (
          <div className="flex items-center gap-1 text-sm">
            <span className="text-green-400">{change}</span>
            <span className="text-gray-500">from last month</span>
          </div>
        ) : (
          <p className="text-gray-500 text-sm">Your current data</p>
        )}
      </div>
    </div>
  );
}

export default StatsCard;
