# celery_worker_template.py — Aetheron X402 Worker Template

import os
import re
import time
import json
from datetime import datetime

from dotenv import load_dotenv
from celery import Celery

from r2_client import r2_upload_bytes  # structural import
from pdf_utils import build_aetheron_pdf
from ledger_utils import add_entry
from web_search import search_project_info  # structural import

# -------------------------------------------------------------------------
# ENV + BOOTSTRAP
# -------------------------------------------------------------------------

load_dotenv()

SNAPSHOT_DIR = "./contract_snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def snapshot_path(address, network):
    """Builds a consistent path for snapshot storage."""
    safe = f"{network}_{address}".replace("/", "_")
    return os.path.join(SNAPSHOT_DIR, safe + ".json")


def store_contract_snapshot(address, network, data):
    """Placeholder: store contract snapshot JSON."""
    # In production this writes full data to disk.
    pass


def load_last_snapshot(address, network):
    """Placeholder: load previous snapshot JSON."""
    # In production this reads from disk if present.
    return None


print("CELERY WORKER TEMPLATE LOADING")


# -------------------------------------------------------------------------
# ENV VARS (STRUCTURE ONLY)
# -------------------------------------------------------------------------

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
HONEYPOT_API_KEY = os.getenv("HONEYPOT_API_KEY")

BUBBLEMAP_MODE = os.getenv("BUBBLEMAP_MODE", "both").lower()
BUBBLEMAP_MAX_HOLDERS = int(os.getenv("BUBBLEMAP_MAX_HOLDERS", "10"))
BUBBLEMAP_MAX_ETH_TX = int(os.getenv("BUBBLEMAP_MAX_ETH_TX", "250"))
BUBBLEMAP_MAX_SOL_TX = int(os.getenv("BUBBLEMAP_MAX_SOL_TX", "100"))

R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_BASE = os.getenv("R2_PUBLIC_BASE")


# -------------------------------------------------------------------------
# CELERY APP + CONFIG
# -------------------------------------------------------------------------

