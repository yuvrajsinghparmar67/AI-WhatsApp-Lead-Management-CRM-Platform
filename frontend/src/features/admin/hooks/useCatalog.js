import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useCatalog() {
  return useQuery({ queryKey: ["catalog"], queryFn: () => api.get("/catalog") });
}

export function useCreateCatalogItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => api.post("/catalog", payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["catalog"] }),
  });
}

export function useUpdateCatalogItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }) => api.patch(`/catalog/${id}`, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["catalog"] }),
  });
}

export function useDeleteCatalogItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.del(`/catalog/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["catalog"] }),
  });
}
