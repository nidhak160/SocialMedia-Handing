import { FiMoreVertical } from "react-icons/fi";

function formatDate(dateString) {
  if (!dateString) return "";

  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(dateString));
}

function formatTime(dateString) {
  if (!dateString) return "";

  return new Intl.DateTimeFormat("en", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(dateString));
}

function ScheduledPosts({ posts = [] }) {
  const scheduledPosts = posts
    .filter((post) => post.status === "scheduled")
    .slice(0, 4);

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white text-lg font-semibold">Upcoming Scheduled Posts</h2>
        <button className="text-purple-400 text-sm hover:text-purple-300 transition-colors">
          View Calendar
        </button>
      </div>

      <div className="space-y-3">
        {scheduledPosts.length === 0 && (
          <div className="rounded-lg border border-dashed border-gray-700 p-6 text-center">
            <p className="text-gray-300 text-sm font-medium">No scheduled posts</p>
            <p className="text-gray-500 text-xs mt-1">
              Scheduled posts will show here after you create them.
            </p>
          </div>
        )}

        {scheduledPosts.map((post) => (
          <div
            key={post.id}
            className="flex items-center gap-4 p-3 rounded-lg hover:bg-[#0f0f1a] transition-colors group"
          >
            <div className="w-10 h-10 bg-purple-500/10 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg className="text-purple-400" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
            </div>

            <div className="flex-1 min-w-0">
              <h3 className="text-white text-sm font-medium mb-1">
                {post.title || "Untitled post"}
              </h3>
              <div className="flex items-center gap-3 text-xs text-gray-400">
                <span>{formatDate(post.scheduled_time)}</span>
                <span>-</span>
                <span>{formatTime(post.scheduled_time)}</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="px-3 py-1 bg-purple-500/10 text-purple-400 text-xs rounded-full font-medium capitalize">
                {post.status}
              </span>
              <button className="text-gray-500 hover:text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">
                <FiMoreVertical size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ScheduledPosts;
