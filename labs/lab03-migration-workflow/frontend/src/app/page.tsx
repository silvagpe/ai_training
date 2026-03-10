"use client";

import { ChangeEvent, FormEvent, useMemo, useState } from "react";

type FileEntry = {
  id: string;
  filename: string;
  content: string;
};

type PlanStep = {
  id: number;
  description: string;
  status: string;
};

type ValidationIssue = {
  line?: number;
  issue: string;
  suggestion?: string;
};

type FileValidation = {
  file: string;
  valid: boolean;
  issues: ValidationIssue[];
};

type Verification = {
  files_migrated?: number;
  steps_completed?: number;
  issues?: string[];
  validations?: FileValidation[];
};

type MigrationResponse = {
  success?: boolean;
  migrated_files?: Record<string, string>;
  plan_executed?: PlanStep[];
  verification?: Verification;
  errors?: string[];
  detail?: string;
};

const MAX_FILES = 2;

const frameworkOptions = [
  "express",
  "fastapi",
  "flask",
  "nestjs",
  "django",
  "spring",
  "laravel"
];

const createFileEntry = (): FileEntry => ({
  id: crypto.randomUUID(),
  filename: "",
  content: ""
});

const defaultFiles: FileEntry[] = [createFileEntry()];

export default function HomePage() {
  const [sourceFramework, setSourceFramework] = useState("express");
  const [targetFramework, setTargetFramework] = useState("fastapi");
  const [files, setFiles] = useState<FileEntry[]>(defaultFiles);
  const [result, setResult] = useState<MigrationResponse | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const canAddMoreFiles = files.length < MAX_FILES;

  const migratedFiles = useMemo(() => Object.entries(result?.migrated_files ?? {}), [result]);
  const planSteps = result?.plan_executed ?? [];
  const validationItems = result?.verification?.validations ?? [];
  const backendErrors = result?.errors ?? [];

  const updateFileEntry = (id: string, patch: Partial<FileEntry>) => {
    setFiles((current) => current.map((entry) => (entry.id === id ? { ...entry, ...patch } : entry)));
  };

  const addFileEntry = () => {
    if (!canAddMoreFiles) {
      setFormError("You can only submit up to two files.");
      return;
    }

    setFormError(null);
    setFiles((current) => [...current, createFileEntry()]);
  };

  const removeFileEntry = (id: string) => {
    setFiles((current) => {
      const next = current.filter((entry) => entry.id !== id);
      return next.length > 0 ? next : [createFileEntry()];
    });
  };

  const handleUpload = async (event: ChangeEvent<HTMLInputElement>, fileId: string) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    try {
      const content = await selectedFile.text();
      updateFileEntry(fileId, {
        filename: selectedFile.name,
        content
      });
      setFormError(null);
    } catch {
      setFormError("Failed to read the selected file.");
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    setResult(null);

    const sanitizedFiles = files
      .map((entry) => ({
        filename: entry.filename.trim(),
        content: entry.content
      }))
      .filter((entry) => entry.filename.length > 0 || entry.content.trim().length > 0);

    if (sanitizedFiles.length === 0) {
      setFormError("Add at least one file before submitting.");
      return;
    }

    const missingData = sanitizedFiles.some((entry) => !entry.filename || !entry.content.trim());
    if (missingData) {
      setFormError("Each file must include both a file name and file content.");
      return;
    }

    const payloadFiles = sanitizedFiles.reduce<Record<string, string>>((accumulator, entry) => {
      accumulator[entry.filename] = entry.content;
      return accumulator;
    }, {});

    setIsSubmitting(true);
    try {
      const response = await fetch("/api/migrate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          source_framework: sourceFramework,
          target_framework: targetFramework,
          files: payloadFiles
        })
      });

      const text = await response.text();
      const parsed = text ? (JSON.parse(text) as MigrationResponse) : {};

      if (!response.ok) {
        const errorMessage = parsed.detail || parsed.errors?.join(" ") || "Migration request failed.";
        throw new Error(errorMessage);
      }

      setResult(parsed);
    } catch (submitError) {
      const message = submitError instanceof Error ? submitError.message : "Unexpected migration error.";
      setFormError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 lg:py-12">
      <section className="rounded-2xl border border-brand-accent/30 bg-brand-900/70 p-6 shadow-2xl shadow-black/30 backdrop-blur-sm sm:p-8">
        <p className="text-xs uppercase tracking-[0.2em] text-brand-accent">Lab 03</p>
        <h1 className="mt-2 text-3xl font-semibold text-white sm:text-4xl">Migration Workflow Frontend</h1>
        <p className="mt-3 max-w-3xl text-sm text-[color:var(--ink-soft)] sm:text-base">
          Submit up to two source files and receive migrated output, execution steps, and verification details from the migration API.
        </p>
      </section>

      <section className="grid gap-6 lg:grid-cols-[minmax(0,1.15fr),minmax(0,1fr)]">
        <form onSubmit={handleSubmit} className="rounded-2xl border border-brand-500/35 bg-brand-700/50 p-5 shadow-xl shadow-black/20 sm:p-6">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="space-y-2 text-sm font-medium text-white">
              Source framework
              <select
                value={sourceFramework}
                onChange={(event) => setSourceFramework(event.target.value)}
                className="w-full rounded-lg border border-brand-accent/40 bg-brand-950/70 px-3 py-2 text-sm text-white outline-none transition focus:border-brand-accent"
              >
                {frameworkOptions.map((framework) => (
                  <option key={`source-${framework}`} value={framework}>
                    {framework}
                  </option>
                ))}
              </select>
            </label>

            <label className="space-y-2 text-sm font-medium text-white">
              Target framework
              <select
                value={targetFramework}
                onChange={(event) => setTargetFramework(event.target.value)}
                className="w-full rounded-lg border border-brand-accent/40 bg-brand-950/70 px-3 py-2 text-sm text-white outline-none transition focus:border-brand-accent"
              >
                {frameworkOptions.map((framework) => (
                  <option key={`target-${framework}`} value={framework}>
                    {framework}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="mt-5 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="text-lg font-semibold text-white">Source files</h2>
              <button
                type="button"
                onClick={addFileEntry}
                disabled={!canAddMoreFiles}
                className="rounded-lg border border-brand-accent/50 bg-brand-accent/15 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-brand-accent transition hover:bg-brand-accent/25 disabled:cursor-not-allowed disabled:opacity-55"
              >
                Add file
              </button>
            </div>

            {files.map((entry, index) => (
              <article key={entry.id} className="rounded-xl border border-brand-500/35 bg-brand-900/60 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-white">File {index + 1}</p>
                  <button
                    type="button"
                    onClick={() => removeFileEntry(entry.id)}
                    className="rounded-md border border-rose-300/40 px-2 py-1 text-xs font-medium text-rose-200 transition hover:bg-rose-500/15"
                  >
                    Remove
                  </button>
                </div>

                <label className="mt-3 block text-xs font-medium uppercase tracking-wide text-brand-accent" htmlFor={`filename-${entry.id}`}>
                  File name
                </label>
                <input
                  id={`filename-${entry.id}`}
                  value={entry.filename}
                  onChange={(event) => updateFileEntry(entry.id, { filename: event.target.value })}
                  placeholder="routes/users.js"
                  className="mt-1 w-full rounded-lg border border-brand-accent/35 bg-brand-950/70 px-3 py-2 text-sm text-white outline-none transition focus:border-brand-accent"
                />

                <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
                  <label className="text-xs font-medium uppercase tracking-wide text-brand-accent" htmlFor={`upload-${entry.id}`}>
                    Upload local file
                  </label>
                  <input
                    id={`upload-${entry.id}`}
                    type="file"
                    onChange={(event) => {
                      void handleUpload(event, entry.id);
                    }}
                    className="max-w-full text-xs text-[color:var(--ink-soft)] file:mr-3 file:rounded-md file:border-0 file:bg-brand-600 file:px-2 file:py-1.5 file:text-xs file:font-semibold file:text-white hover:file:bg-brand-500"
                  />
                </div>

                <label className="mt-3 block text-xs font-medium uppercase tracking-wide text-brand-accent" htmlFor={`content-${entry.id}`}>
                  File content
                </label>
                <textarea
                  id={`content-${entry.id}`}
                  value={entry.content}
                  onChange={(event) => updateFileEntry(entry.id, { content: event.target.value })}
                  spellCheck={false}
                  placeholder="Paste source code here"
                  className="mt-1 min-h-[180px] w-full rounded-lg border border-brand-accent/35 bg-brand-950/70 px-3 py-2 text-sm text-white outline-none transition focus:border-brand-accent"
                />
              </article>
            ))}
          </div>

          {formError ? (
            <p className="mt-4 rounded-lg border border-rose-300/45 bg-rose-500/15 px-3 py-2 text-sm text-rose-200">{formError}</p>
          ) : null}

          <div className="mt-5 flex gap-3">
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-lg bg-brand-accent px-4 py-2 text-sm font-semibold text-brand-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-65"
            >
              {isSubmitting ? "Migrating..." : "Run migration"}
            </button>
            <button
              type="button"
              onClick={() => {
                setResult(null);
                setFormError(null);
              }}
              className="rounded-lg border border-brand-accent/45 px-4 py-2 text-sm font-semibold text-brand-accent transition hover:bg-brand-accent/10"
            >
              Clear output
            </button>
          </div>
        </form>

        <section className="rounded-2xl border border-brand-accent/25 bg-brand-700/35 p-5 shadow-xl shadow-black/20 sm:p-6">
          <h2 className="text-xl font-semibold text-white">Submission overview</h2>
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <article className="rounded-xl border border-brand-accent/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-accent">Files in request</p>
              <p className="mt-2 text-2xl font-semibold text-white">{files.filter((entry) => entry.filename || entry.content).length}</p>
            </article>
            <article className="rounded-xl border border-brand-accent/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-accent">Status</p>
              <p className="mt-2 text-lg font-semibold text-white">{isSubmitting ? "Processing" : result ? "Completed" : "Idle"}</p>
            </article>
            <article className="rounded-xl border border-brand-accent/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-accent">Migrated files</p>
              <p className="mt-2 text-lg font-semibold text-white">{migratedFiles.length || "-"}</p>
            </article>
            <article className="rounded-xl border border-brand-accent/30 bg-brand-900/55 p-4">
              <p className="text-xs uppercase tracking-wide text-brand-accent">Plan steps</p>
              <p className="mt-2 text-lg font-semibold text-white">{planSteps.length || "-"}</p>
            </article>
          </div>
        </section>
      </section>

      {result ? (
        <section className="space-y-5">
          <article className="rounded-2xl border border-brand-accent/30 bg-brand-900/65 p-5 shadow-lg shadow-black/25 sm:p-6">
            <h2 className="text-xl font-semibold text-white">Migrated files</h2>
            {migratedFiles.length === 0 ? (
              <p className="mt-3 text-sm text-[color:var(--ink-soft)]">No migrated files were returned.</p>
            ) : (
              <div className="mt-4 space-y-4">
                {migratedFiles.map(([filename, content]) => (
                  <article key={filename} className="rounded-xl border border-brand-accent/25 bg-brand-950/70 p-4">
                    <h3 className="text-sm font-semibold text-brand-accent">{filename}</h3>
                    <pre className="mt-3 overflow-x-auto rounded-lg border border-brand-500/35 bg-[#000c2a] p-3 text-xs leading-relaxed text-[color:var(--ink-strong)]">
                      <code>{content}</code>
                    </pre>
                  </article>
                ))}
              </div>
            )}
          </article>

          <article className="rounded-2xl border border-brand-accent/30 bg-brand-900/65 p-5 shadow-lg shadow-black/25 sm:p-6">
            <h2 className="text-xl font-semibold text-white">Executed plan</h2>
            {planSteps.length === 0 ? (
              <p className="mt-3 text-sm text-[color:var(--ink-soft)]">No execution plan was returned.</p>
            ) : (
              <div className="mt-4 space-y-3">
                {planSteps.map((step) => (
                  <article key={step.id} className="rounded-xl border border-brand-500/30 bg-brand-700/35 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-brand-accent">Step {step.id}</p>
                    <p className="mt-2 text-sm text-white">{step.description}</p>
                    <p className="mt-2 inline-flex rounded-full border border-brand-accent/40 bg-brand-accent/15 px-2 py-1 text-xs font-semibold uppercase text-brand-accent">
                      {step.status}
                    </p>
                  </article>
                ))}
              </div>
            )}
          </article>

          <article className="rounded-2xl border border-brand-accent/30 bg-brand-900/65 p-5 shadow-lg shadow-black/25 sm:p-6">
            <h2 className="text-xl font-semibold text-white">Verification</h2>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <article className="rounded-xl border border-brand-500/30 bg-brand-950/60 p-4">
                <p className="text-xs uppercase tracking-wide text-brand-accent">Files migrated</p>
                <p className="mt-2 text-2xl font-semibold text-white">{result.verification?.files_migrated ?? "-"}</p>
              </article>
              <article className="rounded-xl border border-brand-500/30 bg-brand-950/60 p-4">
                <p className="text-xs uppercase tracking-wide text-brand-accent">Steps completed</p>
                <p className="mt-2 text-2xl font-semibold text-white">{result.verification?.steps_completed ?? "-"}</p>
              </article>
              <article className="rounded-xl border border-brand-500/30 bg-brand-950/60 p-4">
                <p className="text-xs uppercase tracking-wide text-brand-accent">Success</p>
                <p className="mt-2 text-2xl font-semibold text-white">{String(Boolean(result.success))}</p>
              </article>
            </div>

            {validationItems.length > 0 ? (
              <div className="mt-4 space-y-3">
                {validationItems.map((validation, index) => (
                  <article key={`${validation.file}-${index}`} className="rounded-xl border border-brand-500/30 bg-brand-700/35 p-4">
                    <p className="text-sm font-semibold text-brand-accent">{validation.file}</p>
                    <p className="mt-1 text-xs uppercase tracking-wide text-[color:var(--ink-soft)]">
                      valid: {String(validation.valid)}
                    </p>
                    {validation.issues.length > 0 ? (
                      <ul className="mt-2 space-y-2">
                        {validation.issues.map((issue, issueIndex) => (
                          <li key={`${validation.file}-issue-${issueIndex}`} className="rounded-lg border border-brand-accent/25 bg-brand-900/45 p-3 text-sm text-[color:var(--ink-soft)]">
                            <p className="font-medium text-white">{issue.issue}</p>
                            {typeof issue.line === "number" ? <p className="mt-1 text-xs text-brand-accent">Line: {issue.line}</p> : null}
                            {issue.suggestion ? <p className="mt-1 text-xs">Suggestion: {issue.suggestion}</p> : null}
                          </li>
                        ))}
                      </ul>
                    ) : null}
                  </article>
                ))}
              </div>
            ) : null}
          </article>

          {backendErrors.length > 0 ? (
            <article className="rounded-2xl border border-rose-300/40 bg-rose-500/10 p-5 shadow-lg shadow-black/25 sm:p-6">
              <h2 className="text-xl font-semibold text-rose-100">API errors</h2>
              <ul className="mt-3 space-y-2">
                {backendErrors.map((error, index) => (
                  <li key={`${error}-${index}`} className="rounded-lg border border-rose-300/25 bg-rose-500/10 px-3 py-2 text-sm text-rose-100">
                    {error}
                  </li>
                ))}
              </ul>
            </article>
          ) : null}
        </section>
      ) : (
        <section className="rounded-2xl border border-dashed border-brand-accent/35 bg-brand-900/45 p-8 text-center">
          <p className="text-sm text-[color:var(--ink-soft)]">Run a migration to display output blocks here.</p>
        </section>
      )}
    </main>
  );
}
