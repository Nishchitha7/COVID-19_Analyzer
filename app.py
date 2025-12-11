from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, max, min
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'csv'}

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('output', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_covid_data(csv_path):
    """Analyze COVID-19 data using PySpark"""
    # Create Spark Session
    spark = SparkSession.builder \
        .appName("COVID Analysis") \
        .master("local[*]") \
        .getOrCreate()
    
    # Load and clean data
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    clean_df = df.dropna()
    
    # Calculate metrics
    total_cases = clean_df.groupBy("country").agg(sum("new_cases").alias("total_cases"))
    total_deaths = clean_df.groupBy("country").agg(sum("new_deaths").alias("total_deaths"))
    avg_cases = clean_df.groupBy("country").agg(avg("new_cases").alias("avg_daily_cases"))
    max_cases = clean_df.groupBy("country").agg(max("new_cases").alias("max_daily_cases"))
    high_case_days = clean_df.filter(col("new_cases") > 10000)
    total_vaccinated = clean_df.groupBy("country").agg(sum("vaccinated").alias("total_vaccinated"))
    
    # Convert to Pandas and save
    total_cases.toPandas().to_csv("output/total_cases.csv", index=False)
    total_deaths.toPandas().to_csv("output/total_deaths.csv", index=False)
    avg_cases.toPandas().to_csv("output/average_cases.csv", index=False)
    max_cases.toPandas().to_csv("output/max_cases.csv", index=False)
    total_vaccinated.toPandas().to_csv("output/total_vaccinated.csv", index=False)
    
    # Save raw data preview
    clean_df.limit(20).toPandas().to_csv("output/raw_data_preview.csv", index=False)
    
    spark.stop()
    
    return {
        'success': True
    }

@app.route('/')
def index():
    # Check if we have existing results
    try:
        # Read CSV files
        total_cases = pd.read_csv('output/total_cases.csv')
        total_deaths = pd.read_csv('output/total_deaths.csv')
        avg_cases = pd.read_csv('output/average_cases.csv')
        max_cases = pd.read_csv('output/max_cases.csv')
        total_vaccinated = pd.read_csv('output/total_vaccinated.csv')
        raw_data = pd.read_csv('output/raw_data_preview.csv')
        
        # Convert to dictionaries for template
        cases_data = total_cases.to_dict('records')
        deaths_data = total_deaths.to_dict('records')
        avg_data = avg_cases.to_dict('records')
        max_data = max_cases.to_dict('records')
        vaccinated_data = total_vaccinated.to_dict('records')
        raw_data_records = raw_data.to_dict('records')
        
        return render_template('index.html', 
                             cases=cases_data, 
                             deaths=deaths_data, 
                             averages=avg_data,
                             max_cases=max_data,
                             vaccinated=vaccinated_data,
                             raw_data=raw_data_records)
    except:
        # If no existing results, show upload page
        return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analyze the uploaded file
            results = analyze_covid_data(filepath)
            return redirect(url_for('index'))
        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Only CSV files allowed.'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
