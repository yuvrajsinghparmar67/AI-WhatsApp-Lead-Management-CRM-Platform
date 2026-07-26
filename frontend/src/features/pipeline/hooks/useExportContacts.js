import { useMutation } from "@tanstack/react-query";
import { api } from "../../../lib/api";
import { downloadBlob } from "../../../lib/utils";

/**
 * Downloads the Customer Database as a CSV file, honoring whatever
 * search/filter is currently applied on screen (Milestone 16).
 */
export function useExportContacts() {
  return useMutation({
    mutationFn: async ({ search = "", priority = "", sentiment = "" } = {}) => {
      const params = new URLSearchParams();
      if (search) params.set("search", search);
      if (priority) params.set("priority", priority);
      if (sentiment) params.set("sentiment", sentiment);
      const qs = params.toString();

      const { blob, filename } = await api.getBlob(`/contacts/export${qs ? `?${qs}` : ""}`);
      downloadBlob(blob, filename);
    },
  });
}
