import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { api } from "../lib/api";

/**
 * Milestone 1's proof-of-life screen: confirms the frontend can reach the
 * FastAPI backend's /health endpoint. Real dashboard pages (inbox, leads,
 * analytics) replace this in later milestones.
 */
export default function SystemStatus() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["health"],
    queryFn: () => api.get("/health"),
  });

  return (
    <div className="h-full flex flex-col items-center justify-center px-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="glass-panel w-full max-w-md p-8 text-center"
      >
        <h1 className="text-2xl font-bold mb-1 bg-gradient-to-r from-brand-600 to-brand-400 bg-clip-text text-transparent">
          AI WhatsApp CRM
        </h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Milestone 1 — Architecture Foundation
        </p>

        <div className="flex items-center justify-center gap-2 rounded-xl bg-gray-50 dark:bg-white/5 py-4">
          {isLoading && (
            <>
              <Loader2 className="animate-spin text-brand-500" size={20} />
              <span className="text-sm text-gray-500 dark:text-gray-400">Checking backend...</span>
            </>
          )}
          {isError && (
            <>
              <XCircle className="text-red-500" size={20} />
              <span className="text-sm text-red-500">Backend unreachable</span>
            </>
          )}
          {data && (
            <>
              <CheckCircle2 className="text-emerald-500" size={20} />
              <span className="text-sm text-emerald-600 dark:text-emerald-400 font-medium">
                Backend status: {data.status}
              </span>
            </>
          )}
        </div>
      </motion.div>
    </div>
  );
}
