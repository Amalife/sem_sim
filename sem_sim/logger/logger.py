import logging
import logging.config
import json
from datetime import datetime
from pathlib import Path

# Настройка логгера для отслеживания хода работы

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": datetime.now().isoformat(),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)

def setup_logging(config_path: Path):
    logs_folder = Path("logs")
    if not logs_folder.is_dir():
        logs_folder.mkdir()

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["formatters"]["json"]["()"] = JSONFormatter

    logging.config.dictConfig(config)

app_logger = logging.getLogger()