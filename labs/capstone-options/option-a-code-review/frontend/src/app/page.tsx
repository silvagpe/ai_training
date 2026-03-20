"use client";

import { FormEvent, useMemo, useState } from "react";

type AnalyzerIssue = {
  severity: "critical" | "high" | "medium" | "low" | string;
  line: number;
  category: string;
  description: string;
  suggestion: string;
};

type AnalyzerMetrics = {
  complexity: string;
  readability: string;
  test_coverage_estimate: string;
};

type AnalyzerResponse = {
  summary: string;
  issues: AnalyzerIssue[];
  suggestions: string[];
  metrics: AnalyzerMetrics;
};

const API_URL = "https://lab02analyzer-production.up.railway.app/analyze";

const LANGUAGE_OPTIONS = [
  "python",
  "javascript",
  "typescript",
  "java",
  "go",
  "rust",
  "csharp",
  "php"
];

const SAMPLE_CODE = `def add(a,b):
    return a+b

def process(data):
    result[]
    for i in range(len(data)):
        if data[i]>0:
            result.append(data[i]*2)
    return result`;

const severityClassMap: Record<string, string> = {
  critical: "bg-rose-500/20 text-rose-200 border-rose-400/60",
  high: "bg-orange-500/20 text-orange-200 border-orange-400/60",
  medium: "bg-amber-500/20 text-amber-200 border-amber-400/60",
  low: "bg-sky-500/20 text-sky-200 border-sky-400/60"
};

