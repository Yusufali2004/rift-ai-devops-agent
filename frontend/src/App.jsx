import React, { useState, useEffect } from 'react';
import { Play, CheckCircle, XCircle, Clock, Award, GitBranch, Terminal } from 'lucide-react';

const API_BASE = "http://localhost:8000"; // Update to your deployed URL later

export default function App() {
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [data, setData] = useState(null);
  const [repoUrl, setRepoUrl] = useState("");
  const [teamName, setTeamName] = useState("RIFT_DEVS");
  const [leaderName, setLeaderName] = useState("YUSUF_ALI");

  // Poll for results every 3 seconds if a job is running
  useEffect(() => {
    let interval;
    if (loading && jobId) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/results/${jobId}`);
          const result = await res.json();
          if (result.status !== "processing") {
            setData(result);
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
      {/* Header & Inputs */}
      <header className="max-w-6xl mx-auto mb-10 border-b border-slate-700 pb-6">
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
          <Terminal className="text-blue-400" /> RIFT Autonomous DevOps Agent
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-800 p-6 rounded-xl border border-slate-700">
          <input placeholder="GitHub Repo URL" className="bg-slate-900 border border-slate-600 p-2 rounded col-span-2" value={repoUrl} onChange={e => setRepoUrl(e.target.value)} />
          <input placeholder="Team Name" className="bg-slate-900 border border-slate-600 p-2 rounded" value={teamName} onChange={e => setTeamName(e.target.value)} />
          <input placeholder="Leader Name" className="bg-slate-900 border border-slate-600 p-2 rounded" value={leaderName} onChange={e => setLeaderName(e.target.value)} />
          <button onClick={startAgent} disabled={loading} className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white font-bold py-2 px-4 rounded transition flex items-center justify-center gap-2">
            {loading ? <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" /> : <Play size={18} />}
            {loading ? "Agent Running..." : "Analyze Repository"}
          </button>
        </div>
      </header>

      {data && (
        <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {/* Summary Card */}
          <section className="lg:col-span-2 space-y-6">
            <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl flex justify-between items-center">
              <div>
                <p className="text-slate-400 text-sm uppercase tracking-wider">Status</p>
                <div className={`text-4xl font-black ${data.status === 'PASSED' ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {data.status}
                </div>
              </div>
              <div className="text-right">
                <p className="text-slate-400 text-sm">Target Branch</p>
                <code className="bg-slate-900 px-3 py-1 rounded text-blue-300 flex items-center gap-2">
                  <GitBranch size={14} /> {data.branch_name}
                </code>
              </div>
            </div>

            {/* Fixes Table */}
            <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
              <div className="p-4 border-b border-slate-700 bg-slate-800/50 font-bold">Applied Fixes</div>
              <table className="w-full text-left">
                <thead className="text-xs text-slate-400 uppercase bg-slate-900">
                  <tr>
                    <th className="px-6 py-3">File</th>
                    <th className="px-6 py-3">Bug Type</th>
                    <th className="px-6 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {data.fixes.map((fix, idx) => (
                    <tr key={idx} className="hover:bg-slate-700/30 transition">
                      <td className="px-6 py-4 font-mono text-sm text-blue-200">{fix.file}</td>
                      <td className="px-6 py-4"><span className="bg-amber-900/40 text-amber-300 px-2 py-1 rounded text-xs border border-amber-700/50">{fix.bug_type}</span></td>
                      <td className="px-6 py-4 text-emerald-400 flex items-center gap-1"><CheckCircle size={14} /> {fix.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {/* Scoring & Timeline */}
          <section className="space-y-6">
            <div className="bg-gradient-to-br from-blue-900/40 to-slate-800 p-6 rounded-xl border border-blue-500/30">
              <h3 className="flex items-center gap-2 text-slate-300 mb-4"><Award className="text-yellow-400" /> Agent Performance</h3>
              <div className="text-5xl font-bold mb-2">{data.final_score} <span className="text-lg font-normal text-slate-400">pts</span></div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span>Base Score</span><span>100</span></div>
                <div className="flex justify-between text-emerald-400"><span>Speed Bonus</span><span>+10</span></div>
                <div className="flex justify-between text-slate-400 italic"><span>Time taken: {data.processing_time_seconds}s</span></div>
              </div>
            </div>

            <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl">
              <h3 className="flex items-center gap-2 text-slate-300 mb-4"><Clock size={18} /> Run Timeline</h3>
              <div className="space-y-4">
                {data.fixes.map((_, i) => (
                  <div key={i} className="flex gap-3 items-start">
                    <div className="flex flex-col items-center">
                      <div className="w-4 h-4 rounded-full bg-blue-500 ring-4 ring-blue-900" />
                      {i < data.fixes.length - 1 && <div className="w-0.5 h-8 bg-slate-700" />}
                    </div>
                    <div>
                      <p className="text-sm font-bold">Iteration {i + 1}</p>
                      <p className="text-xs text-slate-400">Fix applied successfully</p>
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