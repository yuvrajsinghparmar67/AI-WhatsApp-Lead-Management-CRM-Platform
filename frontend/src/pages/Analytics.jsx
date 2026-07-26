import { Users, MessageSquare, Clock } from "lucide-react";
import StatCard from "../features/analytics/components/StatCard";
import BarBreakdown from "../features/analytics/components/BarBreakdown";
import MessageTrendChart from "../features/analytics/components/MessageTrendChart";
import { useAnalyticsOverview } from "../features/analytics/hooks/useAnalyticsOverview";
import { formatDuration } from "../lib/utils";

export default function Analytics() {
  const { data, isLoading } = useAnalyticsOverview();

  if (isLoading || !data) {
    return <div className="flex h-full items-center justify-center text-sm text-gray-400">Loading analytics...</div>;
  }

  return (
    <div className="h-full overflow-y-auto p-6 space-y-6">
      <div>
        <h1 className="font-display font-bold text-lg">Analytics</h1>
        <p className="text-sm text-gray-400 mt-0.5">
          A live view of lead flow, sentiment, and response speed across the inbox.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard label="Total contacts" value={data.total_contacts} icon={Users} />
        <StatCard label="Total conversations" value={data.total_conversations} icon={MessageSquare} accent="text-blue-500" />
        <StatCard
          label="Avg. response time"
          value={formatDuration(data.avg_response_time_seconds)}
          icon={Clock}
          accent="text-amber-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <BarBreakdown title="Lead funnel" data={data.lead_funnel} />
        <BarBreakdown title="Priority breakdown" data={data.priority_breakdown} />
        <BarBreakdown title="Sentiment breakdown" data={data.sentiment_breakdown} />
      </div>

      <MessageTrendChart data={data.messages_per_day} />
    </div>
  );
}
