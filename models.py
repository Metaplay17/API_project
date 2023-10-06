class User:
    def __init__(self, user_id, first_name, last_name, email, total_reactions=0, posts=None):
        if posts is None:
            posts = []
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts

    def get_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
            "posts": self.posts,
        }


class Post:
    def __init__(self, post_id, author_id, text):
        self.id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []
        self.total_reactions = 0

    def get_reactions_count(self):
        return len(self.reactions)

    def get_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "reactions": self.reactions,
            "text": self.text,
            "total_reactions": self.total_reactions
        }
