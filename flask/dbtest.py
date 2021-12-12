from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer
txt1 = "Elon Musk's Boring Co to build high-speed airport link in Chicago"
txt2 = "Elon Musk's Boring Company to build high-speed Chicago airport link"
txt3 = "Elon Musk’s Boring Company approved to build high-speed transit between downtown Chicago and O’Hare Airport"
txt4 = "Both apple and orange are fruit"
text = [txt1, txt2, txt3, txt4]
# tokens = [w for s in text for w in s ]
# print(tokens)

vectorizer = CountVectorizer()
vector = vectorizer.fit_transform(text)
feature_names = vectorizer.get_feature_names()
array = vector.toarray()

# print(feature_names)
print(array)
print(euclidean_distances([array[0]], [array[2]])[0][0])



