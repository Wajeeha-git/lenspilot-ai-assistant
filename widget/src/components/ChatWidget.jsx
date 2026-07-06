import { useState, useRef, useEffect } from "react";
import { ChatService } from "../services/chatService.js";
import { ASSISTANT_IDENTITY, SUGGESTED_QUESTIONS } from "../mock/knowledgeBase.js";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", text: ASSISTANT_IDENTITY.greeting, sources: [] },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, loading, error]);

  // `text` lets suggested-question chips reuse this function; free-typed
  // input from the form always falls through to `input` state.
  const send = async (text) => {
    const trimmed = (text ?? input).trim();
    if (!trimmed || loading) return;
    setMessages((m) => [...m, { role: "user", text: trimmed }]);
    setInput("");
    setLoading(true);
    setError(null);
    try {
      const res = await ChatService.sendMessage(trimmed);
      if (res.error) {
        setError(res.error);
      } else {
        setMessages((m) => [...m, { role: "assistant", text: res.reply, sources: res.sources || [] }]);
      }
    } catch (e) {
      setError("Couldn't reach the assistant. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const retry = () => {
    const lastUser = [...messages].reverse().find((m) => m.role === "user");
    if (lastUser) send(lastUser.text);
  };

  const sourceLabel = (source) => {
    if (!source) return "Source";
    if (typeof source === "string") return source;
    const title = source.document_title || source.category || "Source";
    const category = source.category ? ` ${source.category}` : "";
    return `${title}${category}`;
  };

  const sourceKey = (source, index) => {
    if (typeof source === "string") return `${source}-${index}`;
    return `${source.document_id || "doc"}-${source.category || "cat"}-${index}`;
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end font-body">
      {open && (
        <div
          className="mb-4 w-[92vw] max-w-sm sm:w-96 rounded-2xl bg-panel/90 border border-hair backdrop-blur-xl shadow-glow overflow-hidden flex flex-col animate-rise"
          style={{ height: "min(600px, 72vh)" }}
        >
          {/* header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-hair bg-panel/60 shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-full bg-white flex items-center justify-center shrink-0 overflow-hidden">
                <img src="/logo.png" alt="LensPilot logo" className="w-[78%] h-[78%] object-contain" />
              </div>
              <div>
                <p className="text-sm font-semibold text-white leading-tight">{ASSISTANT_IDENTITY.name}</p>
                <p className="text-[11px] text-teal-300 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-400 inline-block" /> Online
                </p>
              </div>
            </div>
            <button
              onClick={() => setOpen(false)}
              aria-label="Close chat"
              className="text-slate-400 hover:text-white transition-colors p-1"
            >
              ✕
            </button>
          </div>

          {/* messages */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"} animate-rise`}>
                <div
                  className={`max-w-[80%] rounded-2xl px-3.5 py-2.5 text-[13.5px] leading-relaxed ${
                    m.role === "user"
                      ? "bg-gradient-to-br from-iris to-iris2 text-white rounded-br-sm"
                      : "bg-panel2 text-slate-200 border border-hair rounded-bl-sm"
                  }`}
                >
                  <p className="m-0">{m.text}</p>
                  {m.sources && m.sources.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {m.sources.map((s, j) => (
                        <span
                          key={sourceKey(s, `${i}-${j}`)}
                          className="inline-flex items-center gap-1 text-[10.5px] px-2 py-0.5 rounded-full bg-black/25 border border-hair text-teal-300"
                        >
                          🏷 {sourceLabel(s)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-panel2 border border-hair rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-400 dot-1" />
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-400 dot-2" />
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-400 dot-3" />
                </div>
              </div>
            )}

            {error && (
              <div className="flex justify-start">
                <div className="bg-red-500/10 border border-red-500/30 text-red-300 rounded-2xl px-3.5 py-2.5 text-[13px] flex items-center justify-between gap-3 max-w-[85%]">
                  <span>{error}</span>
                  <button onClick={retry} className="text-red-200 underline underline-offset-2 shrink-0 hover:text-white">
                    Retry
                  </button>
                </div>
              </div>
            )}

            {messages.length === 1 && !loading && (
              <div className="flex flex-wrap gap-2 pt-1">
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => send(q)}
                    className="text-[12px] px-3 py-1.5 rounded-full border border-hair bg-panel2/70 text-slate-300 hover:text-white hover:border-iris/60 transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* input — free text, always available */}
          <div className="p-3 border-t border-hair bg-panel/60 shrink-0">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                send();
              }}
              className="flex items-center gap-2"
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 bg-panel2 border border-hair rounded-full px-4 py-2.5 text-[13.5px] text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-iris/50"
              />
              <button
                type="submit"
                disabled={!input.trim() || loading}
                aria-label="Send message"
                className="w-9 h-9 rounded-full bg-gradient-to-br from-iris to-iris2 flex items-center justify-center text-white disabled:opacity-40 transition-opacity shrink-0"
              >
                ➤
              </button>
            </form>
            <p className="text-center text-[10.5px] text-slate-500 mt-2">
              Powered by <span className="text-slate-300 font-medium">LensPilot</span>
            </p>
          </div>
        </div>
      )}

      {/* floating toggle button */}
      <button
        onClick={() => setOpen(!open)}
        aria-label={open ? "Close chat widget" : "Open chat widget"}
        className="relative w-14 h-14 rounded-full bg-gradient-to-br from-iris to-iris2 shadow-glow flex items-center justify-center text-white hover:scale-105 active:scale-95 transition-transform"
      >
        {open ? "✕" : "💬"}
        {!open && <span className="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-red-500 border-2 border-ink" />}
      </button>
    </div>
  );
}
