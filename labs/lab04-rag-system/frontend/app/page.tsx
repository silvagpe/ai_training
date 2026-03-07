"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { queryFiles, APIError } from "@/lib/api";
import { ChatMessage, Source } from "@/lib/types";
import { Loader2, Send, FileCode, Info, AlertCircle } from "lucide-react";
import Link from "next/link";

export default function QueryPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSources, setSelectedSources] = useState<Source[] | null>(null);
  const [selectedContext, setSelectedContext] = useState<string | null>(null);
  const [showSourcesDialog, setShowSourcesDialog] = useState(false);
  const [showContextDialog, setShowContextDialog] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "question",
      content: question.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setIsLoading(true);
    setError(null);

    try {
      const response = await queryFiles({ question: userMessage.content });
      
      const answerMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: "answer",
        content: response.answer,
        sources: response.sources,
        context: response.context_used,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, answerMessage]);
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleShowSources = (sources: Source[]) => {
    setSelectedSources(sources);
    setShowSourcesDialog(true);
  };

  const handleShowContext = (context: string) => {
    setSelectedContext(context);
    setShowContextDialog(true);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-rag-dark mb-2">Query Indexed Files</h1>
        <p className="text-gray-600">
          Ask questions about your indexed source code files.
        </p>
      </div>

      {messages.length === 0 && !isLoading && (
        <Card className="border-rag-cyan/30">
          <CardContent className="pt-6">
            <div className="text-center space-y-3">
              <AlertCircle className="h-12 w-12 text-rag-cyan mx-auto" />
              <h3 className="font-semibold text-lg">No Conversations Yet</h3>
              <p className="text-gray-600">
                Start by asking a question about your indexed files.
              </p>
              <p className="text-sm text-gray-500">
                Haven't indexed any files yet?{" "}
                <Link href="/index" className="text-rag-cyan hover:underline">
                  Go to Index Files
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4">
        {messages.map((message) => (
          <Card
            key={message.id}
            className={
              message.type === "question"
                ? "bg-rag-cyan/5 border-rag-cyan/30"
                : "bg-white"
            }
          >
            <CardContent className="pt-6">
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <Badge
                    variant={message.type === "question" ? "default" : "secondary"}
                    className={
                      message.type === "question"
                        ? "bg-rag-cyan hover:bg-rag-cyan"
                        : ""
                    }
                  >
                    {message.type === "question" ? "Q" : "A"}
                  </Badge>
                  <div className="flex-1">
                    <p className="text-sm text-gray-900 whitespace-pre-wrap">
                      {message.content}
                    </p>
                  </div>
                </div>

                {message.type === "answer" && message.sources && message.context && (
                  <div className="flex gap-2 ml-8">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleShowSources(message.sources!)}
                      className="text-xs"
                    >
                      <FileCode className="h-3 w-3 mr-1" />
                      View Sources ({message.sources.length})
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleShowContext(message.context!)}
                      className="text-xs"
                    >
                      <Info className="h-3 w-3 mr-1" />
                      View Context
                    </Button>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}

        {isLoading && (
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <Loader2 className="h-5 w-5 animate-spin text-rag-cyan" />
                <p className="text-gray-600">Searching for answer...</p>
              </div>
            </CardContent>
          </Card>
        )}

        {error && (
          <Card className="border-red-500">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                <div>
                  <p className="text-red-900 font-medium">Error</p>
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      <Card className="sticky bottom-4 shadow-lg">
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit} className="space-y-3">
            <Textarea
              placeholder="Ask a question about your indexed files..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              rows={3}
              disabled={isLoading}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <div className="flex justify-between items-center">
              <p className="text-xs text-gray-500">
                Press Enter to send, Shift+Enter for new line
              </p>
              <Button
                type="submit"
                disabled={!question.trim() || isLoading}
                className="bg-rag-cyan hover:bg-rag-cyan/90 text-white"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Send
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Sources Dialog */}
      <Dialog open={showSourcesDialog} onOpenChange={setShowSourcesDialog}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Sources</DialogTitle>
            <DialogDescription>
              Code sources used to generate this answer
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3 mt-4">
            {selectedSources?.map((source, index) => (
              <Card key={index}>
                <CardContent className="pt-4">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline">{source.file}</Badge>
                        <span className="text-sm text-gray-600">
                          Line {source.line}
                        </span>
                      </div>
                      {source.relevance > 0 && (
                        <Badge variant="secondary">
                          Relevance: {(source.relevance * 100).toFixed(0)}%
                        </Badge>
                      )}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">{source.type}:</span>{" "}
                      <code className="text-rag-cyan">{source.name}</code>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </DialogContent>
      </Dialog>

      {/* Context Dialog */}
      <Dialog open={showContextDialog} onOpenChange={setShowContextDialog}>
        <DialogContent className="!max-w-none w-[80git avw] max-h-[80vh] h-[95vh] overflow-hidden flex flex-col">
          <DialogHeader>
            <DialogTitle>Context Used</DialogTitle>
            <DialogDescription>
              Full code context used to generate the answer
            </DialogDescription>
          </DialogHeader>
          <div className="mt-4 flex-1 overflow-y-auto">
            <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono h-full whitespace-pre-wrap break-words">
              {selectedContext}
            </pre>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
