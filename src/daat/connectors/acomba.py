"""Private offline Acomba *export* reader, no SDK/ODBC and absolutely no write path.

Entity kind and monetary-column semantics must be declared by an accountant or
reviewer; unknown layouts remain unreviewed source evidence, not ledger truth.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from ..errors import AdmissionError
from ..source import Evidence, ReadLimits
from .common import read_dataset

_ENTITY_KINDS = {"customers", "suppliers", "invoices", "payments", "entries", "credit_notes", "balances"}
_MONEY_FIELDS = {"amount", "total", "debit", "credit", "tax", "subtotal", "balance", "paid", "due", "montant", "solde"}


def read_acomba(path: Path, limits: ReadLimits, label: str, record_type: str | None) -> tuple[list[Evidence], str, list[str]]:
    if record_type not in _ENTITY_KINDS:
        raise AdmissionError("SOURCE_ACOMBA_UNTYPED", "Explicit accounting export record type is required")
    records, sha = read_dataset(path, limits, label)
    warnings = ["private_offline_export_only", "no_sdk_no_odbc_no_ledger_write"]
    for record in records:
        fields = record.data
        for key, value in fields.items():
            if key.lower() in _MONEY_FIELDS and value not in (None, ""):
                # Preserve source representation. No implicit currency conversion.
                if isinstance(value, float) or isinstance(value, bool):
                    raise AdmissionError("SOURCE_ACOMBA_AMBIGUOUS", "Float/bool money value is unsafe")
                try:
                    money = Decimal(str(value))
                except InvalidOperation as exc:
                    raise AdmissionError("SOURCE_ACOMBA_AMBIGUOUS", "Invalid decimal accounting value") from exc
                if not money.is_finite():
                    raise AdmissionError("SOURCE_ACOMBA_AMBIGUOUS", "Non-finite accounting value")
        if record_type in {"invoices", "payments", "entries", "credit_notes", "balances"}:
            if not any(name.lower() in ("currency", "devise", "code_devise") and fields[name]
                       for name in fields):
                raise AdmissionError("SOURCE_ACOMBA_AMBIGUOUS", "Accounting amount lacks source currency")
    typed = [Evidence(item.anchor_kind, item.location, item.source_sha256,
                      dict(item.data), "accounting_export_" + record_type, item.warnings)
             for item in records]
    return typed, sha, warnings
