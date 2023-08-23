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


def add_tag_to_title(text: str):
    """
        Add <a> to <h1> titles.
    """
    def replace_h1(match):
        title = match.group(1)
        return f"""<a href='#' onclick='copyTitleToClipboard("#{title}");' id='{title}' class='title'><h1>{title}</h1></a>"""

    new_text = re.sub(r"<h1>(.*?)<\/h1>", replace_h1, text)

    return new_text
