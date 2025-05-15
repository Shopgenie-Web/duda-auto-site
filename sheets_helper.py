import os, gspread, tempfile, pathlib, json

def _creds_path():
    # Highest priority: explicit path
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    # Fallback: inline JSON
    sa_json = os.getenv("GOOGLE_SA_JSON")
    if sa_json:
        tmp = pathlib.Path("/tmp/creds.json")
        if not tmp.exists():              # write once per dyno boot
            tmp.write_text(sa_json)
        return str(tmp)

    raise RuntimeError("Google SA credentials not found")

_gc = gspread.service_account(filename=_creds_path())
SHEET = _gc.open_by_key(os.environ["SHEET_ID"]).sheet1   # 1st tab

# Map header titles → 1‑based column indexes once at startup
_HEADERS = {h: i+1 for i, h in enumerate(SHEET.row_values(1))}

def get_row_dict(row_num: int):
    """Return a dict keyed by header for the given (1‑based) row."""
    values = SHEET.row_values(row_num)
    return {h: values[i] if i < len(values) else "" for h, i in _HEADERS.items()}

def set_processed(row_num: int):
    col = _HEADERS.get("processed")
    if col:
        SHEET.update_cell(row_num, col, "yes")
