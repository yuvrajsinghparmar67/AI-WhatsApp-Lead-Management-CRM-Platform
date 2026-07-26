import { useState } from "react";
import { FileText, File, Type, Trash2, Plus, UploadCloud } from "lucide-react";
import Button from "../../../components/ui/Button";
import ManualEntryModal from "./ManualEntryModal";
import UploadDocumentModal from "./UploadDocumentModal";
import { useDeleteDocument, useKnowledgeBase } from "../hooks/useKnowledgeBase";

const SOURCE_ICON = { manual: Type, pdf: FileText, docx: FileText, txt: File };

export default function KnowledgeBasePanel() {
  const { data: documents, isLoading } = useKnowledgeBase();
  const deleteDocument = useDeleteDocument();
  const [showManualModal, setShowManualModal] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);

  return (
    <div className="max-w-2xl">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-display font-bold text-lg">Knowledge Base & Documents</h2>
          <p className="text-sm text-gray-400 mt-0.5">
            Pricing, policies, and uploaded documents the AI can draw on when suggesting replies.
          </p>
        </div>
        <div className="flex gap-2 shrink-0">
          <Button variant="secondary" onClick={() => setShowManualModal(true)} className="!px-3 !py-1.5 text-xs">
            <Plus size={14} /> Add entry
          </Button>
          <Button onClick={() => setShowUploadModal(true)} className="!px-3 !py-1.5 text-xs">
            <UploadCloud size={14} /> Upload
          </Button>
        </div>
      </div>

      <div className="mt-5 space-y-2">
        {isLoading && <p className="text-sm text-gray-400">Loading...</p>}

        {!isLoading && documents?.length === 0 && (
          <div className="glass-panel p-6 text-sm text-gray-400 text-center">
            Nothing here yet. Add a pricing plan or upload a document to get started.
          </div>
        )}

        {documents?.map((doc) => {
          const Icon = SOURCE_ICON[doc.source_type] || File;
          return (
            <div key={doc.id} className="glass-panel p-4 flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gray-50 dark:bg-white/5 text-brand-500 shrink-0">
                <Icon size={16} />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium truncate">{doc.title}</p>
                <p className="text-xs text-gray-400">
                  {doc.source_type.toUpperCase()} · {doc.chunk_count} indexed chunk{doc.chunk_count === 1 ? "" : "s"} ·{" "}
                  {new Date(doc.created_at).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => deleteDocument.mutate(doc.id)}
                title="Delete"
                className="text-gray-300 hover:text-red-500 transition-colors duration-150 shrink-0"
              >
                <Trash2 size={16} />
              </button>
            </div>
          );
        })}
      </div>

      {showManualModal && <ManualEntryModal onClose={() => setShowManualModal(false)} />}
      {showUploadModal && <UploadDocumentModal onClose={() => setShowUploadModal(false)} />}
    </div>
  );
}
