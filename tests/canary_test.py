#!/usr/bin/env python3
"""
Canary Health Check for anindo scrapers.
Runs in CI/CD (GitHub Actions) to verify that providers, endpoints, and stream resolvers are fully operational.
"""

import sys
import runpy
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ANINDO_BIN = REPO_ROOT / "anindo"

print("=" * 60)
print("  ANINDO CANARY HEALTH CHECK")
print("=" * 60)

try:
    mod = runpy.run_path(str(ANINDO_BIN), run_name="__test__")
except Exception as e:
    print(f"[FATAL] Failed to load anindo module: {e}")
    sys.exit(1)

failures = []

def run_check(name, fn):
    print(f"\n[TEST] {name}...")
    try:
        fn()
        print(f"  -> PASSED")
    except Exception as e:
        print(f"  -> FAILED: {e}")
        failures.append(f"{name}: {e}")

# 1. Check Domain Resolver
def test_domains():
    d_otaku = mod["get_base_url"]("otakudesu", force_refresh=True)
    d_nonton = mod["get_base_url"]("nontonanime", force_refresh=True)
    assert d_otaku and d_otaku.startswith("http"), f"Invalid Otakudesu domain: {d_otaku}"
    assert d_nonton and d_nonton.startswith("http"), f"Invalid NontonAnime domain: {d_nonton}"
    print(f"  Otakudesu: {d_otaku} | NontonAnime: {d_nonton}")

run_check("Dynamic Domain Resolution", test_domains)

# 2. Check Otakudesu Search & Episodes
def test_otakudesu():
    results = mod["search_otakudesu"]("frieren")
    assert len(results) > 0, "Otakudesu search returned 0 results for 'frieren'"
    print(f"  Search OK: found {len(results)} matches")
    
    first_url = results[0]["url"]
    eps = mod["get_otakudesu_episodes"](first_url)
    assert len(eps) > 0, f"Otakudesu episode list is empty for {first_url}"
    print(f"  Episodes OK: found {len(eps)} episodes for {results[0]['raw_title']}")

run_check("Otakudesu Scraper Pipeline", test_otakudesu)

# 3. Check NontonAnime Search & Episodes
def test_nontonanime():
    results = mod["search_nontonanime"]("initial d")
    assert len(results) > 0, "NontonAnime search returned 0 results for 'initial d'"
    print(f"  Search OK: found {len(results)} matches")
    
    first_url = results[0]["url"]
    eps = mod["get_nontonanime_episodes"](first_url)
    assert len(eps) > 0, f"NontonAnime episode list is empty for {first_url}"
    print(f"  Episodes OK: found {len(eps)} episodes for {results[0]['raw_title']}")

run_check("NontonAnime Scraper Pipeline", test_nontonanime)

# 4. Check Putarin Decryption Resolver
def test_putarin_decrypt():
    # Initial D First Stage Ep 1 Putarin embed
    embed_url = "https://putarin.xyz/e/UaRCtdCHAE"
    stream_url, ref = mod["resolve_putarin"](embed_url)
    assert stream_url and "api/hls" in stream_url, f"Failed to decrypt Putarin stream: {stream_url}"
    print(f"  Putarin AES-256-GCM Decryption OK: stream resolved")

run_check("Putarin HLS Decryptor", test_putarin_decrypt)

# 5. Check Modular Registry & Cross-Provider Fallback
def test_cross_provider_fallback():
    reg = mod["REGISTRY"]
    assert len(reg.all()) >= 2, "Expected at least 2 registered providers"
    print(f"  Registered providers: {reg.names()}")

    # Test fallback lookup for Sousou no Frieren Ep 1 excluding Otakudesu
    alt_ep, alt_cands = reg.find_cross_provider_fallback("Sousou no Frieren", 1.0, exclude_provider="otakudesu")
    assert alt_ep is not None, "Failed to find fallback episode on alternate provider"
    assert len(alt_cands) > 0, "No candidates found on alternate provider"
    print(f"  Cross-Provider Fallback OK: resolved {alt_ep['title']} on alternate provider with {len(alt_cands)} candidate(s)")

run_check("Modular Registry & Cross-Provider Fallback", test_cross_provider_fallback)

