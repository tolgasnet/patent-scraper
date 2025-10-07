# patent_xml.py
"""
Domain model for a USPTO <us-patent-application> record.
Knows how to extract fields and apply CPC logic.
"""

from typing import List, Optional
from lxml import etree as ET


def _txt(node: Optional[ET._Element]) -> Optional[str]:
    t = node.text if node is not None else None
    return t.strip() if t else None

def _norm(s: str) -> str:
    return s.upper().replace(" ", "") if s else ""

class PatentApplication:
    """Wrapper around a <us-patent-application> element with handy accessors."""
    APP_TAG = "{*}us-patent-application"

    def __init__(self, elem: ET._Element):
        self.elem = elem

    # ---- Fields ----
    def pub_date(self) -> Optional[str]:
        # Prefer root attribute @date-publ; fallback to inner doc-id date
        return self.elem.get("date-publ") or _txt(
            self.elem.find(".//{*}publication-reference/{*}document-id/{*}date")
        )

    def title(self) -> Optional[str]:
        return _txt(self.elem.find(".//{*}invention-title"))

    def cpc_codes(self) -> List[str]:
        """Return minimal-normalized CPC codes, good for prefix checks."""
        out: List[str] = []
        for c in self.elem.findall(".//{*}classifications-cpc//{*}classification-cpc"):
            sec = _txt(c.find("./{*}section")) or ""
            cls = _txt(c.find("./{*}class")) or ""
            sub = _txt(c.find("./{*}subclass")) or ""
            mg  = _txt(c.find("./{*}main-group")) or ""
            sg  = _txt(c.find("./{*}subgroup")) or ""
            base = _norm(sec + cls + sub)
            tail = f"{mg}/{sg}" if (mg and sg) else mg or ""
            code = _norm(base + tail)
            if code:
                out.append(code)
        return out

    # ---- CPC filter ----
    def matches_synbio_cpc(self, prefixes: List[str]) -> bool:
        codes = [_norm(c) for c in self.cpc_codes()]
        if not codes:
            return False
        prefs = [_norm(p) for p in (prefixes or [])]
        return any(any(code.startswith(p) for p in prefs) for code in codes)