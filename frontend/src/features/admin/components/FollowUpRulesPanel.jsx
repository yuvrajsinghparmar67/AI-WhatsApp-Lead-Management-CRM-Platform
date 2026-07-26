import { useState } from "react";
import { Plus, Trash2, Pencil, Clock, PlayCircle, MessageCircle } from "lucide-react";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import FollowUpRuleModal from "./FollowUpRuleModal";
import {
  useFollowUpRules,
  useFollowUpLogs,
  useDeleteFollowUpRule,
  useUpdateFollowUpRule,
  useRunFollowUpRulesNow,
} from "../hooks/useFollowUpRules";

export default function FollowUpRulesPanel() {
  const { data: rules, isLoading } = useFollowUpRules();
  const { data: logs, isLoading: logsLoading } = useFollowUpLogs();
  const deleteRule = useDeleteFollowUpRule();
  const updateRule = useUpdateFollowUpRule();
  const runNow = useRunFollowUpRulesNow();
  const [modalRule, setModalRule] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const openCreate = () => {
    setModalRule(null);
    setShowModal(true);
  };

  const openEdit = (rule) => {
    setModalRule(rule);
    setShowModal(true);
  };

  const toggleActive = (rule) => {
    updateRule.mutate({ id: rule.id, payload: { is_active: !rule.is_active } });
  };

  return (
    <div className="max-w-2xl space-y-8">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="font-display font-bold text-lg">Follow-up Rules</h2>
          <p className="text-sm text-gray-400 mt-0.5">
            Automatically re-engage leads who've gone quiet. A background scheduler checks every conversation on a
            timer and sends the rule's message once a customer's last message has sat unanswered long enough.
          </p>
        </div>
      </div>

      {/* Rules */}
      <div>
        <div className="flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-sm font-semibold">
            <Clock size={15} className="text-brand-500" /> Rules
          </h3>
          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              onClick={() => runNow.mutate()}
              disabled={runNow.isPending}
              className="!px-3 !py-1.5 text-xs"
              title="Check all open conversations against active rules right now, instead of waiting for the scheduler"
            >
              <PlayCircle size={14} /> {runNow.isPending ? "Running..." : "Run now"}
            </Button>
            <Button variant="secondary" onClick={openCreate} className="!px-3 !py-1.5 text-xs">
              <Plus size={14} /> Add rule
            </Button>
          </div>
        </div>

        <div className="mt-3 space-y-2">
          {!isLoading && (rules || []).length === 0 && (
            <div className="glass-panel p-4 text-sm text-gray-400 text-center">No follow-up rules yet.</div>
          )}
          {(rules || []).map((rule) => (
            <div key={rule.id} className="glass-panel p-3.5 flex items-start gap-3">
              <button onClick={() => toggleActive(rule)} title={rule.is_active ? "Active — click to disable" : "Disabled — click to enable"}>
                <Badge priority="low" className={rule.is_active ? "" : "opacity-40"}>
                  {rule.is_active ? "Active" : "Off"}
                </Badge>
              </button>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium">{rule.name}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                  After <span className="font-medium">{rule.idle_hours}h</span> of no reply
                  {rule.lead_status_filter ? (
                    <> for <span className="font-medium capitalize">{rule.lead_status_filter}</span> leads</>
                  ) : (
                    <> for any open lead</>
                  )}
                  , send: <span className="italic">&ldquo;{rule.message_template}&rdquo;</span>
                </p>
              </div>
              <div className="flex items-center gap-1 shrink-0">
                <button onClick={() => openEdit(rule)} className="text-gray-300 hover:text-brand-500 transition-colors duration-150">
                  <Pencil size={14} />
                </button>
                <button onClick={() => deleteRule.mutate(rule.id)} className="text-gray-300 hover:text-red-500 transition-colors duration-150">
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent activity */}
      <div>
        <h3 className="flex items-center gap-2 text-sm font-semibold">
          <MessageCircle size={15} className="text-brand-500" /> Recent activity
        </h3>
        <p className="text-xs text-gray-400 mt-1">The last follow-up messages actually sent, most recent first.</p>

        <div className="mt-3 space-y-2">
          {!logsLoading && (logs || []).length === 0 && (
            <div className="glass-panel p-4 text-sm text-gray-400 text-center">No follow-ups sent yet.</div>
          )}
          {(logs || []).map((log) => (
            <div key={log.id} className="glass-panel p-3.5">
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-medium">
                  {log.contact_display_name || log.contact_phone_number || "Unknown contact"}
                </p>
                <span className="text-xs text-gray-400 shrink-0">{new Date(log.sent_at).toLocaleString()}</span>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                via <span className="font-medium">{log.rule_name || "deleted rule"}</span> — &ldquo;{log.message_body}&rdquo;
              </p>
            </div>
          ))}
        </div>
      </div>

      {showModal && <FollowUpRuleModal rule={modalRule} onClose={() => setShowModal(false)} />}
    </div>
  );
}
