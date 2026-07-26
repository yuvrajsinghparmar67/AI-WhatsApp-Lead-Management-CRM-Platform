import { useQuery } from "@tanstack/react-query";
import { api } from "../../../lib/api";

export function useAnalyticsOverview() {
  return useQuery({
    queryKey: ["analytics-overview"],
    queryFn: () => api.get("/analytics/overview"),
    refetchInterval: 10000,
  });
}
