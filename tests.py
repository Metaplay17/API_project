import requests

test_user_id = 0
test_post_id = 0


def test_create_user():
    global test_user_id
    response1 = requests.post("http://127.0.0.1:5000/users/create", json={
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
    })
    curr_json = response1.json()
    assert response1.status_code == 200, "Wrong Status Code"
    assert curr_json["first_name"] == "John", "Incorrect First name"
    assert curr_json["last_name"] == "Doe", "Incorrect Last name"
    assert curr_json["email"] == "john.doe@example.com", "Incorrect Email name"
    test_user_id = curr_json["id"]
    print('Test "create_user" is successful')


def test_get_user_data(user_id):
    response2 = requests.get(f"http://127.0.0.1:5000/users/{user_id}")
    curr_json = response2.json()
    assert response2.status_code == 200, "Wrong Status Code"
    assert curr_json["first_name"] == "John", "Incorrect First name"
    assert curr_json["last_name"] == "Doe", "Incorrect Last name"
    assert curr_json["email"] == "john.doe@example.com", "Incorrect Email"
    print('Test "get_user_data" is successful')

def test_post_create(author_id):
    global test_post_id
    response3 = requests.post("http://127.0.0.1:5000/posts/create", json={
        "author_id": f"{author_id}",
        "text": "test text"
    })
    curr_json = response3.json()
    assert curr_json["author_id"] == author_id
    assert curr_json["text"] == "test text"
    test_post_id = curr_json["id"]
    print('Test "post_create" is successful')

def test_get_post_data(post_id):
    response4 = requests.get(f"http://127.0.0.1:5000/posts/{post_id}")
    curr_json = response4.json()
    # TODO Не совсем понятно как проверить корректность работы этой функции в данном случае

def test_give_reaction(post_id):
    response5 = requests.post(f"http://127.0.0.1:5000/posts/{post_id}")
    assert response5.status_code == 200, "Wrong Status Code"
    # TODO Аналогично предыдущей функции

def test_get_posts(user_id):
    response6 = requests.get(f"http://127.0.0.1:5000/users/{user_id}/posts")
    assert response6.status_code == 200, "Wrong Status Code"
    # TODO Аналогично предыдущей функции



test_create_user()
test_get_user_data(test_user_id)
test_post_create(test_user_id)