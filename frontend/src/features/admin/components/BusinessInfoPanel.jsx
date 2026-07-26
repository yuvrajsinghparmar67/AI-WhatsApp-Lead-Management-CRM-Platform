import { useEffect, useState } from "react";
import { Check } from "lucide-react";
import Button from "../../../components/ui/Button";
import BusinessHoursEditor from "./BusinessHoursEditor";
import { useCompany, useUpdateCompany } from "../hooks/useCompany";

const FIELD_META = [
  { key: "business_name", label: "Business name", placeholder: "Iron Peak Gym" },
  { key: "address", label: "Address", placeholder: "221B Baker Street, London" },
  { key: "phone", label: "Phone", placeholder: "+1 555 010 0100" },
  { key: "email", label: "Email", placeholder: "hello@ironpeakgym.com" },
  { key: "website", label: "Website", placeholder: "https://ironpeakgym.com" },
];

export default function BusinessInfoPanel() {
  const { data: company, isLoading } = useCompany();
  const updateCompany = useUpdateCompany();
  const [form, setForm] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (company) setForm(company);
  }, [company]);

  if (isLoading || !form) {
    return <div className="text-sm text-gray-400">Loading business information...</div>;
  }

  const handleSave = async (e) => {
    e.preventDefault();
    await updateCompany.mutateAsync({
      business_name: form.business_name,
      address: form.address,
      phone: form.phone,
      email: form.email,
      website: form.website,
      business_hours: form.business_hours,
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <form onSubmit={handleSave} className="max-w-xl space-y-6">
      <div>
        <h2 className="font-display font-bold text-lg">Business Information</h2>
        <p className="text-sm text-gray-400 mt-0.5">
          This is what the AI uses to answer questions like "what are your hours" or "where are you located."
        </p>
      </div>

      <div className="space-y-4">
        {FIELD_META.map(({ key, label, placeholder }) => (
          <div key={key}>
            <label className="text-xs font-medium text-gray-500">{label}</label>
            <input
              value={form[key] || ""}
              onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              placeholder={placeholder}
              className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
            />
          </div>
        ))}
      </div>

      <div>
        <label className="text-xs font-medium text-gray-500 mb-2 block">Business hours</label>
        <BusinessHoursEditor
          hours={form.business_hours}
          onChange={(hours) => setForm({ ...form, business_hours: hours })}
        />
      </div>

      <div className="flex items-center gap-3">
        <Button type="submit" disabled={updateCompany.isPending}>
          {updateCompany.isPending ? "Saving..." : "Save changes"}
        </Button>
        {saved && (
          <span className="flex items-center gap-1 text-sm text-emerald-500">
            <Check size={14} /> Saved
          </span>
        )}
      </div>
    </form>
  );
}
