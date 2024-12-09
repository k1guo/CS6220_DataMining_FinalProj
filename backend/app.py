from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

file_path = os.getenv("CSV_FILE_PATH", "silicon_valley_stop_points.csv")
output_dir = os.getenv("OUTPUT_DIR", "./output")
os.makedirs(output_dir, exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Bus Station Optimization API</h1>
    <p>Use the API endpoints to optimize bus stations:</p>
    <ul>
        <li><code>POST /optimize-bus-stations</code>: Optimize bus station locations.</li>
        <li><code>GET /files/&lt;filename&gt;</code>: Retrieve generated files.</li>
    </ul>
    """

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(output_dir, filename)

@app.route('/optimize-bus-stations', methods=['POST', 'OPTIONS'])
def optimize_bus_stations():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight OK'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    try:
        target_stations = int(request.json.get("target_stations", 100))
        eps = float(request.json.get("eps", 0.05))
        min_samples = int(request.json.get("min_samples", 8))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input parameters"}), 400

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 500

    required_columns = ['Latitude', 'Longitude', 'Population Density']
    if not all(col in df.columns for col in required_columns):
        return jsonify({"error": f"CSV 文件中必须包含列: {required_columns}"}), 400

    scaler = StandardScaler()
    df[['Latitude', 'Longitude', 'Population Density']] = scaler.fit_transform(
        df[['Latitude', 'Longitude', 'Population Density']]
    )

    coords = df[['Latitude', 'Longitude', 'Population Density']].values

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    df['DBSCAN_Cluster'] = db.labels_

    dbscan_clusters = df[df['DBSCAN_Cluster'] != -1].groupby('DBSCAN_Cluster').agg({
        'Latitude': 'mean',
        'Longitude': 'mean',
        'Population Density': 'sum'
    }).reset_index()
    dbscan_top_clusters = dbscan_clusters.nlargest(target_stations, 'Population Density')

    kmeans = KMeans(n_clusters=target_stations, random_state=42).fit(coords)
    df['KMeans_Cluster'] = kmeans.labels_

    kmeans_clusters = pd.DataFrame(kmeans.cluster_centers_, columns=['Latitude', 'Longitude', 'Population Density'])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_image = f'comparison_optimized_stops_{timestamp}.png'
    dbscan_csv_path = f'dbscan_optimized_stops_{timestamp}.csv'
    kmeans_csv_path = f'kmeans_optimized_stops_{timestamp}.csv'

    plt.figure(figsize=(16, 8))
    plt.scatter(df['Longitude'], df['Latitude'], c=df['Population Density'], cmap='Blues', s=5)
    plt.scatter(dbscan_top_clusters['Longitude'], dbscan_top_clusters['Latitude'], c='red', s=100)
    plt.scatter(kmeans_clusters['Longitude'], kmeans_clusters['Latitude'], c='blue', s=100)

    plt.savefig(os.path.join(output_dir, comparison_image))
    plt.close()

    dbscan_top_clusters.to_csv(os.path.join(output_dir, dbscan_csv_path), index=False)
    kmeans_clusters.to_csv(os.path.join(output_dir, kmeans_csv_path), index=False)

    return jsonify({
        "message": "Optimization complete",
        "dbscan_csv_path": dbscan_csv_path,
        "kmeans_csv_path": kmeans_csv_path,
        "comparison_image": comparison_image
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)