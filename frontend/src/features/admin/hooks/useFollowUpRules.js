import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useFollowUpRules() {
  return useQuery({ queryKey: ["follow-up-rules"], queryFn: () => api.get("/follow-up-rules") });
}

export function useFollowUpLogs() {
  return useQuery({ queryKey: ["follow-up-rules", "logs"], queryFn: () => api.get("/follow-up-rules/logs") });
}

export function useCreateFollowUpRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => api.post("/follow-up-rules", payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["follow-up-rules"] }),
  });
}

export function useUpdateFollowUpRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }) => api.patch(`/follow-up-rules/${id}`, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["follow-up-rules"] }),
  });
}

export function useDeleteFollowUpRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.del(`/follow-up-rules/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["follow-up-rules"] }),
  });
}

export function useRunFollowUpRulesNow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => api.post("/follow-up-rules/run-now"),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["follow-up-rules"] }),
  });
}
