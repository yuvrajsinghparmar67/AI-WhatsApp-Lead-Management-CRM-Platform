import { useEffect, useState } from "react";
import { Check } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useAISettings, useUpdateAISettings } from "../hooks/useAISettings";

export default function AISettingsPanel() {
  const { data: settings, isLoading } = useAISettings();
  const updateSettings = useUpdateAISettings();
  const [form, setForm] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (settings) setForm(settings);
  }, [settings]);

  if (isLoading || !form) {
    return <div className="text-sm text-gray-400">Loading AI settings...</div>;
  }

  const handleSave = async (e) => {
    e.preventDefault();
    await updateSettings.mutateAsync({
      chat_model: form.chat_model,
      temperature: Number(form.temperature),
      auto_analysis_enabled: form.auto_analysis_enabled,
      rag_enabled: form.rag_enabled,
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <form onSubmit={handleSave} className="max-w-xl space-y-6">
      <div>
        <h2 className="font-display font-bold text-lg">AI Settings</h2>
        <p className="text-sm text-gray-400 mt-0.5">
          Controls how the AI pipeline behaves — no redeploy needed, changes apply to the next AI call.
        </p>
      </div>

      <div>
        <label className="text-xs font-medium text-gray-500">Chat model</label>
        <input
          value={form.chat_model}
          onChange={(e) => setForm({ ...form, chat_model: e.target.value })}
          className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
        />
        <p className="text-xs text-gray-400 mt-1">Must be a valid Gemini model name (e.g. gemini-3.5-flash).</p>
      </div>

      <div>
        <div className="flex items-center justify-between">
          <label className="text-xs font-medium text-gray-500">Temperature</label>
          <span className="text-xs text-gray-400">{Number(form.temperature).toFixed(1)}</span>
        </div>
        <input
          type="range"
          min="0"
          max="2"
          step="0.1"
          value={form.temperature}
          onChange={(e) => setForm({ ...form, temperature: e.target.value })}
          className="mt-2 w-full accent-brand-500"
        />
        <div className="flex justify-between text-[10px] text-gray-400 mt-1">
          <span>Precise & consistent</span>
          <span>Creative & varied</span>
        </div>
      </div>

      <div className="space-y-3">
        <label className="flex items-center justify-between rounded-xl bg-gray-50 dark:bg-white/5 p-3.5 cursor-pointer">
          <div>
            <p className="text-sm font-medium">Auto-analysis</p>
            <p className="text-xs text-gray-400">Automatically score intent/priority/sentiment on every inbound message.</p>
          </div>
          <input
            type="checkbox"
            checked={form.auto_analysis_enabled}
            onChange={(e) => setForm({ ...form, auto_analysis_enabled: e.target.checked })}
            className="rounded border-gray-300"
          />
        </label>

        <label className="flex items-center justify-between rounded-xl bg-gray-50 dark:bg-white/5 p-3.5 cursor-pointer">
          <div>
            <p className="text-sm font-medium">Retrieval-augmented replies (RAG)</p>
            <p className="text-xs text-gray-400">Let suggested replies search the catalog, FAQs, knowledge base, and past conversations.</p>
          </div>
          <input
            type="checkbox"
            checked={form.rag_enabled}
            onChange={(e) => setForm({ ...form, rag_enabled: e.target.checked })}
            className="rounded border-gray-300"
          />
        </label>
      </div>

      <div className="flex items-center gap-3">
        <Button type="submit" disabled={updateSettings.isPending}>
          {updateSettings.isPending ? "Saving..." : "Save changes"}
        </Button>
        {saved && (
          <span className="flex items-center gap-1 text-sm text-emerald-500">
            <Check size={14} /> Saved
          </span>
        )}
      </div>
    </form>
  );
}
