# Zumar's Logic-tics Stop — Global Transportation & Logistics Optimization

An interactive, AI-assisted decision-support suite for transportation and logistics. It uses operations-research solvers and real freight-economics data to **predict, suggest, and explain** logistics operations — from a single delivery route to a global multi-modal control tower.

**Live demo:** https://zumaralihassan-collab.github.io/logioptima/

![status](https://img.shields.io/badge/status-prototype-blue) ![type](https://img.shields.io/badge/stack-static%20HTML%20%2B%20JS-success) ![ai](https://img.shields.io/badge/AI-bring--your--own--key-purple)

## What it does

A single self-contained app, anchored on a **Control Tower** and going deep on five modules. A persistent **AI copilot** runs across every screen (offline data-aware fallback, or full real-time AI with your own OpenAI-compatible key).

- **🛰️ Control Tower (home).** Live multimodal map — ocean, air, rail, road — with shipments plotted, ETAs, and a **predictive ETA + disruption-risk** score per shipment. A side **Exception Inbox** turns alerts into one-click actions: reroute, switch carrier, file a D&D dispute, resolve. KPI strip for OTIF, OTD, in-transit, exceptions, at-risk, spend and D&D leakage. Excel import/export of the shipment register.
- **📊 Performance & Carriers.** OTIF/OTD trends, SLA adherence vs target, a **carrier scorecard** (on-time, tender acceptance, damage rate, $/mile, letter grade) that feeds carrier sourcing, plus a sustainability view with CO₂ by mode and a **modal-shift recommender**.
- **💸 Cost Intelligence.** The signature **Should-Move Cost™** engine computes what a lane *should* cost and audits invoices against it (overpriced-lane flags), a **detention & demurrage leak tracker**, **Cost-to-Serve** by customer/lane/commodity ("where am I quietly losing money?"), a multi-modal comparator, and a **landed-cost calculator** with tariffs, duties and Incoterms® 2020.
- **🧮 Optimization Studio.** An interactive, visual alternative to Excel Solver: define decision variables and constraints, solve a linear program, and read a full **sensitivity report** (shadow prices, reduced costs, objective & RHS ranging). Templates for mode/load optimization, transportation/min-cost flow, contract mix, and consolidation. **AI interprets** the result, and you can **export Model + Answer + Sensitivity sheets to Excel**. A second tab does visual TSP / VRP / facility / min-cost-flow / **disruption re-routing**.
- **🌍 Global & Crude.** A real-world route & hub planner (TSP + 2-opt, p-median hubs, center-of-gravity) and an enhanced **global crude shipping network** — export terminals, refining hubs, chokepoints with EIA volumes, tanker classes, a **voyage optimizer** with Worldscale-style economics, a **Cape-of-Good-Hope reroute** toggle, and a longitude/latitude graticule.
- **🔌 Data & Reports.** ERP connectors (SAP / Oracle / NetSuite / Excel), **lead-time history analytics** with variability stats, supplier/lane scorecards, inventory planning (safety stock & reorder point), and an **ad-hoc report builder** that pivots any dataset to a table + chart and exports to Excel/CSV/print.

## Data & sources

Figures are public-data-based and labeled approximate where sources vary:

- U.S. freight modal split — U.S. Bureau of Transportation Statistics (FAF / Freight Facts & Figures).
- Oil chokepoint volumes — U.S. EIA *World Oil Transit Chokepoints* (2023–2024): Hormuz ~20 Mb/d, Malacca ~22.5, Suez+SUMED ~4.8, Bab-el-Mandeb ~4.1 (the latter two down sharply as Red Sea disruptions pushed tankers around the Cape).
- Incoterms® 2020 — 11 rules (7 any-mode, 4 sea/inland-waterway).

The shipment dataset is synthetic but realistic, and seeded for reproducibility. Costs, freight rates and tanker economics are illustrative planning estimates, not quotes. Replace any dataset with your own via Excel import.

## Run locally

It's a single static file — no build step.

```bash
open index.html                 # macOS
# or
python3 -m http.server 8000     # then visit http://localhost:8000
```

## AI copilot

Works offline with a data-aware assistant (ops summaries, "which lanes bled money?", SLA breaches, Incoterms, crude risk, sensitivity interpretation). Click ⚙ to add an OpenAI-compatible key (OpenAI, Azure, OpenRouter, or any compatible gateway) for full real-time AI. The key is stored only in your browser.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The full suite (deployed entry point) |
| `logioptima_prototype.html` | Earlier single-view UX prototype |
| `ARCHITECTURE_AND_ROADMAP.md` | Architecture & phased roadmap |
