from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

docs_train = [
   "Top 10 rose flower shops in the city",
   "How to care for rose plants at home",
   "Affordable bouquet shops selling roses nearby"
]
y_train = [3, 1, 2]

model = make_pipeline(TfidfVectorizer(), LinearRegression())
model.fit(docs_train, y_train)

# Ứng dụng cho truy vấn mới
query = "luxury jewelry shop"  # truy vấn mới

candidates_new = [
   "Exclusive diamond jewelry boutique in Paris",
   "Affordable silver jewelry for everyday wear",
   "Luxury gold and platinum jewelry showroom in New York",
   "History of ancient jewelry making techniques"
]

# Dự đoán điểm liên quan
pred_scores = model.predict(candidates_new)

# Sắp xếp theo điểm dự đoán giảm dần
for doc, score in sorted(zip(candidates_new, pred_scores), key=lambda x: x[1], reverse=True):
   print(f"{score:.2f} -> {doc}")
