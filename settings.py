from pathlib import Path
import ast

BASE_DIR = Path(__file__).resolve().parent
report_path = BASE_DIR/'mapping.conf'
with open(report_path) as f:
    MAPPING = ast.literal_eval(f.read())