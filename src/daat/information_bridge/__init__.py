"""DaaT information bridge: source-aware preparation, not Kristal authoring.

Local proposed API; it neither grants provider rights nor adopts owner contracts.
"""
from .model import Rights, SourceItem, Fragment, BridgeError, Limits
from .registry import SourceRegistry, AccessPlanner
from .ingest import LocalIngestor, PreparedCorpus
from .context import ContextBuilder, verify_export

__all__ = ['Rights', 'SourceItem', 'Fragment', 'BridgeError', 'Limits',
           'SourceRegistry', 'AccessPlanner', 'LocalIngestor', 'PreparedCorpus',
           'ContextBuilder', 'verify_export']
