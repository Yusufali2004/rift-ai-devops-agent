import React, { useState, useEffect } from 'react';
import { Play, CheckCircle, Clock, Award, GitBranch, Terminal, ShieldCheck } from 'lucide-react';

const API_BASE = "http://localhost:8000";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [data, setData] = useState(null);
  const [repoUrl, setRepoUrl] = useState("");
  const [teamName, setTeamName] = useState("ALGO_NINJAS");
  const [leaderName, setLeaderName] = useState("YUSUF_ALI");

  useEffect(() => {
    let interval;
    if (loading && jobId) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/results/${jobId}`);
          const result = await res.json();
          if (result.status === "completed") {
            setData(result.data); // Mapping to the 'results' object from backend
            setLoading(false);
            clearInterval(interval);
          } else if (result.status === "error") {
            alert("Agent Error: " + result.progress);
            setLoading(false);
            clearInterval(interval);
          }
        } catch (e) { console.error("Polling error", e); }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [loading, jobId]);

  const startAgent = async () => {
    setLoading(true);
    setData(null);
    try {
      const res = await fetch(`${API_BASE}/run-agent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl, team_name: teamName, leader_name: leaderName }),
      });
      const startData = await res.json();
      setJobId(startData.job_id);
    } catch (e) { alert("Backend connection failed!"); setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-10 border-b border-slate-700 pb-6">
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
          <Terminal className="text-blue-400" /> RIFT 2026: Autonomous DevOps Agent
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-800 p-6 rounded-xl border border-slate-700">
          <input placeholder="GitHub Repo URL" className="bg-slate-900 border border-slate-600 p-2 rounded col-span-2" value={repoUrl} onChange={e => setRepoUrl(e.target.value)} />
          <input placeholder="Team Name" className="bg-slate-900 border border-slate-600 p-2 rounded" value={teamName} onChange={e => setTeamName(e.target.value)} />
          <input placeholder="Leader Name" className="bg-slate-900 border border-slate-600 p-2 rounded" value={leaderName} onChange={e => setLeaderName(e.target.value)} />
          <button onClick={startAgent} disabled={loading} className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white font-bold py-2 px-4 rounded transition flex items-center justify-center gap-2">
            {loading ? <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" /> : <Play size={18} />}
            {loading ? "Agent Healing..." : "Run Agent"}
          </button>
        </div>
      </header>

      {data && (
        <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
          <section className="lg:col-span-2 space-y-6">
            {/* Run Summary Card */}
            <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl flex justify-between items-center">
              <div>
                <p className="text-slate-400 text-sm uppercase">Pipeline Status</p>
                <div className={`text-4xl font-black ${data.run_summary.final_status === 'PASSED' ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {data.run_summary.final_status}
                </div>
              </div>
              <div className="text-right">
                <p className="text-slate-400 text-sm">Deployment Branch</p>
                <code className="bg-slate-900 px-3 py-1 rounded text-blue-300 flex items-center gap-2 text-xs">
                  <GitBranch size={14} /> {data.run_summary.branch_created}
                </code>
              </div>
            </div>

            {/* Fixes Applied Table */}
            <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
              <table className="w-full text-left">
                <thead className="text-xs text-slate-400 uppercase bg-slate-900">
                  <tr>
                    <th className="px-6 py-3">File | Line</th>
                    <th className="px-6 py-3">Bug Type</th>
                    <th className="px-6 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {data.fixes_applied.map((fix, idx) => (
                    <tr key={idx} className="hover:bg-slate-700/30 transition">
                      <td className="px-6 py-4 font-mono text-sm text-blue-200">{fix.file} : L{fix.line_number}</td>
                      <td className="px-6 py-4">
                        <span className="bg-amber-900/40 text-amber-300 px-2 py-1 rounded text-xs border border-amber-700/50">
                          {fix.bug_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-emerald-400 flex items-center gap-1"><CheckCircle size={14} /> Fixed</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="space-y-6">
            {/* Score Breakdown Panel */}
            <div className="bg-gradient-to-br from-blue-900/40 to-slate-800 p-6 rounded-xl border border-blue-500/30">
              <h3 className="flex items-center gap-2 text-slate-300 mb-4"><Award className="text-yellow-400" /> Score Breakdown</h3>
              <div className="text-5xl font-bold mb-4">{data.score_breakdown.final_score} <span className="text-lg font-normal text-slate-400">pts</span></div>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between"><span>Base Score</span><span>{data.score_breakdown.breakdown.base_score}</span></div>
                <div className="flex justify-between text-emerald-400"><span>Speed Bonus</span><span>+{data.score_breakdown.breakdown.speed_bonus}</span></div>
                <div className="flex justify-between text-rose-400"><span>Efficiency Penalty</span><span>{data.score_breakdown.breakdown.efficiency_penalty}</span></div>
                <div className="pt-2 border-t border-slate-700 flex justify-between text-slate-400 italic">
                  <span><Clock size={12} className="inline mr-1"/> {data.run_summary.total_time_seconds}s total</span>
                </div>
              </div>
            </div>

            {/* CI/CD Timeline */}
            <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl">
              <h3 className="flex items-center gap-2 text-slate-300 mb-4 font-bold">CI/CD Status Timeline ({data.ci_cd_timeline.iterations_used})</h3>
              <div className="space-y-4">
                {data.ci_cd_timeline.timeline.map((step, i) => (
                  <div key={i} className="flex gap-3 items-start">
                    <div className={`w-3 h-3 mt-1 rounded-full ${step.status === 'PASSED' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 'bg-rose-500'}`} />
                    <div>
                      <p className="text-sm font-bold">Iteration {step.iteration}</p>
                      <p className="text-xs text-slate-400">{step.timestamp} - {step.status}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </main>
      )}
    </div>
  );
}