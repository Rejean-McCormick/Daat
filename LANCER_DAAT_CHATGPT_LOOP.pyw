# -*- coding: utf-8 -*-
"""Windows double-click launcher; uses pythonw association, never opens CMD."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent / 'tools' / 'DaAT_ChatGPT_Loop.pyw'), run_name='__main__')
