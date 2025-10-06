# validators.py
from __future__ import annotations
import re
from datetime import datetime

# --------- small utils ---------
def _s(x) -> str:
    return "" if x is None else str(x).strip()

def _collapse_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def _ensure_len(s: str, min_len: int, max_len: int, field: str) -> None:
    n = len(s)
    if n < min_len or n > max_len:
        raise ValueError(f"{field} length must be {min_len}–{max_len} chars")

# --------- client fields ---------
def validate_name(raw: str) -> str:
    s = _collapse_spaces(_s(raw))
    if not s:
        raise ValueError("Name is required")
    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ .'\-]+", s):
        raise ValueError("Name contains invalid characters")
    _ensure_len(s, 1, 100, "Name")
    return s

def validate_company_name(raw: str) -> str:
    s = _collapse_spaces(_s(raw))
    if not s:
        raise ValueError("CompanyName is required")
    if not re.fullmatch(r"[A-Za-z0-9 &.,'\-]+", s):
        raise ValueError("CompanyName contains invalid characters")
    _ensure_len(s, 2, 120, "CompanyName")
    return s

def validate_phone(raw: str, allow_plus: bool = False) -> str:
    """
    Strict mode: By default, only digits are allowed; set allow_plus=True to permit a single leading +
    Sanitization: Remove common separators (spaces, (), -, /, .) first; any other non-digit character will cause an error.
    Length constraint: 7–20 digits.
    """
    s = _s(raw)
    # 去掉常见视觉分隔符
    s = re.sub(r"[\s().\-/.]+", "", s)

    if allow_plus:
        # Allow one leading plus sign; the remainder must be numeric.
        if not re.fullmatch(r"\+?\d{7,20}", s):
            raise ValueError("Phone must be digits with optional leading '+', length 7–20")
    else:
        # must be numeric.
        if not s.isdigit():
            raise ValueError("Phone must contain digits only")
        if not (7 <= len(s) <= 20):
            raise ValueError("Phone length must be 7–20 digits")
    return s

def validate_zip(raw: str) -> str:
    s = _s(raw).upper()
    if not s:
        raise ValueError("Zip is required")
    if not re.fullmatch(r"[A-Z0-9 \-]{3,12}", s):
        raise ValueError("Zip must be 3–12 chars of A-Z, 0-9, space or '-'")
    return s

def validate_state(raw: str) -> str:
    s = _collapse_spaces(_s(raw))
    if not s:
        raise ValueError("State is required")
    if not re.fullmatch(r"[A-Za-z0-9 .'\-]+", s):
        raise ValueError("State contains invalid characters")
    _ensure_len(s, 1, 64, "State")
    return s

def validate_address(raw: str, required: bool = True) -> str:
    s = _collapse_spaces(_s(raw))
    if not s:
        if required:
            raise ValueError("Address is required")
        return ""
    if not re.fullmatch(r"[A-Za-z0-9 ,.\/#'\-]+", s):
        raise ValueError("Address contains invalid characters")
    _ensure_len(s, 1, 120, "Address")
    return s

def validate_country(raw: str) -> str:
    s = _collapse_spaces(_s(raw))
    if not s:
        raise ValueError("Country is required")
    _ensure_len(s, 1, 64, "Country")
    return s

def validate_city(raw: str) -> str:
    s = _collapse_spaces(_s(raw))
    if not s:
        raise ValueError("City is required")
    if not re.fullmatch(r"[A-Za-z0-9 .'\-]+", s):
        raise ValueError("City contains invalid characters")
    _ensure_len(s, 1, 64, "City")
    return s

# --------- flight fields ---------
def validate_datetime(raw: str) -> str:
    s = _s(raw)
    try:
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
    except Exception as e:
        raise ValueError("Date must be 'YYYY-MM-DD HH:MM'") from e
    # 5 mins step
    if dt.minute % 5 != 0:
        raise ValueError("Minutes must be in 5-minute steps")
    return s
