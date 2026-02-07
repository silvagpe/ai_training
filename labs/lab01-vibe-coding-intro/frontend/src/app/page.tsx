"use client";

import { useState } from "react";

type ShortenResponse = {
  short_code: string;
  short_url: string;
};

export default function HomePage() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<ShortenResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setResult(null);
    setCopied(false);

    if (!url.trim()) {
      setError("Please enter a URL before submitting.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("/api/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url.trim() })
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || "Failed to shorten URL");
      }

      const data = (await response.json()) as ShortenResponse;
      setResult(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unexpected error";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!result) {
      return;
    }
    await navigator.clipboard.writeText(result.short_url);
    setCopied(true);
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-6 py-12">
      <div className="w-full max-w-xl space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl">
        <header className="space-y-2">
          <h1 className="text-3xl font-semibold">URL Shortener</h1>
          <p className="text-sm text-slate-300">
            Paste your URL and get a short link in seconds.
          </p>
        </header>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-200" htmlFor="url">
              URL
            </label>
            <input
              id="url"
              name="url"
              type="url"
              placeholder="https://example.com"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none focus:border-indigo-500"
            />
          </div>

          {error ? (
            <p className="text-sm text-rose-400">{error}</p>
          ) : null}

          <button
            type="submit"
            disabled={isLoading}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isLoading ? "Shortening..." : "Shorten"}
          </button>
        </form>

        {result ? (
          <section className="space-y-3 rounded-lg border border-slate-800 bg-slate-950 px-4 py-3">
            <div className="space-y-1">
              <p className="text-xs uppercase text-slate-400">Short link</p>
              <a
                className="break-all text-sm text-indigo-300 hover:text-indigo-200"
                href={result.short_url}
                target="_blank"
                rel="noreferrer"
              >
                {result.short_url}
              </a>
            </div>
            <button
              type="button"
              onClick={handleCopy}
              className="inline-flex items-center gap-2 rounded-md border border-slate-700 px-3 py-2 text-xs font-semibold text-slate-200 transition hover:border-indigo-400 hover:text-indigo-200"
            >
              {copied ? "Copied" : "Copy"}
            </button>
          </section>
        ) : null}
      </div>
    </main>
  );
}
