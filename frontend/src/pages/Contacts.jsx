import { useMemo, useState } from "react";
import { Search, Download, X } from "lucide-react";
import PipelineColumn from "../features/pipeline/components/PipelineColumn";
import ContactDetailDrawer from "../features/pipeline/components/ContactDetailDrawer";
import Button from "../components/ui/Button";
import { useContacts } from "../features/pipeline/hooks/useContacts";
import { useUpdateContact } from "../features/pipeline/hooks/useUpdateContact";
import { useExportContacts } from "../features/pipeline/hooks/useExportContacts";
import { useDebouncedValue } from "../hooks/useDebouncedValue";

const STATUSES = ["new", "qualified", "nurturing", "won", "lost"];

/**
 * Lead pipeline board: every contact the AI (or an agent) has qualified,
 * grouped by lead_status into draggable Kanban columns. Dragging a card to
 * a new column PATCHes the contact - a manual override that sticks until
 * the next AI analysis pass reassesses it.
 *
 * Also doubles as the Customer Database (Milestone 16): the search/filter
 * bar and CSV export both apply server-side, so the export always matches
 * whatever's currently on screen. Lead status itself isn't a filter here -
 * the board already segments by status via the columns.
 */
export default function Contacts() {
  const [search, setSearch] = useState("");
  const [priority, setPriority] = useState("");
  const [sentiment, setSentiment] = useState("");
  const debouncedSearch = useDebouncedValue(search, 300);

  const { data: contacts, isLoading } = useContacts({ search: debouncedSearch, priority, sentiment });
  const updateContact = useUpdateContact();
  const exportContacts = useExportContacts();
  const [selectedContact, setSelectedContact] = useState(null);
  const [dragOverStatus, setDragOverStatus] = useState(null);

  const hasActiveFilters = Boolean(search || priority || sentiment);

  const columns = useMemo(() => {
    const grouped = Object.fromEntries(STATUSES.map((s) => [s, []]));
    for (const contact of contacts || []) {
      (grouped[contact.lead_status] || grouped.new).push(contact);
    }
    return grouped;
  }, [contacts]);

  const handleDragStart = (e, contactId) => {
    e.dataTransfer.setData("text/plain", contactId);
  };

  const handleDrop = (e, newStatus) => {
    e.preventDefault();
    setDragOverStatus(null);
    const contactId = e.dataTransfer.getData("text/plain");
    const contact = (contacts || []).find((c) => c.id === contactId);
    if (contact && contact.lead_status !== newStatus) {
      updateContact.mutate({ contactId, updates: { lead_status: newStatus } });
    }
  };

  const clearFilters = () => {
    setSearch("");
    setPriority("");
    setSentiment("");
  };

  if (isLoading) {
    return <div className="flex h-full items-center justify-center text-sm text-gray-400">Loading pipeline...</div>;
  }

  return (
    <div className="flex h-full flex-col">
      <div className="px-6 py-5 border-b border-gray-100 dark:border-white/5">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 className="font-display font-bold text-lg">Lead Pipeline</h1>
            <p className="text-sm text-gray-400 mt-0.5">
              Drag a card to override the AI's lead status. Click a card for details.
            </p>
          </div>
          <Button
            variant="secondary"
            onClick={() => exportContacts.mutate({ search: debouncedSearch, priority, sentiment })}
            disabled={exportContacts.isPending}
            className="!px-3 !py-1.5 text-xs"
            title="Download the contacts shown below as a CSV file"
          >
            <Download size={14} /> {exportContacts.isPending ? "Exporting..." : "Export CSV"}
          </Button>
        </div>

        <div className="flex items-center gap-2 mt-3 flex-wrap">
          <div className="relative">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search name or phone..."
              className="w-56 rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 py-1.5 pl-8 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
            />
          </div>

          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-sm"
          >
            <option value="">Any priority</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <select
            value={sentiment}
            onChange={(e) => setSentiment(e.target.value)}
            className="rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-2 py-1.5 text-sm"
          >
            <option value="">Any sentiment</option>
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>

          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
            >
              <X size={12} /> Clear filters
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-x-auto p-6">
        <div className="flex h-full gap-4">
          {STATUSES.map((status) => (
            <PipelineColumn
              key={status}
              status={status}
              contacts={columns[status]}
              onDragStart={handleDragStart}
              onDrop={handleDrop}
              onDragOver={setDragOverStatus}
              onDragLeave={() => setDragOverStatus(null)}
              isDragOver={dragOverStatus === status}
              onCardClick={setSelectedContact}
              emptyLabel={hasActiveFilters ? "No matches" : "No leads here yet"}
            />
          ))}
        </div>
      </div>

      {selectedContact && (
        <ContactDetailDrawer contact={selectedContact} onClose={() => setSelectedContact(null)} />
      )}
    </div>
  );
}
