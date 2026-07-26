import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useSimulateInbound } from "../hooks/useSimulateInbound";

/**
 * Stands in for a real WhatsApp webhook: lets you "play customer" and send
 * an inbound message so the inbox has something to show without needing
 * real WhatsApp Business API credentials yet.
 */
export default function SimulateInboundPanel({ onClose }) {
  const [phone, setPhone] = useState("");
  const [name, setName] = useState("");
  const [body, setBody] = useState("");
  const simulate = useSimulateInbound();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!phone.trim() || !body.trim()) return;

    await simulate.mutateAsync({
      phone_number: phone.trim(),
      display_name: name.trim() || null,
      body: body.trim(),
    });
    setBody("");
    onClose();
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.form
          initial={{ opacity: 0, y: 12, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 12, scale: 0.98 }}
          onClick={(e) => e.stopPropagation()}
          onSubmit={handleSubmit}
          className="glass-panel w-full max-w-sm p-6 z-50"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold">Simulate incoming message</h3>
            <button type="button" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={18} />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">Phone number</label>
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+1 555 000 1234"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">Name (optional)</label>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Jordan Lee"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">Message</label>
              <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                rows={3}
                placeholder="Hi, I'm interested in your pricing plans..."
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>
          </div>

          <Button type="submit" className="w-full mt-5" disabled={simulate.isPending}>
            {simulate.isPending ? "Sending..." : "Send as customer"}
          </Button>
        </motion.form>
      </motion.div>
    </AnimatePresence>
  );
}
