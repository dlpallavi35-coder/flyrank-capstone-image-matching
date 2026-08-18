from sqlalchemy.orm import Session
from app.models.post import Post


def find_best_matching_post(
    image_description: str,
    db: Session
):
    posts = db.query(Post).all()

    if not posts:
        return None

    image_text = image_description.lower()

    best_post = None
    best_score = 0

    for post in posts:
        post_text = f"{post.title} {post.content}".lower()

        image_words = set(image_text.split())
        post_words = set(post_text.split())

        common_words = image_words.intersection(post_words)

        score = len(common_words)

        if score > best_score:
            best_score = score
            best_post = post

    return best_post