import { useState } from "react";
import { Send, Sparkles, Loader2 } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useSuggestReply } from "../hooks/useSuggestReply";

export default function MessageComposer({ conversationId, onSend, isSending }) {
  const [value, setValue] = useState("");
  const [usedContextCount, setUsedContextCount] = useState(0);
  const suggestReply = useSuggestReply(conversationId);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim()) return;
    onSend(value.trim());
    setValue("");
    setUsedContextCount(0);
  };

  const handleSuggest = async () => {
    try {
      const result = await suggestReply.mutateAsync();
      setValue(result.suggested_reply);
      setUsedContextCount(result.used_similar_conversations || 0);
    } catch {
      // Surfaced via suggestReply.isError below - the composer stays usable either way.
    }
  };

  return (
    <div className="border-t border-gray-100 dark:border-white/5">
      {suggestReply.isError && (
        <p className="px-4 pt-2 text-xs text-red-500">
          Couldn't generate a suggestion — check your GEMINI_API_KEY and try again.
        </p>
      )}
      {!suggestReply.isError && usedContextCount > 0 && (
        <p className="px-4 pt-2 text-xs text-brand-500">
          This draft was informed by {usedContextCount} similar past conversation{usedContextCount > 1 ? "s" : ""}.
        </p>
      )}
      <form onSubmit={handleSubmit} className="flex items-center gap-2 p-4">
        <button
          type="button"
          onClick={handleSuggest}
          disabled={suggestReply.isPending}
          title="Suggest a reply with AI"
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-brand-500 hover:bg-brand-50 dark:hover:bg-brand-500/10 disabled:opacity-50 transition-colors duration-150"
        >
          {suggestReply.isPending ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
        </button>
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Type a reply, or tap the sparkle for an AI draft..."
          className="flex-1 rounded-full border border-gray-200 dark:border-white/10 bg-gray-50 dark:bg-white/5 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
        />
        <Button type="submit" disabled={isSending || !value.trim()} className="!rounded-full !px-3.5">
          <Send size={16} />
        </Button>
      </form>
    </div>
  );
}
