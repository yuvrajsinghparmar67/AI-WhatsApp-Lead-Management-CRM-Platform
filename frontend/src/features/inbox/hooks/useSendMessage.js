import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useSendMessage(conversationId) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (body) => api.post(`/conversations/${conversationId}/messages`, { body }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
}
