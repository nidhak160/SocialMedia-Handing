import { NavLink } from "react-router-dom";
import { 
  FiHome, 
  FiFileText, 
  FiPlusCircle, 
  FiCalendar, 
  FiCalendar as FiCalendarIcon,
  FiImage, 
  FiUsers, 
  FiBarChart2, 
  FiInbox, 
  FiSettings, 
  FiUser 
} from "react-icons/fi";

function Sidebar() {
  const navItems = [
    { path: "/dashboard", icon: FiHome, label: "Dashboard" },
    { path: "/dashboard/posts", icon: FiFileText, label: "Posts" },
    { path: "/dashboard/create-post", icon: FiPlusCircle, label: "Create Post" },
    { path: "/dashboard/scheduled", icon: FiCalendar, label: "Scheduled Posts" },
    { path: "/dashboard/calendar", icon: FiCalendarIcon, label: "Calendar" },
    { path: "/dashboard/media", icon: FiImage, label: "Media Library" },
    { path: "/dashboard/accounts", icon: FiUsers, label: "Social Accounts" },
    { path: "/dashboard/analytics", icon: FiBarChart2, label: "Analytics" },
    { path: "/dashboard/inbox", icon: FiInbox, label: "Inbox" },
    { path: "/dashboard/settings", icon: FiSettings, label: "Settings" },
    { path: "/dashboard/profile", icon: FiUser, label: "Profile" },
  ];

  return (
    <div className="w-64 shrink-0 bg-[#0f0f1a] h-screen flex flex-col">
      {/* Logo */}
      <div className="p-6 flex items-center gap-3">
        <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-lg">S</span>
        </div>
        <span className="text-white text-xl font-bold">SocialHub</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                isActive
                  ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white"
                  : "text-gray-400 hover:bg-gray-800 hover:text-white"
              }`
            }
          >
            <item.icon size={20} />
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Upgrade Section */}
      <div className="p-4">
        <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 border border-purple-500/20 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-yellow-400 text-xl">⭐</span>
            <span className="text-white font-semibold text-sm">Upgrade to Pro</span>
          </div>
          <p className="text-gray-400 text-xs mb-3">
            Unlock advanced analytics, team members and more features.
          </p>
          <button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white text-sm font-medium py-2 rounded-lg hover:opacity-90 transition-opacity">
            Upgrade Now
          </button>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
