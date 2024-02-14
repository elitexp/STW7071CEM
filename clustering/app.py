
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from flask import Flask, render_template, request, jsonify, Response
from wordcloud import WordCloud

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import plotly.graph_objs as go
import io


app = Flask(__name__)
stemmer = PorterStemmer()


def stem_words(words_list, stemmer):
    return [stemmer.stem(word) for word in words_list]


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_words(tokens, stemmer)
    return stems


print("Reading Data...")

data = pd.read_json("./data/News_Category_Dataset_v3.json", lines=True)
categories = ['SPORTS', 'BUSINESS', 'HEALTHY LIVING']
dataFrame = data[data['category'].isin(categories)]
dataFrame['category'] = dataFrame['category'].replace(
    'HEALTHY LIVING', 'HEALTH')

print(dataFrame.info())
# Combine headline and short_description into a single text column
dataFrame['text'] = dataFrame['headline'] + \
    ' ' + dataFrame['short_description'] + \
    ' ' + dataFrame['category']

dataFrame = dataFrame.drop(columns=['link', 'authors', 'date'])
dataFrame = dataFrame.reindex(
    columns=['text', 'headline', 'short_description', 'category'])


tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(dataFrame['text'])

model = KMeans(n_clusters=3, random_state=5123)
clusters = model.fit_predict(tfs)
dataFrame['cluster'] = clusters

# Find the cluster closest to SPORTS, BUSINESS, or HEALTHY LIVING
sports_cluster = dataFrame[dataFrame['category']
                           == 'SPORTS']['cluster'].iloc[0]
business_cluster = dataFrame[dataFrame['category']
                             == 'BUSINESS']['cluster'].iloc[0]
health_cluster = dataFrame[dataFrame['category']
                           == 'HEALTH']['cluster'].iloc[0]
cluster_map = {
    sports_cluster: 'SPORTS',
    business_cluster: 'BUSINESS',
    health_cluster: 'HEALTH'
}
print("Cluster closest to SPORTS:", sports_cluster)
print("Cluster closest to BUSINESS:", business_cluster)
print("Cluster closest to HEALTH:", health_cluster)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/clusters', methods=['GET'])
def clusters():
    fig = go.Figure(data=[go.Pie(labels=dataFrame['category'],
                                 textinfo='label+percent',
                                 marker=dict(colors=['#491D8B', '#7D3AC1', '#EB548C']))])
    fig.update_layout(title='Data Distribution', template='plotly')
    img_base64 = fig.to_image(format="png", width=800, height=600)
    return Response(img_base64, mimetype='image/png')


@app.route('/wordcloud')
def generate_wordcloud():
    # Get the top words based on TF-IDF scores
    feature_names = tfidf.get_feature_names_out()
    tfidf_scores = tfs.sum(axis=0).A1
    # Assuming you want the top 500 words
    top_indices = tfidf_scores.argsort()[-500:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    # Generate the word cloud
    wordcloud = WordCloud(
        width=800, height=200, background_color='white').generate(' '.join(top_words))

    # Convert the word cloud to a PNG image
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return Response(img_buffer, mimetype='image/png')


@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    # Ensure 'headline' key exists in the JSON data
    if 'headline' not in data:
        return jsonify({'error': 'No headline provided'})
    headline = data['headline']
    # Transform the headline using TF-IDF
    headline_tfs = tfidf.transform([headline])
    predicted_cluster = model.predict(headline_tfs)[0]
    cluster_label = cluster_map.get(predicted_cluster)
    response = {'cluster': cluster_label}
    return jsonify(response)


app.jinja_env.variable_start_string = '{%'
app.jinja_env.variable_end_string = '%}'
if __name__ == '__main__':
    app.run(debug=True)
