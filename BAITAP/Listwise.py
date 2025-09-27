import numpy as np
import lightgbm as lgb

X_train = np.random.rand(60, 5)  # 5 đặc trưng
y_train = np.random.randint(0, 4, size=60)
group = [60]
train = lgb.Dataset(X_train, label=y_train, group=group)

params = {
   'objective': 'lambdarank',
   'metric': 'ndcg',
   'learning_rate': 0.1,
   'num_leaves': 15,
   'min_data_in_leaf': 1,
   'min_data_in_bin': 1
}

model = lgb.train(params, train, num_boost_round=50)

# Truy vấn mới
X_new = np.random.rand(10, 5)
scores = model.predict(X_new)
order = np.argsort(scores)[::-1]
print("Scores:", scores)
print("Kết quả xếp hạng:")
for rank, idx in enumerate(order, start=1):
    print(f"{rank}. Mẫu {idx} - Điểm: {scores[idx]:.4f}")
