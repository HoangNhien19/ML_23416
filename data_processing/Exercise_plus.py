import pandas as pd

# Đọc dữ liệu
df = pd.read_csv('../datasets/SalesTransactions/SalesTransactions.csv')

# Tính doanh thu từng sản phẩm và lấy 3 sản phẩm cao nhất
top3 = (
    df.groupby('ProductID')
      .apply(lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum())
      .sort_values(ascending=False)
      .head(3)
)

print("Ba sản phẩm có tổng giá bán ra cao nhất:")
print(top3)
