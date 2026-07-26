import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useCreateBusinessRule, useUpdateBusinessRule } from "../hooks/useBusinessRules";

const TRIGGER_FIELD_OPTIONS = {
  intent: ["sales_inquiry", "support_request", "complaint", "general_question", "spam"],
  sentiment: ["positive", "neutral", "negative"],
  priority: ["low", "medium", "high", "urgent"],
};
const ACTION_FIELD_OPTIONS = {
  lead_status: ["new", "qualified", "nurturing", "won", "lost"],
  priority: ["low", "medium", "high", "urgent"],
};

export default function BusinessRuleModal({ rule, defaultType = "guardrail", onClose }) {
  const isEditing = Boolean(rule);
  const [ruleType] = useState(rule?.rule_type || defaultType);
  const [name, setName] = useState(rule?.name || "");
  const [guardrailText, setGuardrailText] = useState(rule?.guardrail_text || "");
  const [triggerField, setTriggerField] = useState(rule?.trigger_field || "sentiment");
  const [triggerValue, setTriggerValue] = useState(rule?.trigger_value || TRIGGER_FIELD_OPTIONS.sentiment[0]);
  const [actionField, setActionField] = useState(rule?.action_field || "priority");
  const [actionValue, setActionValue] = useState(rule?.action_value || ACTION_FIELD_OPTIONS.priority[0]);

  const createRule = useCreateBusinessRule();
  const updateRule = useUpdateBusinessRule();
  const isSaving = createRule.isPending || updateRule.isPending;
  const isError = createRule.isError || updateRule.isError;

  const handleTriggerFieldChange = (field) => {
    setTriggerField(field);
    setTriggerValue(TRIGGER_FIELD_OPTIONS[field][0]);
  };

  const handleActionFieldChange = (field) => {
    setActionField(field);
    setActionValue(ACTION_FIELD_OPTIONS[field][0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload =
      ruleType === "guardrail"
        ? { name, rule_type: "guardrail", guardrail_text: guardrailText }
        : {
            name,
            rule_type: "automation",
            trigger_field: triggerField,
            trigger_value: triggerValue,
            action_field: actionField,
            action_value: actionValue,
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
            <h3 className="font-display font-bold">
              {isEditing ? "Edit rule" : ruleType === "guardrail" ? "Add guardrail" : "Add automation rule"}
            </h3>
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
                placeholder={ruleType === "guardrail" ? "No refund promises" : "Escalate negative sentiment"}
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>

            {ruleType === "guardrail" ? (
              <div>
                <label className="text-xs font-medium text-gray-500">Rule text (what the AI must never/always do)</label>
                <textarea
                  value={guardrailText}
                  onChange={(e) => setGuardrailText(e.target.value)}
                  rows={3}
                  placeholder="Never promise refunds or compensation — always say a human will follow up."
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                  required
                />
              </div>
            ) : (
              <div className="rounded-xl bg-gray-50 dark:bg-white/5 p-3 space-y-3">
                <p className="text-xs font-medium text-gray-500">If...</p>
                <div className="grid grid-cols-2 gap-2">
                  <select
                    value={triggerField}
                    onChange={(e) => handleTriggerFieldChange(e.target.value)}
                    className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-sm"
                  >
                    {Object.keys(TRIGGER_FIELD_OPTIONS).map((field) => (
                      <option key={field} value={field}>{field}</option>
                    ))}
                  </select>
                  <select
                    value={triggerValue}
                    onChange={(e) => setTriggerValue(e.target.value)}
                    className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-sm"
                  >
                    {TRIGGER_FIELD_OPTIONS[triggerField].map((v) => (
                      <option key={v} value={v}>is {v}</option>
                    ))}
                  </select>
                </div>

                <p className="text-xs font-medium text-gray-500">Then set...</p>
                <div className="grid grid-cols-2 gap-2">
                  <select
                    value={actionField}
                    onChange={(e) => handleActionFieldChange(e.target.value)}
                    className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-sm"
                  >
                    {Object.keys(ACTION_FIELD_OPTIONS).map((field) => (
                      <option key={field} value={field}>{field}</option>
                    ))}
                  </select>
                  <select
                    value={actionValue}
                    onChange={(e) => setActionValue(e.target.value)}
                    className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-sm"
                  >
                    {ACTION_FIELD_OPTIONS[actionField].map((v) => (
                      <option key={v} value={v}>to {v}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}
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
