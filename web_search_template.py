"""
Aetheron — Web Search Utility Template
--------------------------------------

This file provides a documentation-safe template for the project
discovery system used in the Aetheron backend.

The real implementation (see web_search.py) includes:
• SerpAPI-powered Google search queries
• URL classification (website, twitter, telegram, discord)
• HTML extraction via BeautifulSoup
• Description, team, and roadmap parsing
• Structured content normalization
• Error handling and timeout-protected scraping

All logic, network calls, and parsing algorithms are removed here.
Only structure, signatures, and output shapes are preserved.
"""


# -------------------------------------------------------------------------
# TEMPLATE SEARCH FUNCTION (STRUCTURE ONLY)
# -------------------------------------------------------------------------

def search_project_info(query: str, api_key: str = None):
    """
    Template project discovery helper.

    REAL BACKEND (ref: web_search.py):
    • Performs a SerpAPI Google search
    • Extracts organic results
    • Categorizes URLs into socials + websites
    • Scrapes the primary website for:
        - description_extract
        - team_extract
        - roadmap_extract
    • Uses keyword detection for semantic blocks
    • Returns a structured dictionary of findings

    TEMPLATE VERSION:
    • Returns a fixed-placeholder structure only.
    """

    return {
        "website_candidates": [],
        "twitter_candidates": [],
        "telegram_candidates": [],
        "discord_candidates": [],
        "description_extract": None,
        "team_extract": None,
        "roadmap_extract": None,
    }
