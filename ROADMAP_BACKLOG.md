# Zumar's Logic-tics Stop — Autonomous Backlog

**Status markers:** `[ ]` pending · `[~] ` in progress · `[x]` done · `[!]` blocked (needs human)

**Executor rule:** implement the FIRST `[ ]` item in this file, harness-verify, then mark it `[x]` with the date. **One item per run.** If verification fails, revert and mark `[!]` with a one-line reason. Never rewrite the whole file — read the relevant code first, make surgical edits, reuse existing helpers (`$`, `mkChart`, `kpiGrid`, `sr/sint/spick`, `f$`, `pct`, `fmt`, `MODECOL`, `SHIPMENTS`, etc.).

**Acceptance for every item:** `node logic_test.js` shows 0 failed AND `python3 audit.py` stays at 100/100 with Correctness 100%.

---

## Queue (execution order — smallest & safest first)

- [x] (2026-06-20) **C3 — Light/dark theme toggle.** Add a `◐` button in the header that toggles a `light` class on `document.body` and saves to `localStorage('lts_theme')`; define a light palette by overriding the `:root` CSS variables under `body.light{...}`. Restore the saved theme on load. WHERE: header (after the badge), `:root` vars block, init. Verify charts/text stay legible.

- [x] (2026-06-20) **D2 — CI via GitHub Actions.** Add `.github/workflows/ci.yml` that, on push and pull_request, sets up Python + Node and runs `python3 audit.py` and `node logic_test.js`, failing the job on a non-zero exit. WHERE: new workflow file only (no app changes).

- [x] (2026-06-20, done in-session) **D1 — Harness business-logic fixtures.** Extend `logic_test.js` with optional assertions (guarded by `typeof fn==='function'`) for `shouldCost`, `carrierStats`, `forecast` (already), and the risk `DISRUPTIONS` map (e.g. air premium, Hormuz addDays>0). WHERE: `logic_test.js` TESTS block. Re-run to confirm new assertions pass.

- [x] (2026-06-20) **B6a — Control Tower marker clustering.** Lazy-load `leaflet.markercluster` from CDN and cluster the shipment markers in `drawCTMap` when count is high; fall back gracefully if the plugin is unavailable. WHERE: `<head>` CDN + `drawCTMap`. Keep arcs unchanged.

- [ ] **B6b — "Simulate live" toggle.** Add a toggle on the Control Tower that, when on, advances in-transit shipment positions/ETAs on a 3s timer and re-renders; off by default; clears the timer on view change. WHERE: control-tower toolbar + a timer + `renderControl`.

- [x] (2026-06-20, in-session) **C1 — Executive one-pager.** Add a compact `Executive summary` card at the top of the Control Tower (or a print-only section) that pulls the headline KPIs + top 3 exceptions + biggest cost leak, with a "Download PDF" using the existing print path. WHERE: control view + print CSS.

- [x] (2026-06-20, in-session) **A1 — Procurement & Freight RFP module.** New tab `procure` / `renderProcure`: a lane-rate benchmark table (should-cost vs market vs invoiced from `SHIPMENTS`), a carrier-bid comparison (reuse `CARRIERS` cpm/rel), contract-vs-spot mix chart, and an allocation recommendation. Register in nav, RENDER, init. WHERE: new view HTML + render fn + wiring.

- [x] (2026-06-20, in-session) **B3 — Sustainability SBT glide path.** Add a science-based-target glide-path line chart (current vs target trajectory to a -42% by 2030 style goal) and CO2-by-customer table to the Sustainability module. WHERE: `view-sustain` HTML + `renderSustain`.

- [x] (2026-06-20, in-session) **A5 — Supplier Management module.** New tab `supplier` / `renderSupplier`: supplier scorecards (reuse lead-time analytics + on-time), lead-time variability chart, dual-source coverage, ESG flags. WHERE: new view + render fn + wiring.

- [ ] **B2 — Demand multi-method forecasting.** Add moving-average and Holt methods alongside the current seasonal model in `forecast`, pick the best by in-sample MAPE, and show which method won. WHERE: `forecast` + `renderDemand` (method label).

- [ ] **A2 — Returns & Reverse Logistics module.** New tab `returns` / `renderReturns`: return rate by reason/lane (seeded), reverse-flow cost, disposition mix doughnut, RMA aging. WHERE: new view + render fn + wiring.

- [ ] **E1 — Copilot function-calling (lightweight).** Let the offline copilot recognize action intents ("reroute SHP-1049", "run hormuz simulation") and call the existing functions (`excAction`, `runDisruption`) with a confirmation toast. WHERE: `offline`/`ask` + a small intent parser.

- [ ] **B1 — Optimization Studio real MILP.** Integrate `javascript-lp-solver` (CDN) behind the existing solve path to support integer/binary variables; keep the sensitivity report. WHERE: `<head>` CDN + opt solve. (Larger — may take more than one run; if so, mark `[!]` for a human.)

- [ ] **C6 — Universal Excel import.** Generalize `importXlsx`/`validateImport` so other data tables (carriers, lanes, lead-times) can be imported, each with its own required-column set. WHERE: import helpers + per-module import buttons.

---

## Backlog (not yet queued — see the PDF for full detail)

A3 Trade & Customs Compliance · A4 Last-Mile & Delivery · A6 Order Management/Perfect-Order ·
B4 Risk Monte-Carlo · B5 Fulfillment dock & slotting · C2 Cross-module scenario compare ·
C4 Mobile/PWA · C5 Role-based dashboards · C7 i18n · C8 Audit log + undo/redo ·
D3 Performance budget · D4 a11y + visual regression · D5 Modularize/build · D6 Error telemetry ·
E2 Proactive insights · E3 Streaming + citations · E4 Multi-language copilot

---

## Progress log
_(the executor appends to AUTORUN_LOG.md each run; this file only tracks status)_
