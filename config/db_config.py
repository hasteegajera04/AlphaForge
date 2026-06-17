from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports" / "validation"
STOCKS_FILE = CONFIG_DIR / "stocks.json"

DB_TYPE = "sqlite"
DB_PATH = DATA_DIR / "algo_trading.db"