export default function HomePage() {
  const [code, setCode] = useState(SAMPLE_CODE);
  const [language, setLanguage] = useState("python");
  const [analysis, setAnalysis] = useState<AnalyzerResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const issuesCount = useMemo(() => analysis?.issues.length ?? 0, [analysis]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setAnalysis(null);

    if (!code.trim()) {
      setError("Add source code before starting analysis.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          code: code.trim(),
          language
        })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "Failed to analyze code.");
      }

      const data = (await response.json()) as AnalyzerResponse;
      setAnalysis(data);
    } catch (submitError) {
      const message = submitError instanceof Error ? submitError.message : "Unexpected request error.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setAnalysis(null);
    setError(null);
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 lg:py-12">
      <section className="rounded-2xl border border-brand-400/30 bg-brand-900/65 p-6 shadow-2xl shadow-black/30 backdrop-blur-sm sm:p-8">
        <p className="text-xs uppercase tracking-[0.18em] text-brand-400">Lab 02</p>
        <h1 className="mt-2 text-3xl font-semibold text-white sm:text-4xl">Code Analyzer Agent</h1>
        <p className="mt-3 max-w-2xl text-sm text-[color:var(--ink-soft)] sm:text-base">
          Send your source code to the analyzer API and inspect the result in structured blocks: summary, issues,
          suggestions, and quality metrics.
        </p>
      </section>

      <section className="grid gap-6 lg:grid-cols-[minmax(0,1.2fr),minmax(0,1fr)]">
        <form onSubmit={handleSubmit} className="rounded-2xl border border-brand-500/35 bg-brand-800/55 p-5 shadow-xl shadow-black/20 sm:p-6">
          <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
            <div>
              <h2 className="text-xl font-semibold text-white">Source Input</h2>
              <p className="text-sm text-[color:var(--ink-soft)]">Paste code and pick the language.</p>
            </div>
            <label className="text-sm font-medium text-brand-400" htmlFor="language">
              Language
            </label>
            <select
              id="language"
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
              className="rounded-md border border-brand-400/40 bg-brand-900/70 px-3 py-2 text-sm text-white outline-none transition focus:border-brand-400"
            >
              {LANGUAGE_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>

          <textarea
            value={code}
            onChange={(event) => setCode(event.target.value)}
            spellCheck={false}
            placeholder="Paste your code here"
            className="min-h-[300px] w-full rounded-xl border border-brand-500/35 bg-brand-900/75 px-4 py-3 text-sm leading-relaxed text-white outline-none transition focus:border-brand-400"
          />

          {error ? <p className="mt-3 rounded-md border border-rose-400/35 bg-rose-500/15 px-3 py-2 text-sm text-rose-200">{error}</p> : null}

          <div className="mt-4 flex flex-wrap gap-3">
            <button
              type="submit"
              disabled={isLoading}
              className="rounded-lg bg-brand-500 px-4 py-2 text-sm font-semibold text-brand-900 transition hover:bg-brand-400 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? "Analyzing..." : "Analyze Code"}
            </button>
            <button
              type="button"
              onClick={handleClear}
              className="rounded-lg border border-brand-400/45 bg-transparent px-4 py-2 text-sm font-semibold text-brand-400 transition hover:bg-brand-700/40"
            >
              Clear Results
            </button>
          </div>
        </form>

        <section className="rounded-2xl border border-brand-400/30 bg-brand-800/40 p-5 shadow-xl shadow-black/20 sm:p-6">
          <h2 className="text-xl font-semibold text-white">Analysis Snapshot</h2>
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
            <article className="rounded-xl border border-brand-500/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-400">Issues</p>
              <p className="mt-2 text-2xl font-semibold text-white">{issuesCount}</p>
            </article>
            <article className="rounded-xl border border-brand-500/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-400">Complexity</p>
              <p className="mt-2 text-lg font-semibold text-white">{analysis?.metrics.complexity ?? "-"}</p>
            </article>
            <article className="rounded-xl border border-brand-500/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-400">Readability</p>
              <p className="mt-2 text-lg font-semibold text-white">{analysis?.metrics.readability ?? "-"}</p>
            </article>
          </div>
          <article className="mt-4 rounded-xl border border-brand-500/30 bg-brand-900/55 p-4">
            <p className="text-xs uppercase tracking-wide text-brand-400">Coverage Estimate</p>
            <p className="mt-2 text-lg font-semibold text-white">{analysis?.metrics.test_coverage_estimate ?? "-"}</p>
          </article>
        </section>
      </section>

      {analysis ? (
        <section className="grid gap-6">
          <article className="rounded-2xl border border-brand-400/35 bg-brand-900/60 p-5 shadow-lg shadow-black/25 sm:p-6">
            <h2 className="text-xl font-semibold text-white">Summary</h2>
            <p className="mt-3 text-sm leading-relaxed text-[color:var(--ink-soft)] sm:text-base">{analysis.summary}</p>
          </article>

          <article className="rounded-2xl border border-brand-400/35 bg-brand-900/60 p-5 shadow-lg shadow-black/25 sm:p-6">
            <h2 className="text-xl font-semibold text-white">Issues</h2>
            <div className="mt-4 space-y-3">
              {analysis.issues.length === 0 ? (
                <p className="rounded-lg border border-brand-500/30 bg-brand-800/35 p-3 text-sm text-[color:var(--ink-soft)]">
                  No issues reported by the analyzer.
                </p>
              ) : (
                analysis.issues.map((issue, index) => (
                  <article key={`${issue.line}-${issue.category}-${index}`} className="rounded-xl border border-brand-500/30 bg-brand-800/35 p-4">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`rounded-full border px-2 py-1 text-xs font-semibold uppercase tracking-wide ${severityClassMap[issue.severity] ?? "bg-slate-500/20 text-slate-200 border-slate-300/60"}`}>
                        {issue.severity}
                      </span>
                      <span className="text-xs font-medium uppercase tracking-wide text-brand-400">line {issue.line}</span>
                      <span className="text-xs text-[color:var(--ink-soft)]">{issue.category}</span>
                    </div>
                    <p className="mt-3 text-sm text-white">{issue.description}</p>
                    <p className="mt-2 text-sm text-[color:var(--ink-soft)]">
                      <strong className="text-brand-400">Suggestion:</strong> {issue.suggestion}
                    </p>
                  </article>
                ))
              )}
            </div>
          </article>

          <article className="rounded-2xl border border-brand-400/35 bg-brand-900/60 p-5 shadow-lg shadow-black/25 sm:p-6">
            <h2 className="text-xl font-semibold text-white">Suggestions</h2>
            <ul className="mt-4 space-y-3">
              {analysis.suggestions.map((suggestion, index) => (
                <li key={`${suggestion.slice(0, 30)}-${index}`} className="rounded-xl border border-brand-500/30 bg-brand-800/35 p-4 text-sm text-[color:var(--ink-soft)]">
                  <span className="mr-2 inline-flex h-6 w-6 items-center justify-center rounded-full bg-brand-500/20 text-xs font-semibold text-brand-400">
                    {index + 1}
                  </span>
                  {suggestion}
                </li>
              ))}
            </ul>
          </article>
        </section>
      ) : (
        <section className="rounded-2xl border border-dashed border-brand-500/35 bg-brand-900/35 p-8 text-center">
          <p className="text-sm text-[color:var(--ink-soft)]">Submit code to visualize analysis blocks here.</p>
        </section>
      )}
    </main>
  );
}
