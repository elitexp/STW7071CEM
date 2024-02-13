# Import Libraries
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

print("Reading Data...")
data = pd.read_json("./data/News_Category_Dataset_v3.json", lines=True)
categories = ['SPORTS', 'BUSINESS', 'HEALTHY LIVING']
dataFrame = data[data['category'].isin(categories)]
print(dataFrame.info())
dataFrame = dataFrame.drop(columns=['authors', 'link', 'date'])
dataFrame = dataFrame.reindex(
    columns=['headline', 'short_description', 'category'])

dataFrame['text'] = dataFrame['headline'] + \
    ' ' + dataFrame['short_description']
vectorizer = TfidfVectorizer(
    min_df=2, max_df=0.4, stop_words='english', use_idf=True)
X = vectorizer.fit_transform(dataFrame['text'])
clustering = KMeans(n_clusters=3, random_state=4166)
y_means = clustering.fit_predict(X)




# news_headline = "People filed lawsuit for minimum wage"
# vectorized_headline = vectorizer.transform([news_headline])
# predicted_cluster_label = clustering.predict(vectorized_headline)[0]
# cluster_label_map = {
#     0: 'SPORTS',
#     1: 'BUSINESS',
#     2: 'HEALTHY LIVING'
# }
# predicted_cluster = cluster_label_map.get(predicted_cluster_label)
# print(f"Predicted Cluster: {predicted_cluster}")
