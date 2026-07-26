import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, UploadCloud } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useUploadDocument } from "../hooks/useKnowledgeBase";

const ACCEPTED = ".pdf,.docx,.txt";

export default function UploadDocumentModal({ onClose }) {
  const [file, setFile] = useState(null);
  const upload = useUploadDocument();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    await upload.mutateAsync(file);
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
            <h3 className="font-display font-bold">Upload a document</h3>
            <button type="button" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={18} />
            </button>
          </div>

          <label className="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-gray-200 dark:border-white/10 py-8 cursor-pointer hover:border-brand-400 transition-colors duration-150">
            <UploadCloud size={24} className="text-gray-400" />
            <span className="text-sm text-gray-500">{file ? file.name : "Click to choose a PDF, DOCX, or TXT file"}</span>
            <span className="text-xs text-gray-400">Max 10 MB</span>
            <input type="file" accept={ACCEPTED} onChange={(e) => setFile(e.target.files?.[0] || null)} className="hidden" />
          </label>

          {upload.isError && (
            <p className="text-xs text-red-500 mt-3">{upload.error?.message || "Upload failed — try again."}</p>
          )}

          <Button type="submit" className="w-full mt-5" disabled={!file || upload.isPending}>
            {upload.isPending ? "Uploading & indexing..." : "Upload"}
          </Button>
        </motion.form>
      </motion.div>
    </AnimatePresence>
  );
}
