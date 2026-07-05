import ChatWidget from "./components/ChatWidget.jsx";

const FEATURES = [
  { icon: "⚡", title: "Instant Answers", desc: "Accurate responses within seconds." },
  { icon: "🛡", title: "Secure & Private", desc: "Your data is encrypted, never sold." },
  { icon: "⧉", title: "Easy to Integrate", desc: "One script tag, any website." },
  { icon: "✨", title: "Always Learning", desc: "Improves as your docs improve." },
];

const STEPS = [
  { n: 1, icon: "⧉", title: "Connect your docs", desc: "Point LensPilot at your product docs, FAQs, and policies." },
  { n: 2, icon: "💬", title: "It learns your content", desc: "LensPilot indexes everything and drafts response rules with you." },
  { n: 3, icon: "⚡", title: "Embed and go live", desc: "Drop in one script tag — the widget appears on your site." },
];

function LogoBadge({ className = "w-8 h-8" }) {
  return (
    <span className={`inline-flex items-center justify-center bg-white rounded-full overflow-hidden shrink-0 ${className}`}>
      <img src="/logo.png" alt="LensPilot logo" className="w-[78%] h-[78%] object-contain" />
    </span>
  );
}

export default function App() {
  return (
    <div className="min-h-screen flex flex-col text-slate-200 font-body">
      {/* Navbar */}
      <nav className="max-w-7xl mx-auto w-full flex items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2.5">
          <LogoBadge className="w-8 h-8" />
          <span className="font-display font-bold text-lg text-white tracking-tight">LensPilot</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-slate-300">
          {["Home", "Features", "How it works", "Pricing", "Docs"].map((l) => (
            <span key={l} className="hover:text-white transition-colors cursor-default">{l}</span>
          ))}
        </div>
        <button className="hidden sm:flex items-center gap-1.5 text-sm font-medium bg-panel2 border border-hair text-white px-4 py-2 rounded-full">
          Get Started →
        </button>
      </nav>

      {/* Hero */}
      <header className="max-w-7xl mx-auto w-full px-6 pt-10 pb-20 grid lg:grid-cols-2 gap-14 items-center">
        <div>
          <span className="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-full border border-hair bg-panel2 text-iris2 mb-6">
            ✦ AI-Powered Support
          </span>
          <h1 className="font-display font-extrabold text-white text-4xl sm:text-5xl lg:text-6xl leading-[1.05] tracking-tight">
            Smart answers,<br />
            <span className="bg-gradient-to-r from-iris to-iris2 bg-clip-text text-transparent">anytime, anywhere.</span>
          </h1>
          <p className="mt-6 text-slate-400 text-base sm:text-lg max-w-md leading-relaxed">
            Your AI assistant is ready to help. Get instant, source-backed answers right in your app or website.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <button className="flex items-center gap-2 font-medium text-white px-5 py-3 rounded-full bg-gradient-to-r from-iris to-iris2 shadow-glow hover:brightness-110 transition">
              Try the Demo →
            </button>
            <button className="flex items-center gap-2 font-medium text-slate-200 px-5 py-3 rounded-full border border-hair">
              View Documentation
            </button>
          </div>

          <div className="mt-14 grid grid-cols-2 gap-4 max-w-lg">
            {FEATURES.map((f) => (
              <div key={f.title} className="rounded-xl bg-panel/70 border border-hair p-4">
                <div className="w-9 h-9 rounded-lg bg-panel2 flex items-center justify-center mb-3 text-iris2">{f.icon}</div>
                <p className="text-sm font-semibold text-white">{f.title}</p>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="relative flex justify-center lg:justify-end">
          <div className="w-full max-w-sm aspect-[4/5] rounded-3xl bg-panel/70 border border-hair shadow-glow flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-iris/20 to-iris2/10" />
            <LogoBadge className="w-28 h-28 relative z-10" />
          </div>
        </div>
      </header>


      {/* How it works */}
      <section className="max-w-5xl mx-auto w-full px-6 pb-24 text-center">
        <span className="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-full border border-hair bg-panel2 text-iris2 mb-5">
          How it works
        </span>
        <h2 className="font-display font-bold text-white text-3xl sm:text-4xl tracking-tight">Simple. Fast. Powerful.</h2>
        <p className="mt-3 text-slate-400 max-w-lg mx-auto">
          Set up in minutes — this is the exact three-step flow every new integration follows, in order.
        </p>
        <div className="mt-12 grid sm:grid-cols-3 gap-5">
          {STEPS.map((s) => (
            <div key={s.n} className="rounded-2xl bg-panel/70 border border-hair p-6 text-left">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 rounded-full bg-gradient-to-br from-iris to-iris2 text-white text-xs font-bold flex items-center justify-center">
                  {s.n}
                </span>
                <span>{s.icon}</span>
              </div>
              <p className="font-semibold text-white text-sm">{s.title}</p>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-hair mt-auto">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <LogoBadge className="w-5 h-5" />
            <span>LensPilot — frontend widget demo</span>
          </div>
          <span>Chat widget is fully functional (mock data). Rest of page is view-only.</span>
        </div>
      </footer>

      <ChatWidget />
    </div>
  );
}
