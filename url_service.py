import secrets
import string

from sqlalchemy.orm import Session

from url_models import URLModel


def generate_short_code():

    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(6)
    )


def create_short_url(original_url: str, db: Session):

    for attempt in range(5):

        code = generate_short_code()

        existing = db.query(URLModel).filter(
            URLModel.short_code == code
        ).first()

        if existing is None:
            break

    else:
        raise Exception("Unable to generate unique code")

    new_url = URLModel(
        original_url=original_url,
        short_code=code
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url


def get_url_by_code(short_code: str, db: Session):

    return db.query(URLModel).filter(
        URLModel.short_code == short_code
    ).first()


def get_all_urls(db: Session):

    return db.query(URLModel).all()