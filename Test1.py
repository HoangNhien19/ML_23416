from flask import Flask
from flaskext.mysql import MySQL
from markupsafe import Markup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        # MySQL configurations
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ", e)
    return None
def closeConnection(conn):
    if conn != None:
        conn.close()

def queryDataset(conn, sql):
    cursor = conn.cursor()

    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    return df

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

sql1 = "select * from customer"
df1 = queryDataset(conn, sql1)
print(df1)

sql2="select distinct customer.CustomerId, Age, Annual_Income, Spending_Score " \
     "from customer, customer_spend_score " \
     "where customer.CustomerId=customer_spend_score.CustomerID"

df2=queryDataset(conn,sql2)
df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

print(df2)

print(df2.head())

print(df2.describe())

def showHistogram(df, columns):
    plt.figure(1, figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, colunmsForElbow):
    X = df.loc[:, colunmsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n,
                       init='k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '--', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns=['Age', 'Spending Score']
elbowMethod(df2, columns)

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n,
                       init='k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize=(15,6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-.', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns = ['Age', 'Spending Score']
elbowMethod(df2, columns)

def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)

    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels


X = df2.loc[:, columns].values
cluster = 4
colors = ["red", "green", "blue", "purple", "black", "pink", "orange"]

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2["Cluster"] = labels

def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 10))
    for i in range(cluster):
        plt.scatter(
            X[y_kmeans == i, 0],
            X[y_kmeans == i, 1],
            s=100,
            c=colors[i],
            label='Cluster %i' % (i + 1)
        )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)

columns =['Annual Income', 'Spending Score']
elbowMethod(df2, columns)
X = df2.loc[:, columns].values
cluster=5

y_kmeans,centroids,labels=runKMeans(X,cluster)

print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"]=labels
visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)

columns=['Age','Annual Income','Spending Score']
elbowMethod(df2,columns)
X = df2.loc[:, columns].values
cluster=6

y_kmeans,centroids,labels=runKMeans(X,cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"]=labels
print(df2)


def visualize3DKmeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(
        df,
        x=columns[0],
        y=columns[1],
        z=columns[2],
        color='cluster',
        hover_data=hover_data,
        category_orders={"cluster": range(0, cluster)}
    )

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()

hover_data = df2.columns
visualize3DKmeans(df2,columns,hover_data,cluster)



# OOP cho phân tích cụm


class CustomerClusterAnalyzer:
    def __init__(self, df_customers: pd.DataFrame):
        self.df_raw = df_customers.copy()
        self.results = {}

    def run_clustering(self, k: int, feature_cols: list[str]):
        X = self.df_raw.loc[:, feature_cols].values

        model = KMeans(
            n_clusters=k,
            init='k-means++',
            max_iter=500,
            random_state=42
        )
        labels = model.fit_predict(X)
        centroids = model.cluster_centers_

        df_with_cluster = self.df_raw.copy()
        df_with_cluster["cluster"] = labels

        self.results[k] = {
            "labels": labels,
            "centroids": centroids,
            "features": feature_cols,
            "df": df_with_cluster
        }

    def print_clusters_to_console(self, k: int):
        if k not in self.results:
            print(f"[WARN] Chưa có kết quả cluster cho k={k}. Hãy gọi run_clustering trước.")
            return

        df_k = self.results[k]["df"]

        print(f"\n===== CLUSTER REPORT (k={k}) =====")
        for cluster_id in sorted(df_k["cluster"].unique()):
            print(f"\n--- Cluster {cluster_id} ---")
            sub = df_k[df_k["cluster"] == cluster_id]
            print(sub[["CustomerId", "Age", "Annual Income", "Spending Score"]].to_string(index=False))
        print("===== END REPORT =====\n")

    def get_clusters_for_web(self, k: int) -> dict[int, list[dict]]:
        if k not in self.results:
            print(f"[WARN] Chưa có kết quả cluster cho k={k}. Hãy gọi run_clustering trước.")
            return {}

        df_k = self.results[k]["df"]

        clusters_dict: dict[int, list[dict]] = {}
        for cluster_id in sorted(df_k["cluster"].unique()):
            sub = df_k[df_k["cluster"] == cluster_id]
            rows = []
            for _, row in sub.iterrows():
                rows.append({
                    "CustomerId": row["CustomerId"],
                    "Age": row["Age"],
                    "Annual Income": row["Annual Income"],
                    "Spending Score": row["Spending Score"],
                    "cluster": int(row["cluster"])
                })
            clusters_dict[int(cluster_id)] = rows

        return clusters_dict

analyzer = CustomerClusterAnalyzer(df2)

# k=4 với 2 feature ['Age','Spending Score']
analyzer.run_clustering(
    k=4,
    feature_cols=["Age", "Spending Score"]
)

# k=5 với 2 feature ['Annual Income','Spending Score']
analyzer.run_clustering(
    k=5,
    feature_cols=["Annual Income", "Spending Score"]
)

# k=6 với 3 feature ['Age','Annual Income','Spending Score']
analyzer.run_clustering(
    k=6,
    feature_cols=["Age", "Annual Income", "Spending Score"]
)

# (1) In ra console cho từng k
analyzer.print_clusters_to_console(4)
analyzer.print_clusters_to_console(5)
analyzer.print_clusters_to_console(6)

# (2) Lấy dữ liệu chuẩn bị render web (ví dụ cho k=6)
clusters_web_data = analyzer.get_clusters_for_web(6)
print("WEB DATA (k=6):")
for cid, custs in clusters_web_data.items():
    print(f"Cluster {cid}: {len(custs)} customers")



@app.route("/")
def index():
    return """
    <h1>Customer Clustering App</h1>
    <p>Chọn số cụm (k) để xem kết quả:</p>
    <ul>
        <li><a href="/clusters/4">Xem kết quả k=4</a></li>
        <li><a href="/clusters/5">Xem kết quả k=5</a></li>
        <li><a href="/clusters/6">Xem kết quả k=6</a></li>
    </ul>
    """

@app.route("/clusters/<int:k>")
def show_clusters_web(k: int):
    data = analyzer.get_clusters_for_web(k)
    if not data:
        return f"<h2>Không có kết quả cho k={k}</h2>"
    parts = [f"<h1>Customer Clusters (k={k})</h1>"]
    for cid, rows in data.items():
        parts.append(f"<h2>Cluster {cid}</h2>")
        parts.append('<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse">')
        parts.append("<tr><th>CustomerId</th><th>Age</th><th>Annual Income</th><th>Spending Score</th></tr>")
        for r in rows:
            parts.append(
                f"<tr><td>{r['CustomerId']}</td><td>{r['Age']}</td>"
                f"<td>{r['Annual Income']}</td><td>{r['Spending Score']}</td></tr>"
            )
        parts.append("</table><br/>")
    return Markup("\n".join(parts))

if __name__ == "__main__":
    app.run(debug=True)