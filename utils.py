import json
from json import JSONDecodeError


def get_posts_all() -> list[dict]:
    """Возвращает все посты"""
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return "Файл не найден"
    except JSONDecodeError:
        return "Файл не удалось прочитать"  # error may be appear cause file is not json


def get_comments_all() -> list[dict]:
    """Возвращает все комментарии"""
    try:
        with open('data/comments.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return "Файл не найден"
    except JSONDecodeError:
        return "Файл не удалось прочитать"  # error may be appear cause file is not json


def get_posts_by_user(user_name) -> list[dict]:
    """Возвращает посты определенного пользователя.
     Функция должна вызывать ошибку `ValueError` если такого пользователя нет и пустой список,
    если у пользователя нет постов"""
    posts_list = []
    for post in get_posts_all():
        if user_name.lower() == post["poster_name"].lower():
            posts_list.append(post)
    if len(posts_list) == 0:
        raise ValueError('У этого пользователя нет постов, либо такого пользователя не существует')
    return posts_list

# print(get_posts_by_user("larr"))


def get_comments_by_post_id(post_id) -> list[dict]:
    """Возвращает комментарии определенного поста.
    Функция должна вызывать ошибку `ValueError`
    если такого поста нет и пустой список, если у поста нет комментов"""
    comments_list = []
    posts = get_posts_all()
    post_ids = [post['pk'] for post in posts]
    for comment in get_comments_all():
        if post_id == comment["post_id"]:
            comments_list.append(comment)
        if post_id not in post_ids:
            raise ValueError('Введён несуществующий ID')
    return comments_list

# print(get_comments_by_post_id(1))


def search_for_posts(query) -> list[dict]:
    """Возвращает список постов по ключевому слову"""
    posts_list = []
    for post in get_posts_all():
        if query.lower() in post["content"] or query.title() in post["content"]:
            posts_list.append(post)
        elif query.lower() in post['poster_name'] or query.title() in post['poster_name']:
            posts_list.append(post)
    if len(posts_list) == 0:
        raise ValueError('Постов с содержанием этого слова не найдено')
    return posts_list


def get_post_by_pk(pk):
    """Возвращает один пост по его идентификатору"""
    for post in get_posts_all():
        if pk == post['pk']:
            return post


def get_post_by_post_id(post_id):
    """Находит пост по его id"""
    try:
        for post in get_posts_all():
            if post_id == int(post['pk']):
                return post
    except ValueError:
        return "Такого поста не существует"
