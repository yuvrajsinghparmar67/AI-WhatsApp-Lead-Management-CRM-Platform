import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useBusinessRules() {
  return useQuery({ queryKey: ["business-rules"], queryFn: () => api.get("/business-rules") });
}

export function useCreateBusinessRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => api.post("/business-rules", payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["business-rules"] }),
  });
}

export function useUpdateBusinessRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }) => api.patch(`/business-rules/${id}`, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["business-rules"] }),
  });
}

export function useDeleteBusinessRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.del(`/business-rules/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["business-rules"] }),
  });
}
