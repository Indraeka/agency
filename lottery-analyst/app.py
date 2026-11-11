#!/usr/bin/env python3
"""Local web interface for the lottery analyst.

    python3 app.py            then open http://127.0.0.1:8649

Buttons on the page call this server, which runs the same code as the CLI:
  Refresh results  -> fetch.refresh()        adds draws published since last time
  Generate numbers -> analyze.make_picks()   two sets per game for the next draw

Everything stays on this machine; the only outbound traffic is the results
download during a refresh.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import analyze
import fetch

HERE = Path(__file__).parent
HISTORY = HERE / "history.json"
LOCK = threading.Lock()
EVIDENCE_CACHE: dict = {}


def load_history() -> list:
    return json.loads(HISTORY.read_text()) if HISTORY.exists() else []


def state() -> dict:
    today = dt.date.today()
    games, results = {}, {}
    for gid, cfg in analyze.GAMES.items():
        dates, main, bonus, pools = analyze.load(gid)
        results[gid] = {d: (set(m.tolist()), int(b)) for d, m, b in zip(dates, main, bonus)}
        games[gid] = {
            "label": cfg["label"],
            "k": cfg["k"],
            "pool": int(pools[-1]),
            "draws": len(dates),
            "first": dates[0],
            "last": dates[-1],
            "next_draw": analyze.next_draw(dates[-1], cfg["weekdays"], today),
            "recent": [
                {"date": d, "main": m.tolist(), "bonus": int(b)}
                for d, m, b in list(zip(dates, main, bonus))[-6:][::-1]
            ],
        }
    history = []
    for h in load_history():
        entry = dict(h, label=analyze.GAMES[h["game"]]["label"], drawn=None)
        hit = results[h["game"]].get(h["draw_date"])
        if hit:
            drawn, bonus = hit
            entry["drawn"] = {"main": sorted(drawn), "bonus": bonus}
            for key in ("set_a", "set_b"):
                entry[f"{key}_matches"] = len(drawn.intersection(h[key]))
                entry[f"{key}_bonus"] = bonus in h[key]
        history.append(entry)
    history.sort(key=lambda e: (e["draw_date"], e["game"]), reverse=True)
    return {"today": today.isoformat(), "games": games, "history": history}


def generate(variants: dict) -> dict:
    """Make picks for both games and remember them (one entry per game and draw).

    variants[game] = 0 gives the default pair; higher numbers give alternatives.
    """
    history = load_history()
    picks = {}
    for gid in analyze.GAMES:
        variant = max(0, min(int(variants.get(gid, 0)), 10**6))
        p = analyze.make_picks(gid, "" if variant == 0 else str(variant))
        picks[gid] = p
        history = [h for h in history if not (h["game"] == gid and h["draw_date"] == p["next_draw"])]
        history.append({
            "game": gid, "draw_date": p["next_draw"], "variant": variant,
            "set_a": p["set_a"], "set_b": p["set_b"],
            "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        })
    HISTORY.write_text(json.dumps(history, indent=1) + "\n")
    return picks


def evidence(sims: int) -> dict:
    out = {}
    for gid in analyze.GAMES:
        key = (gid, analyze.load(gid)[0][-1])
        if key not in EVIDENCE_CACHE:
            res, _ = analyze.run_game(gid, sims, "", dt.date.today())
            if len(EVIDENCE_CACHE) > 8:
                EVIDENCE_CACHE.clear()
            EVIDENCE_CACHE[key] = {k: res[k] for k in ("tests", "backtest", "hot", "cold", "overdue", "jackpot_odds")}
        out[gid] = EVIDENCE_CACHE[key]
    return out


class Handler(BaseHTTPRequestHandler):
    sims = 1000

    def send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, obj, code: int = 200) -> None:
        self.send(code, json.dumps(obj).encode(), "application/json")

    def guarded(self, fn) -> None:
        try:
            with LOCK:
                self.send_json(fn())
        except Exception as exc:  # noqa: BLE001 - report any failure to the page
            traceback.print_exc()
            self.send_json({"error": f"{type(exc).__name__}: {exc}"}, 500)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self.send(200, (HERE / "ui.html").read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/state":
            self.guarded(state)
        elif path == "/api/evidence":
            self.guarded(lambda: evidence(self.sims))
        else:
            self.send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            body = {}
        if self.path == "/api/refresh":
            self.guarded(lambda: {"refresh": fetch.refresh(log=lambda *_: None), "state": state()})
        elif self.path == "/api/generate":
            variants = body.get("variants") if isinstance(body.get("variants"), dict) else {}
            self.guarded(lambda: {"picks": generate(variants), "state": state()})
        else:
            self.send_json({"error": "not found"}, 404)

    def log_message(self, fmt, *args) -> None:
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8649)
    ap.add_argument("--sims", type=int, default=1000, help="fair-draw simulations for the evidence panel")
    args = ap.parse_args()
    Handler.sims = args.sims
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Lottery analyst running at http://{args.host}:{args.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
