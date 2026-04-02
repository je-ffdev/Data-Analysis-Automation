import os
import base64
import pandas as pd
from flask import Flask, render_template, request, jsonify
from loader import load_csvs
from cleaner import clean_all
from analyzer import analyze_all
from visualizer import visualize_all
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
PLOT_FOLDER = "./output_plots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

def encode_image(path: str) -> str:
    """Convert a plot image to base64 for embedding in HTML."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    # Clear old uploads and plots before each run
    shutil.rmtree(UPLOAD_FOLDER)
    shutil.rmtree(PLOT_FOLDER)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PLOT_FOLDER, exist_ok=True)

    # Save uploaded files
    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    # Rest of the route stays exactly the same...
    # Run pipeline
    data = load_csvs(UPLOAD_FOLDER)
    cleaned = clean_all(data)
    results = analyze_all(cleaned)
    visualize_all(cleaned)

    # Build response
    response = []
    for filename, df in cleaned.items():
        file_result = {"filename": filename}

        # Cleaning summary
        file_result["shape"] = {"rows": df.shape[0], "cols": df.shape[1]}

        # Summary stats
        summary = df.select_dtypes(include="number").describe().round(3)
        file_result["summary"] = summary.to_dict()

        # Top 5 value counts per categorical column
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        value_counts = {}
        for col in cat_cols:
            value_counts[col] = df[col].value_counts().head(5).to_dict()
        file_result["value_counts"] = value_counts

        # Charts
        # Charts — grab all plots generated for this file
        charts = []
        for plot_file in sorted(os.listdir(PLOT_FOLDER)):
            if plot_file.startswith(filename) and plot_file.endswith(".png"):
                plot_path = os.path.join(PLOT_FOLDER, plot_file)
                charts.append(encode_image(plot_path))
        file_result["charts"] = charts

        response.append(file_result)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)