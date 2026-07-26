import { useState } from "react";
import { Plus, Trash2, Pencil, Package, Wrench } from "lucide-react";
import clsx from "clsx";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import CatalogItemModal from "./CatalogItemModal";
import { useCatalog, useDeleteCatalogItem } from "../hooks/useCatalog";

const BILLING_LABEL = { one_time: "one-time", monthly: "/mo", yearly: "/yr" };

function formatPrice(item) {
  if (item.price == null) return "Contact for pricing";
  return `${item.currency} ${item.price.toLocaleString()}${item.billing_period ? BILLING_LABEL[item.billing_period] || "" : ""}`;
}

export default function CatalogPanel() {
  const { data: items, isLoading } = useCatalog();
  const deleteItem = useDeleteCatalogItem();
  const [modalItem, setModalItem] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const openCreate = () => {
    setModalItem(null);
    setShowModal(true);
  };

  const openEdit = (item) => {
    setModalItem(item);
    setShowModal(true);
  };

  return (
    <div className="max-w-3xl">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-display font-bold text-lg">Products, Services & Pricing</h2>
          <p className="text-sm text-gray-400 mt-0.5">
            What you sell and what it costs — used by the AI to answer pricing and plan questions confidently.
          </p>
        </div>
        <Button onClick={openCreate} className="!px-3 !py-1.5 text-xs shrink-0">
          <Plus size={14} /> Add item
        </Button>
      </div>

      <div className="mt-5 space-y-2">
        {isLoading && <p className="text-sm text-gray-400">Loading...</p>}

        {!isLoading && items?.length === 0 && (
          <div className="glass-panel p-6 text-sm text-gray-400 text-center">
            No products or services yet. Add one — e.g. "Premium Gym Membership", ₹2500/month.
          </div>
        )}

        {items?.map((item) => {
          const Icon = item.item_type === "product" ? Package : Wrench;
          return (
            <div key={item.id} className="glass-panel p-4">
              <div className="flex items-start gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gray-50 dark:bg-white/5 text-brand-500 shrink-0">
                  <Icon size={16} />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-medium">{item.name}</p>
                    {!item.is_active && <Badge priority="low">Inactive</Badge>}
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{formatPrice(item)}</p>
                  {item.description && <p className="text-xs text-gray-400 mt-1">{item.description}</p>}
                  {item.features?.length > 0 && (
                    <ul className="flex flex-wrap gap-1.5 mt-2">
                      {item.features.map((feature, i) => (
                        <li key={i} className="text-[11px] bg-gray-50 dark:bg-white/5 rounded-full px-2 py-0.5 text-gray-500 dark:text-gray-400">
                          {feature}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  <button onClick={() => openEdit(item)} className="text-gray-300 hover:text-brand-500 transition-colors duration-150">
                    <Pencil size={15} />
                  </button>
                  <button onClick={() => deleteItem.mutate(item.id)} className="text-gray-300 hover:text-red-500 transition-colors duration-150">
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {showModal && <CatalogItemModal item={modalItem} onClose={() => setShowModal(false)} />}
    </div>
  );
}
