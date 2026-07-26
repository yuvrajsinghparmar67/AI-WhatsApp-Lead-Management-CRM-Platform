import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { MessageSquareText } from "lucide-react";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import Button from "../components/ui/Button";

export default function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [formError, setFormError] = useState(null);

  const onSubmit = async (data) => {
    setFormError(null);
    try {
      const result = await api.post("/auth/login", data);
      login(result.access_token);
      navigate("/", { replace: true });
    } catch (err) {
      setFormError(err.message || "Login failed");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-surface-light dark:bg-surface-dark px-4">
      <motion.form
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: "easeOut" }}
        onSubmit={handleSubmit(onSubmit)}
        className="glass-panel w-full max-w-sm p-8"
      >
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 text-white mb-4">
          <MessageSquareText size={18} />
        </div>
        <h1 className="font-display font-bold text-xl mb-1">Welcome back</h1>
        <p className="text-sm text-gray-400 mb-6">Sign in to your AI WhatsApp CRM</p>

        {formError && (
          <p className="text-sm text-red-500 mb-4 rounded-lg bg-red-50 dark:bg-red-500/10 px-3 py-2">{formError}</p>
        )}

        <div className="space-y-4">
          <div>
            <label className="text-xs font-medium text-gray-500">Email</label>
            <input
              type="email"
              {...register("email", { required: "Email is required" })}
              className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
            />
            {errors.email && <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500">Password</label>
            <input
              type="password"
              {...register("password", { required: "Password is required" })}
              className="mt-1 w-full rounded-lg border border-gray-200 dark:border-white/10 bg-white dark:bg-white/5 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400"
            />
            {errors.password && <p className="text-xs text-red-500 mt-1">{errors.password.message}</p>}
          </div>
        </div>

        <Button type="submit" disabled={isSubmitting} className="w-full mt-6">
          {isSubmitting ? "Signing in..." : "Sign in"}
        </Button>

        <p className="text-xs text-gray-400 text-center mt-4">
          Don't have an account?{" "}
          <Link to="/register" className="text-brand-500 font-medium">
            Create one
          </Link>
        </p>
      </motion.form>
    </div>
  );
}
