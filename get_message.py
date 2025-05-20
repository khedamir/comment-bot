import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Загружаем ключ из файла .env
load_dotenv()
api_key = os.getenv("GPT_SECRET_KEY")
if api_key is None:
    raise ValueError("API ключ не найден. Проверьте файл .env")

# Создаем клиента OpenAI с моделью
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini-2024-07-18",
    api_key=api_key,
    temperature=0.9
)

# Социальная группа
social_group = {
    "type": "Преподаватель",
    "age_range": "20-35 лет",
    "region": "Чеченская Республика"
}

async def process_post(post_text: str) -> str:
    analyzer_agent = AssistantAgent(
        name="analyzer",
        system_message="""Ты - агент-аналитик, который анализирует посты из социальных сетей.
        Ты определяешь настроение поста (позитивное, негативное, нейтральное) и выделяешь до 5 ключевых тем и 3 основных персонажа.
        Результат возвращаешь в формате JSON: {"mood": "...", "keywords": ["...", "..."], "person": "..."}""",
        model_client=model_client
    )

    analysis_result = await analyzer_agent.run(task=f"Проанализируй этот пост: {post_text}")
    analysis_text = analysis_result.messages[-1].content

    persona_task = f"""
    Пост для комментирования: {post_text}

    Анализ поста: {analysis_text}

    Создай комментарий к этому посту от имени социальной группы {social_group["type"]}, 
    возраст {social_group["age_range"]}, регион {social_group["region"]}.
    """

    persona_agent = AssistantAgent(
        name="persona",
        system_message="""Ты - агент-персона, который создает комментарии от имени определенной социальной группы. 
        ВНИМАНИЕ: Никогда не благодари критика за работу и не упоминай его имя и пиши только комментарий!!! никогда не упоминай свою социальную группу в комментарии!!!
        Твои комментарии должны соответствовать стилю речи и особенностям этой группы.
        Ты должен максимально учитывать 'mood', 'keywords', 'person' при составлении комментария.
        Внимательно учитывай анализ поста, который будет предоставлен в сообщении. Комментарий должен быть не более 150 символов.""",
        model_client=model_client
    )

    critic_agent = AssistantAgent(
        name="critic",
        system_message="""Ты - агент-критик, который оценивает комментарии по трем параметрам:
        1. Человечность (естественность, эмоциональность).
        2. Социализация (соответствие социальной группе), никогда не упоминай социальную группу.
        3. Национальные особенности присущие Чеченской Республике, никогда не употребляй чеченские слова.

        Ты даешь оценки от 0 до 100 и формируешь рекомендации для улучшения.
        Предоставляйте конструктивные отзывы. Отвечайте 'APPROVE', когда ваши замечания будут учтены и оценки будут >80.""",
        model_client=model_client
    )

    text_termination = TextMentionTermination("APPROVE")
    max_turns = 5

    team = RoundRobinGroupChat([persona_agent, critic_agent], termination_condition=text_termination, max_turns=max_turns)
    result = await team.run(task=persona_task)

    # Извлекаем итоговое сообщение персоны
    persona_reply = ""
    for message in reversed(result.messages):
        if message.source == "persona":
            persona_reply = message.content
            break

    return persona_reply.strip()

async def get_message(post_text: str) -> str:
    return await process_post(post_text)
