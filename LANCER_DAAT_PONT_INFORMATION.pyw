"""Windows double-click launcher; pythonw avoids CMD windows."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from daat.information_bridge.gui import main
if __name__=='__main__':main()
