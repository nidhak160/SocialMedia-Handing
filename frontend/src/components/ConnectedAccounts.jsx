import { FiMoreVertical, FiPlus } from "react-icons/fi";

function ConnectedAccounts({ accounts = [] }) {
  const connectedAccounts = accounts.filter((account) => account.is_connected);

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-white text-lg font-semibold">Connected Accounts</h2>
          <p className="text-gray-400 text-xs mt-1">Manage your social accounts</p>
        </div>
        <button className="w-8 h-8 bg-purple-500/10 hover:bg-purple-500/20 rounded-lg flex items-center justify-center text-purple-400 transition-colors">
          <FiPlus size={18} />
        </button>
      </div>

      <div className="space-y-3">
        {connectedAccounts.length === 0 && (
          <div className="rounded-lg border border-dashed border-gray-700 p-5 text-center">
            <p className="text-gray-300 text-sm font-medium">No accounts connected</p>
            <p className="text-gray-500 text-xs mt-1">
              Connected social accounts will appear here.
            </p>
          </div>
        )}

        {connectedAccounts.map((account) => (
          <div
            key={account.id}
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#0f0f1a] transition-colors group"
          >
            <div className="w-10 h-10 rounded-lg bg-[#0f0f1a] flex items-center justify-center text-sm text-purple-300 font-semibold uppercase">
              {account.platform?.slice(0, 1)}
            </div>

            <div className="flex-1 min-w-0">
              <h3 className="text-white text-sm font-medium capitalize">
                {account.platform}
              </h3>
              <p className="text-gray-400 text-xs">{account.account_name}</p>
            </div>

            <button className="text-gray-500 hover:text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">
              <FiMoreVertical size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ConnectedAccounts;
