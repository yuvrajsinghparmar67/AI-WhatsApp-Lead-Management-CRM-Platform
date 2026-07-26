import { useMutation } from "@tanstack/react-query";
import { api } from "../../../lib/api";

/** Powers the composer's "Suggest reply" button - calls the AI on demand rather than on every message. */
export function useSuggestReply(conversationId) {
  return useMutation({
    mutationFn: () => api.post(`/conversations/${conversationId}/suggest-reply`, {}),
  });
}
