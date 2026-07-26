import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useAISettings() {
  return useQuery({ queryKey: ["ai-settings"], queryFn: () => api.get("/ai-settings") });
}

export function useUpdateAISettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (updates) => api.put("/ai-settings", updates),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["ai-settings"] }),
  });
}
