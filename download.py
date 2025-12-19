import ffmpeg
import pandas as pd

df = pd.read_csv("mediaspace.csv")

for index, row in df.iterrows():
    output_file = row[0] + ".mp4"
    input_url = row[1]
    (
        ffmpeg
        .input(input_url)
        .output(output_file, c="copy")
        .run()
    )