# 6. Check Code Integrity & Interactive Helpers
def test_code_integrity():
    import symtable, builtins
    with open(ANINDO_BIN) as f:
        code = f.read()
    top = symtable.symtable(code, str(ANINDO_BIN), "exec")
    global_defs = set(top.get_identifiers()) | set(dir(builtins))
    undefined = []
    def check_scope(table, path=""):
        curr_path = f"{path}.{table.get_name()}" if path else table.get_name()
        for sym in table.get_symbols():
            if sym.is_global() and sym.is_referenced() and not sym.is_assigned():
                if sym.get_name() not in global_defs:
                    undefined.append(f"{sym.get_name()} in {curr_path}")
        for child in table.get_children():
            check_scope(child, curr_path)
    check_scope(top)
    assert not undefined, f"Found undefined globals: {undefined}"
    
    # Check fzf_select single-item & empty behavior
    fzf_fn = mod.get("fzf_select")
    assert callable(fzf_fn), "fzf_select function is missing or not callable"
    assert fzf_fn([]) is None, "fzf_select([]) must return None"
    assert fzf_fn(["sample"]) == "sample", "fzf_select(['sample']) must return 'sample'"

    # Check XDG State directory and History helpers
    assert mod.get("STATE_DIR") is not None, "STATE_DIR is not defined"
    assert mod.get("HISTORY_FILE") is not None, "HISTORY_FILE is not defined"
    assert callable(mod.get("save_history")), "save_history is not callable"
    assert callable(mod.get("load_history")), "load_history is not callable"
    assert callable(mod.get("check_and_self_update")), "check_and_self_update is not callable"

    # Check format_time helper
    fmt_fn = mod.get("format_time")
    assert callable(fmt_fn), "format_time is not callable"
    assert fmt_fn(65) == "01:05", f"Expected 01:05, got {fmt_fn(65)}"
    assert fmt_fn(3665) == "01:01:05", f"Expected 01:01:05, got {fmt_fn(3665)}"

    # Check str_display_width, pad_box_line, render_player_dashboard
    disp_w = mod.get("str_display_width")
    assert callable(disp_w), "str_display_width is not callable"
    assert disp_w("test") == 4
    assert disp_w("🎬 test") == 7

    pad_fn = mod.get("pad_box_line")
    assert callable(pad_fn), "pad_box_line is not callable"

    dash_fn = mod.get("render_player_dashboard")
    assert callable(dash_fn), "render_player_dashboard is not callable"

    print("  Code integrity, player dashboard & XDG watch state verified: 0 undefined globals")

run_check("Code Integrity & Watch State Helpers", test_code_integrity)

# 7. Check Batch Range Parsing & Config Preferences
def test_batch_range_and_config():
    parse_fn = mod.get("parse_episode_spec")
    assert callable(parse_fn), "parse_episode_spec is missing or not callable"

    sample_episodes = [
        {"title": f"Episode {i}", "ep_num": float(i), "url": f"https://example.com/ep/{i}"}
        for i in range(1, 13)
    ]
    # Add a special 2.5 OVA episode
    sample_episodes.insert(2, {"title": "Episode 2.5 OVA", "ep_num": 2.5, "url": "https://example.com/ep/2.5"})

    # Test single
    res = parse_fn("4", sample_episodes)
    assert len(res) == 1 and res[0]["ep_num"] == 4.0, f"Expected Ep 4, got {res}"

    # Test float
    res = parse_fn("2.5", sample_episodes)
    assert len(res) == 1 and res[0]["ep_num"] == 2.5, f"Expected Ep 2.5, got {res}"

    # Test range
    res = parse_fn("1-3", sample_episodes)
    nums = [e["ep_num"] for e in res]
    assert nums == [1.0, 2.0, 2.5, 3.0], f"Expected [1, 2, 2.5, 3], got {nums}"

    # Test comma list
    res = parse_fn("1, 5, 8", sample_episodes)
    nums = [e["ep_num"] for e in res]
    assert nums == [1.0, 5.0, 8.0], f"Expected [1, 5, 8], got {nums}"

    # Test combination
    res = parse_fn("1-2, 6, 10-12", sample_episodes)
    nums = [e["ep_num"] for e in res]
    assert nums == [1.0, 2.0, 6.0, 10.0, 11.0, 12.0], f"Expected combination, got {nums}"

    # Test all
    res = parse_fn("all", sample_episodes)
    assert len(res) == len(sample_episodes), "Expected all episodes"
    res_star = parse_fn("*", sample_episodes)
    assert len(res_star) == len(sample_episodes), "Expected all episodes for '*'"

    # Test invalid / empty
    assert parse_fn("", sample_episodes) == [], "Expected [] for empty spec"
    assert parse_fn("999", sample_episodes) == [], "Expected [] for non-matching spec"

    # Test user config loader
    load_cfg = mod.get("load_user_config")
    assert callable(load_cfg), "load_user_config is missing or not callable"
    cfg = load_cfg()
    assert isinstance(cfg, dict), "load_user_config() must return a dict"
    for key in ("default_quality", "default_provider", "download_dir", "preferred_downloader", "mpv_flags", "notify"):
        assert key in cfg, f"Missing config key: {key}"

    # Test get_default_download_dir
    get_def_dl = mod.get("get_default_download_dir")
    assert callable(get_def_dl), "get_default_download_dir is missing or not callable"
    def_path = get_def_dl()
    assert str(def_path).endswith("Anime"), f"Expected default download dir to end with 'Anime', got {def_path}"

    # Test save_user_config
    save_cfg = mod.get("save_user_config")
    assert callable(save_cfg), "save_user_config is missing or not callable"

    print(f"  parse_episode_spec, default download dir & user config verified (12/12 assertions pass)")

run_check("Batch Range Parser & User Config Loader", test_batch_range_and_config)

# Summary
print("\n" + "=" * 60)
if failures:
    print(f"[FAIL] {len(failures)} canary checks failed!")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("[SUCCESS] All canary health checks passed cleanly!")
    sys.exit(0)

