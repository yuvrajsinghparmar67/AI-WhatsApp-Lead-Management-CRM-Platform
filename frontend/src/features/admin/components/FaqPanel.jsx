import { useState } from "react";
import { Plus, Trash2, Pencil, HelpCircle } from "lucide-react";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import FaqModal from "./FaqModal";
import { useDeleteFaq, useFaqs } from "../hooks/useFaqs";

export default function FaqPanel() {
  const { data: faqs, isLoading } = useFaqs();
  const deleteFaq = useDeleteFaq();
  const [modalFaq, setModalFaq] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const openCreate = () => {
    setModalFaq(null);
    setShowModal(true);
  };

  const openEdit = (faq) => {
    setModalFaq(faq);
    setShowModal(true);
  };

  return (
    <div className="max-w-2xl">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-display font-bold text-lg">FAQs</h2>
          <p className="text-sm text-gray-400 mt-0.5">
            Pre-answered questions the AI uses verbatim when a customer asks something close enough.
          </p>
        </div>
        <Button onClick={openCreate} className="!px-3 !py-1.5 text-xs shrink-0">
          <Plus size={14} /> Add FAQ
        </Button>
      </div>

      <div className="mt-5 space-y-2">
        {isLoading && <p className="text-sm text-gray-400">Loading...</p>}

        {!isLoading && faqs?.length === 0 && (
          <div className="glass-panel p-6 text-sm text-gray-400 text-center">
            No FAQs yet. Add one — e.g. "Do you offer a free trial?"
          </div>
        )}

        {faqs?.map((faq) => (
          <div key={faq.id} className="glass-panel p-4">
            <div className="flex items-start gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gray-50 dark:bg-white/5 text-brand-500 shrink-0">
                <HelpCircle size={16} />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <p className="text-sm font-medium">{faq.question}</p>
                  {faq.category && <Badge priority="medium" className="!bg-gray-100 !text-gray-600 dark:!bg-white/10 dark:!text-gray-300">{faq.category}</Badge>}
                  {!faq.is_active && <Badge priority="low">Inactive</Badge>}
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{faq.answer}</p>
              </div>
              <div className="flex items-center gap-1 shrink-0">
                <button onClick={() => openEdit(faq)} className="text-gray-300 hover:text-brand-500 transition-colors duration-150">
                  <Pencil size={15} />
                </button>
                <button onClick={() => deleteFaq.mutate(faq.id)} className="text-gray-300 hover:text-red-500 transition-colors duration-150">
                  <Trash2 size={15} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {showModal && <FaqModal faq={modalFaq} onClose={() => setShowModal(false)} />}
    </div>
  );
}
