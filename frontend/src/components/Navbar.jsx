import { useNavigate } from "react-router-dom";
import { FiMoon, FiBell, FiUser, FiLogOut } from "react-icons/fi";

function Navbar() {
  const navigate = useNavigate();
  const username = localStorage.getItem("username") || "User";

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
    navigate("/");
  };

  return (
    <div className="h-16 bg-[#0f0f1a] flex items-center justify-between px-6">
      <div className="flex-1 max-w-2xl">
        <div className="relative">
          <input
            type="text"
            placeholder="Search posts, accounts, hashtags..."
            className="w-full bg-[#1a1a2e] text-gray-300 placeholder-gray-500 rounded-lg pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 border border-gray-800"
          />
          <svg
            className="absolute left-3 top-2.5 text-gray-500"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2" >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>  
        </div>
      </div>

      <div className="flex items-center gap-4 ml-6"> 
        <button className="p-2 text-gray-400 hover:text-white transition-colors">
          <FiMoon size={20} />
        </button>

        <button className="p-2 text-gray-400 hover:text-white transition-colors relative">
          <FiBell size={20} />
        </button>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-white text-sm font-medium">{username}</div>
            <div className="text-gray-500 text-2xl font-bold">User</div>
          </div>
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
            <FiUser className="text-white" size={20} />
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="ml-4 p-2 text-gray-400 hover:text-white transition-colors rounded-full border border-gray-700 hover:border-gray-500"
          title="Logout"
        >
          <FiLogOut size={20} />
        </button>
      </div>
    </div>
  );
}

export default Navbar;


