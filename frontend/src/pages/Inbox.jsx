import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import ConversationList from "../features/inbox/components/ConversationList";
import MessageThread from "../features/inbox/components/MessageThread";
import { useConversations } from "../features/inbox/hooks/useConversations";

export default function Inbox() {
  const { data: conversations, isLoading } = useConversations();
  const [activeId, setActiveId] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();

  // Deep link support: /?contact=<id> (used by the "Open conversation in
  // inbox" link on the pipeline board) selects that contact's conversation
  // once the list has loaded.
  useEffect(() => {
    const contactId = searchParams.get("contact");
    if (contactId && conversations?.length) {
      const match = conversations.find((c) => c.contact.id === contactId);
      if (match) {
        setActiveId(match.id);
        setSearchParams({}, { replace: true });
        return;
      }
    }
    if (!activeId && conversations?.length) {
      setActiveId(conversations[0].id);
    }
  }, [conversations, activeId, searchParams, setSearchParams]);

  return (
    <div className="grid h-full grid-cols-[340px_1fr]">
      <div className="border-r border-gray-100 dark:border-white/5">
        <ConversationList
          conversations={conversations}
          isLoading={isLoading}
          activeId={activeId}
          onSelect={setActiveId}
        />
      </div>
      <MessageThread conversationId={activeId} />
    </div>
  );
}
