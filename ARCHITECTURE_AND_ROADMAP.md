# LogiOptima — Transportation & Logistics Optimization Tool

**Vision:** A decision-support tool that uses analytical data, scenarios, and operations-research solvers to *predict, suggest, and explain* logistics operations — inspired by real Amazon-style network challenges (regional warehouses & fulfillment centers, strategic facility placement, trucking/route optimization, and on-time-delivery assurance). Excel in and out, an interactive and visually appealing interface, and an AI chatbot that answers both in-scope and general questions.

**Decisions locked (16 Jun 2026):**

- Platform: **Python optimization engine + Excel I/O + web dashboard**
- Scope (v1): **TSP, Vehicle Routing (VRP), Facility Location, Min-Cost Network Flow**
- Data: **Synthetic to build, real/anonymized data swapped in later**
- Chatbot: **Bring-your-own API key** (OpenAI-compatible / Claude)

---

## Architecture — three layers

The guiding principle is a clean separation so the UI, Excel, and chatbot never touch optimization internals. Everything speaks one **solution format**, so a solve started from Excel, the web UI, or a script produces the same object the chatbot can read and narrate.

**1. Core engine (Python).** Each problem type is an independent solver module with a uniform contract: `solve(inputs) -> Solution`.

- `tsp.py` — single-route ordering. Nearest-neighbor construction + 2-opt improvement; OR-Tools for exact/larger instances.
- `vrp.py` — multiple vehicles, capacities, time windows. Google OR-Tools routing.
- `facility.py` — p-median / facility location. PuLP or OR-Tools MIP: which warehouses to open to minimize demand-weighted cost.
- `network.py` — min-cost transportation/flow from FCs to regions. PuLP / `networkx`.
- `model.py` — shared data classes (`Location`, `Vehicle`, `Demand`, `Solution`, `KPIs`).

**2. I/O layer.** `excel_io.py` reads `.xlsx` inputs (locations, demand, costs, vehicle specs) into the model and writes results (routes, assignments, KPIs) back to a formatted workbook — built with `openpyxl`. `datagen.py` produces realistic synthetic networks for building and demos.

**3. Presentation layer.** A web dashboard (map, scenario controls, KPI cards, strategy-comparison charts) served by a lightweight Python backend (FastAPI or Flask). The **chatbot** receives the *current scenario state* as context, so it can explain "why this route / why this warehouse" in-scope and still answer general questions via your API key.

```
        ┌─────────────── Web dashboard (HTML/JS) ───────────────┐
        │  map · controls · KPIs · charts · AI chat             │
        └───────────────┬───────────────────────┬──────────────┘
                        │ HTTP/JSON              │ scenario context
        ┌───────────────▼──────────┐   ┌─────────▼─────────┐
        │  FastAPI backend         │   │  Chatbot (BYO key)│
        └───────┬──────────┬───────┘   └───────────────────┘
                │          │
   ┌────────────▼───┐  ┌───▼─────────────┐
   │ Core engine    │  │ Excel I/O +     │
   │ tsp/vrp/fac/net│  │ synthetic data  │
   └────────────────┘  └─────────────────┘
```

---

## Excel I/O schema (draft)

**Input workbook** (one sheet per concept):

- `Locations`: id, name, type (depot/FC/stop/region), lat/x, lon/y
- `Demand`: location_id, units, time_window_start, time_window_end
- `Vehicles`: id, capacity, cost_per_km, max_hours
- `Costs`: from_id, to_id, distance_km, cost (optional override)
- `Settings`: problem_type, strategy, objective (min cost / max OTD)

**Output workbook:**

- `Routes`: vehicle_id, sequence, location_id, arrival, load
- `Assignments`: demand_id → facility/FC
- `KPIs`: total_distance, total_cost, drive_time, on_time_rate, vehicles_used
- `Comparison`: strategy → objective value

---

## Chatbot scope

In-scope (answered from live scenario state): explain the current solution, why a route/placement was chosen, cost & on-time levers, definitions (TSP, VRP, p-median). Out-of-scope (answered via your LLM key): anything else. A clean offline fallback answers in-scope questions with no key, so the tool is always useful.

---

## Roadmap

**Phase 0 — UX preview (done).** Self-contained interactive HTML prototype: live map, working TSP/VRP/facility/network solvers in JS, scenario controls, KPI cards, strategy comparison, chatbot shell with API-key integration point. Purpose: align on look, feel, and scope before backend investment.

**Phase 1 — Core engine + Excel I/O.** Python package with the four solvers (OR-Tools/PuLP), shared model, synthetic data generator, and round-trip `.xlsx` import/export. CLI to run a scenario end-to-end. Unit tests per solver.

**Phase 2 — Web dashboard.** FastAPI backend exposing solve endpoints; refined front end (real map tiles via Leaflet, animated routes, scenario library, save/load). Upload an Excel file → solve → download results.

**Phase 3 — AI chatbot, live.** Wire the BYO-key chatbot to the backend with full scenario context; streaming responses; "explain this decision" deep-links from the map.

**Phase 4 — Extended scope.** Multi-echelon networks (FC → sort center → last mile), time-window VRP, demand forecasting to *predict* load, scenario A/B comparison, sensitivity analysis ("what if fuel +10%?"), and on-time-rate optimization as a first-class objective.

---

## Open questions for later

- Real map/geocoding: use lat-lon + a routing distance API, or stay on planar coordinates for speed?
- Deployment: run locally on your machine, or host it?
- Data scale: typical number of stops / FCs / regions you want to handle?
