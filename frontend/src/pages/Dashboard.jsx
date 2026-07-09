import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import StatsCard from "../components/StatsCard";
import RecentPosts from "../components/RecentPosts";
import ScheduledPosts from "../components/ScheduledPosts";
import Charts from "../components/Charts";
import ConnectedAccounts from "../components/ConnectedAccounts";
import QuickActions from "../components/QuickActions";
import RecentActivity from "../components/RecentActivity";
import { FiFileText, FiCalendar, FiSend, FiUsers } from "react-icons/fi";
import api from "../services/api";

function Dashboard() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [profileRes, postsRes, accountsRes] = await Promise.all([
          api.get("auth/profile/"),
          api.get("posts/"),
          api.get("social-accounts/"),
        ]);

        setProfile(profileRes.data);
        setPosts(Array.isArray(postsRes.data) ? postsRes.data : []);
        setAccounts(Array.isArray(accountsRes.data) ? accountsRes.data : []);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  const stats = useMemo(() => {
    const scheduled = posts.filter((post) => post.status === "scheduled").length;
    const published = posts.filter((post) =>
      ["posted", "published"].includes(post.status)
    ).length;

    return {
      total: posts.length,
      scheduled,
      published,
      connectedAccounts: accounts.filter((account) => account.is_connected).length,
    };
  }, [posts, accounts]);

  const displayName =
    profile?.username || localStorage.getItem("username") || "User";

  return (
    <div className="min-w-0 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-white text-2xl font-bold mb-1">
            Welcome back, {displayName}!
          </h1>
          <p className="text-gray-400 text-sm">
            {loading
              ? "Loading your dashboard..."
              : "Manage your social media content from one place."}
          </p>
        </div>
        <button
          onClick={() => navigate("/dashboard/posts")}
          className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center gap-2"
        >
          <span className="text-xl">+</span>
          Create New Post
        </button>
      </div>

      <div className="grid min-w-0 grid-cols-4 gap-6">
        <StatsCard
          title="Total Posts"
          value={stats.total}
          icon={FiFileText}
          gradient="bg-gradient-to-br from-purple-600 to-blue-600"
        />
        <StatsCard
          title="Scheduled Posts"
          value={stats.scheduled}
          icon={FiCalendar}
          gradient="bg-gradient-to-br from-green-600 to-emerald-600"
        />
        <StatsCard
          title="Published Posts"
          value={stats.published}
          icon={FiSend}
          gradient="bg-gradient-to-br from-blue-600 to-cyan-600"
        />
        <StatsCard
          title="Connected Accounts"
          value={stats.connectedAccounts}
          icon={FiUsers}
          gradient="bg-gradient-to-br from-orange-600 to-red-600"
        />
      </div>

      <div className="grid min-w-0 grid-cols-3 gap-6">
        <div className="min-w-0 col-span-2 space-y-6">
          <RecentPosts posts={posts} />
          <ScheduledPosts posts={posts} />
          <Charts posts={posts} />
        </div>

        <div className="min-w-0 space-y-6">
          <ConnectedAccounts accounts={accounts} />
          <QuickActions />
          <RecentActivity posts={posts} accounts={accounts} />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
