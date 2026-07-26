import { initials } from "../../lib/utils";

/** Gradient-initial avatar - avoids needing real profile photos for a demo/portfolio project. */
export default function Avatar({ name, size = 40 }) {
  return (
    <div
      className="flex items-center justify-center rounded-full bg-gradient-to-br from-brand-500 to-brand-700 text-white font-semibold shrink-0"
      style={{ width: size, height: size, fontSize: size * 0.38 }}
    >
      {initials(name)}
    </div>
  );
}
