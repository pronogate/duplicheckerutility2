from flask import Flask, request, render_template
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)

def find_similar_questions(df):
    similar_pairs = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            text1 = df.at[i, 'Question Text']
            text2 = df.at[j, 'Question Text']
            similarity = fuzz.ratio(text1, text2)
            if similarity > 70:
                similar_pairs.append((i + 1, j + 1, similarity))
    return similar_pairs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            similar_question_pairs = find_similar_questions(df)
            return render_template('index.html', similar_question_pairs=similar_question_pairs)
    return render_template('index.html', similar_question_pairs=None)

if __name__ == '__main__':
    app.run(debug=True)
