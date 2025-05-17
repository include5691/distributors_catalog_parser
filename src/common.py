import os

KSIZE_URL = os.getenv("KSIZE_URL")
KSIZE_DESCRIPTION_PROMPT="Оптимизируй текст под SEO для каждого товара. Основной товар - автомагнитолы. Исключи серию и модель магнитолы. Задействуй не более 500 символов. Не дублируй характеристики в краткое описание. Добавь 10 характеристик в виде таблицы с использованием тегов ul и li"

CARSMART_URL = os.getenv("CARSMART_URL")
CARSMART_DESCRIPTION_PROMPT = KSIZE_DESCRIPTION_PROMPT + "Исключи все брэнды магнитол и их производителей из текста. Задействуй не более 500 символов. Не дублируй характеристики в краткое описание. Добавь 10 характеристик в виде таблицы с использованием тегов ul и li"

DISTRIBUTOR_NAME = os.getenv("DISTRIBUTOR_NAME")

OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")