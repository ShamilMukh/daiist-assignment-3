"""Central configuration. Everything tunable lives here."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

CORPUS_DIR = ROOT / "corpus"      # indexed by `main.py index`
ADDON_DIR = ROOT / "addon"        # held back for the before/after experiment
INDEX_DIR = ROOT / "index"        # ChromaDB + query-embedding cache (committed)
EVAL_DIR = ROOT / "eval"

EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-2")   # SETUP.md: free tier ~1,000 texts/day
EMBED_DIM = 768                   # truncated (Matryoshka); vectors are re-normalised
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini-2.5-flash")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "gemini-2.5-flash")

# chunking
MAX_WORDS = 400                   # structure-based: split an article only above this
FIXED_WORDS = 400                 # fixed-window baseline
FIXED_OVERLAP = 60

# designs: name -> (collection kind, hybrid?)
DESIGNS = {
    "fixed": ("fixed", False),            # baseline: structure-blind sliding window, vectors only
    "article": ("article", False),        # structure-based (one chunk per Article/Annex), vectors only
    "article_hybrid": ("article", True),  # structure-based + BM25, fused with RRF
}
# Production design used by the MCP server. Set from the numbers in REPORT.md.
DEFAULT_DESIGN = os.getenv("RAG_DESIGN", "article_hybrid")

# EUR-Lex texts are reusable under Commission Decision 2011/833/EU (attribution required).
CORPUS = {
    "gdpr":     dict(celex="32016R0679", dir="corpus", title="GDPR (Regulation (EU) 2016/679)"),
    "ai_act":   dict(celex="32024R1689", dir="corpus", title="AI Act (Regulation (EU) 2024/1689)"),
    "eprivacy": dict(celex="32002L0058", dir="corpus", title="ePrivacy Directive (2002/58/EC)"),
    # held out on purpose: answers questions the core corpus cannot
    "data_act": dict(celex="32023R2854", dir="addon",  title="Data Act (Regulation (EU) 2023/2854)"),
}

def get_key() -> str:
    """API key via the course helper (api_key.load_api_key), falling back to the environment."""
    try:
        from api_key import load_api_key
        k = load_api_key()
        return k[0] if isinstance(k, tuple) else k
    except ImportError:
        return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")


NOT_FOUND = "NOT_FOUND"           # an answer starting with this token is a refusal
