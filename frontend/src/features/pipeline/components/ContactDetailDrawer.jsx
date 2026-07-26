import { motion, AnimatePresence } from "framer-motion";
import { X, MessageCircle } from "lucide-react";
import { Link } from "react-router-dom";
import Avatar from "../../../components/ui/Avatar";
import Badge from "../../../components/ui/Badge";

export default function ContactDetailDrawer({ contact, onClose }) {
  if (!contact) return null;
  const name = contact.display_name || contact.phone_number;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40"
        onClick={onClose}
      />
      <motion.div
        initial={{ x: "100%" }}
        animate={{ x: 0 }}
        exit={{ x: "100%" }}
        transition={{ type: "spring", damping: 28, stiffness: 300 }}
        className="fixed right-0 top-0 h-full w-full max-w-sm bg-white dark:bg-surface-dark-card z-50 shadow-soft-dark p-6 overflow-y-auto"
      >
        <button onClick={onClose} className="absolute top-5 right-5 text-gray-400 hover:text-gray-600">
          <X size={18} />
        </button>

        <div className="flex items-center gap-3 mt-2">
          <Avatar name={name} size={48} />
          <div>
            <h3 className="font-display font-bold">{name}</h3>
            <p className="text-sm text-gray-400">{contact.phone_number}</p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mt-4">
          <Badge priority={contact.priority} />
          {contact.sentiment && (
            <Badge priority={contact.sentiment === "negative" ? "urgent" : contact.sentiment === "positive" ? "low" : "medium"}>
              {contact.sentiment}
            </Badge>
          )}
          <span className="text-xs text-gray-400 self-center capitalize">{contact.lead_status}</span>
        </div>

        <dl className="mt-6 space-y-3 text-sm">
          {contact.estimated_budget != null && (
            <div className="flex justify-between">
              <dt className="text-gray-400">Estimated budget</dt>
              <dd className="font-medium">${contact.estimated_budget.toLocaleString()}</dd>
            </div>
          )}
          {contact.confidence_score != null && (
            <div className="flex justify-between">
              <dt className="text-gray-400">AI confidence</dt>
              <dd className="font-medium">{Math.round(contact.confidence_score * 100)}%</dd>
            </div>
          )}
          <div className="flex justify-between">
            <dt className="text-gray-400">Lead since</dt>
            <dd className="font-medium">{new Date(contact.created_at).toLocaleDateString()}</dd>
          </div>
        </dl>

        <Link
          to={`/?contact=${contact.id}`}
          className="mt-6 flex items-center justify-center gap-2 rounded-xl bg-brand-600 text-white py-2.5 text-sm font-medium hover:bg-brand-700 transition-colors duration-150"
        >
          <MessageCircle size={16} /> Open conversation in inbox
        </Link>
      </motion.div>
    </AnimatePresence>
  );
}
