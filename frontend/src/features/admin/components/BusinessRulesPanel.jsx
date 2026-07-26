import { useState } from "react";
import { Plus, Trash2, Pencil, ShieldCheck, Workflow } from "lucide-react";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import BusinessRuleModal from "./BusinessRuleModal";
import { useBusinessRules, useDeleteBusinessRule, useUpdateBusinessRule } from "../hooks/useBusinessRules";

export default function BusinessRulesPanel() {
  const { data: rules, isLoading } = useBusinessRules();
  const deleteRule = useDeleteBusinessRule();
  const updateRule = useUpdateBusinessRule();
  const [modalRule, setModalRule] = useState(null);
  const [modalType, setModalType] = useState("guardrail");
  const [showModal, setShowModal] = useState(false);

  const guardrails = rules?.filter((r) => r.rule_type === "guardrail") || [];
  const automations = rules?.filter((r) => r.rule_type === "automation") || [];

  const openCreate = (type) => {
    setModalRule(null);
    setModalType(type);
    setShowModal(true);
  };

  const openEdit = (rule) => {
    setModalRule(rule);
    setModalType(rule.rule_type);
    setShowModal(true);
  };

  const toggleActive = (rule) => {
    updateRule.mutate({ id: rule.id, payload: { is_active: !rule.is_active } });
  };

  return (
    <div className="max-w-2xl space-y-8">
      <div>
        <h2 className="font-display font-bold text-lg">Business Rules</h2>
        <p className="text-sm text-gray-400 mt-0.5">
          The stage between knowledge retrieval and Gemini: mandatory constraints on every AI reply, and
          deterministic overrides on top of the AI's own analysis.
        </p>
      </div>

      {/* Guardrails */}
      <div>
        <div className="flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-sm font-semibold">
            <ShieldCheck size={15} className="text-brand-500" /> Guardrails
          </h3>
          <Button variant="secondary" onClick={() => openCreate("guardrail")} className="!px-3 !py-1.5 text-xs">
            <Plus size={14} /> Add guardrail
          </Button>
        </div>
        <p className="text-xs text-gray-400 mt-1">Injected into every suggested reply as a mandatory instruction.</p>

        <div className="mt-3 space-y-2">
          {!isLoading && guardrails.length === 0 && (
            <div className="glass-panel p-4 text-sm text-gray-400 text-center">No guardrails yet.</div>
          )}
          {guardrails.map((rule) => (
            <div key={rule.id} className="glass-panel p-3.5 flex items-start gap-3">
              <button onClick={() => toggleActive(rule)} title={rule.is_active ? "Active — click to disable" : "Disabled — click to enable"}>
                <Badge priority={rule.is_active ? "low" : "low"} className={rule.is_active ? "" : "opacity-40"}>
                  {rule.is_active ? "Active" : "Off"}
                </Badge>
              </button>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium">{rule.name}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{rule.guardrail_text}</p>
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

      {/* Automation rules */}
      <div>
        <div className="flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-sm font-semibold">
            <Workflow size={15} className="text-brand-500" /> Automation rules
          </h3>
          <Button variant="secondary" onClick={() => openCreate("automation")} className="!px-3 !py-1.5 text-xs">
            <Plus size={14} /> Add automation
          </Button>
        </div>
        <p className="text-xs text-gray-400 mt-1">Applied deterministically after AI analysis — an admin's rule always wins over the AI's own guess for that field.</p>

        <div className="mt-3 space-y-2">
          {!isLoading && automations.length === 0 && (
            <div className="glass-panel p-4 text-sm text-gray-400 text-center">No automation rules yet.</div>
          )}
          {automations.map((rule) => (
            <div key={rule.id} className="glass-panel p-3.5 flex items-start gap-3">
              <button onClick={() => toggleActive(rule)}>
                <Badge priority="low" className={rule.is_active ? "" : "opacity-40"}>
                  {rule.is_active ? "Active" : "Off"}
                </Badge>
              </button>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium">{rule.name}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                  If <span className="font-medium">{rule.trigger_field}</span> is <span className="font-medium">{rule.trigger_value}</span> →
                  set <span className="font-medium">{rule.action_field}</span> to <span className="font-medium">{rule.action_value}</span>
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

      {showModal && <BusinessRuleModal rule={modalRule} defaultType={modalType} onClose={() => setShowModal(false)} />}
    </div>
  );
}
