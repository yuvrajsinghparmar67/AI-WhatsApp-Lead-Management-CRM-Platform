import { useEffect, useState } from "react";
import { AlertTriangle, RotateCcw, Check } from "lucide-react";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import { usePromptSettings, useUpdatePromptSetting } from "../hooks/usePromptSettings";

function PromptEditor({ prompt }) {
  const [text, setText] = useState(prompt.effective_text);
  const [saved, setSaved] = useState(false);
  const updatePrompt = useUpdatePromptSetting();

  useEffect(() => {
    setText(prompt.effective_text);
  }, [prompt.effective_text]);

  const handleSave = async () => {
    await updatePrompt.mutateAsync({ key: prompt.key, customText: text });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleReset = async () => {
    await updatePrompt.mutateAsync({ key: prompt.key, customText: null });
  };

  return (
    <div className="glass-panel p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <p className="text-sm font-semibold">{prompt.label}</p>
          <Badge priority={prompt.is_custom ? "medium" : "low"}>{prompt.is_custom ? "Custom" : "Default"}</Badge>
        </div>
        {prompt.is_custom && (
          <button
            onClick={handleReset}
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-brand-500 transition-colors duration-150"
          >
            <RotateCcw size={12} /> Reset to default
          </button>
        )}
      </div>

      {/* This panel is data-driven from the backend's PROMPT_REGISTRY warnings,
          not hardcoded per-prompt logic - see prompt_settings_service.py. */}

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={10}
        className="w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-brand-400"
      />

      <div className="flex items-center gap-3 mt-3">
        <Button onClick={handleSave} disabled={updatePrompt.isPending} className="!px-3 !py-1.5 text-xs">
          {updatePrompt.isPending ? "Saving..." : "Save"}
        </Button>
        {saved && (
          <span className="flex items-center gap-1 text-xs text-emerald-500">
            <Check size={12} /> Saved
          </span>
        )}
      </div>
    </div>
  );
}

export default function PromptSettingsPanel() {
  const { data: prompts, isLoading } = usePromptSettings();

  return (
    <div className="max-w-2xl">
      <div>
        <h2 className="font-display font-bold text-lg">Prompt Settings</h2>
        <p className="text-sm text-gray-400 mt-0.5">
          The actual system prompts the AI pipeline runs — edit with care, changes apply immediately.
        </p>
      </div>

      <div className="mt-3 flex items-start gap-2 rounded-xl bg-amber-50 dark:bg-amber-500/10 p-3 text-xs text-amber-700 dark:text-amber-400">
        <AlertTriangle size={14} className="shrink-0 mt-0.5" />
        <p>
          The <strong>Conversation Analysis</strong> prompt drives automatic lead scoring and must keep instructing
          the model to respond with only the documented JSON shape — removing that instruction won't crash anything
          (the pipeline fails soft), it will just silently stop updating lead status, priority, and sentiment.
        </p>
      </div>

      <div className="mt-4 space-y-4">
        {isLoading && <p className="text-sm text-gray-400">Loading...</p>}
        {prompts?.map((prompt) => (
          <PromptEditor key={prompt.key} prompt={prompt} />
        ))}
      </div>
    </div>
  );
}
