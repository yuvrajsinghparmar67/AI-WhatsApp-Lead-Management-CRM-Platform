import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../../lib/api";

/** Powers drag-and-drop on the pipeline board and manual priority edits. */
export function useUpdateContact() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ contactId, updates }) => api.patch(`/contacts/${contactId}`, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contacts"] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
}
