import { Doughnut, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

function EmptyChart({ message }) {
  return (
    <div className="h-64 rounded-lg border border-dashed border-gray-700 flex items-center justify-center text-center px-6">
      <div>
        <p className="text-gray-300 text-sm font-medium">{message}</p>
        <p className="text-gray-500 text-xs mt-1">
          Charts will update automatically when you add posts.
        </p>
      </div>
    </div>
  );
}

function PostsOverview({ posts = [] }) {
  const counts = {
    posted: posts.filter((post) => ["posted", "published"].includes(post.status)).length,
    scheduled: posts.filter((post) => post.status === "scheduled").length,
    failed: posts.filter((post) => post.status === "failed").length,
  };
  const total = posts.length;

  const doughnutData = {
    labels: ["Published", "Scheduled", "Failed"],
    datasets: [
      {
        data: [counts.posted, counts.scheduled, counts.failed],
        backgroundColor: ["#8b5cf6", "#3b82f6", "#ef4444"],
        borderWidth: 0,
        hoverOffset: 4,
      },
    ],
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "70%",
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#1a1a2e",
        titleColor: "#fff",
        bodyColor: "#9ca3af",
        borderColor: "#374151",
        borderWidth: 1,
        padding: 10,
        displayColors: true,
      },
    },
  };

  const percent = (value) => Math.round((value / total) * 100);

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white text-lg font-semibold">Posts Overview</h2>
      </div>

      {total === 0 ? (
        <EmptyChart message="No post data yet" />
      ) : (
        <div className="flex items-center gap-6">
          <div className="relative w-48 h-48">
            <Doughnut data={doughnutData} options={doughnutOptions} />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-white text-2xl font-bold">{total}</div>
                <div className="text-gray-400 text-xs">Total</div>
              </div>
            </div>
          </div>

          <div className="flex-1 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                <span className="text-gray-300 text-sm">Published</span>
              </div>
              <div className="text-right">
                <span className="text-white text-sm font-medium">{counts.posted}</span>
                <span className="text-gray-500 text-xs ml-2">({percent(counts.posted)}%)</span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                <span className="text-gray-300 text-sm">Scheduled</span>
              </div>
              <div className="text-right">
                <span className="text-white text-sm font-medium">{counts.scheduled}</span>
                <span className="text-gray-500 text-xs ml-2">({percent(counts.scheduled)}%)</span>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span className="text-gray-300 text-sm">Failed</span>
              </div>
              <div className="text-right">
                <span className="text-white text-sm font-medium">{counts.failed}</span>
                <span className="text-gray-500 text-xs ml-2">({percent(counts.failed)}%)</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function PostsByPlatform({ posts = [] }) {
  const barData = {
    labels: ["Created Posts"],
    datasets: [
      {
        label: "Posts",
        data: [posts.length],
        backgroundColor: ["#8b5cf6"],
        borderRadius: 6,
        barThickness: 20,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: "y",
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#1a1a2e",
        titleColor: "#fff",
        bodyColor: "#9ca3af",
        borderColor: "#374151",
        borderWidth: 1,
        padding: 10,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          color: "#374151",
          drawBorder: false,
        },
        ticks: {
          color: "#9ca3af",
          precision: 0,
          font: {
            size: 11,
          },
        },
      },
      y: {
        grid: {
          display: false,
        },
        ticks: {
          color: "#9ca3af",
          font: {
            size: 12,
          },
        },
      },
    },
  };

  return (
    <div className="bg-[#1a1a2e] border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white text-lg font-semibold">Posts Summary</h2>
      </div>

      {posts.length === 0 ? (
        <EmptyChart message="No post summary yet" />
      ) : (
        <div className="h-64">
          <Bar data={barData} options={barOptions} />
        </div>
      )}
    </div>
  );
}

function Charts({ posts = [] }) {
  return (
    <div className="grid grid-cols-2 gap-6">
      <PostsOverview posts={posts} />
      <PostsByPlatform posts={posts} />
    </div>
  );
}

export default Charts;
