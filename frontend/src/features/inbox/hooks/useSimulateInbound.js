import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

/** Powers the "Simulate incoming message" panel - stands in for a real WhatsApp webhook. */
export function useSimulateInbound() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload) => api.post("/simulate/inbound", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
}
