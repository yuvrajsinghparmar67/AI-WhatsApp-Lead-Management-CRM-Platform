import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useUsers() {
  return useQuery({ queryKey: ["users"], queryFn: () => api.get("/users") });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }) => api.patch(`/users/${id}`, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}
