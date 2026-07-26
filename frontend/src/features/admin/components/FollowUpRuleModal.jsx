import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useCreateFollowUpRule, useUpdateFollowUpRule } from "../hooks/useFollowUpRules";

const LEAD_STATUS_OPTIONS = ["", "new", "qualified", "nurturing"];
const LEAD_STATUS_LABELS = { "": "Any open status", new: "New", qualified: "Qualified", nurturing: "Nurturing" };

export default function FollowUpRuleModal({ rule, onClose }) {
  const isEditing = Boolean(rule);
  const [name, setName] = useState(rule?.name || "");
  const [idleHours, setIdleHours] = useState(rule?.idle_hours ?? 24);
  const [leadStatusFilter, setLeadStatusFilter] = useState(rule?.lead_status_filter || "");
  const [messageTemplate, setMessageTemplate] = useState(
    rule?.message_template || "Hi {display_name}, just checking in — still interested? Happy to answer any questions!"
  );

  const createRule = useCreateFollowUpRule();
  const updateRule = useUpdateFollowUpRule();
  const isSaving = createRule.isPending || updateRule.isPending;
  const isError = createRule.isError || updateRule.isError;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      name,
      idle_hours: Number(idleHours),
      lead_status_filter: leadStatusFilter || null,
      message_template: messageTemplate,
    };

    if (isEditing) {
      await updateRule.mutateAsync({ id: rule.id, payload });
    } else {
      await createRule.mutateAsync(payload);
    }
    onClose();
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.form
          initial={{ opacity: 0, y: 12, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 12, scale: 0.98 }}
          onClick={(e) => e.stopPropagation()}
          onSubmit={handleSubmit}
          className="glass-panel w-full max-w-md p-6 z-50"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold">{isEditing ? "Edit follow-up rule" : "Add follow-up rule"}</h3>
            <button type="button" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={18} />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">Name</label>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Nudge quiet new leads"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs font-medium text-gray-500">Idle hours before sending</label>
                <input
                  type="number"
                  min={1}
                  max={720}
                  value={idleHours}
                  onChange={(e) => setIdleHours(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500">Only for lead status</label>
                <select
                  value={leadStatusFilter}
                  onChange={(e) => setLeadStatusFilter(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-2 text-sm"
                >
                  {LEAD_STATUS_OPTIONS.map((value) => (
                    <option key={value} value={value}>{LEAD_STATUS_LABELS[value]}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-gray-500">Message ({"{display_name}"} is filled in per contact)</label>
              <textarea
                value={messageTemplate}
                onChange={(e) => setMessageTemplate(e.target.value)}
                rows={3}
                placeholder="Hi {display_name}, just checking in — still interested?"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>

            <p className="text-xs text-gray-400">
              Fires once per quiet period, only while the customer's last message is still unanswered. Never sent to Won/Lost contacts.
            </p>
          </div>

          {isError && <p className="text-xs text-red-500 mt-3">Couldn't save this rule — try again.</p>}

          <Button type="submit" className="w-full mt-5" disabled={isSaving}>
            {isSaving ? "Saving..." : isEditing ? "Save changes" : "Add rule"}
          </Button>
        </motion.form>
      </motion.div>
    </AnimatePresence>
  );
}
