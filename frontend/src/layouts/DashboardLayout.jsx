import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function DashboardLayout() {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-[#0f0f1a]">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Area */}
      <div className="min-w-0 flex-1 flex flex-col overflow-hidden">
        {/* Navbar */}
        <Navbar />

        {/* Page Content */}
        <div className="min-w-0 flex-1 overflow-y-auto overflow-x-hidden p-6">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default DashboardLayout;
