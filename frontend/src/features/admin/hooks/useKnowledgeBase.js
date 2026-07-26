import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useKnowledgeBase() {
  return useQuery({ queryKey: ["knowledge-base"], queryFn: () => api.get("/knowledge-base") });
}

export function useCreateManualEntry() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ title, content }) => api.post("/knowledge-base/manual", { title, content }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["knowledge-base"] }),
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (file) => {
      const formData = new FormData();
      formData.append("file", file);
      return api.upload("/knowledge-base/upload", formData);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["knowledge-base"] }),
  });
}

export function useDeleteDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (documentId) => api.del(`/knowledge-base/${documentId}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["knowledge-base"] }),
  });
}
