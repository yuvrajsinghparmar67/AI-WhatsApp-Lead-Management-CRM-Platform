import { useQuery } from "@tanstack/react-query";
import { api } from "../../../lib/api";

function buildQueryString({ search, priority, sentiment }) {
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (priority) params.set("priority", priority);
  if (sentiment) params.set("sentiment", sentiment);
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export function useContacts({ search = "", priority = "", sentiment = "" } = {}) {
  return useQuery({
    queryKey: ["contacts", { search, priority, sentiment }],
    queryFn: () => api.get(`/contacts${buildQueryString({ search, priority, sentiment })}`),
    refetchInterval: 5000,
  });
}
