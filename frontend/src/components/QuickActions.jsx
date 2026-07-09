import { useNavigate } from "react-router-dom";
import { FiEdit, FiImage, FiCalendar, FiBarChart2, FiUsers } from "react-icons/fi";

function QuickActions() {
  const navigate = useNavigate();
  const actions = [
    { icon: FiEdit, label: "Create New Post", color: "purple", path: "/dashboard/posts" },
    { icon: FiImage, label: "Upload Media", color: "blue", path: "/dashboard/posts" },
    { icon: FiCalendar, label: "View Calendar", color: "green", path: "/dashboard" },
    { icon: FiBarChart2, label: "Analytics Report", color: "orange", path: "/dashboard" },
    { icon: FiUsers, label: "Manage Accounts", color: "pink", path: "/dashboard" },
  ];

  const colorClasses = {
    purple: "bg-purple-500/10 text-purple-400 hover:bg-purple-500/20",
    blue: "bg-blue-500/10 text-blue-400 hover:bg-blue-500/20",
    green: "bg-green-500/10 text-green-400 hover:bg-green-500/20",
    orange: "bg-orange-500/10 text-orange-400 hover:bg-orange-500/20",
    pink: "bg-pink-500/10 text-pink-400 hover:bg-pink-500/20",
  };

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <h2 className="text-white text-lg font-semibold mb-4">Quick Actions</h2>

      <div className="space-y-2">
        {actions.map((action) => (
          <button
            key={action.label}
            onClick={() => navigate(action.path)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${colorClasses[action.color]}`}
          >
            <action.icon size={18} />
            <span className="text-sm font-medium">{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default QuickActions;
