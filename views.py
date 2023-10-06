import http.client

from flask import Flask, request, Response
import json
from models import User, Post
from validate_email import validate_email
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)

def get_user_id_by_post_id(post_id):
    with open('app/data/posts.json', 'r') as data:
        curr_data = json.load(data)
    return curr_data[post_id]["author_id"]


def get_name_lastname_by_id(user_id):
    with open('app/data/users.json', 'r') as data:
        curr_data = json.load(data)
    return curr_data[user_id]["first_name"], curr_data[user_id]['last_name']


def get_new_user_id():
    return str(uuid.uuid4())


def get_new_post_id():
    return str(uuid.uuid4())


# Возвращаем количество реакций на всех постах пользователя
def get_sum_of_reactions(user_id):
    with open('app/data/users.json', 'r') as curr_json:
        curr_data = json.load(curr_json)
    return curr_data[str(user_id)]["total_reactions"]


# Создание пользователя
@app.post("/users/create")
def index_create_user():
    request_data = request.get_json()
    if validate_email(request_data["email"]):  # Проверка корректности email
        curr_user = User(  # Класс User используется как конструктор словаря для экспорта или сохранения данных
            get_new_user_id(),
            request_data["first_name"],
            request_data[
                "last_name"
            ],  # Создание объекта класса User для удобного экспорта данных
            request_data["email"],
        )
        with open(
                "app/data/users.json", "r"
        ) as data:  # Открываем json с данными пользователей
            curr_data = json.load(data)

        curr_data[
            curr_user.id
        ] = curr_user.get_dict()  # Создаём новую пару ключ - значение
        # с ключом - id нового пользователя

        with open("app/data/users.json", "w") as users:  # Сохраняем данные пользователей
            json.dump(curr_data, users)

        return (
            curr_user.get_dict()
        )  # Вот пример использования этого конструктора с помощью get_dict()
    else:
        return "Incorrect email"


# Получение данных пользователя по id
@app.get("/users/<user_id>")
def index_get_user_data(user_id):
    with open("app/data/users.json", "r") as curr_json:
        data = json.load(curr_json)  # Загружаем данные всех пользователей
        try:
            curr_user = data[
                str(user_id)
            ]  # Проверяем существование пользователя с заданным id
            return curr_user
        except KeyError:
            return "User does not exist."


# Создание поста
@app.post("/posts/create")
def index_create_post():
    post_data = request.get_json()
    author_id = post_data["author_id"]  # Достаём данные из json request
    post_text = post_data["text"]
    curr_post = Post(
        get_new_post_id(), author_id, post_text
    )  # Класс Post так же используется
    # как конструктор удобной хеш-таблицы
    with open("app/data/users.json", "r") as data:  # Загружаем данные всех пользователей
        curr_data = json.load(data)

    curr_data[str(author_id)]["posts"].append(
        curr_post.id
    )  # Добавляем id поста в список постов пользователя

    with open("app/data/users.json", "w") as users:  # Сохраняем данные пользователей
        json.dump(curr_data, users)

    with open("app/data/posts.json", "r") as data:  # Загружаем данные постов
        curr_data = json.load(data)

    curr_data[
        str(curr_post.id)
    ] = curr_post.get_dict()  # Создаем новую пару ключ - значение (с ключом - id поста
    # и значением - хеш-таблица, полученная с помощью конструктора Post (ф-ия get_dict())

    with open(
            "app/data/posts.json", "w"
    ) as posts:  # Сохраняем изменённые данные постов
        json.dump(curr_data, posts)

    return curr_post.get_dict()  # Возвращаем данные по созданному посту


# Получение данных поста по id
@app.get("/posts/<post_id>")
def index_get_post_data(post_id):
    with open("app/data/posts.json", "r") as curr_json:
        data = json.load(curr_json)
        try:
            curr_post = data[str(post_id)]
            return curr_post
        except KeyError:
            return "Post does not exist."


