#!/usr/bin/env python3
"""
Zumar's Logic-tics Stop — automated quality audit + improvement harness.

Scores index.html across correctness (real logic tests), features, accessibility,
SEO/meta, performance, and robustness. Prints a prioritized issue list and writes
audit_report.md. Drives the iterate-fix-verify loop: run it, fix the top issues,
run it again. Score climbs as the tool improves.

Usage:
  python3 tools/audit.py                      # one pass
  python3 tools/audit.py --loop 5 --sleep 2   # re-run N times (watcher/scheduled use)
  python3 tools/audit.py --file path/to.html  # audit a specific file
"""
import argparse, os, re, subprocess, sys, time, datetime

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = _here if os.path.exists(os.path.join(_here, "index.html")) else os.path.dirname(_here)
SCRIPT_DIR = _here

def load(fp):
    with open(fp, encoding="utf-8") as f:
        return f.read()

def run_logic_tests(fp):
    """Returns (passed:int, failed:int, ok:bool, raw:str)."""
    try:
        r = subprocess.run(["node", os.path.join(SCRIPT_DIR, "logic_test.js"), fp],
                           capture_output=True, text=True, timeout=60)
        out = r.stdout + r.stderr
        m = re.search(r"LOGIC:\s*(\d+)\s*passed,\s*(\d+)\s*failed", out)
        if m:
            return int(m.group(1)), int(m.group(2)), r.returncode == 0, out
        return 0, 1, False, out
    except Exception as e:
        return 0, 1, False, str(e)

# Each check: (id, category, weight, ok(bool), detail, fix_hint)
def audit(fp):
    html = load(fp)
    low = html.lower()
    checks = []
    def add(cid, cat, w, ok, detail, hint=""):
        checks.append(dict(id=cid, cat=cat, w=w, ok=bool(ok), detail=detail, hint=hint))

    # ---- Correctness (real logic execution) ----
    p, f, ok, raw = run_logic_tests(fp)
    add("logic-tests", "Correctness", 30, ok and f == 0,
        f"{p} logic assertions passed, {f} failed", "See logic_test.js output; fix the failing function")
    audit.raw_logic = raw  # stash for report

    # ---- Core features present (regression guard) ----
    feat = {
        "Control Tower module": "view-control" in low and "renderinbox" in low,
        "Exception inbox + actions": "excaction" in low,
        "Predictive ETA & disruption risk": "disruption" in low or "etarisk" in low or "predict" in low,
        "Carrier scorecard": "carrierstats" in low,
        "Modal-shift recommender": "modalshift" in low,
        "Should-Move Cost engine": "should-move" in low or "smcinvoiced" in low or "smc" in low,
        "Cost-to-serve": "ctsagg" in low or "cost-to-serve" in low or "ctsbody" in low,
        "Landed-cost calculator": "runlanded" in low or "lcrun" in low,
        "Incoterms 2020": "incoterms" in low or "findinco" in low,
        "Optimization Studio (LP)": "view-opt" in low,
        "Sensitivity report": "rendersens" in low or "sensitivity" in low,
        "AI interprets solution": "interpretsolution" in low,
        "Excel import/export (SheetJS)": "importxlsx" in low and "exportxlsx" in low,
        "Great-circle arcs": "arcpts" in low,
        "Global crude network": "drawcrude" in low or "drawchokes" in low,
        "Chokepoints (EIA)": "chokes" in low or "hormuz" in low,
        "Route/hub engine (TSP + p-median)": "tsporder" in low and "hubsolve" in low,
        "Center-of-gravity": "centroid" in low,
        "Lead-time analytics": "genleadtime" in low or "leadtime" in low,
        "Inventory planning": "runinventory" in low,
        "Report builder": "runreport" in low,
        "AI copilot + BYO key": "apikey" in low or "api key" in low,
        "State persistence (localStorage)": "saveshipments" in low,
        "Shareable view link": "copysharelink" in low or "encodestate" in low,
        "Print / PDF export": "window.print" in low.replace(" ", ""),
        "Branded Excel export": "brandedexport" in low,
        "Robust import validation": "validateimport" in low,
        "Sustainability / carbon module": "view-sustain" in low and "rendersustain" in low,
        "Risk & resilience module": "view-risk" in low and "rundisruption" in low,
        "Demand & S&OP forecasting": "view-demand" in low and "function forecast" in low,
        "Fulfillment Ops (FC network)": "view-fc" in low and "renderfc" in low,
        "Procurement & Freight RFP": "view-procure" in low and "renderprocure" in low,
        "Supplier Management": "view-supplier" in low and "rendersupplier" in low,
        "Executive one-pager": "execpanel" in low and "renderexec" in low,
        "Sustainability SBT glide path": "chsbt" in low,
    }
    for name, present in feat.items():
        add("feat:" + name, "Features", 3, present, name, "Implement '" + name + "'")

    # ---- Accessibility ----
    add("a11y-lang", "Accessibility", 3, re.search(r"<html[^>]*\blang=", html, re.I), "html lang attribute", 'Add lang="en" to <html>')
    add("a11y-title", "Accessibility", 2, "<title>" in low, "page <title>", "Add a <title>")
    add("a11y-viewport", "Accessibility", 2, 'name="viewport"' in low, "responsive viewport meta", "Add viewport meta")
    add("a11y-labels", "Accessibility", 2, low.count("<label") >= 8, f"{low.count('<label')} <label> elements", "Label form controls")
    add("a11y-aria", "Accessibility", 3, low.count("aria-label") >= 4, f"{low.count('aria-label')} aria-labels", "Add aria-labels to icon buttons/inputs")
    add("a11y-focus", "Accessibility", 2, ":focus" in low, "visible focus styles", "Add :focus / :focus-visible outlines")
    add("a11y-reduced-motion", "Accessibility", 2, "prefers-reduced-motion" in low, "reduced-motion support", "Add a prefers-reduced-motion media query")
    add("a11y-table-scope", "Accessibility", 2, 'scope="col"' in low, "table header scope", "Add scope=col to data-table headers")

    # ---- SEO / meta / branding ----
    add("seo-desc", "SEO/Meta", 2, 'name="description"' in low, "meta description", "Add <meta name=description>")
    add("seo-og", "SEO/Meta", 3, 'property="og:' in low, "Open Graph tags", "Add og:title/og:description for social previews")
    add("seo-favicon", "SEO/Meta", 2, 'rel="icon"' in low or "favicon" in low, "favicon", "Add a favicon (inline SVG data URI is fine)")
    add("seo-theme", "SEO/Meta", 1, 'name="theme-color"' in low, "theme-color", "Add theme-color meta")
    add("brand", "SEO/Meta", 2, "logic-tics" in low, "brand name present", "Use the tool name in title/header")

    # ---- Robustness ----
    add("rob-trycatch", "Robustness", 3, low.count("try") >= 2 and "catch" in low, "error handling (try/catch)", "Wrap fetch/parse in try/catch")
    add("rob-geocode-guard", "Robustness", 2, "could not" in low or "not found" in low or "catch" in low, "geocode failure feedback", "Toast on geocode failure")
    add("rob-empty", "Robustness", 2, "at least 2" in low or "add at least" in low, "empty-state guidance", "Guide the user when too few inputs")
    add("rob-https", "Robustness", 2, "http://" not in low.replace("http://www.w3.org", "x").replace("http://localhost", "x"), "no insecure http resources", "Use https for all external resources")

    # ---- Performance ----
    size = len(html.encode("utf-8"))
    add("perf-size", "Performance", 3, size < 320_000, f"page weight {size/1024:.0f} KB", "Keep the single file lean (<320 KB)")
    add("perf-defer", "Performance", 1, "load" in low and "addeventlistener('load'" in low.replace(" ", ""), "init deferred to load", "Init after load")

    return checks, size

