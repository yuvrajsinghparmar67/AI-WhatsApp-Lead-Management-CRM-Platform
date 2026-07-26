import { ShieldCheck } from "lucide-react";
import Avatar from "../../../components/ui/Avatar";
import Badge from "../../../components/ui/Badge";
import { useAuth } from "../../../context/AuthContext";
import { useUpdateUser, useUsers } from "../hooks/useUsers";

export default function TeamMembersPanel() {
  const { data: members, isLoading } = useUsers();
  const updateUser = useUpdateUser();
  const { user: currentUser } = useAuth();

  const handleRoleChange = (member, role) => {
    updateUser.mutate({ id: member.id, payload: { role } });
  };

  const toggleActive = (member) => {
    updateUser.mutate({ id: member.id, payload: { is_active: !member.is_active } });
  };

  return (
    <div className="max-w-2xl">
      <div>
        <h2 className="font-display font-bold text-lg">Team Members & Roles</h2>
        <p className="text-sm text-gray-400 mt-0.5">
          Two fixed roles: <strong>Admin</strong> (full access, including this Admin Portal) and{" "}
          <strong>Agent</strong> (Inbox, Contacts, and Analytics only — no Admin Portal access).
        </p>
      </div>

      <div className="mt-5 space-y-2">
        {isLoading && <p className="text-sm text-gray-400">Loading...</p>}

        {members?.map((member) => {
          const isSelf = member.id === currentUser?.id;
          return (
            <div key={member.id} className="glass-panel p-4 flex items-center gap-3">
              <Avatar name={member.full_name} size={36} />
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <p className="text-sm font-medium">{member.full_name}</p>
                  {isSelf && <span className="text-[10px] text-gray-400">(you)</span>}
                  {!member.is_active && <Badge priority="low">Inactive</Badge>}
                </div>
                <p className="text-xs text-gray-400">{member.email}</p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <select
                  value={member.role}
                  disabled={isSelf}
                  onChange={(e) => handleRoleChange(member, e.target.value)}
                  title={isSelf ? "You can't change your own role" : "Change role"}
                  className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-xs disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <option value="agent">Agent</option>
                  <option value="admin">Admin</option>
                </select>

                <button
                  onClick={() => toggleActive(member)}
                  disabled={isSelf}
                  title={isSelf ? "You can't deactivate your own account" : member.is_active ? "Deactivate" : "Activate"}
                  className="text-xs rounded-lg border border-gray-200 dark:border-white/10 px-2.5 py-1.5 text-gray-500 hover:bg-gray-50 dark:hover:bg-white/5 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {member.is_active ? "Deactivate" : "Activate"}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 flex items-start gap-2 text-xs text-gray-400">
        <ShieldCheck size={13} className="shrink-0 mt-0.5" />
        <p>
          New team members join by registering at the login screen — the first account ever created
          automatically became admin; everyone after that starts as an Agent until promoted here.
        </p>
      </div>
    </div>
  );
}
