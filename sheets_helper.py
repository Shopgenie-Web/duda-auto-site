import os, gspread

_gc = gspread.service_account(
    filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    or None  # if CREDS written to /tmp via GOOGLE_SA_JSON, gspread picks it up
)

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
