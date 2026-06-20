# Zumar's Logic-tics Stop — deeper-upgrade proposal

Prioritized, approval-ready improvements for the existing Control Tower app (1,418 lines). Nothing here is applied yet — each item lists **what**, **where** in your code, **risk**, and **effort** so you can pick. The harness (`audit.py` + `logic_test.js`) will verify each change.

Baseline after today's safe fixes: **100/100** on the recalibrated audit, 15/15 logic assertions passing.

## Tier 1 — high value, low risk

1. **Persist & share state.** Today `genShipments()` regenerates synthetic data every load, so edits and resolved exceptions don't survive a refresh. Add `localStorage` persistence of the shipment register + filters, and a shareable URL (encode active module, filters, selected shipment in the hash). *Where:* init path around `genShipments`, `renderControl`, `excAction`. *Risk:* low. *Effort:* M.

2. **Robust Excel import.** `importXlsx` should validate columns against the template, report row-level errors, and offer a one-click sample template with the exact expected headers. *Where:* `importXlsx`, `ctTemplate`. *Risk:* low. *Effort:* S–M.

3. **Accessibility round 2.** Build on today's aria-labels: keyboard operability for Exception Inbox actions (reroute/switch/resolve), `role="table"`/scope on data tables, `aria-live` on the KPI strip, and `prefers-reduced-motion`. *Where:* `renderInbox`, `renderCTTable`, KPI render. *Risk:* low. *Effort:* M.

4. **Branded exports.** XLSX with column widths, number/currency formats and a cover sheet; a print stylesheet + "Export PDF" for the Control Tower. *Where:* `exportXlsx`, `exportReport`, new `@media print`. *Risk:* low. *Effort:* S–M.

## Tier 2 — meaningful capability, moderate risk

5. **Solver upgrade (Optimization Studio).** If the LP is hand-rolled, swap in a vetted simplex (e.g. `javascript-lp-solver`) for larger models and **integer/MILP** support, keeping your sensitivity report (`renderSens`, `interpretSolution`). *Where:* `view-opt` solve path. *Risk:* med (math). *Effort:* M–L.

6. **Map performance at scale.** Add marker clustering (Leaflet.markercluster) and viewport rendering so the Control Tower stays smooth with hundreds of shipments. *Where:* `drawCTMap`, `initCTMap`. *Risk:* low–med. *Effort:* M.

7. **Optional real routing/ETA.** Keep great-circle (`arcPts`) as default; add an opt-in road-distance/ETA via a routing API for truck legs, improving ETA realism. *Where:* ETA calc, `drawCTMap`. *Risk:* med (external dep). *Effort:* M.

8. **"Simulate live" mode.** A toggle that advances shipment positions/ETAs on a timer so the control tower demos dynamically (great for stakeholders). *Where:* new timer over the shipment model + `renderControl`. *Risk:* low. *Effort:* M.

## Tier 3 — polish

9. **Light/dark theme toggle** with saved preference. *Risk:* low. *Effort:* S.
10. **Harness depth.** Extend `logic_test.js` with fixtures for `carrierStats`, `ctsAgg`, `runLanded`, `interpretSolution`, and Incoterms lookups so the loop guards your **business** logic, not just the geo engine. *Risk:* none (test-only). *Effort:* M.

## Suggested first sprint

Tier 1 (items 1–4) in one pass — all low-risk, each harness-verified, each reversible via git. Then pick from Tier 2.

> Tell me which numbers to implement and I'll do them surgically (read → edit → harness-verify → show diff → deploy), never a blind rewrite.