celery = Celery(
    "aetheron",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery.conf.update(
    worker_max_tasks_per_child=1,
    worker_max_memory_per_child=250000,  # 250 MB
    worker_prefetch_multiplier=1,
    task_acks_late=False,
)


# -------------------------------------------------------------------------
# MARKDOWN CLEANER (STRUCTURE ONLY)
# -------------------------------------------------------------------------

def clean_markdown(md: str) -> str:
    """
    Template markdown cleaner.

    In the real worker, this normalizes output text so it is compatible
    with the PDF engine and TXT export, keeping metrics and structure.
    """
    text = (md or "").strip()

    # Example of structural cleanup steps (logic simplified for template):
    text = re.sub(r"(?m)^---+$", "", text)         # horizontal rules
    text = re.sub(r"\*\*", "", text)               # bold markers
    text = text.replace("(/10)", "0/10")           # normalize broken metrics

    return text.strip()


# -------------------------------------------------------------------------
# UTILS — TIMESTAMP + FILE GENERATION (TEMPLATE)
# -------------------------------------------------------------------------

def now_stamp():
    """Returns a UTC timestamp string."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def generate_pdf(asset_id, wallet, title, subtitle, md_text):
    """
    Template PDF generator.

    In the real worker:
    - Builds a styled PDF via build_aetheron_pdf(...)
    - Uploads bytes to R2 via r2_upload_bytes(...)
    - Returns (filename, public_url)
    """
    # Placeholder layout: call the real pdf_utils in production.
    buffer, fname = build_aetheron_pdf(
        asset_id=asset_id,
        timestamp=now_stamp(),
        wallet=wallet,
        title=title,
        subtitle=subtitle,
        md_text=md_text,
    )

    # Placeholder upload flow:
    r2_url = r2_upload_bytes(buffer.getvalue(), fname)
    return fname, r2_url


def generate_txt(md_text):
    """
    Template TXT generator.

    In the real worker:
    - Encodes text with UTF-8 BOM for full compatibility.
    - Uploads bytes to R2 and returns (filename, public_url).
    """
    fname = f"aetheron_asset_{int(time.time())}.txt"
    data = "\ufeff" + (md_text or "")
    data_bytes = data.encode("utf-8")
    r2_url = r2_upload_bytes(data_bytes, fname)
    return fname, r2_url


def run_llm(system_prompt, user_payload, style_note):
    """
    Template text-generation helper.

    In the real worker:
    - Sends a structured request to a text-generation backend.
    - Applies consistent temperature, length, and format.
    - Returns cleaned markdown via clean_markdown().
    """
    # Template placeholder:
    placeholder = f"{system_prompt}\n\nUSER:\n{user_payload}\n\n[Generated content here]"
    return clean_markdown(placeholder)


# -------------------------------------------------------------------------
# EXTERNAL DATA HELPERS (STRUCTURAL STUBS)
# -------------------------------------------------------------------------
# These helpers encapsulate:
# - project info aggregation
# - holder / liquidity lookups
# - risk / metadata fetches
# - contract / token info inspection
# In the template, they only expose signatures and basic shapes.

def fetch_honeypot_analysis(address, chain_id=None):
    """Fetches token safety / tax / risk metadata from external services."""
    return {"status": "ok", "address": address, "chain_id": chain_id}


def fetch_dexscreener_pair_api_holders(chain, pair_address):
    """Fetches top holders via Dexscreener pair API."""
    return {"holders": [], "source": "dexscreener_api_pair"}


def fetch_dexscreener_token_holders_eth(token_address):
    """Fetches top holders via Dexscreener token page (Ethereum)."""
    return {"holders": [], "source": "dexscreener_token_eth"}


def fetch_dexscreener_holders(pair_address):
    """Fetches top holders via Dexscreener HTML for Solana pairs."""
    return {"holders": [], "source": "dexscreener_html"}


def fetch_ethereum_dexscreener_holders(pair_address):
    """Fetches top holders via Dexscreener HTML for Ethereum pairs."""
    return {"holders": [], "source": "dexscreener_eth_html"}


def fetch_project_profile(token_address, token_symbol, token_name, network):
    """
    High-level wrapper to build a project profile.

    In the real worker:
    - Queries search_project_info(...)
    - Scrapes candidate sites
    - Extracts sections like team, roadmap, description, whitepaper
    """
    return {
        "network": network,
        "token_address": token_address,
        "token_symbol": token_symbol,
        "token_name": token_name,
        "website_candidates": [],
        "roadmap_extract": "",
        "team_extract": "",
        "description_extract": "",
        "whitepaper_extract": "",
    }


# -------------------------------------------------------------------------
# CELERY TASKS (STRUCTURAL FOR 4 CORE COMPONENTS)
# -------------------------------------------------------------------------

# 1 — Prompt Optimizer
@celery.task(name="process_prompt")
def process_prompt(asset_id, user_text, out_format, wallet):
    """
    Background flow for generating a structured text asset
    from an initial user prompt.
    """
    system_prompt = "Template system prompt for prompt optimization."
    style_note = "Template style note for formatting."
    md_clean = run_llm(system_prompt, user_text, style_note)

    final_md = f"Prompt Quality Check: Optimization run completed.\n\n{md_clean}"
    fmt = (out_format or "pdf").lower()

    if fmt == "txt":
        filename, url = generate_txt(final_md)
    else:
        filename, url = generate_pdf(
            asset_id,
            wallet or "DEMO_OK",
            title="Prompt Optimizer",
            subtitle="Prompt Refinement & Analysis",
            md_text=final_md,
        )

    add_entry(
        asset_id=asset_id,
        wallet=(wallet or "DEMO_OK"),
        tx_sig=None,
        component="prompt-optimizer",
        price=0.25,
        status="success",
        filename=filename,
    )

    return {"download_url": url, "filename": filename, "format": fmt}


# 2 — Code Explainer
@celery.task(name="process_code")
def process_code(asset_id, code_text, out_format, wallet):
    """
    Background flow for analyzing and explaining code input.
    """
    system_prompt = "Template system prompt for code analysis."
    style_note = "Template style note for code structure."
    md_clean = run_llm(system_prompt, code_text, style_note)

    final_md = f"Code Intelligence Asset\n\n{md_clean}"
    fmt = (out_format or "pdf").lower()

    if fmt == "txt":
        filename, url = generate_txt(final_md)
    else:
        filename, url = generate_pdf(
            asset_id,
            wallet or "DEMO_OK",
            title="Code Explainer",
            subtitle="Structure, Behavior & Risk Overview",
            md_text=final_md,
        )

    add_entry(
        asset_id=asset_id,
        wallet=(wallet or "DEMO_OK"),
        tx_sig=None,
        component="code-explainer",
        price=0.50,
        status="success",
        filename=filename,
    )

    return {"download_url": url, "filename": filename, "format": fmt}


# 3 — Prompt Tester (PersonaSim)
@celery.task(name="process_tester")
def process_tester(asset_id, user_text, out_format, wallet):
    """
    Background flow for testing prompts in different configurations.
    """
    system_prompt = "Template system prompt for prompt testing."
    style_note = "Template style note for simulation output."
    md_clean = run_llm(system_prompt, user_text, style_note)

    final_md = f"Prompt Test Session\n\n{md_clean}"
    fmt = (out_format or "pdf").lower()

    if fmt == "txt":
        filename, url = generate_txt(final_md)
    else:
        filename, url = generate_pdf(
            asset_id,
            wallet or "DEMO_OK",
            title="Prompt Tester",
            subtitle="Configuration & Response Overview",
            md_text=final_md,
        )

    add_entry(
        asset_id=asset_id,
        wallet=(wallet or "DEMO_OK"),
        tx_sig=None,
        component="prompt-tester",
        price=0.50,
        status="success",
        filename=filename,
    )

    return {"download_url": url, "filename": filename, "format": fmt}


# 4 — Contract Intel / Token Analyzer
@celery.task(name="process_contract_intel")
def process_contract_intel(asset_id, address, network, out_format, wallet):
    """
    Background flow for aggregating contract / token intelligence.
    Combines on-chain metadata, holder info, and external project details.
    """
    # Template: fetch structural data only
    project_profile = fetch_project_profile(
        token_address=address,
        token_symbol="TKN",
        token_name="Token Name",
        network=network,
    )
    honeypot_info = fetch_honeypot_analysis(address)
    holder_info = {
        "dexscreener_pair": fetch_dexscreener_pair_api_holders(network, "PAIR_ADDRESS"),
        "dexscreener_token": fetch_dexscreener_token_holders_eth(address),
    }

    # Build a markdown-style summary for demonstration
    md_sections = [
        f"Contract Address: {address}",
        f"Network: {network}",
        "",
        "Project Profile (Template):",
        json.dumps(project_profile, indent=2),
        "",
        "Risk / Safety Snapshot (Template):",
        json.dumps(honeypot_info, indent=2),
        "",
        "Holder Overview (Template):",
        json.dumps(holder_info, indent=2),
    ]
    final_md = "\n".join(md_sections)

    fmt = (out_format or "pdf").lower()
    if fmt == "txt":
        filename, url = generate_txt(final_md)
    else:
        filename, url = generate_pdf(
            asset_id,
            wallet or "DEMO_OK",
            title="Contract Intelligence",
            subtitle="Template Analysis Snapshot",
            md_text=final_md,
        )

    add_entry(
        asset_id=asset_id,
        wallet=(wallet or "DEMO_OK"),
        tx_sig=None,
        component="contract-intel",
        price=1.00,
        status="success",
        filename=filename,
    )

    return {"download_url": url, "filename": filename, "format": fmt}
