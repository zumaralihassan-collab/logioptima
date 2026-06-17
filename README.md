# LogiOptima — Global Transportation & Logistics Optimization

An interactive, AI-assisted decision-support tool for transportation and logistics. It uses operations-research solvers and real freight-economics data to **predict, suggest, and explain** logistics operations — from a single delivery route to global crude-oil shipping networks.

**Live demo:** _(GitHub Pages URL appears here once deployed)_

![status](https://img.shields.io/badge/status-prototype-blue) ![type](https://img.shields.io/badge/stack-static%20HTML%20%2B%20JS-success) ![ai](https://img.shields.io/badge/AI-bring--your--own--key-purple)

## What it does

Four connected views in one self-contained app:

- **🌍 Global Network** — a world map of major real-world crude-oil shipping lanes (Middle East → Asia/Europe, US Gulf exports, West Africa, Russia, Brazil) plus a multi-port tanker **voyage optimizer** (Traveling Salesman Problem with nearest-neighbor + 2-opt).
- **⚡ Route Optimizer** — interactive TSP, Vehicle Routing (VRP), facility location, and min-cost network-flow solvers with live maps, KPIs, and strategy comparison.
- **📊 Executive Dashboard** — U.S. freight modal split (by value and by weight), a collapsible commodity → ideal-mode matrix, international trade by mode, and strategic insight cards.
- **💰 Cost Optimization** — a multi-modal cost & transit comparator (same shipment across truck / rail / ocean / air / pipeline, domestic vs import/export), an import/export/freight-forwarding cost stack, and a carrier-mode rate reference.

A persistent **AI assistant** runs across all views. It works offline with a data-aware fallback, and becomes fully conversational (in- and out-of-scope) when you add your own API key (⚙ — OpenAI-compatible: OpenAI, Azure, OpenRouter, or any compatible gateway). The key is stored only in your browser.

## Data & sources

Figures are drawn from public data and labeled approximate where sources vary:

- U.S. freight modal split — U.S. Bureau of Transportation Statistics, Freight Analysis Framework / Freight Facts & Figures.
- Crude oil transport economics — pipeline ≈ $5/bbl, rail ≈ $10–15, truck ≈ $20, marine in between.
- Air vs ocean — air ≈ $2.80–7.50/kg vs ocean ≈ $0.10–0.80/kg (~10×); air ≈ 3 days vs ocean ≈ 30.
- International U.S. trade — ~80% of tonnage by water; by value water ~47%, air ~27%, truck ~18%.

Cost-comparator rates are illustrative planning estimates, not quotes.

## Run locally

It's a single static file — no build step.

```bash
# just open it
open index.html          # macOS
# or serve it
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Deploy (GitHub Pages)

This repo is Pages-ready (`index.html` at the root). After pushing:

1. Repo **Settings → Pages**
2. **Source:** Deploy from a branch → **main** / **/(root)**
3. Save — your live URL is `https://<username>.github.io/<repo>/`

## Roadmap

See [`ARCHITECTURE_AND_ROADMAP.md`](ARCHITECTURE_AND_ROADMAP.md) for the full three-layer design (Python optimization engine · Excel I/O · web + chatbot) and the phased build plan — including the planned move from in-browser heuristics to a real **Google OR-Tools / PuLP** backend with `.xlsx` round-trip import/export.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The full global app (deployed entry point) |
| `logioptima_prototype.html` | Earlier single-view UX prototype |
| `ARCHITECTURE_AND_ROADMAP.md` | Architecture & phased roadmap |

---

Inspired by real fulfillment-network challenges: warehouse/FC placement, trucking optimization, and on-time-delivery assurance.
