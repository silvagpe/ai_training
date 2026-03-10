"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { indexFiles, APIError } from "@/lib/api";
import { FileInput } from "@/lib/types";
import { Loader2, Upload, X, CheckCircle2, AlertCircle } from "lucide-react";

const MAX_FILE_SIZE = 100 * 1024; // 100KB

export default function IndexFilesPage() {
  const [files, setFiles] = useState<FileInput[]>([
    { id: "1", filename: "", content: "" },
    { id: "2", filename: "", content: "" },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string; details?: { indexed_chunks: number; files: string[] } } | null>(null);

  const handleFileUpload = (id: string, event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.size > MAX_FILE_SIZE) {
      setResult({
        success: false,
        message: `File "${file.name}" exceeds 100KB limit`,
      });
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      setFiles((prev) =>
        prev.map((f) =>
          f.id === id ? { ...f, filename: file.name, content } : f
        )
      );
    };
    reader.readAsText(file);
  };

  const handleFilenameChange = (id: string, filename: string) => {
    setFiles((prev) =>
      prev.map((f) => (f.id === id ? { ...f, filename } : f))
    );
  };

  const handleContentChange = (id: string, content: string) => {
    setFiles((prev) =>
      prev.map((f) => (f.id === id ? { ...f, content } : f))
    );
  };

  const handleClearFile = (id: string) => {
    setFiles((prev) =>
      prev.map((f) => (f.id === id ? { ...f, filename: "", content: "" } : f))
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);

    const validFiles = files.filter((f) => f.filename && f.content);

    if (validFiles.length === 0) {
      setResult({
        success: false,
        message: "Please add at least one file",
      });
      return;
    }

    setIsLoading(true);

    try {
      const fileMap: { [key: string]: string } = {};
      validFiles.forEach((f) => {
        fileMap[f.filename] = f.content;
      });

      const response = await indexFiles({ files: fileMap });
      setResult({
        success: true,
        message: "Files indexed successfully!",
        details: response,
      });
    } catch (error) {
      if (error instanceof APIError) {
        setResult({
          success: false,
          message: `Error: ${error.message}`,
        });
      } else {
        setResult({
          success: false,
          message: "An unexpected error occurred",
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearAll = () => {
    setFiles([
      { id: "1", filename: "", content: "" },
      { id: "2", filename: "", content: "" },
    ]);
    setResult(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-rag-dark mb-2">Index Source Code Files</h1>
        <p className="text-gray-600">
          Add up to 2 source code files to index them for querying. You can manually enter the content or upload files.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {files.map((file, index) => (
          <Card key={file.id}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg">File {index + 1}</CardTitle>
                  <CardDescription>
                    Enter filename and content manually or upload a file
                  </CardDescription>
                </div>
                {file.filename && (
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => handleClearFile(file.id)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor={`filename-${file.id}`}>Filename</Label>
                <Input
                  id={`filename-${file.id}`}
                  placeholder="e.g., auth.py"
                  value={file.filename}
                  onChange={(e) => handleFilenameChange(file.id, e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor={`content-${file.id}`}>File Content</Label>
                <Textarea
                  id={`content-${file.id}`}
                  placeholder="Paste your code here..."
                  value={file.content}
                  onChange={(e) => handleContentChange(file.id, e.target.value)}
                  rows={8}
                  className="font-mono text-sm"
                />
              </div>

              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-500">or</span>
                <Label
                  htmlFor={`upload-${file.id}`}
                  className="cursor-pointer"
                >
                  <div className="flex items-center gap-2 px-4 py-2 border border-input rounded-md hover:bg-accent hover:text-accent-foreground transition-colors">
                    <Upload className="h-4 w-4" />
                    <span className="text-sm">Upload File</span>
                  </div>
                  <input
                    id={`upload-${file.id}`}
                    type="file"
                    className="hidden"
                    onChange={(e) => handleFileUpload(file.id, e)}
                    accept=".py,.js,.ts,.tsx,.jsx,.java,.cpp,.c,.go,.rs,.rb,.php,.html,.css,.json,.yaml,.yml,.txt"
                  />
                </Label>
                <span className="text-xs text-gray-500">(Max 100KB)</span>
              </div>
            </CardContent>
          </Card>
        ))}

        <div className="flex gap-2">
          <Button
            type="submit"
            disabled={isLoading}
            className="bg-rag-cyan hover:bg-rag-cyan/90 text-white"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Indexing...
              </>
            ) : (
              "Index Files"
            )}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={handleClearAll}
            disabled={isLoading}
          >
            Clear All
          </Button>
        </div>
      </form>

      {result && (
        <Card className={result.success ? "border-green-500" : "border-red-500"}>
          <CardContent className="pt-6">
            <div className="flex items-start gap-3">
              {result.success ? (
                <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
              )}
              <div className="flex-1 space-y-2">
                <p className={result.success ? "text-green-900" : "text-red-900"}>
                  {result.message}
                </p>
                {result.details && (
                  <div className="space-y-1">
                    <p className="text-sm text-gray-600">
                      Indexed {result.details.indexed_chunks} chunks
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {result.details.files.map((file) => (
                        <Badge key={file} variant="secondary">
                          {file}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
