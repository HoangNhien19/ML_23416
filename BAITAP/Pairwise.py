from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

# Truy vấn gốc: "fruit good for health"
docs_train = [
   "Top 10 fruits that boost immunity",
   "Benefits of eating apples and bananas daily",
   "Cake recipes with strawberries",
   "History of fruit trade in the 18th century"
]
scores_train = [3, 2, 1, 0]  # 3 = rất liên quan, 0 = không liên quan

vec = TfidfVectorizer()
X_train = vec.fit_transform(docs_train).toarray()

# Tạo cặp (pairwise)
pairs, labels = [], []
for i in range(len(docs_train)):
   for j in range(len(docs_train)):
       if scores_train[i] > scores_train[j]:
           pairs.append(X_train[i] - X_train[j])
           labels.append(1)

           pairs.append(X_train[j] - X_train[i])
           labels.append(0)

pairs, labels = np.array(pairs), np.array(labels)

# Huấn luyện Logistic Regression
model = LogisticRegression()
model.fit(pairs, labels)

# Truy vấn mới
query_new = "Luxury jewelry shop"
candidates_new = [
   "Exclusive diamond jewelry boutique in Paris",
   "Affordable silver jewelry for everyday wear",
   "Luxury gold and platinum jewelry showroom in New York",
   "History of ancient jewelry making techniques"
]
X_new = vec.transform(candidates_new).toarray()

# So sánh từng cặp
n = len(candidates_new)
wins = np.zeros(n)
for i in range(n):
   for j in range(n):
       if i != j:
           pred = model.predict([X_new[i] - X_new[j]])[0]
           if pred == 1:
               wins[i] += 1

ranking = np.argsort(-wins)

print("Kết quả xếp hạng cho truy vấn:", query_new)
for idx in ranking:
   print(f"{wins[idx]} -> {candidates_new[idx]}")
