import { useEffect, useRef } from "react";
import Avatar from "../../../components/ui/Avatar";
import Badge from "../../../components/ui/Badge";
import AIInsightsPanel from "./AIInsightsPanel";
import MessageBubble from "./MessageBubble";
import MessageComposer from "./MessageComposer";
import { useConversationDetail } from "../hooks/useConversationDetail";
import { useSendMessage } from "../hooks/useSendMessage";

export default function MessageThread({ conversationId }) {
  const { data: conversation, isLoading } = useConversationDetail(conversationId);
  const sendMessage = useSendMessage(conversationId);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversation?.messages?.length]);

  if (!conversationId) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-gray-400">
        Select a conversation to start replying.
      </div>
    );
  }

  if (isLoading || !conversation) {
    return <div className="flex h-full items-center justify-center text-sm text-gray-400">Loading conversation...</div>;
  }

  const name = conversation.contact.display_name || conversation.contact.phone_number;

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-3 border-b border-gray-100 dark:border-white/5 px-5 py-4">
        <Avatar name={name} size={36} />
        <div>
          <p className="font-medium text-sm">{name}</p>
          <p className="text-xs text-gray-400">{conversation.contact.phone_number}</p>
        </div>
        <Badge priority={conversation.contact.priority} className="ml-auto" />
      </div>

      <div className="flex-1 overflow-y-auto">
        <AIInsightsPanel conversation={conversation} />
        <div className="px-5 pb-4 space-y-3 bg-gray-50/50 dark:bg-black/10">
          {conversation.messages.length === 0 && (
            <p className="text-center text-sm text-gray-400 mt-8">No messages in this conversation yet.</p>
          )}
          {conversation.messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          <div ref={bottomRef} />
        </div>
      </div>

      <MessageComposer
        conversationId={conversationId}
        onSend={(body) => sendMessage.mutate(body)}
        isSending={sendMessage.isPending}
      />
    </div>
  );
}
