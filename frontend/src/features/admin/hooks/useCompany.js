import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useCompany() {
  return useQuery({ queryKey: ["company"], queryFn: () => api.get("/company") });
}

export function useUpdateCompany() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (updates) => api.put("/company", updates),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["company"] }),
  });
}
