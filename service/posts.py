from core.db.database import session
from models.db_models import Post
from sqlalchemy import func
import utils
import html
import markdown


def make_post_key(title):
    """
        Return new key if it is not exists and {key-{keys.count()}} if it exists.
    """
    # Make key
    key = utils.transliterate_title(title)

    # If exists reply key - add exists reply keys count to end.
    key_count = session.query(Post).filter(func.lower(Post.key).ilike(f"%{key.lower()}%")).count()
    if key_count > 0:
        key = '%s-%s' % (key, key_count + 1)

    return key


def convert_markdown_to_html(text):
    """
        Convert markdownV2 to HTML and Shielding.
    """
    return utils.add_tag_to_title(
        markdown.markdown(html.escape(text)).replace('\n', '<br>')
    )
