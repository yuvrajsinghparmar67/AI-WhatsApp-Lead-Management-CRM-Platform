import { useQuery } from "@tanstack/react-query";
import { api } from "../../../lib/api";

/**
 * On-demand semantic search: fetches similar past conversations only when
 * explicitly requested (enabled: false + refetch()), so browsing the inbox
 * doesn't trigger an embedding call on every conversation you open.
 */
export function useSimilarConversations(conversationId) {
  return useQuery({
    queryKey: ["similar-conversations", conversationId],
    queryFn: () => api.get(`/conversations/${conversationId}/similar`),
    enabled: false,
  });
}
