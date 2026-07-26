import { useState } from "react";
import { Plus } from "lucide-react";
import ConversationListItem from "./ConversationListItem";
import SimulateInboundPanel from "./SimulateInboundPanel";
import Button from "../../../components/ui/Button";

export default function ConversationList({ conversations, isLoading, activeId, onSelect }) {
  const [showSimulator, setShowSimulator] = useState(false);

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between px-4 py-4 border-b border-gray-100 dark:border-white/5">
        <h2 className="font-display font-bold text-lg">Inbox</h2>
        <Button variant="secondary" onClick={() => setShowSimulator(true)} className="!px-3 !py-1.5 text-xs">
          <Plus size={14} /> Simulate message
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {isLoading && (
          <div className="p-4 space-y-3">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-16 rounded-xl bg-gray-100 dark:bg-white/5 animate-pulse" />
            ))}
          </div>
        )}

        {!isLoading && conversations?.length === 0 && (
          <div className="p-8 text-center text-sm text-gray-400">
            No conversations yet. Try simulating an incoming message to see the
            inbox come alive.
          </div>
        )}

        {conversations?.map((item) => (
          <ConversationListItem
            key={item.id}
            item={item}
            isActive={item.id === activeId}
            onClick={() => onSelect(item.id)}
          />
        ))}
      </div>

      {showSimulator && <SimulateInboundPanel onClose={() => setShowSimulator(false)} />}
    </div>
  );
}
