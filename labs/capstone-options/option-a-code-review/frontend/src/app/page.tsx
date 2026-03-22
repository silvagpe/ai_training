"use client";

import { ChangeEvent, FormEvent, useMemo, useState } from "react";

type AnalyzerIssue = {
  severity: "critical" | "high" | "medium" | "low" | string;
  line: number | null;
  category: string;
  description: string;
  suggestion: string;
};

type AnalyzerMetrics = {
  overall_score: number;
  complexity: string;
  maintainability: string;
};

type AnalyzerResponse = {
  summary: string;
  issues: AnalyzerIssue[];
  suggestions: string[];
  metrics: AnalyzerMetrics;
};

type BatchResultItem = {
  path: string;
  language: string;
  result: AnalyzerResponse;
};

type BatchResponse = {
  summary: string;
  results: BatchResultItem[];
  metrics: {
    files_reviewed: number;
    total_issues: number;
  };
};

type TabMode = "simple" | "batch";

const API_BASE_URL = "https://codereview-production-b0b5.up.railway.app";
const REVIEW_URL = `${API_BASE_URL}/review`;
const REVIEW_BATCH_URL = `${API_BASE_URL}/review/batch`;

const LANGUAGE_OPTIONS = [
  "python",
  "javascript",
  "typescript",
  "java",
  "go",
  "rust"
];

const FOCUS_OPTIONS = ["bug", "security", "performance", "style", "maintainability"];

const SAMPLE_CODE = `def add(a,b):
    return a+b

def process(data):
    result[]
    for i in range(len(data)):
        if data[i]>0:
            result.append(data[i]*2)
    return result`;

const severityClassMap: Record<string, string> = {
  critical: "bg-rose-100 text-rose-700 border-rose-200",
  high: "bg-orange-100 text-orange-700 border-orange-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  low: "bg-sky-100 text-sky-700 border-sky-200"
};

const extensionLanguageMap: Record<string, string> = {
  py: "python",
  js: "javascript",
  jsx: "javascript",
  ts: "typescript",
  tsx: "typescript",
  java: "java",
  go: "go",
  rs: "rust"
};

function inferLanguageFromFilename(name: string): string {
  const extension = name.split(".").pop()?.toLowerCase() ?? "";
  return extensionLanguageMap[extension] ?? "python";
}

function parseApiError(rawText: string): string {
  try {
    const data = JSON.parse(rawText) as { error?: string; detail?: string };
    return data.error || data.detail || rawText;
  } catch {
    return rawText || "Request failed.";
  }
}

