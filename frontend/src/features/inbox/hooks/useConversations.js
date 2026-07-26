import { useQuery } from "@tanstack/react-query";
import { api } from "../../../lib/api";

/** Polls the inbox list so new simulated inbound messages show up without a manual refresh. */
export function useConversations() {
  return useQuery({
    queryKey: ["conversations"],
    queryFn: () => api.get("/conversations"),
    refetchInterval: 4000,
  });
}
