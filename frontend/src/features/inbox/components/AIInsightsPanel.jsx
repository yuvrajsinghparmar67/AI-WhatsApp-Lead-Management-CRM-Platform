import { Sparkles, DollarSign, Gauge, Search, Loader2 } from "lucide-react";
import Badge from "../../../components/ui/Badge";
import { useSimilarConversations } from "../hooks/useSimilarConversations";

/**
 * Surfaces what the AI pipeline inferred about this conversation - intent,
 * priority/sentiment, estimated budget, its own confidence, and a running
 * summary - plus an on-demand semantic search over past conversations
 * (Gemini Embedding 2) so an agent can see how similar customers were
 * handled before.
 */
export default function AIInsightsPanel({ conversation }) {
  const { contact, intent, ai_summary } = conversation;
  const hasInsights = intent || ai_summary || contact.sentiment;
  const similar = useSimilarConversations(conversation.id);

  return (
    <div className="m-4 space-y-3">
      {!hasInsights && (
        <div className="glass-panel p-4 text-sm text-gray-400 flex items-center gap-2">
          <Sparkles size={14} className="text-brand-400" />
          AI insights will appear here once the conversation has a customer message.
        </div>
      )}

      {hasInsights && (
        <div className="glass-panel p-4 space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-600 dark:text-brand-400 uppercase tracking-wide">
            <Sparkles size={13} />
            AI Insights
          </div>

          {ai_summary && <p className="text-sm text-gray-700 dark:text-gray-300">{ai_summary}</p>}

          <div className="flex flex-wrap items-center gap-2">
            {intent && (
              <Badge priority="medium" className="!bg-gray-100 !text-gray-700 dark:!bg-white/10 dark:!text-gray-300">
                {intent.replace("_", " ")}
              </Badge>
            )}
            {contact.sentiment && (
              <Badge
                priority={contact.sentiment === "negative" ? "urgent" : contact.sentiment === "positive" ? "low" : "medium"}
              >
                {contact.sentiment}
              </Badge>
            )}
            {contact.estimated_budget != null && (
              <span className="inline-flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                <DollarSign size={12} /> ~${contact.estimated_budget.toLocaleString()}
              </span>
            )}
            {contact.confidence_score != null && (
              <span className="inline-flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                <Gauge size={12} /> {Math.round(contact.confidence_score * 100)}% confidence
              </span>
            )}
          </div>
        </div>
      )}

      <div className="glass-panel p-4">
        <button
          onClick={() => similar.refetch()}
          disabled={similar.isFetching}
          className="flex items-center gap-2 text-xs font-semibold text-brand-600 dark:text-brand-400 uppercase tracking-wide disabled:opacity-60"
        >
          {similar.isFetching ? <Loader2 size={13} className="animate-spin" /> : <Search size={13} />}
          Find similar conversations
        </button>

        {similar.isFetched && similar.data?.length === 0 && (
          <p className="text-sm text-gray-400 mt-2">No sufficiently similar past conversations found.</p>
        )}

        {similar.data?.length > 0 && (
          <ul className="mt-3 space-y-2">
            {similar.data.map((item) => (
              <li key={item.conversation_id} className="rounded-lg bg-gray-50 dark:bg-white/5 p-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium">{item.contact_name}</span>
                  <span className="text-xs text-gray-400">{Math.round(item.similarity * 100)}% similar</span>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">"{item.snippet}"</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
