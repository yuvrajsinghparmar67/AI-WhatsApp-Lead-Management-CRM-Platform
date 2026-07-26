import { useQuery } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useConversationDetail(conversationId) {
  return useQuery({
    queryKey: ["conversation", conversationId],
    queryFn: () => api.get(`/conversations/${conversationId}`),
    enabled: Boolean(conversationId),
    refetchInterval: 4000,
  });
}