def report(checks, size, fp):
    by_cat = {}
    got = tot = 0
    for c in checks:
        by_cat.setdefault(c["cat"], []).append(c)
        tot += c["w"]; got += c["w"] if c["ok"] else 0
    score = round(100 * got / tot) if tot else 0

    lines = []
    lines.append(f"# Audit report — {os.path.basename(fp)}")
    lines.append(f"_{datetime.datetime.now():%Y-%m-%d %H:%M:%S}_  ·  page weight {size/1024:.0f} KB\n")
    lines.append(f"## Score: {score}/100\n")
    for cat, items in by_cat.items():
        cg = sum(i["w"] for i in items if i["ok"]); ct = sum(i["w"] for i in items)
        lines.append(f"### {cat} — {round(100*cg/ct)}%")
        for i in items:
            lines.append(f"- {'✅' if i['ok'] else '❌'} {i['detail']}" + ("" if i["ok"] else f"  → _{i['hint']}_"))
        lines.append("")
    fails = [c for c in checks if not c["ok"]]
    if fails:
        lines.append("## Prioritized fixes (highest impact first)")
        for c in sorted(fails, key=lambda x: -x["w"]):
            lines.append(f"- [{c['w']:>2} pts] **{c['detail']}** — {c['hint']}")
    else:
        lines.append("## ✨ All checks pass.")
    md = "\n".join(lines)
    with open(os.path.join(ROOT, "audit_report.md"), "w", encoding="utf-8") as f:
        f.write(md + "\n\n---\n### Logic test output\n```\n" + getattr(audit, "raw_logic", "") + "\n```\n")
    return score, fails

def one_pass(fp):
    checks, size = audit(fp)
    score, fails = report(checks, size, fp)
    print(f"\n=== SCORE {score}/100  ({len([c for c in checks if c['ok']])}/{len(checks)} checks)  {size/1024:.0f} KB ===")
    cats = {}
    for c in checks:
        cats.setdefault(c["cat"], [0, 0])
        cats[c["cat"]][1] += c["w"]; cats[c["cat"]][0] += c["w"] if c["ok"] else 0
    for cat, (g, t) in cats.items():
        print(f"  {cat:<14} {round(100*g/t):>3}%")
    if fails:
        print("\nTop fixes:")
        for c in sorted(fails, key=lambda x: -x["w"])[:12]:
            print(f"  [{c['w']:>2}] {c['detail']}  ->  {c['hint']}")
    print("\nFull report: audit_report.md")
    return score

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=os.path.join(ROOT, "index.html"))
    ap.add_argument("--loop", type=int, default=1, help="re-run the audit N times")
    ap.add_argument("--sleep", type=float, default=1.0)
    a = ap.parse_args()
    last = 0
    for i in range(a.loop):
        if a.loop > 1:
            print(f"\n########## PASS {i+1}/{a.loop}  {datetime.datetime.now():%H:%M:%S} ##########")
        last = one_pass(a.file)
        if i < a.loop - 1:
            time.sleep(a.sleep)
    sys.exit(0 if last >= 90 else 1)

if __name__ == "__main__":
    main()