# Поставить реакцию посту по id
@app.post("/posts/<post_id>/reaction")
def index_give_reaction(post_id):
    text = request.get_json()
    with open("app/data/posts.json", "r") as curr_json:
        post_data = json.load(curr_json)
    try:
        post_data[str(post_id)]["reactions"].append(
            text["reaction"]
        )  # Добавляем текст реакции в список реакций поста
        post_data[str(post_id)]["total_reactions"] += 1
        with open("app/data/users.json", "r") as data:
            user_data = json.load(data)
        user_data[str(get_user_id_by_post_id(post_id))]["total_reactions"] += 1
        with open("app/data/users.json", "w") as curr_json:  # Обновляем счётчик реакций поьзователя
            json.dump(user_data, curr_json)
        with open("app/data/posts.json", "w") as curr_json:  # Сохраняем данные постов
            json.dump(post_data, curr_json)
        return Response(http.HTTPStatus.OK)
    except KeyError:
        return "Post does not exist."


# Получение списка постов пользователя, отсортированных по количеству реакций
@app.get("/users/<user_id>/posts")
def index_get_sorted_reactions_list(user_id):
    sort_method = request.get_json()["sort"]  # Достаём вид сортировки из request
    with open("app/data/users.json", "r") as curr_json:
        user_data = json.load(curr_json)

    with open("app/data/posts.json", "r") as curr_json:
        post_data = json.load(curr_json)

    curr_user_data = user_data[str(user_id)]
    posts_list = []
    for post_id in curr_user_data["posts"]:
        posts_list.append([post_data[post_id]["total_reactions"], post_id])
    # Создаём двумерный список вида [кол-во реакций, id поста], таким образом, при стандартной сортировке списка
    # все посты будут отсортированы именно по количеству реакций
    if sort_method == "asc":
        posts_list.sort()  # Сортируем список
    elif sort_method == "desc":
        posts_list.sort(reverse=True)
    else:
        return "Incorrect sorting method"

    output = {"posts": []}
    for (
            post
    ) in (
            posts_list
    ):  # Помещаем все посты в отсортированном порядке в список и возвращем в качестве response
        output["posts"].append(post_data[str(post[1])])

    return output


# Получение первых 10 пользователей по кол-ву реакций
@app.get("/users/leaderboard")
def index_get_leaderboard():
    with open("app/data/users.json") as curr_json:
        users_data = json.load(curr_json)
        # Загружаем данные
    with open("app/data/posts.json") as curr_json:
        posts_data = json.load(curr_json)

    users_list = []

    for (
            key, value
    ) in (
            users_data.items()
    ):  # Создаем двумерный список вида [кол-во реакций, id]
        users_list.append(
            [
                get_sum_of_reactions(key),
                key,
            ]
        )
        if len(users_list) >= 10:  # Ограничиваем длину списка до 10
            break

    names = [
        f"{get_name_lastname_by_id(user[1])[0]} {get_name_lastname_by_id(user[1])[1]}" for user in users_list
    ]  # Заполняем список имён строками вида "имя фамилия"
    reactions_count = [
        user[0] for user in users_list
    ]  # Заполняем список количеств реакций,
    # соответствующих пользователям
    type_of_showing = request.get_json()["type"]
    if type_of_showing == "graph":
        plt.figure(figsize=(16, 10))
        ax = plt.subplot()

        ax.bar(names, reactions_count)

        ax.set_ylabel("Количество реакций")
        ax.set_xlabel("Пользователи")

        plt.savefig("leaderboard.png")

        return "<img src=leaderboard.png>"

    if type_of_showing == "list":
        type_of_sorting = request.get_json()["sort"]
        if type_of_sorting == "asc":
            users_list.sort()
        if type_of_sorting == "desc":  # Выполняем сортировку в соответствии с запросом
            users_list.sort(reverse=True)
        output = {"users": []}
        for user in users_list:
            output["users"].append(users_data[user[1]])
        return output
