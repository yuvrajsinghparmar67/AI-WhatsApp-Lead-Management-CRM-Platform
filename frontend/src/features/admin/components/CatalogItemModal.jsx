import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Plus, Trash2 } from "lucide-react";
import Button from "../../../components/ui/Button";
import { useCreateCatalogItem, useUpdateCatalogItem } from "../hooks/useCatalog";

const BLANK = {
  name: "",
  item_type: "service",
  price: "",
  currency: "USD",
  billing_period: "monthly",
  description: "",
  features: [],
};

export default function CatalogItemModal({ item, onClose }) {
  const isEditing = Boolean(item);
  const [form, setForm] = useState(item ? { ...item, price: item.price ?? "" } : BLANK);
  const [featureDraft, setFeatureDraft] = useState("");
  const createItem = useCreateCatalogItem();
  const updateItem = useUpdateCatalogItem();
  const isSaving = createItem.isPending || updateItem.isPending;
  const isError = createItem.isError || updateItem.isError;

  const addFeature = () => {
    if (!featureDraft.trim()) return;
    setForm({ ...form, features: [...form.features, featureDraft.trim()] });
    setFeatureDraft("");
  };

  const removeFeature = (index) => {
    setForm({ ...form, features: form.features.filter((_, i) => i !== index) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      ...form,
      price: form.price === "" ? null : Number(form.price),
      billing_period: form.item_type === "product" && !form.price ? null : form.billing_period,
    };

    if (isEditing) {
      await updateItem.mutateAsync({ id: item.id, payload });
    } else {
      await createItem.mutateAsync(payload);
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
          className="glass-panel w-full max-w-md p-6 z-50 max-h-[85vh] overflow-y-auto"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-display font-bold">{isEditing ? "Edit item" : "Add product or service"}</h3>
            <button type="button" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={18} />
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">Name</label>
              <input
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="Premium Gym Membership"
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-medium text-gray-500">Type</label>
                <select
                  value={form.item_type}
                  onChange={(e) => setForm({ ...form, item_type: e.target.value })}
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
                >
                  <option value="product">Product</option>
                  <option value="service">Service</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500">Active</label>
                <select
                  value={form.is_active ? "true" : "false"}
                  onChange={(e) => setForm({ ...form, is_active: e.target.value === "true" })}
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
                >
                  <option value="true">Active</option>
                  <option value="false">Inactive</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="text-xs font-medium text-gray-500">Currency</label>
                <input
                  value={form.currency}
                  onChange={(e) => setForm({ ...form, currency: e.target.value })}
                  placeholder="USD"
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500">Price</label>
                <input
                  type="number"
                  step="0.01"
                  value={form.price}
                  onChange={(e) => setForm({ ...form, price: e.target.value })}
                  placeholder="2500"
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500">Billing</label>
                <select
                  value={form.billing_period || ""}
                  onChange={(e) => setForm({ ...form, billing_period: e.target.value || null })}
                  className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
                >
                  <option value="one_time">One-time</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-gray-500">Description</label>
              <textarea
                value={form.description || ""}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                rows={2}
                className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-gray-500">Features</label>
              <div className="flex gap-2 mt-1">
                <input
                  value={featureDraft}
                  onChange={(e) => setFeatureDraft(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addFeature();
                    }
                  }}
                  placeholder="Unlimited access"
                  className="flex-1 rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm"
                />
                <button
                  type="button"
                  onClick={addFeature}
                  className="flex h-9 w-9 items-center justify-center rounded-lg bg-gray-100 dark:bg-white/10 text-gray-600 dark:text-gray-300"
                >
                  <Plus size={14} />
                </button>
              </div>
              {form.features.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {form.features.map((feature, index) => (
                    <li key={index} className="flex items-center justify-between text-xs bg-gray-50 dark:bg-white/5 rounded-lg px-2.5 py-1.5">
                      <span>{feature}</span>
                      <button type="button" onClick={() => removeFeature(index)} className="text-gray-300 hover:text-red-500">
                        <Trash2 size={12} />
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          {isError && (
            <p className="text-xs text-red-500 mt-3">Couldn't save this item — check your GEMINI_API_KEY and try again.</p>
          )}

          <Button type="submit" className="w-full mt-5" disabled={isSaving}>
            {isSaving ? "Saving..." : isEditing ? "Save changes" : "Add item"}
          </Button>
        </motion.form>
      </motion.div>
    </AnimatePresence>
  );
}
