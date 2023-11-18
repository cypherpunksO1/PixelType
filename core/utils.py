from sqlalchemy import func

from core.conf.database import session
from core.models import Post


import html
import re
import markdown
import datetime
import transliterate


def transliterate_title(title):
    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    try:
        formatted_title = transliterate.translit(title, reversed=True)
        formatted_title = formatted_title.lower().replace(" ", "-")
    except Exception:
        formatted_title = title.replace(" ", "-")

    formatted_title = re.sub(r"[^\w\s]", "-", formatted_title)
    transformed_title = f"{formatted_title}-{month}-{day}"
    return transformed_title


languages = ["py", "js", "html", "css"]


def add_pre_to_code(html: str):
    """
    Add <a> to <h1> titles.
    """

    def replace_h1(match):
        code = match.group(1)
        if len(code.split("<br>")) > 2:
            language = code.split("<br>")[0]
            code = code[len(language) + 4:]
        else:
            language = "bash"
        return f"""<pre class="{language}"><code>{code}</code></pre>"""

    new_text = re.sub(r"<code>(.*?)<\/code>", replace_h1, html)
    new_text = re.sub(r"`(.*?)`", replace_h1, new_text)

    return new_text


def add_tag_to_title(html: str):
    """ Add <a> to <h1> titles. """

    def replace_h1(match):
        title = match.group(1)
        return f"""<a href='#' onclick='copyTitleToClipboard("#{title}");'
                    id='{title}' class='title'><h1>{title}</h1></a>"""

    new_text = re.sub(r"<h1>(.*?)<\/h1>", replace_h1, add_pre_to_code(html))

    return new_text


def transliterate_str(title):
    """
        Return new key if it is not exists 
        and {key-{keys.count()}} if it exists.
    """
    
    key = transliterate_title(title.replace("\n", ""))
    

    key_count = session.query(Post).filter(
        func.lower(Post.key)
        .ilike(f"%{key.lower()}%")
    ).count()
    if key_count > 0:
        key = '%s-%s' % (key, key_count + 1)

    return key


def replace_urls(text):
    url_pattern = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|((?<![http://])(?<![https://])[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
    return url_pattern.sub(r'<a target="_blank" href="https://\g<0>">\g<0></a>', text)


def markdown_to_html(text):
    """ 
        Convert markdownV2 to 
        HTML and Shielding. 
    """
    
    return add_tag_to_title(
        replace_urls(
            markdown.markdown(html.escape(text))
            .replace('\n', '<br>')
        )
    )
