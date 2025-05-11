from sem_sim.configuration.configuration import configuration
from sem_sim.logger.logger import setup_logging
from sem_sim.use_cases.sent_processor import SentProcessor

logger_config_path = configuration.project_root / "logger_config.json"
setup_logging(
    config_path=logger_config_path
)

TEST_SENT = "сегодня ночью наше судно отплывает по расписанию"

TEST_PHRASE = "корабль"


if __name__ == "__main__":
    proccessor = SentProcessor()

    print(proccessor.find_word(TEST_SENT, TEST_PHRASE))