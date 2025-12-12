# COVID-19 Data Analysis Dashboard

A comprehensive web application for analyzing COVID-19 pandemic data using Apache Spark (PySpark) with an interactive dashboard interface.

## 🚀 Features

- **Interactive Web Interface**: Upload CSV files and get instant analysis
- **Real-time Processing**: Powered by Apache Spark for fast data processing
- **Multiple Metrics**: Analyzes 5 key pandemic indicators
- **Data Visualization**: Beautiful dashboard with sortable tables
- **Export Capabilities**: Generates CSV reports for further analysis
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📊 Analysis Metrics

1. **Total Cases by Country**
2. **Total Deaths by Country**
3. **Average Daily Cases**
4. **Maximum Daily Cases**
5. **Total Vaccinations**

## 🛠️ Tech Stack

- **Backend**: Python, PySpark, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Apache Spark
- **Data Format**: CSV files

## 📁 Project Structure

```
covid_analysis/
├── app.py              # Main Flask application
├── covid_data.csv       # Sample COVID-19 data
├── README.md            # This file
├── output/              # Analysis results (CSV files)
├── templates/           # HTML templates
│   ├── index.html       # Main dashboard
│   └── upload.html      # File upload page
└── uploads/             # User uploaded files
```

## 🚀 Quick Start

### Prerequisites

- Java JDK 11, 17, or 21 (Not Java 25 - see compatibility notes)
- Python 3.7+
- Pip package manager

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd covid_analysis
   ```

2. **Install required packages**
   ```bash
   pip install pyspark flask pandas
   ```

3. **Set Java Environment Variables**
   ```bash
   # Windows (PowerShell)
   $env:JAVA_HOME="C:\Program Files\Java\jdk-17"
   $env:PATH="$env:JAVA_HOME\bin;$env:PATH"
   
   # Linux/macOS
   export JAVA_HOME=/path/to/java/jdk-17
   export PATH=$JAVA_HOME/bin:$PATH
   ```

### Running the Application

1. **Start the web server**
   ```bash
   python app.py
   ```

2. **Access the dashboard**
   Open your browser and go to: `http://localhost:5000`

3. **Use the application**
   - Upload a CSV file with COVID-19 data
   - View raw data preview
   - See analysis results in real-time dashboard
   - Download CSV reports from the `output/` folder

## 📤 CSV File Format

The application expects CSV files with the following columns:

```csv
date,country,new_cases,new_deaths,new_recoveries,vaccinated
2020-05-10,India,3278,112,2000,15000
```

**Required Columns:**
- `date`: Date in YYYY-MM-DD format
- `country`: Country name
- `new_cases`: Daily new cases count
- `new_deaths`: Daily deaths count
- `new_recoveries`: Daily recoveries count
- `vaccinated`: Vaccination count

## 🔧 Troubleshooting

### Java Compatibility Issues

**Problem**: `getSubject is not supported` error
**Solution**: Use Java 11, 17, or 21 instead of Java 25

### Windows File Output Issues

**Problem**: Permission errors when saving files
**Solution**: The application uses Pandas fallback for file output to avoid winutils.exe requirements

### Port Already in Use

**Problem**: Port 5000 is already occupied
**Solution**: Stop other applications or modify the port in `app.py`

## 📈 Sample Data

The project includes sample data in `covid_data.csv` with records from India, USA, and UK covering May 2020.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Apache Spark community for PySpark
- Flask team for the web framework
- Pandas team for data manipulation tools

## 📞 Support

For issues, questions, or feedback, please create an issue in the repository.