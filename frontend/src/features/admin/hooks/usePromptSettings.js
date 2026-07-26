import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function usePromptSettings() {
  return useQuery({ queryKey: ["prompt-settings"], queryFn: () => api.get("/prompt-settings") });
}

export function useUpdatePromptSetting() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ key, customText }) => api.put(`/prompt-settings/${key}`, { custom_text: customText }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["prompt-settings"] }),
  });
}
