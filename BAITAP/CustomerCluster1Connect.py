from flask import Flask
from markupsafe import Markup  # Sửa dòng này
from flaskext.mysql import MySQL
import pandas as pd
app = Flask(__name__)
analyzer = None


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
    except Exception as e:
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


class CustomerClusterAnalyzer:
    def __init__(self, df_customers: pd.DataFrame):
        self.df_raw = df_customers.copy()
        self.results = {}

    def run_clustering(self, k: int, feature_cols: list[str]):
        from sklearn.cluster import KMeans
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

    # (1) Hàm truy suất danh sách chi tiết ra console
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

    # (2) Hàm xuất danh sách chi tiết cho web
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


def initialize_data():
    """Khởi tạo dữ liệu cho ứng dụng"""
    global analyzer

    print("Đang kết nối database...")
    conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

    if conn is None:
        print("Không thể kết nối database!")
        return None

    print("Kết nối database thành công!")

    # Lấy dữ liệu cho phân tích cụm
    sql2 = "select distinct customer.CustomerId, Age, Annual_Income, Spending_Score " \
           "from customer, customer_spend_score " \
           "where customer.CustomerId=customer_spend_score.CustomerID"

    df2 = queryDataset(conn, sql2)
    df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']
    closeConnection(conn)

    print("Dữ liệu phân tích cụm:")
    print(df2.head())
    print(df2.describe())

    # Khởi tạo analyzer và chạy clustering
    print("Đang chạy phân tích cụm...")
    analyzer = CustomerClusterAnalyzer(df2)
    analyzer.run_clustering(k=4, feature_cols=["Age", "Spending Score"])
    analyzer.run_clustering(k=5, feature_cols=["Annual Income", "Spending Score"])
    analyzer.run_clustering(k=6, feature_cols=["Age", "Annual Income", "Spending Score"])

    # (1) In ra console cho từng k
    analyzer.print_clusters_to_console(4)
    analyzer.print_clusters_to_console(5)
    analyzer.print_clusters_to_console(6)

    print("Khởi tạo dữ liệu hoàn tất!")
    return df2


# Khởi tạo dữ liệu khi app start
print("Đang khởi động ứng dụng...")
df2 = initialize_data()


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Clustering App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 15px 0;
            }
            a {
                display: block;
                padding: 15px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
                transition: background 0.3s;
            }
            a:hover {
                background: #0056b3;
            }
            .info {
                background: #e7f3ff;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Customer Clustering App</h1>
            <div class="info">
                <strong>Ứng dụng phân cụm khách hàng sử dụng K-Means</strong>
                <p>Chọn số cụm (k) để xem kết quả phân nhóm khách hàng:</p>
            </div>
            <ul>
                <li><a href="/clusters/4">Xem kết quả k=4 (Age vs Spending Score)</a></li>
                <li><a href="/clusters/5">Xem kết quả k=5 (Income vs Spending Score)</a></li>
                <li><a href="/clusters/6">Xem kết quả k=6 (3D Clustering)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """


@app.route("/clusters/<int:k>")
def show_clusters_web(k: int):
    if analyzer is None:
        return """
        <h2>Ứng dụng chưa được khởi tạo</h2>
        <p>Vui lòng refresh lại trang sau vài giây.</p>
        <a href="/">Quay lại trang chủ</a>
        """

    data = analyzer.get_clusters_for_web(k)
    if not data:
        return f"""
        <h2>Không có kết quả cho k={k}</h2>
        <p>Số cụm {k} không tồn tại trong kết quả phân tích.</p>
        <a href="/">Quay lại trang chủ</a>
        """

    parts = [f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clusters k={k}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .cluster-section {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007bff;
                color: white;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .cluster-badge {{
                background: #007bff;
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 14px;
            }}
            .back-link {{
                display: inline-block;
                padding: 10px 15px;
                background: #6c757d;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .back-link:hover {{
                background: #545b62;
            }}
            .stats {{
                background: #e7f3ff;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <a href="/" class="back-link">Quay lại trang chủ</a>
        <div class="header">
            <h1>Customer Clusters (k={k})</h1>
            <div class="stats">
                <strong>Tổng số khách hàng:</strong> {sum(len(customers) for customers in data.values())} |
                <strong>Số cụm:</strong> {len(data)}
            </div>
        </div>
    """]

    for cid, rows in data.items():
        parts.append(f'<div class="cluster-section">')
        parts.append(f'<h2><span class="cluster-badge">Cluster {cid}</span></h2>')
        parts.append(f'<div class="stats">Số khách hàng: {len(rows)}</div>')
        parts.append('<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse">')
        parts.append("<tr><th>CustomerId</th><th>Age</th><th>Annual Income</th><th>Spending Score</th></tr>")
        for r in rows:
            parts.append(
                f"<tr>"
                f"<td>{r['CustomerId']}</td>"
                f"<td>{r['Age']}</td>"
                f"<td>{r['Annual Income']}</td>"
                f"<td>{r['Spending Score']}</td>"
                f"</tr>"
            )
        parts.append("</table>")
        parts.append("</div>")

    parts.append("""
        </body>
        </html>
    """)

    return Markup("\n".join(parts))


if __name__ == "__main__":
    print("Khởi động Flask server...")
    print("Truy cập: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)