import { useState, useEffect, useCallback } from "react";

const API = "http://127.0.0.1:8000";
const HEADERS = { "Content-Type": "application/json", Authorization: "Bearer demo-jwt-token-taskmanager" };

const PRIORITIES = ["Critical", "High", "Medium", "Low"];
const STATUSES = ["Open", "In Progress", "Closed"];
const MODULES = ["General", "Auth", "Task Management", "UI", "Testing", "DevOps", "API", "Database"];

const PRIORITY_COLOR: Record<string, string> = {
  Critical: "#ef4444", High: "#f97316", Medium: "#eab308", Low: "#22c55e",
};
const STATUS_COLOR: Record<string, string> = {
  Open: "#3b82f6", "In Progress": "#a855f7", Closed: "#22c55e",
};

type Task = {
  id: string; title: string; description: string;
  status: string; priority: string; module: string;
  assigned_to: string; created_at: string;
};
type Stats = { total: number; open: number; in_progress: number; closed: number };
type FormData = Omit<Task, "id" | "created_at">;

const EMPTY_FORM: FormData = { title: "", description: "", status: "Open", priority: "Medium", module: "General", assigned_to: "" };

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<Stats>({ total: 0, open: 0, in_progress: 0, closed: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const [filterPriority, setFilterPriority] = useState("");
  const [modal, setModal] = useState<"create" | "edit" | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [form, setForm] = useState<FormData>(EMPTY_FORM);
  const [formError, setFormError] = useState("");
  const [deleteConfirm, setDeleteConfirm] = useState<Task | null>(null);
  const [saving, setSaving] = useState(false);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      if (filterStatus) params.append("status", filterStatus);
      if (filterPriority) params.append("priority", filterPriority);
      if (search) params.append("search", search);

      const [taskRes, statRes] = await Promise.all([
        fetch(`${API}/tasks?${params}`, { headers: HEADERS }),
        fetch(`${API}/tasks/stats/summary`, { headers: HEADERS }),
      ]);

      if (!taskRes.ok) throw new Error(`Tasks API error: ${taskRes.status}`);
      if (!statRes.ok) throw new Error(`Stats API error: ${statRes.status}`);

      setTasks(await taskRes.json());
      setStats(await statRes.json());
    } catch (e: any) {
      setError(e.message || "Cannot connect to backend. Make sure it is running on port 8000.");
    } finally {
      setLoading(false);
    }
  }, [filterStatus, filterPriority, search]);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  const openCreate = () => { setForm(EMPTY_FORM); setFormError(""); setModal("create"); };
  const openEdit = (t: Task) => { setEditingTask(t); setForm({ title: t.title, description: t.description, status: t.status, priority: t.priority, module: t.module, assigned_to: t.assigned_to }); setFormError(""); setModal("edit"); };
  const closeModal = () => { setModal(null); setEditingTask(null); setFormError(""); };

  const handleSave = async () => {
    if (!form.title.trim()) { setFormError("Title is required."); return; }
    setSaving(true);
    try {
      const url = modal === "edit" && editingTask ? `${API}/tasks/${editingTask.id}` : `${API}/tasks`;
      const method = modal === "edit" ? "PUT" : "POST";
      const res = await fetch(url, { method, headers: HEADERS, body: JSON.stringify(form) });
      if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Save failed"); }
      closeModal();
      fetchAll();
    } catch (e: any) {
      setFormError(e.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (task: Task) => {
    try {
      const res = await fetch(`${API}/tasks/${task.id}`, { method: "DELETE", headers: HEADERS });
      if (!res.ok) throw new Error("Delete failed");
      setDeleteConfirm(null);
      fetchAll();
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0f172a", fontFamily: "'Segoe UI', system-ui, sans-serif", color: "#e2e8f0" }}>
      <header style={{ background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)", borderBottom: "1px solid #1e3a5f", padding: "0 32px", display: "flex", alignItems: "center", justifyContent: "space-between", height: 64 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, background: "linear-gradient(135deg, #3b82f6, #8b5cf6)", borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18 }}>✓</div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 18, letterSpacing: "-0.5px", color: "#f1f5f9" }}>TaskManager Pro</div>
            <div style={{ fontSize: 11, color: "#64748b" }}>RTM & STLC Testing Suite</div>
          </div>
        </div>
        <button onClick={openCreate} style={{ background: "linear-gradient(135deg, #3b82f6, #6366f1)", color: "#fff", border: "none", borderRadius: 8, padding: "9px 20px", fontWeight: 600, fontSize: 14, cursor: "pointer" }}>
          + New Task
        </button>
      </header>

      <main style={{ maxWidth: 1280, margin: "0 auto", padding: "28px 32px" }}>
        {error && (
          <div style={{ background: "#7f1d1d", border: "1px solid #ef4444", borderRadius: 10, padding: "12px 16px", marginBottom: 24, display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 14 }}>
            <span>⚠️ {error}</span>
            <div style={{ display: "flex", gap: 10 }}>
              <button onClick={fetchAll} style={{ background: "#ef4444", color: "#fff", border: "none", borderRadius: 6, padding: "5px 12px", cursor: "pointer", fontSize: 13 }}>Retry</button>
              <button onClick={() => setError("")} style={{ background: "transparent", color: "#fca5a5", border: "none", cursor: "pointer", fontSize: 18 }}>×</button>
            </div>
          </div>
        )}

        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 28 }}>
          {[
            { label: "Total Tasks", value: stats.total, color: "#3b82f6", icon: "📋" },
            { label: "Open", value: stats.open, color: "#f97316", icon: "🔓" },
            { label: "In Progress", value: stats.in_progress, color: "#a855f7", icon: "⚙️" },
            { label: "Closed", value: stats.closed, color: "#22c55e", icon: "✅" },
          ].map(s => (
            <div key={s.label} style={{ background: "#1e293b", border: `1px solid ${s.color}30`, borderRadius: 14, padding: "20px 24px", borderLeft: `4px solid ${s.color}` }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <div style={{ fontSize: 13, color: "#94a3b8", marginBottom: 6 }}>{s.label}</div>
                  <div style={{ fontSize: 32, fontWeight: 700, color: s.color }}>{loading ? "—" : s.value}</div>
                </div>
                <div style={{ fontSize: 28 }}>{s.icon}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ background: "#1e293b", borderRadius: 14, padding: "16px 20px", marginBottom: 20, display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center", border: "1px solid #334155" }}>
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="🔍 Search tasks..."
            style={{ flex: "1 1 220px", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "9px 14px", color: "#e2e8f0", fontSize: 14, outline: "none" }} />
          <select value={filterStatus} onChange={e => setFilterStatus(e.target.value)}
            style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "9px 14px", color: "#e2e8f0", fontSize: 14, cursor: "pointer" }}>
            <option value="">All Statuses</option>
            {STATUSES.map(s => <option key={s}>{s}</option>)}
          </select>
          <select value={filterPriority} onChange={e => setFilterPriority(e.target.value)}
            style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "9px 14px", color: "#e2e8f0", fontSize: 14, cursor: "pointer" }}>
            <option value="">All Priorities</option>
            {PRIORITIES.map(p => <option key={p}>{p}</option>)}
          </select>
          {(filterStatus || filterPriority || search) && (
            <button onClick={() => { setFilterStatus(""); setFilterPriority(""); setSearch(""); }}
              style={{ background: "#334155", color: "#94a3b8", border: "none", borderRadius: 8, padding: "9px 14px", cursor: "pointer", fontSize: 13 }}>Clear ×</button>
          )}
        </div>

        <div style={{ background: "#1e293b", borderRadius: 14, border: "1px solid #334155", overflow: "hidden" }}>
          <div style={{ padding: "16px 24px", borderBottom: "1px solid #334155" }}>
            <span style={{ fontWeight: 600, fontSize: 15 }}>Tasks ({loading ? "…" : tasks.length})</span>
          </div>
          {loading ? (
            <div style={{ padding: 60, textAlign: "center", color: "#64748b" }}>Loading tasks…</div>
          ) : tasks.length === 0 ? (
            <div style={{ padding: 60, textAlign: "center", color: "#64748b" }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>📭</div>
              No tasks found. <button onClick={openCreate} style={{ color: "#3b82f6", background: "none", border: "none", cursor: "pointer", textDecoration: "underline" }}>Create one.</button>
            </div>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "#0f172a" }}>
                  {["Title", "Module", "Status", "Priority", "Assigned To", "Actions"].map(h => (
                    <th key={h} style={{ padding: "12px 20px", textAlign: "left", fontSize: 12, fontWeight: 600, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tasks.map((task, i) => (
                  <tr key={task.id} style={{ borderTop: "1px solid #334155", background: i % 2 === 0 ? "transparent" : "#1a2744" }}>
                    <td style={{ padding: "14px 20px", maxWidth: 300 }}>
                      <div style={{ fontWeight: 500, fontSize: 14 }}>{task.title}</div>
                      {task.description && <div style={{ fontSize: 12, color: "#64748b", marginTop: 3 }}>{task.description.slice(0, 60)}{task.description.length > 60 ? "…" : ""}</div>}
                    </td>
                    <td style={{ padding: "14px 20px" }}>
                      <span style={{ background: "#1e3a5f", color: "#93c5fd", borderRadius: 6, padding: "3px 10px", fontSize: 12 }}>{task.module}</span>
                    </td>
                    <td style={{ padding: "14px 20px" }}>
                      <span style={{ background: `${STATUS_COLOR[task.status]}20`, color: STATUS_COLOR[task.status], border: `1px solid ${STATUS_COLOR[task.status]}40`, borderRadius: 20, padding: "3px 12px", fontSize: 12, fontWeight: 600 }}>{task.status}</span>
                    </td>
                    <td style={{ padding: "14px 20px" }}>
                      <span style={{ display: "inline-flex", alignItems: "center", gap: 5, fontSize: 13 }}>
                        <span style={{ width: 8, height: 8, borderRadius: "50%", background: PRIORITY_COLOR[task.priority], display: "inline-block" }} />
                        <span style={{ color: PRIORITY_COLOR[task.priority], fontWeight: 600 }}>{task.priority}</span>
                      </span>
                    </td>
                    <td style={{ padding: "14px 20px", fontSize: 13, color: "#94a3b8" }}>{task.assigned_to || "—"}</td>
                    <td style={{ padding: "14px 20px" }}>
                      <div style={{ display: "flex", gap: 8 }}>
                        <button onClick={() => openEdit(task)} style={{ background: "#1e3a5f", color: "#93c5fd", border: "1px solid #1d4ed8", borderRadius: 6, padding: "5px 12px", cursor: "pointer", fontSize: 12 }}>Edit</button>
                        <button onClick={() => setDeleteConfirm(task)} style={{ background: "#7f1d1d", color: "#fca5a5", border: "1px solid #ef444440", borderRadius: 6, padding: "5px 12px", cursor: "pointer", fontSize: 12 }}>Delete</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>

      {modal && (
        <div style={{ position: "fixed", inset: 0, background: "#00000080", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100, padding: 20 }}>
          <div style={{ background: "#1e293b", borderRadius: 16, width: "100%", maxWidth: 520, border: "1px solid #334155", boxShadow: "0 25px 60px #00000060" }}>
            <div style={{ padding: "20px 24px", borderBottom: "1px solid #334155", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h2 style={{ margin: 0, fontSize: 17, fontWeight: 700 }}>{modal === "edit" ? "Edit Task" : "New Task"}</h2>
              <button onClick={closeModal} style={{ background: "transparent", border: "none", color: "#64748b", fontSize: 22, cursor: "pointer" }}>×</button>
            </div>
            <div style={{ padding: "24px", display: "flex", flexDirection: "column", gap: 16 }}>
              {formError && <div style={{ background: "#7f1d1d", color: "#fca5a5", borderRadius: 8, padding: "10px 14px", fontSize: 13 }}>{formError}</div>}
              <div>
                <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginBottom: 6 }}>Title *</label>
                <input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })}
                  style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "10px 14px", color: "#e2e8f0", fontSize: 14, outline: "none", boxSizing: "border-box" }} />
              </div>
              <div>
                <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginBottom: 6 }}>Description</label>
                <textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} rows={3}
                  style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "10px 14px", color: "#e2e8f0", fontSize: 14, outline: "none", resize: "vertical", boxSizing: "border-box" }} />
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                {[
                  { label: "Status", key: "status", opts: STATUSES },
                  { label: "Priority", key: "priority", opts: PRIORITIES },
                  { label: "Module", key: "module", opts: MODULES },
                ].map(f => (
                  <div key={f.key}>
                    <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginBottom: 6 }}>{f.label}</label>
                    <select value={(form as any)[f.key]} onChange={e => setForm({ ...form, [f.key]: e.target.value })}
                      style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "10px 14px", color: "#e2e8f0", fontSize: 14, cursor: "pointer" }}>
                      {f.opts.map(o => <option key={o}>{o}</option>)}
                    </select>
                  </div>
                ))}
                <div>
                  <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginBottom: 6 }}>Assigned To</label>
                  <input value={form.assigned_to} onChange={e => setForm({ ...form, assigned_to: e.target.value })}
                    style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "10px 14px", color: "#e2e8f0", fontSize: 14, outline: "none", boxSizing: "border-box" }} />
                </div>
              </div>
            </div>
            <div style={{ padding: "16px 24px", borderTop: "1px solid #334155", display: "flex", justifyContent: "flex-end", gap: 10 }}>
              <button onClick={closeModal} style={{ background: "#334155", color: "#94a3b8", border: "none", borderRadius: 8, padding: "10px 20px", cursor: "pointer", fontSize: 14 }}>Cancel</button>
              <button onClick={handleSave} disabled={saving} style={{ background: "linear-gradient(135deg, #3b82f6, #6366f1)", color: "#fff", border: "none", borderRadius: 8, padding: "10px 24px", cursor: "pointer", fontSize: 14, fontWeight: 600 }}>
                {saving ? "Saving…" : modal === "edit" ? "Update" : "Create"}
              </button>
            </div>
          </div>
        </div>
      )}

      {deleteConfirm && (
        <div style={{ position: "fixed", inset: 0, background: "#00000080", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100 }}>
          <div style={{ background: "#1e293b", borderRadius: 16, width: "100%", maxWidth: 420, border: "1px solid #7f1d1d", padding: 28 }}>
            <div style={{ fontSize: 36, marginBottom: 12, textAlign: "center" }}>🗑️</div>
            <h3 style={{ margin: "0 0 8px", textAlign: "center", fontSize: 17 }}>Delete Task?</h3>
            <p style={{ margin: "0 0 24px", color: "#94a3b8", fontSize: 14, textAlign: "center" }}>
              "<strong style={{ color: "#e2e8f0" }}>{deleteConfirm.title}</strong>" will be permanently deleted.
            </p>
            <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
              <button onClick={() => setDeleteConfirm(null)} style={{ background: "#334155", color: "#94a3b8", border: "none", borderRadius: 8, padding: "10px 24px", cursor: "pointer" }}>Cancel</button>
              <button onClick={() => handleDelete(deleteConfirm)} style={{ background: "#ef4444", color: "#fff", border: "none", borderRadius: 8, padding: "10px 24px", cursor: "pointer", fontWeight: 600 }}>Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}