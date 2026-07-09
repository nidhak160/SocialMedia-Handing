import { useEffect, useState } from "react";
import api from "../services/api";

const FACEBOOK_APP_ID = "4003547963273811";

function Posts() {
  const [posts, setPosts] = useState([]);
  const [form, setForm] = useState({
    id: null,
    title: "",
    content: "",
    image: null,
  });
  const [facebookConnected, setFacebookConnected] = useState(false);

  // 📌 Fetch posts
  const fetchPosts = async () => {
    try {
      const res = await api.get("posts/");
      setPosts(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  // 🕐 Time ago function
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
    checkFacebookStatus();
  }, []);

  // 🧠 Handle input
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

  // 🚀 Submit (Create + Update)
  const handleSubmit = async (e) => {
    e.preventDefault();

    
    const data = new FormData();
    data.append("title", form.title);
    data.append("content", form.content);

    if (form.image) {
      data.append("image", form.image);
    }

    try {
      if (form.id) {
        await api.put(`posts/${form.id}/`, data, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      } else {
        await api.post("posts/", data, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      }

      setForm({ id: null, title: "", content: "", image: null });
      fetchPosts();
    } catch (err) {
      console.log(err);
    }
  };

  // 🗑 Delete post
  const handleDelete = async (id) => {
    try {
      await api.delete(`posts/${id}/`);
      fetchPosts();
    } catch (err) {
      console.log(err);
    }
  };

  // ✏️ Edit post
  const handleEdit = (post) => {
    setForm({
      id: post.id,
      title: post.title,
      content: post.content,
      image: null,
    });
  };

  // 📘 Check Facebook connection status
  const checkFacebookStatus = async () => {
    try {
      const res = await api.get("social-accounts/facebook/status/");
      setFacebookConnected(res.data.is_connected);
    } catch (err) {
      console.log(err);
    }
  };

  // 📘 Share post to Facebook
  const handleShareToFacebook = async (postId) => {
    try {
      const res = await api.post(`social-accounts/facebook/share/${postId}/`);
      alert("Post shared to Facebook successfully!");
      fetchPosts();
    } catch (err) {
      alert("Failed to share to Facebook: " + (err.response?.data?.error || err.message));
      console.log(err);
    }
  };

  // 📘 Login with Facebook
  const handleFacebookLogin = () => {
    const width = 600;
    const height = 400;
    const left = window.screen.width / 2 - width / 2;
    const top = window.screen.height / 2 - height / 2;
    
    // Get Facebook login URL from backend
    api.get("social-accounts/facebook/login/")
      .then(res => {
        const loginUrl = res.data.login_url;
        const popup = window.open(
          loginUrl,
          "Facebook Login",
          `width=${width},height=${height},left=${left},top=${top}`
        );
        
        // Poll for popup close
        const pollTimer = setInterval(() => {
          if (popup?.closed) {
            clearInterval(pollTimer);
            checkFacebookStatus();
          }
        }, 500);
      })
      .catch(err => {
        alert(err.response?.data?.error || "Failed to initiate Facebook login");
        console.log(err);
      });
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">

      {/* Title */}
      <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
        Posts Manager
      </h1>

      <div className="max-w-2xl mx-auto">

        {/* 📝 Create / Edit Post */}
        <form
          onSubmit={handleSubmit}
          className="bg-white p-5 rounded-2xl shadow-md mb-8"
        >
          <input
            type="text"
            name="title"
            placeholder="What's on your mind?"
            value={form.title}
            onChange={handleChange}
            className="w-full border p-3 rounded-xl mb-3 focus:ring-2 focus:ring-blue-400"
          />

          <textarea
            name="content"
            placeholder="Write something amazing..."
            value={form.content}
            onChange={handleChange}
            className="w-full border p-3 rounded-xl mb-3 h-28 resize-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="file"
            onChange={handleFile}
            className="mb-4 text-sm"
          />

          <div className="flex gap-2">
            <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl font-semibold">
              {form.id ? "Update Post" : "Create Post"}
            </button>
            
            {!facebookConnected && (
              <button
                type="button"
                onClick={handleFacebookLogin}
                className="bg-blue-800 hover:bg-blue-900 text-white px-4 py-2 rounded-xl font-semibold flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
                FB
              </button>
            )}
          </div>
        </form>

        {/* 📱 Instagram Feed */}
        <div className="space-y-6">

          {posts.map((post) => (
            <div
              key={post.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200"
            >

              {/* 👤 Header */}
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
                <div className="flex gap-3 text-sm">

                  <button
                    onClick={() => handleEdit(post)}
                    className="text-blue-500"
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(post.id)}
                    className="text-red-500"
                  >
                    Delete
                  </button>

                  {facebookConnected && (
                    <button
                      onClick={() => handleShareToFacebook(post.id)}
                      className="text-blue-600 font-semibold"
                      title="Share to Facebook"
                    >
                      📘 Share
                    </button>
                  )}

                </div>

              </div>

              {/* 🖼 Image */}
              {post.image && (
                <img
                  src={post.image}
                  alt="post"
                  className="w-full max-h-[500px] object-cover"
                />
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
