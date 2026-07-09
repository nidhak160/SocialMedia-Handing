import { FiFileText, FiUsers } from "react-icons/fi";

function getTimeAgo(dateString) {
  if (!dateString) return "";

  const seconds = Math.floor((new Date() - new Date(dateString)) / 1000);
  if (seconds < 60) return "just now";

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours > 1 ? "s" : ""} ago`;

  const days = Math.floor(hours / 24);
  return `${days} day${days > 1 ? "s" : ""} ago`;
}

function RecentActivity({ posts = [], accounts = [] }) {
  const postActivities = posts.slice(0, 3).map((post) => ({
    id: `post-${post.id}`,
    action: `Post created: ${post.title || post.caption?.slice(0, 40) || "Untitled post"}`,
    icon: FiFileText,
    color: "#8b5cf6",
    time: getTimeAgo(post.created_at),
  }));

  const accountActivities = accounts
    .filter((account) => account.is_connected)
    .slice(0, 2)
    .map((account) => ({
      id: `account-${account.id}`,
      action: `${account.platform} account connected`,
      icon: FiUsers,
      color: "#3b82f6",
      time: "Connected",
    }));

  const activities = [...postActivities, ...accountActivities].slice(0, 5);

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <h2 className="text-white text-lg font-semibold mb-6">Recent Activity</h2>

      <div className="space-y-4">
        {activities.length === 0 && (
          <div className="rounded-lg border border-dashed border-gray-700 p-5 text-center">
            <p className="text-gray-300 text-sm font-medium">No activity yet</p>
            <p className="text-gray-500 text-xs mt-1">
              Activity will appear after you create posts or connect accounts.
            </p>
          </div>
        )}

        {activities.map((activity) => (
          <div
            key={activity.id}
            className="flex items-start gap-3 pb-4 border-b border-gray-800 last:border-0 last:pb-0"
          >
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ backgroundColor: `${activity.color}20` }}
            >
              <activity.icon size={16} style={{ color: activity.color }} />
            </div>

            <div className="flex-1 min-w-0">
              <p className="text-gray-300 text-sm">{activity.action}</p>
              <p className="text-gray-500 text-xs mt-1">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentActivity;
