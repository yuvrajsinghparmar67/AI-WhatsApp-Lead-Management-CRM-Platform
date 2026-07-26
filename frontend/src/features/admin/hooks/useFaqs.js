import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useFaqs() {
  return useQuery({ queryKey: ["faqs"], queryFn: () => api.get("/faqs") });
}

export function useCreateFaq() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => api.post("/faqs", payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["faqs"] }),
  });
}

export function useUpdateFaq() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }) => api.patch(`/faqs/${id}`, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["faqs"] }),
  });
}

export function useDeleteFaq() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.del(`/faqs/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["faqs"] }),
  });
}
