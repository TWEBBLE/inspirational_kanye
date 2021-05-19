import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from snowflake_connector import SnowflakeConnector

snowflake_connection_details = {
    "user": os.environ.get("SNOWFLAKE_USER"),
    "role": os.environ.get("SNOWFLAKE_ROLE", "SYSADMIN"),
    "password": os.environ.get("SNOWFLAKE_PASSWORD"),
    "account": str(os.environ.get("SNOWFLAKE_ACCOUNT"))
    + "."
    + os.environ.get("SNOWFLAKE_REGION", "eu-west-1"),
    "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
}

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

snowflake_instance = SnowflakeConnector(snowflake_connection_details)
cursor = snowflake_instance.set_session_parameters(
    role="SYSADMIN", warehouse="COMPUTE_WH"
)

df = snowflake_instance.fetch_dataframe_from_sql(
    cursor,
    f'SELECT * FROM "KANYE_{os.environ.get("ENV", "DEV")}"."QUOTES"."Inspirational_Teachings_of_Mr_West";',
)
print(df)

text = " ".join(quote for quote in df.QUOTES)

print(f"There are {len(text)} words in the combination of all quotes.")

stopwords = set(STOPWORDS)
stopwords.update(
    [
        "got",
        "let",
        "still",
        "george",
        "I'm",
        "am",
        "the",
        "at",
        "is",
        "of",
        "for",
        "in",
        "a",
        "to",
        "an",
    ]
)

# Generate a word cloud image
mask = np.array(Image.open("kanye_face.png"))
wordcloud_kanye = WordCloud(
    stopwords=stopwords,
    background_color="white",
    mode="RGBA",
    max_words=1000,
    mask=mask,
).generate(text)

# create coloring from image
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[7, 7])
plt.imshow(wordcloud_kanye.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

# store to file
plt.savefig("kanye_wordcloud.png", format="png")

plt.show()
