import { useEffect, useState } from "react";
import api from "../services/api";

const AVAILABLE_PLATFORMS = [
  { key: "facebook", label: "Facebook", supported: true },
  { key: "linkedin", label: "LinkedIn", supported: true },
  { key: "instagram", label: "Instagram", supported: false },
  { key: "twitter", label: "X", supported: false },
  { key: "pinterest", label: "Pinterest", supported: false },
  { key: "threads", label: "Threads", supported: false },
];

function Accounts() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAccounts = async () => {
      try {
        const res = await api.get("social-accounts/");
        setAccounts(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadAccounts();
  }, []);

  const handleConnect = async (platform) => {
    const popup = window.open("", "Social Login", "width=600,height=700");
    if (!popup) {
      alert("Popup blocked. Please allow popups for this site and try again.");
      return;
    }

    popup.document.write(`<p>Loading ${platform} login...</p>`);

    const handleMessage = (event) => {
      if (!event.data) return;

      if (event.data.type === "facebookAuth" || event.data.type === "linkedinAuth") {
        localStorage.setItem("access", event.data.access);
        localStorage.setItem("refresh", event.data.refresh);
        localStorage.setItem("username", event.data.username);
        window.removeEventListener("message", handleMessage);
        alert(`${platform.charAt(0).toUpperCase() + platform.slice(1)} connected successfully`);
        window.location.reload();
      }

      if (event.data.type === "facebookAuthError" || event.data.type === "linkedinAuthError") {
        window.removeEventListener("message", handleMessage);
        alert(event.data.message || `${platform} login failed.`);
      }
    };

    window.addEventListener("message", handleMessage);

    try {
      const res = await api.get(`social-accounts/connect/${platform}/login/`);
      popup.location.href = res.data.login_url;
      popup.focus();

      const pollTimer = setInterval(() => {
        if (popup.closed) {
          clearInterval(pollTimer);
          window.removeEventListener("message", handleMessage);
        }
      }, 500);
    } catch (err) {
      console.error(err);
      window.removeEventListener("message", handleMessage);
      popup.close();
      alert(err.response?.data?.error || "Failed to connect account.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">Social Accounts</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {AVAILABLE_PLATFORMS.map((platform) => (
            <div key={platform.key} className="bg-white rounded-2xl shadow-md p-5">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold">{platform.label}</h2>
                  <p className="text-sm text-gray-500">
                    {platform.supported ? `Connect your ${platform.label} account.` : "Coming soon"}
                  </p>
                </div>
                <button
                  onClick={() => platform.supported && handleConnect(platform.key)}
                  disabled={!platform.supported}
                  className={`rounded-xl px-4 py-2 text-sm font-semibold ${
                    platform.supported
                      ? "bg-blue-600 hover:bg-blue-700 text-white"
                      : "bg-gray-300 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  {platform.supported ? "Connect" : "Coming Soon"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Accounts;
