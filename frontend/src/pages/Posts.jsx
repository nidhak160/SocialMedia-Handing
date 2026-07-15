import { useEffect, useState } from "react";
import api from "../services/api";

const AVAILABLE_PLATFORMS = [
  { key: "facebook", label: "Facebook" },
  { key: "instagram", label: "Instagram" },
  { key: "linkedin", label: "LinkedIn" },
  { key: "twitter", label: "X" },
  { key: "pinterest", label: "Pinterest" },
  { key: "threads", label: "Threads" },
];

function Posts() {
  const [posts, setPosts] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [form, setForm] = useState({
    id: null,
    title: "",
    content: "",
    image: null,
    platforms: [],
    scheduled_time: "",
  });
  const [facebookConnected, setFacebookConnected] = useState(false);

  // Fetch posts
  const fetchPosts = async () => {
    try {
      const res = await api.get("posts/");
      setPosts(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const fetchAccounts = async () => {
    try {
      const res = await api.get("social-accounts/");
      const accountList = Array.isArray(res.data) ? res.data : [];
      setAccounts(accountList);

      const facebookAccounts = accountList.filter(
        (acc) => acc.platform === "facebook" && acc.is_connected
      );
      setFacebookConnected(facebookAccounts.length > 0);
    } catch (err) {
      console.log(err);
    }
  };

  // Time ago function
  const getTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    const intervals = [
      { label: "year", seconds: 31536000 },
      { label: "month", seconds: 2592000 },
      { label: "week", seconds: 604800 },
      { label: "day", seconds: 86400 },
      { label: "hour", seconds: 3600 },
      { label: "minute", seconds: 60 },
      { label: "second", seconds: 1 },
    ];

    for (const interval of intervals) {
      const count = Math.floor(seconds / interval.seconds);
      if (count >= 1) {
        return `${count} ${interval.label}${count > 1 ? "s" : ""} ago`;
      }
    }

    return "just now";
  };

  useEffect(() => {
    fetchPosts();
    fetchAccounts();
  }, []);

  // Handle input
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleFile = (e) => {
    setForm({
      ...form,
      image: e.target.files[0],
    });
  };

  const handlePlatformToggle = (platform) => {
    setForm((prev) => {
      const platforms = prev.platforms.includes(platform)
        ? prev.platforms.filter((item) => item !== platform)
        : [...prev.platforms, platform];

      return { ...prev, platforms };
    });
  };

  // Submit (Create + Update)
  const handleSubmit = async (e) => {
    e.preventDefault();

    const contentValue = form.content.trim() || form.title.trim();

    if (!contentValue && !form.image) {
      alert("Post content or image is required.");
      return;
    }

    const data = new FormData();
    data.append("title", form.title);
    data.append("content", contentValue);

    if (form.image) {
      data.append("image", form.image);
    }

    if (form.scheduled_time) {
      data.append("scheduled_time", form.scheduled_time);
    }

    if (form.platforms.length > 0) {
      data.append("platforms", JSON.stringify(form.platforms));
    }

    try {
      let response;

      if (form.id) {
        response = await api.put(`posts/${form.id}/`, data);
      } else {
        response = await api.post("posts/", data);
      }

      console.log(response.data);

      setForm({
        id: null,
        title: "",
        content: "",
        image: null,
        platforms: [],
        scheduled_time: "",
      });

      fetchPosts();
    } catch (err) {
      console.log("Status:", err.response?.status);
      console.log("Error:", err.response?.data);
      alert(err.response?.data?.content || err.response?.data?.error || JSON.stringify(err.response?.data) || "Failed to save post.");
    }
  };

  // Delete post
  const handleDelete = async (id) => {
    try {
      await api.delete(`posts/${id}/`);
      fetchPosts();
    } catch (err) {
      console.log(err);
    }
  };

  // Edit post
  const handleEdit = (post) => {
    setForm({
      id: post.id,
      title: post.title,
      content: post.content,
      image: null,
      platforms: post.platforms || [],
      scheduled_time: post.scheduled_time
        ? post.scheduled_time.slice(0, 16)
        : "",
    });
  };

  //  Share post to Facebook via backend
  const handleShareToFacebook = async (post) => {
    if (!post) return;

    try {
      const response = await api.post(`social-accounts/facebook/share/${post.id}/`);
      alert(response.data.message || "Shared to Facebook successfully");
      fetchPosts();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Failed to share to Facebook");
    }
  };

  const handleShareToLinkedIn = async (post) => {
    if (!post) return;

    try {
      const response = await api.post(`social-accounts/linkedin/share/${post.id}/`);
      alert(response.data.message || "Shared to LinkedIn successfully");
      fetchPosts();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Failed to share to LinkedIn");
    }
  };

  const linkedinConnected = accounts.some(
    (acc) => acc.platform === "linkedin" && acc.is_connected
  );


  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">

      {/* Title */}
      <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
        Posts Manager
      </h1>

      <div className="max-w-2xl mx-auto">


        {/* Create / Edit Post */}
        <form
          onSubmit={handleSubmit}
          className="bg-white p-5 rounded-2xl shadow-md mb-8" >

          <input
            type="text"
            name="title"
            placeholder="What's on your mind?"
            value={form.title}
            onChange={handleChange}
            className="w-full border p-3 rounded-xl mb-3 focus:ring-2 focus:ring-blue-400" />

          <textarea
            name="content"
            placeholder="Write something amazing..."
            value={form.content}
            onChange={handleChange}
            className="w-full border p-3 rounded-xl mb-3 h-28 resize-none focus:ring-2 focus:ring-blue-400" />

          <input
            type="file"
            onChange={handleFile}
            className="mb-4 text-sm" />

          <div className="mb-4">
            <p className="text-sm font-semibold mb-2">Publish to</p>
            <div className="grid grid-cols-3 gap-2">
              {AVAILABLE_PLATFORMS.map((platform) => (
                <button
                  key={platform.key}
                  type="button"
                  onClick={() => handlePlatformToggle(platform.key)}
                  className={`rounded-xl border px-3 py-2 text-sm font-semibold transition ${
                    form.platforms.includes(platform.key)
                      ? "border-blue-600 bg-blue-50 text-blue-700"
                      : "border-gray-300 bg-white text-gray-700"
                  }`}>
                  {platform.label}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Schedule publish
            </label>
            <input
              type="datetime-local"
              name="scheduled_time"
              value={form.scheduled_time}
              onChange={handleChange}
              className="w-full border p-3 rounded-xl focus:ring-2 focus:ring-blue-400" />
            <p className="text-xs text-gray-500 mt-1">
              Leave blank to publish immediately.
            </p>
          </div>

          <div className="flex gap-2">
            <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl font-semibold">
              {form.id ? "Update Post" : "Create Post"}
            </button>
            
          </div>
        </form>

        {/* Instagram Feed */}
        <div className="space-y-6">

          {posts.map((post) => (
            <div
              key={post.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200" >

              {/* Header */}
              <div className="flex items-center justify-between px-4 py-3">

                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gray-300"></div>

                  <div>
                    <h3 className="font-semibold text-sm">
                      {post.username}
                    </h3>
                    <p className="text-xs text-gray-500">
                      {getTimeAgo(post.created_at)}
                    </p>
                  </div>
                </div>

                {/* actions */}
                <div className="flex flex-wrap gap-3 text-sm">

                  <button
                    onClick={() => handleEdit(post)}
                    className="text-blue-500" >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(post.id)}
                    className="text-red-500" >
                    Delete
                  </button>

                  {post.platforms?.includes("facebook") && (
                    <span className="inline-flex items-center gap-1 rounded-full border border-blue-500 bg-blue-50 px-2 py-1 text-blue-700">
                      📘 Facebook
                    </span>
                  )}

                  {post.platforms?.includes("linkedin") && (
                    <span className="inline-flex items-center gap-1 rounded-full border border-blue-700 bg-blue-50 px-2 py-1 text-blue-700">
                      💼 LinkedIn
                    </span>
                  )}

                  {facebookConnected && post.platforms?.includes("facebook") && (
                    <button
                      type="button"
                      onClick={() => handleShareToFacebook(post)}
                      className="text-blue-600 font-semibold"
                      title="Share to Facebook" >
                      Share Now
                    </button>
                  )}

                  {linkedinConnected && post.platforms?.includes("linkedin") && (
                    <button
                      type="button"
                      onClick={() => handleShareToLinkedIn(post)}
                      className="text-blue-600 font-semibold"
                      title="Share to LinkedIn" >
                      Upload to LinkedIn
                    </button>
                  )}

                </div>

              </div>

              {/* Image */}
              {post.image && (
                <img
                  src={post.image}
                  alt="post"
                  className="w-full max-h-[500px] object-cover" />
              )}

              {/* ❤️ Actions */}
              <div className="flex justify-between px-4 py-3 text-2xl">
                <div className="flex gap-4">
                  <span>❤️</span>
                  <span>💬</span>
                  <span>📤</span>
                </div>
                <span>🔖</span>
              </div>

              {/* 📝 Caption */}
              <div className="px-4 pb-4">

                <p className="font-semibold text-sm mb-1">
                  {post.title}
                </p>

                <p className="text-sm text-gray-700">
                  {post.content}
                </p>

              </div>

            </div>
          ))}

        </div>
      </div>
    </div>
  );
}

export default Posts;
