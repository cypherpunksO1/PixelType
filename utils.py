import datetime
import transliterate
import re


def transform_title(title):
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
