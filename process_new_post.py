from telethon.tl.functions.messages import GetDiscussionMessageRequest
from telethon.tl.types import PeerChannel
from get_message import get_message
from datetime import datetime
import os

COMMENTS_LOG = "comments_log.txt"  # сюда будем сохранять все комментарии

def get_next_comment_number():
    """Определить следующий номер комментария на основе уже сохранённых"""
    if not os.path.exists(COMMENTS_LOG):
        return 1

    with open(COMMENTS_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    count = sum(1 for line in lines if line.strip().startswith("#"))
    return count + 1

async def process_new_post(client, channel, message):
    post_id = message.id
    post_text = message.message

    print(f"📝 Готовим комментарий для поста ID {post_id}...")

    discussion = await client(GetDiscussionMessageRequest(channel, post_id))
    linked_chat = discussion.messages[0].peer_id.channel_id
    linked_message_id = discussion.messages[0].id

    # Получаем список комментариев в связанной группе
    # comments = []
    # async for comment in client.iter_messages(linked_chat, reply_to=discussion.messages[0].id):
    #     print(comment)
    #     if comment.message:  # Проверяем, что это текстовое сообщение
    #         comments.append(comment.message)

    new_comment = await get_message(post_text)
    print(f"📝 Новый комментарий: {new_comment}")

    # Готовим данные для сохранения
    # comment_number = get_next_comment_number()
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # log_entry = (
    #     f"#{comment_number} | {current_time}\n"
    #     f"Post ID {post_id}\n"
    #     f"Comment: \"{new_comment}\"\n\n"
    # )

    # Сохраняем в файл
    # with open(COMMENTS_LOG, "a", encoding="utf-8") as f:
    #     f.write(log_entry)

    comment = await client.send_message(linked_chat, new_comment, reply_to=linked_message_id)

    print(comment)

    discussion_entity = await client.get_entity(PeerChannel(linked_chat))
    discussion_username = discussion_entity.username

    # Пересылаем комментарий
    comment_link = f"https://t.me/{discussion_username}/{comment.id}"

    group_name = "CommentsForGGKIT"

    group_entity = await client.get_entity(group_name)

    # Отправка ссылки на комментарий
    await client.send_message(group_entity, f"Новый комментарий: {new_comment}\n🔗 {comment_link}")

    print(f"✅ Комментарий отправлен на сообщение {linked_message_id}.")