function ResultBlock({ title, result }: { title: string; result: AnalyzerResponse }) {
  return (
    <article className="rounded-2xl border border-brand-200 bg-white p-5 shadow-sm sm:p-6">
      <h3 className="text-lg font-semibold text-slate-900">{title}</h3>

      <section className="mt-4 rounded-xl border border-brand-100 bg-brand-50 p-4">
        <p className="text-xs uppercase tracking-wide text-brand-700">Summary</p>
        <p className="mt-2 text-sm text-slate-700">{result.summary}</p>
      </section>

      <section className="mt-4 rounded-xl border border-brand-100 bg-white p-4">
        <p className="text-xs uppercase tracking-wide text-brand-700">Issues</p>
        {result.issues.length === 0 ? (
          <p className="mt-2 text-sm text-slate-600">No issues reported.</p>
        ) : (
          <div className="mt-3 space-y-3">
            {result.issues.map((issue, index) => (
              <article key={`${issue.category}-${issue.line}-${index}`} className="rounded-xl border border-slate-200 bg-slate-50 p-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className={`rounded-full border px-2 py-1 text-xs font-semibold uppercase ${severityClassMap[issue.severity] ?? "bg-slate-100 text-slate-700 border-slate-200"}`}>
                    {issue.severity}
                  </span>
                  <span className="text-xs text-slate-500">{issue.category}</span>
                  <span className="text-xs text-slate-500">line {issue.line ?? "n/a"}</span>
                </div>
                <p className="mt-2 text-sm text-slate-800">{issue.description}</p>
                <p className="mt-1 text-sm text-slate-700">
                  <strong>Suggestion:</strong> {issue.suggestion}
                </p>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="mt-4 rounded-xl border border-brand-100 bg-white p-4">
        <p className="text-xs uppercase tracking-wide text-brand-700">Suggestions</p>
        {result.suggestions.length === 0 ? (
          <p className="mt-2 text-sm text-slate-600">No additional suggestions.</p>
        ) : (
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-700">
            {result.suggestions.map((item, index) => (
              <li key={`${item.slice(0, 20)}-${index}`}>{item}</li>
            ))}
          </ul>
        )}
      </section>

      <section className="mt-4 grid gap-3 sm:grid-cols-3">
        <article className="rounded-xl border border-brand-100 bg-brand-50 p-3">
          <p className="text-xs uppercase tracking-wide text-brand-700">Overall Score</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">{result.metrics.overall_score}</p>
        </article>
        <article className="rounded-xl border border-brand-100 bg-brand-50 p-3">
          <p className="text-xs uppercase tracking-wide text-brand-700">Complexity</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">{result.metrics.complexity}</p>
        </article>
        <article className="rounded-xl border border-brand-100 bg-brand-50 p-3">
          <p className="text-xs uppercase tracking-wide text-brand-700">Maintainability</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">{result.metrics.maintainability}</p>
        </article>
      </section>
    </article>
  );
}

export default function HomePage() {
  const [tab, setTab] = useState<TabMode>("simple");
  const [code, setCode] = useState(SAMPLE_CODE);
  const [language, setLanguage] = useState("python");
  const [focus, setFocus] = useState<string[]>([]);
  const [analysis, setAnalysis] = useState<AnalyzerResponse | null>(null);
  const [batchAnalysis, setBatchAnalysis] = useState<BatchResponse | null>(null);
  const [batchFiles, setBatchFiles] = useState<File[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const issuesCount = useMemo(() => {
    if (tab === "simple") {
      return analysis?.issues.length ?? 0;
    }
    return batchAnalysis?.metrics.total_issues ?? 0;
  }, [analysis, batchAnalysis, tab]);

  const batchFilesReviewed = batchAnalysis?.metrics.files_reviewed ?? 0;

  const toggleFocus = (value: string) => {
    setFocus((previous) =>
      previous.includes(value) ? previous.filter((item) => item !== value) : [...previous, value]
    );
  };

  const handleSimpleFileUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const text = await file.text();
    setCode(text);
    setLanguage(inferLanguageFromFilename(file.name));
  };

  const handleBatchFilesUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const selected = Array.from(event.target.files ?? []);
    if (selected.length > 2) {
      setError("Batch review accepts up to 2 files.");
      setBatchFiles([]);
      return;
    }
    setError(null);
    setBatchFiles(selected);
  };

  const handleSimpleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setAnalysis(null);
    setBatchAnalysis(null);

    if (!code.trim()) {
      setError("Add source code before starting analysis.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(REVIEW_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Client-Id": "code-review-ui"
        },
        body: JSON.stringify({
          code: code.trim(),
          language,
          focus
        })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(parseApiError(text));
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

  const handleBatchSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setAnalysis(null);
    setBatchAnalysis(null);

    if (batchFiles.length === 0) {
      setError("Select 1 or 2 files for batch review.");
      return;
    }

    if (batchFiles.length > 2) {
      setError("Batch review accepts up to 2 files.");
      return;
    }

    setIsLoading(true);
    try {
      const transformedFiles = await Promise.all(
        batchFiles.map(async (file) => {
          const content = await file.text();
          if (!content.trim()) {
            throw new Error(`File ${file.name} is empty.`);
          }

          if (content.length > 30000) {
            throw new Error(`File ${file.name} exceeds 30000 characters.`);
          }

          return {
            path: file.name,
            code: content,
            language: inferLanguageFromFilename(file.name)
          };
        })
      );

      const total = transformedFiles.reduce((sum, item) => sum + item.code.length, 0);
      if (total > 120000) {
        throw new Error("Batch payload exceeds 120000 total characters.");
      }

      const response = await fetch(REVIEW_BATCH_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Client-Id": "code-review-ui"
        },
        body: JSON.stringify({
          files: transformedFiles,
          focus
        })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(parseApiError(text));
      }

      const data = (await response.json()) as BatchResponse;
      setBatchAnalysis(data);
    } catch (submitError) {
      const message = submitError instanceof Error ? submitError.message : "Unexpected request error.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setAnalysis(null);
    setBatchAnalysis(null);
    setError(null);
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 lg:py-12">
      <section className="rounded-2xl border border-brand-200 bg-white p-6 shadow-sm sm:p-8">
        <p className="text-xs uppercase tracking-[0.18em] text-brand-700">Capstone Option A</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900 sm:text-4xl">AI Code Review UI</h1>
        <p className="mt-3 max-w-2xl text-sm text-slate-600 sm:text-base">
          Submit code to the new review API and inspect structured output blocks for summary, issues, suggestions,
          and metrics.
        </p>

        <div className="mt-5 inline-flex rounded-xl border border-brand-200 bg-brand-50 p-1">
          <button
            type="button"
            onClick={() => {
              setTab("simple");
              setError(null);
            }}
            className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
              tab === "simple" ? "bg-white text-brand-700 shadow-sm" : "text-slate-600"
            }`}
          >
            Simple Review
          </button>
          <button
            type="button"
            onClick={() => {
              setTab("batch");
              setError(null);
            }}
            className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
              tab === "batch" ? "bg-white text-brand-700 shadow-sm" : "text-slate-600"
            }`}
          >
            Batch Review
          </button>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[minmax(0,1.2fr),minmax(0,1fr)]">
        <form
          onSubmit={tab === "simple" ? handleSimpleSubmit : handleBatchSubmit}
          className="rounded-2xl border border-brand-200 bg-white p-5 shadow-sm sm:p-6"
        >
          <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
            <div>
              <h2 className="text-xl font-semibold text-slate-900">
                {tab === "simple" ? "Simple Review Input" : "Batch Review Input"}
              </h2>
              <p className="text-sm text-slate-600">
                {tab === "simple"
                  ? "Paste code or upload one file."
                  : "Select up to 2 files for a single batch request."}
              </p>
            </div>
            <label className="text-sm font-medium text-brand-400" htmlFor="language">
              Language
            </label>
            {tab === "simple" ? (
              <select
                id="language"
                value={language}
                onChange={(event) => setLanguage(event.target.value)}
                className="rounded-md border border-brand-200 bg-white px-3 py-2 text-sm text-slate-800 outline-none transition focus:border-brand-500"
              >
                {LANGUAGE_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            ) : (
              <span className="rounded-md border border-brand-200 bg-brand-50 px-3 py-2 text-sm text-slate-600">
                Language inferred from file extension
              </span>
            )}
          </div>

          <fieldset className="mb-4 rounded-xl border border-brand-200 bg-brand-50 p-4">
            <legend className="px-1 text-sm font-semibold text-brand-700">Focus</legend>
            <div className="mt-2 flex flex-wrap gap-2">
              {FOCUS_OPTIONS.map((item) => (
                <label key={item} className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-white px-3 py-1 text-sm text-slate-700">
                  <input
                    type="checkbox"
                    checked={focus.includes(item)}
                    onChange={() => toggleFocus(item)}
                    className="h-4 w-4 accent-brand-600"
                  />
                  {item}
                </label>
              ))}
            </div>
          </fieldset>

          {tab === "simple" ? (
            <>
              <label className="mb-2 block text-sm font-medium text-slate-700" htmlFor="simple-file">
                Upload file (optional)
              </label>
              <input
                id="simple-file"
                type="file"
                onChange={handleSimpleFileUpload}
                className="mb-4 block w-full text-sm text-slate-600"
              />
              <textarea
                value={code}
                onChange={(event) => setCode(event.target.value)}
                spellCheck={false}
                placeholder="Paste your code here"
                className="min-h-[280px] w-full rounded-xl border border-brand-200 bg-white px-4 py-3 text-sm leading-relaxed text-slate-800 outline-none transition focus:border-brand-500"
              />
            </>
          ) : (
            <>
              <label className="mb-2 block text-sm font-medium text-slate-700" htmlFor="batch-files">
                Select up to 2 files
              </label>
              <input
                id="batch-files"
                type="file"
                multiple
                onChange={handleBatchFilesUpload}
                className="mb-4 block w-full text-sm text-slate-600"
              />
              <div className="rounded-xl border border-brand-200 bg-brand-50 p-3">
                {batchFiles.length === 0 ? (
                  <p className="text-sm text-slate-600">No files selected.</p>
                ) : (
                  <ul className="space-y-2 text-sm text-slate-700">
                    {batchFiles.map((file) => (
                      <li key={file.name} className="rounded-lg border border-brand-100 bg-white p-2">
                        {file.name} ({inferLanguageFromFilename(file.name)})
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </>
          )}

          {error ? <p className="mt-3 rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p> : null}

          <div className="mt-4 flex flex-wrap gap-3">
            <button
              type="submit"
              disabled={isLoading || (tab === "simple" ? !code.trim() : batchFiles.length === 0 || batchFiles.length > 2)}
              className="rounded-lg bg-green-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? "Analyzing..." : tab === "simple" ? "Analyze Code" : "Analyze Batch"}
            </button>
            <button
              type="button"
              onClick={handleClear}
              className="rounded-lg border border-brand-300 bg-transparent px-4 py-2 text-sm font-semibold text-brand-700 transition hover:bg-brand-50"
            >
              Clear Results
            </button>
          </div>
        </form>

        <section className="rounded-2xl border border-brand-200 bg-white p-5 shadow-sm sm:p-6">
          <h2 className="text-xl font-semibold text-slate-900">Analysis Snapshot</h2>
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
            <article className="rounded-xl border border-brand-100 bg-brand-50 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-700">Issues</p>
              <p className="mt-2 text-2xl font-semibold text-slate-900">{issuesCount}</p>
            </article>
            <article className="rounded-xl border border-brand-100 bg-brand-50 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-700">Complexity</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">
                {tab === "simple" ? analysis?.metrics.complexity ?? "-" : "-"}
              </p>
            </article>
            <article className="rounded-xl border border-brand-100 bg-brand-50 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-700">Files Reviewed</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{tab === "batch" ? batchFilesReviewed : "-"}</p>
            </article>
          </div>
          <article className="mt-4 rounded-xl border border-brand-100 bg-brand-50 p-4">
            <p className="text-xs uppercase tracking-wide text-brand-700">Maintainability</p>
            <p className="mt-2 text-lg font-semibold text-slate-900">
              {tab === "simple" ? analysis?.metrics.maintainability ?? "-" : "-"}
            </p>
          </article>
        </section>
      </section>

      {tab === "simple" && analysis ? (
        <section className="grid gap-6">
          <h2 className="text-xl font-semibold text-slate-900">Example result</h2>
          <ResultBlock title="Simple Review Result" result={analysis} />
        </section>
      ) : null}

      {tab === "batch" && batchAnalysis ? (
        <section className="grid gap-6">
          <h2 className="text-xl font-semibold text-slate-900">Example result</h2>
          <article className="rounded-2xl border border-brand-200 bg-white p-5 shadow-sm sm:p-6">
            <h3 className="text-lg font-semibold text-slate-900">Batch Summary</h3>
            <p className="mt-2 text-sm text-slate-700">{batchAnalysis.summary}</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <article className="rounded-xl border border-brand-100 bg-brand-50 p-3">
                <p className="text-xs uppercase tracking-wide text-brand-700">Files Reviewed</p>
                <p className="mt-1 text-lg font-semibold text-slate-900">{batchAnalysis.metrics.files_reviewed}</p>
              </article>
              <article className="rounded-xl border border-brand-100 bg-brand-50 p-3">
                <p className="text-xs uppercase tracking-wide text-brand-700">Total Issues</p>
                <p className="mt-1 text-lg font-semibold text-slate-900">{batchAnalysis.metrics.total_issues}</p>
              </article>
            </div>
          </article>
          {batchAnalysis.results.map((item) => (
            <ResultBlock key={`${item.path}-${item.language}`} title={`${item.path} (${item.language})`} result={item.result} />
          ))}
        </section>
      ) : (
        <section className="rounded-2xl border border-dashed border-brand-200 bg-white p-8 text-center">
          <p className="text-sm text-slate-600">Submit input to visualize analysis blocks here.</p>
        </section>
      )}
    </main>
  );
}
