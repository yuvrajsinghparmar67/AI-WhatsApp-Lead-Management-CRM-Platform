import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useCreateFaq, useUpdateFaq } from "../hooks/useFaqs";

export default function FaqModal({ faq, onClose }) {
  const isEditing = Boolean(faq);
  const [question, setQuestion] = useState(faq?.question || "");
  const [answer, setAnswer] = useState(faq?.answer || "");
  const [category, setCategory] = useState(faq?.category || "");
  const createFaq = useCreateFaq();
  const updateFaq = useUpdateFaq();
  const isSaving = createFaq.isPending || updateFaq.isPending;
  const isError = createFaq.isError || updateFaq.isError;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || !answer.trim()) return;

    const payload = { question: question.trim(), answer: answer.trim(), category: category.trim() || null };
    if (isEditing) {
      await updateFaq.mutateAsync({ id: faq.id, payload });
    } else {
      await createFaq.mutateAsync(payload);
    }
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
            <h3 className="font-display font-bold">{isEditing ? "Edit FAQ" : "Add FAQ"}</h3>
            <button type="button" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={18} />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">Question</label>
              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Do you offer a free trial?"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">Answer</label>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                rows={4}
                placeholder="Yes, we offer a 7-day free trial, no card required."
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">Category (optional)</label>
              <input
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="Billing"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
              />
            </div>
          </div>

          {isError && (
            <p className="text-xs text-red-500 mt-3">Couldn't save this FAQ — check your GEMINI_API_KEY and try again.</p>
          )}

          <Button type="submit" className="w-full mt-5" disabled={isSaving}>
            {isSaving ? "Saving..." : isEditing ? "Save changes" : "Add FAQ"}
          </Button>
        </motion.form>
      </motion.div>
    </AnimatePresence>
  );
}
