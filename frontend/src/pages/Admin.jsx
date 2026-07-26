import { useState } from "react";
import { ShieldAlert } from "lucide-react";
import AdminNav from "../features/admin/components/AdminNav";
import BusinessInfoPanel from "../features/admin/components/BusinessInfoPanel";
import CatalogPanel from "../features/admin/components/CatalogPanel";
import FaqPanel from "../features/admin/components/FaqPanel";
import KnowledgeBasePanel from "../features/admin/components/KnowledgeBasePanel";
import BusinessRulesPanel from "../features/admin/components/BusinessRulesPanel";
import FollowUpRulesPanel from "../features/admin/components/FollowUpRulesPanel";
import AISettingsPanel from "../features/admin/components/AISettingsPanel";
import PromptSettingsPanel from "../features/admin/components/PromptSettingsPanel";
import TeamMembersPanel from "../features/admin/components/TeamMembersPanel";
import { useAuth } from "../context/AuthContext";

const PANELS = {
  "business-info": BusinessInfoPanel,
  catalog: CatalogPanel,
  faqs: FaqPanel,
  "knowledge-base": KnowledgeBasePanel,
  "business-rules": BusinessRulesPanel,
  "follow-up-rules": FollowUpRulesPanel,
  "ai-settings": AISettingsPanel,
  "prompt-settings": PromptSettingsPanel,
  team: TeamMembersPanel,
};

export default function Admin() {
  const [activeSection, setActiveSection] = useState("business-info");
  const { user } = useAuth();
  const ActivePanel = PANELS[activeSection];

  // The sidebar already hides this link for non-admins, but the route
  // itself is still reachable by URL - the backend rejects the API calls
  // (403), but without this the panels would just render broken/empty
  // instead of explaining why.
  if (user && user.role !== "admin") {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="glass-panel p-8 max-w-sm text-center">
          <ShieldAlert className="mx-auto text-gray-300 dark:text-gray-600" size={28} />
          <p className="mt-3 text-sm font-medium">Admin access required</p>
          <p className="mt-1 text-xs text-gray-400">
            The Admin Portal is only available to admin accounts. Ask an admin to promote your account
            from the Team Members screen if you need access.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full">
      <AdminNav activeSection={activeSection} onSelect={setActiveSection} />
      <div className="flex-1 overflow-y-auto p-6">
        <ActivePanel />
      </div>
    </div>
  );
}
