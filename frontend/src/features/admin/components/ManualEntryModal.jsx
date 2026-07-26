import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useCreateManualEntry } from "../hooks/useKnowledgeBase";

export default function ManualEntryModal({ onClose }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const createEntry = useCreateManualEntry();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;
    await createEntry.mutateAsync({ title: title.trim(), content: content.trim() });
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
          className="glass-panel w-full max-w-md p-6 z-50"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold">Add knowledge base entry</h3>
            <button type="button" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={18} />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">Title</label>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Premium Gym Membership"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">Content</label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                rows={5}
                placeholder={"₹2500/month\nUnlimited access\nPersonal trainer included"}
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>
          </div>

          {createEntry.isError && (
            <p className="text-xs text-red-500 mt-3">Couldn't save this entry — check your GEMINI_API_KEY and try again.</p>
          )}

          <Button type="submit" className="w-full mt-5" disabled={createEntry.isPending}>
            {createEntry.isPending ? "Saving..." : "Save entry"}
          </Button>
        </motion.form>
      </motion.div>
    </AnimatePresence>
  );
}
