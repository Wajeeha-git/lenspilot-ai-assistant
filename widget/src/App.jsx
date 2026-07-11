const COMPANY_CARDS = [
  {
    label: "Company",
    title: "LensPilot",
    desc: "An AI-powered web platform for browser-based virtual contact lens try-on.",
  },
  {
    label: "Mission",
    title: "Modern lens shopping",
    desc: "LensPilot helps customers preview lens colors and styles before buying.",
  },
  {
    label: "Experience",
    title: "Real-time try-on",
    desc: "Customers open the experience in a browser and see lenses overlaid on their eyes.",
  },
  {
    label: "Retailers",
    title: "Built for optical shops",
    desc: "Shopkeepers can offer a simple QR-code based try-on flow to their customers.",
  },
  {
    label: "Technology",
    title: "AI iris segmentation",
    desc: "The platform uses augmented reality and AI-based iris detection for realistic previews.",
  },
  {
    label: "Benefit",
    title: "No sample lenses needed",
    desc: "LensPilot reduces physical sampling, speeds up decisions, and keeps catalogues consistent.",
  },
];

function LogoBadge({ className = "w-8 h-8" }) {
  return (
    <span className={`inline-flex items-center justify-center bg-white rounded-full overflow-hidden shrink-0 ${className}`}>
      <img src="/logo.png" alt="LensPilot logo" className="w-[78%] h-[78%] object-contain" />
    </span>
  );
}

function InfoCard({ label, title, desc }) {
  return (
    <article className="rounded-xl bg-panel/70 border border-hair p-5 min-h-[150px]">
      <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-iris2">{label}</p>
      <h2 className="mt-4 text-base font-display font-bold text-white tracking-tight">{title}</h2>
      <p className="mt-2 text-sm leading-relaxed text-slate-400">{desc}</p>
    </article>
  );
}

function ChatPreview() {
  return (
    <aside className="relative rounded-[28px] bg-panel/75 border border-hair shadow-glow overflow-hidden min-h-[620px]">
      <div className="absolute inset-0 bg-gradient-to-br from-iris/20 via-transparent to-iris2/10" />
      <div className="relative z-10 h-full flex flex-col">
        <div className="flex items-center justify-between px-5 py-4 border-b border-hair bg-panel/50">
          <div className="flex items-center gap-3">
            <LogoBadge className="w-10 h-10" />
            <div>
              <p className="text-sm font-semibold text-white leading-tight">LensPilot Assistant</p>
              <p className="text-xs text-teal-300">Ready to help</p>
            </div>
          </div>
          <span className="w-2.5 h-2.5 rounded-full bg-teal" />
        </div>

        <div className="flex-1 px-5 py-6 space-y-4">
          <div className="max-w-[82%] rounded-2xl rounded-bl-sm bg-panel2 border border-hair px-4 py-3 text-sm leading-relaxed text-slate-200">
            Hi, I am LensPilot. Ask me about virtual try-on, shopkeeper setup, lens catalogues, or the customer flow.
          </div>
          <div className="ml-auto max-w-[76%] rounded-2xl rounded-br-sm bg-gradient-to-br from-iris to-iris2 px-4 py-3 text-sm leading-relaxed text-white">
            Can you explain the company in simple words?
          </div>
          <div className="max-w-[86%] rounded-2xl rounded-bl-sm bg-panel2 border border-hair px-4 py-3 text-sm leading-relaxed text-slate-200">
            LensPilot lets optical retailers offer contact lens try-on through a browser, using AI and augmented reality.
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 xl:grid-cols-3 gap-2 pt-2">
            {["Virtual try-on", "Shopkeeper QR", "Customer flow"].map((item) => (
              <span key={item} className="rounded-full border border-hair bg-panel/70 px-3 py-2 text-center text-xs text-slate-300">
                {item}
              </span>
            ))}
          </div>
        </div>

        <div className="p-5 border-t border-hair bg-panel/60">
          <div className="rounded-2xl border border-hair bg-panel2/80 p-3">
            <p className="px-2 pb-3 text-sm text-slate-500">Ask about LensPilot...</p>
            <button className="w-full rounded-full bg-gradient-to-r from-iris to-iris2 px-5 py-3 text-sm font-semibold text-white shadow-glow hover:brightness-110 transition">
              Start chat
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default function App() {
  return (
    <div className="min-h-screen text-slate-200 font-body">
      <main className="max-w-7xl mx-auto w-full px-6 py-8 sm:py-10 lg:py-14">
        <section className="grid lg:grid-cols-[minmax(0,1fr)_minmax(360px,460px)] gap-8 lg:gap-12 items-start">
          <div className="flex flex-col">
            <div className="flex items-center gap-3">
              <LogoBadge className="w-10 h-10" />
              <div>
                <p className="font-display font-bold text-xl text-white tracking-tight">LensPilot</p>
                <p className="text-xs text-slate-500">AI virtual contact lens try-on</p>
              </div>
            </div>

            <div className="pt-12 lg:pt-16">
              <h1 className="font-display font-extrabold text-white text-4xl sm:text-5xl lg:text-6xl leading-[1.05] tracking-tight">
                LensPilot
                <span className="block bg-gradient-to-r from-iris to-iris2 bg-clip-text text-transparent">
                  AI Assistant
                </span>
              </h1>
              <p className="mt-6 max-w-xl text-base sm:text-lg leading-relaxed text-slate-400">
                Accurate, realistic, and accessible virtual contact lens try-on for modern optical retail.
              </p>
              <div className="mt-8">
                <button className="w-full max-w-[610px] lg:max-w-[392px] rounded-full bg-gradient-to-r from-iris to-iris2 px-5 py-3 text-sm font-semibold text-white shadow-glow hover:brightness-110 transition">
                  Start chat
                </button>
              </div>
            </div>

            <div className="mt-12 grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
              {COMPANY_CARDS.map((card) => (
                <InfoCard key={card.label} {...card} />
              ))}
            </div>
          </div>

          <ChatPreview />
        </section>
      </main>
    </div>
  );
}
