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
    pattern = re.compile(r'\[([^\]]+)\]')
    return pattern.sub(lambda m: f'<a target="_blank" href="{"https://" if not m.group(1).startswith("http") else ""}{m.group(1)}">{m.group(1)}</a>', text)


def markdown_to_html(text):
    """ 
        Convert markdownV2 to 
        HTML and Shielding. 
    """
    
    text = markdown.markdown(html.escape(text))
    text = text.replace('\n', '<br>')
    # text = text.replace("---", "<br><hr><br>")
    text = text.replace("**", "<center><span style='font-size: 30px;'>***</span></center>")
    text = replace_urls(text)
    
    return text
