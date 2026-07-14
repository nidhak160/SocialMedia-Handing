import {
  FiUserPlus,
  FiLogIn,
  FiHome,
  FiFacebook,
  FiEdit3,
  FiImage,
  FiSend,
  FiClock,
  FiGlobe,
  FiCheckCircle,
  FiBarChart2,
  FiBell,
} from "react-icons/fi";

const steps = [
  { label: "Register", description: "Create your account to start using the platform.", icon: FiUserPlus },
  { label: "Login", description: "Authenticate with JWT and access your dashboard.", icon: FiLogIn },
  { label: "Dashboard", description: "View your analytics, posts, and connected accounts.", icon: FiHome },
  { label: "Connect Facebook", description: "Link your Facebook account for publishing.", icon: FiFacebook },
  { label: "Create Post", description: "Write a post and prepare it for publishing.", icon: FiEdit3 },
  { label: "Upload Image", description: "Attach media to make your post engaging.", icon: FiImage },
  { label: "Publish Now or Schedule", description: "Choose immediate publish or set a future time.", icon: FiSend },
  { label: "Scheduler Checks Time", description: "The scheduler triggers posts at the scheduled moment.", icon: FiClock },
  { label: "Facebook Graph API", description: "The app calls Facebook Graph API to publish your content.", icon: FiGlobe },
  { label: "Post Published", description: "Your post is live on Facebook successfully.", icon: FiCheckCircle },
  { label: "Update Status & Analytics", description: "Track post status, reach and engagement metrics.", icon: FiBarChart2 },
  { label: "Send Notification", description: "Receive alerts once the publish process completes.", icon: FiBell },
];

function WorkflowSteps() {
  return (
    <div className="bg-[#11121f] border border-gray-800 rounded-3xl p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-purple-300 font-semibold">
            Publishing Workflow
          </p>
          <h2 className="text-white text-2xl font-bold mt-2">Step-by-step flow</h2>
          <p className="text-gray-400 text-sm mt-2">
            Follow the sequence from registration to publishing, analytics, and notifications.
          </p>
        </div>
      </div>

      <div className="space-y-5">
        {steps.map((step, index) => {
          const Icon = step.icon;
          return (
            <div key={step.label} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-600 to-blue-600 text-white flex items-center justify-center shadow-lg">
                  <Icon size={20} />
                </div>
                {index < steps.length - 1 && <div className="w-px h-full bg-gray-800 mt-2" />}
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between gap-3">
                  <h3 className="text-white font-semibold">{step.label}</h3>
                  <span className="text-xs uppercase tracking-[0.2em] text-gray-500">
                    Step {index + 1}
                  </span>
                </div>
                <p className="text-gray-400 text-sm mt-1">{step.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default WorkflowSteps;
