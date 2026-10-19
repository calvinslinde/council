#!/usr/bin/env python3
"""Minimal OpenRouter client: keychain auth, reasoning-aware, retry on 429."""
import json, os, subprocess, time, requests, threading

URL = "https://openrouter.ai/api/v1/chat/completions"
_KEY = None
_lock = threading.Lock()

def key():
    """OpenRouter API key: the OPENROUTER_API_KEY environment variable, or on macOS a keychain
    item (service "openrouter", account "key"). Fails with a plain message otherwise."""
    global _KEY
    if _KEY is None:
        _KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not _KEY:
            try:
                _KEY = subprocess.check_output(
                    ["security", "find-generic-password", "-s", "openrouter", "-a", "key", "-w"],
                    text=True, stderr=subprocess.DEVNULL).strip()
            except Exception:
                _KEY = ""
        if not _KEY:
            raise SystemExit("No OpenRouter key. Set OPENROUTER_API_KEY, or on macOS add a keychain item "
                             "(service 'openrouter', account 'key').")
    return _KEY

def call(model, messages, max_tokens=4000, effort=None, no_reasoning=False,
         temperature=None, retries=3, timeout=420):
    body = {"model": model, "messages": messages, "max_tokens": max_tokens}
    if no_reasoning:                body["reasoning"] = {"enabled": False}
    elif effort:                    body["reasoning"] = {"effort": effort}
    if temperature is not None:     body["temperature"] = temperature
    hdr = {"Authorization": f"Bearer {key()}", "Content-Type": "application/json"}
    last = None
    for a in range(retries):
        t0 = time.time()
        try:
            r = requests.post(URL, json=body, headers=hdr, timeout=timeout)
            d = r.json()
            if "choices" in d and d["choices"]:
                m = d["choices"][0]["message"]
                u = d.get("usage", {}) or {}
                return {"ok": True, "model": model, "t": time.time()-t0,
                        "text": (m.get("content") or "").strip(),
                        "reasoning": (m.get("reasoning") or ""),
                        "out": u.get("completion_tokens"), "inp": u.get("prompt_tokens"),
                        "finish": d["choices"][0].get("finish_reason")}
            last = json.dumps(d)[:300]
            if "429" in last or "rate" in last.lower():
                time.sleep(4 * (a+1)); continue
            return {"ok": False, "model": model, "t": time.time()-t0, "err": last}
        except Exception as e:
            last = str(e)[:300]; time.sleep(2*(a+1))
    return {"ok": False, "model": model, "t": 0, "err": last}
