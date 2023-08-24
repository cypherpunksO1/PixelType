import datetime
import transliterate
import re


def transliterate_title(title):
    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    try:
        formatted_title = transliterate.translit(title, reversed=True).lower().replace(" ", "-")
    except:
        formatted_title = title.replace(' ', '-')

    formatted_title = re.sub(r'[^\w\s]', '-', formatted_title)  # Remove punctuation
    transformed_title = f"{formatted_title}-{month}-{day}"
    return transformed_title


languages = ['py', 'js', 'html', 'css']


def add_pre_to_code(html: str):
    """
        Add <a> to <h1> titles.
    """

    def replace_h1(match):
        code = match.group(1)
        if len(code.split('<br>')) > 2:
            language = code.split('<br>')[0]
            code = code[len(language) + 4:]
        else:
            language = 'bash'
        return f"""<pre class="{language}"><code>{code}</code></pre>"""

    new_text = re.sub(r"<code>(.*?)<\/code>", replace_h1, html)
    new_text = re.sub(r"`(.*?)`", replace_h1, new_text)

    return new_text


def add_tag_to_title(html: str):
    """
        Add <a> to <h1> titles.
    """

    def replace_h1(match):
        title = match.group(1)
        return f"""<a href='#' onclick='copyTitleToClipboard("#{title}");' id='{title}' class='title'><h1>{title}</h1></a>"""

    new_text = re.sub(r"<h1>(.*?)<\/h1>", replace_h1, add_pre_to_code(html))

    return new_text
