import streamlit as st
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
    processor = SentProcessor()
    st.title("Поиск слова в тексте")

    # Выбор способа ввода
    input_method = st.radio("Выбор способа ввода:", ("Прямой ввод", "Загрузить файл"))

    if input_method == "Прямой ввод":
        # Прямой ввод текста
        test_sent = st.text_area("Введите предложение:", value="Сегодня ночью наше судно отплывает по расписанию", height=100)
        test_phrase = st.text_input("Введите искомое слово:", value="Корабль")
    else:
        # Загрузка текста из файла
        uploaded_file = st.file_uploader("Загрузите файл (.txt)", type=["txt"])
        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8").splitlines()
            if len(content) >= 2:
                test_sent = content[0].strip()
                test_phrase = content[1].strip()
            else:
                st.warning("Файл должен содержать как минимум две строки.")
                st.stop()

    # Кнопка для запуска поиска
    if st.button("Выполнить"):
        if test_sent and test_phrase:
            with st.spinner("Идет обработка..."):
                result = processor.find_word(test_sent, test_phrase)
                if result is not None:
                    print(result)
                    st.success(f"Похожее слово найдено: {result[1][0]} в позиции {result[0][0][1]} с уверенностью в {round(result[0][0][0], 3)}")
                else:
                    st.error("Ничего не найдено!")
        else:
            st.error("Пожалуйста, введите предложение и искомое слово.")