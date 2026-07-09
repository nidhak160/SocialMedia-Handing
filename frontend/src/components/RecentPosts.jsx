import { FiMoreVertical } from "react-icons/fi";

function getTimeAgo(dateString) {
  if (!dateString) return "";

  const seconds = Math.floor((new Date() - new Date(dateString)) / 1000);
  const intervals = [
    { label: "year", seconds: 31536000 },
    { label: "month", seconds: 2592000 },
    { label: "week", seconds: 604800 },
    { label: "day", seconds: 86400 },
    { label: "hour", seconds: 3600 },
    { label: "minute", seconds: 60 },
  ];

  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      return `${count} ${interval.label}${count > 1 ? "s" : ""} ago`;
    }
  }

  return "just now";
}

function RecentPosts({ posts = [] }) {
  const recentPosts = posts.slice(0, 4);

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white text-lg font-semibold">Recent Posts</h2>
        <button className="text-purple-400 text-sm hover:text-purple-300 transition-colors">
          View All
        </button>
      </div>

      <div className="space-y-4">
        {recentPosts.length === 0 && (
          <div className="rounded-lg border border-dashed border-gray-700 p-6 text-center">
            <p className="text-gray-300 text-sm font-medium">No posts yet</p>
            <p className="text-gray-500 text-xs mt-1">
              Your posts will appear here after you create them.
            </p>
          </div>
        )}

        {recentPosts.map((post) => (
          <div
            key={post.id}
            className="flex gap-4 p-3 rounded-lg hover:bg-[#0f0f1a] transition-colors group"
          >
            {post.image ? (
              <img
                src={post.image}
                alt={post.title || "Post"}
                className="w-16 h-16 rounded-lg object-cover"
              />
            ) : (
              <div className="w-16 h-16 rounded-lg bg-[#0f0f1a] border border-gray-800 flex items-center justify-center text-gray-500 text-xs">
                No image
              </div>
            )}

            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-1">
                <h3 className="text-white text-sm font-medium truncate pr-2">
                  {post.title || "Untitled post"}
                </h3>
                <button className="text-gray-500 hover:text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">
                  <FiMoreVertical size={16} />
                </button>
              </div>

              <p className="text-gray-400 text-xs mb-2 line-clamp-1">
                {post.content || post.caption}
              </p>

              <div className="flex items-center justify-between">
                <span className="text-gray-500 text-xs">Post</span>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 bg-green-500/10 text-green-400 text-xs rounded-full capitalize">
                    {post.status}
                  </span>
                  <span className="text-gray-500 text-xs">{getTimeAgo(post.created_at)}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentPosts;
