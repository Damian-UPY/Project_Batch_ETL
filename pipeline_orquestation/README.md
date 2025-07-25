# **UPY-Crypto-Market-Pipeline**

This project implements a **Batch ETL Pipeline** using **Apache Airflow** as the orchestration tool.
It extracts data from **three major cryptocurrency APIs**, processes it, and stores it into a **MongoDB Data Warehouse**.
The processed data is visualized via an interactive **Streamlit Dashboard**, organized into multiple pages for easy exploration.

---

## 📂 **Project Structure**

```
.
├── dags/                           # Airflow DAGs for ETL process
│   ├── binance_ticker_ingestion.py
│   ├── cryptocurrencymarket.py
│   ├── wazirx_ticker_ingestion.py
│   ├── load_mongo.py
│   ├── main_pipeline.py            # Orchestrates all DAGs
│   └── utils/                      # Shared helpers for DAGs
│       ├── api_helpers.py
│       └── mongo_utils.py
├── streamlit_app/
│   ├── app.py                      # Main Streamlit application
│   ├── pages/                      # Multi-page dashboards
│   │   ├── 1_Crypto.py
│   │   ├── 2_Binance_Tickers.py
│   │   └── 3_WazirX_Tickers.py
│   ├── utils/
│   │   ├── mongo_conn.py
│   │   ├── charts.py
│   │   └── helpers.py
│   ├── styles/style.css
│   └── Dockerfile
├── .gitignore
├── docker-compose.yml              # Orchestrates all containers
├── requirements.txt
├── Dockerfile                      # Airflow Image
└── README.md
```

---

## ⚙️ **Technologies Used**

* **Orchestration**: Apache Airflow
* **Database**: MongoDB, PostgreSQL
* **Data Visualization**: Streamlit
* **Containerization**: Docker & Docker Compose
* **Python Libraries**:

  * pandas
  * plotly
  * pymongo
  * requests

---

## 🛡️ **Data Sources**

### **1️⃣ CoinGecko API**

* **Theme**: Global Crypto Market
* **API Link**: [CoinGecko Markets](https://api.coingecko.com/api/v3/coins/markets)
* **What it provides**:

  * Top 100 cryptocurrencies
  * Market Cap, Price, Volume
  * 24h Price Change % and ATH/ATL
* **Usage**: Global Market Overview Dashboard

---

### **2️⃣ Binance API**

* **Theme**: 24h Market Tickers
* **API Link**: [Binance 24hr Ticker](https://api4.binance.com/api/v3/ticker/24hr)
* **What it provides**:

  * Trading Pairs (ETHBTC, LTCBTC, etc.)
  * Volume (base & quote assets)
  * High/Low Prices and last trade info
* **Usage**: Liquidity Analysis & Pair Rankings

---

### **3️⃣ WazirX API**

* **Theme**: Crypto Prices vs INR
* **API Link**: [WazirX Tickers](https://api.wazirx.com/sapi/v1/tickers/24hr)
* **What it provides**:

  * Trading pairs in INR (e.g., BTCINR)
  * Open/Close Prices, High/Low
* **Usage**: Local market perspective & INR trends

---

## 💾 **Data Pipeline Overview**

The **ETL pipeline** runs as a **Daily Batch Process**:

1. **Extract**: Fetch raw JSON from all three APIs.
2. **Transform**:

   * Clean and normalize numeric fields.
   * Add metadata like timestamp and top assets.
   * Calculate KPIs (price change %, rankings).
3. **Load**: Store data into **MongoDB**:

   * `raw_*` collections: Store raw API data.
   * `processed_*` collections: Store cleaned and structured data for visualization.

---

### **Airflow DAGs**

✅ **Individual DAGs**:

* `cryptocurrencymarket.py`: Handles CoinGecko data.
* `binance_ticker_ingestion.py`: Handles Binance tickers.
* `wazirx_ticker_ingestion.py`: Handles WazirX tickers.
* `load_mongo.py`: Consolidates everything if needed.

✅ **Master DAG**:

* `main_pipeline.py`: Orchestrates all DAGs in sequence using **TriggerDagRunOperator**.

---

## 🖥️ **Streamlit Dashboard**

The dashboard provides **three main sections**:

### **1️⃣ Cryptocurrency Market (CoinGecko)**

* Overview of top coins with **images, prices, market cap**.
* KPIs: Total coins, top coin.
* Charts:

  * Top 10 by Market Cap.
  * Top Movers (24h Price Change %).
* Interactive Table:

  * Shows `id`, `symbol`, `name`, `image`, `current_price`, `price_change_24h`, `price_change_percentage_24h`.

---

### **2️⃣ Binance Market**

* KPIs: Most traded pair, total pairs.
* Chart:

  * Top 10 pairs by Volume.
* Filtered Table:

  * `symbol`, `price_change`, `price_change_percent`, `last_price`, `high_price`, `low_price`.
  * **Removes rows where values are exactly 0.**

---

### **3️⃣ WazirX Market**

* KPIs: Symbols tracked, top INR pair.
* Table:

  * `symbol`, `base_asset`, `open_price`, `high_price`, `low_price`.

---

## 🗃️ **MongoDB Collections**

| Collection Name             | Content                   |
| --------------------------- | ------------------------- |
| `raw_crypto_market`         | Raw CoinGecko data        |
| `processed_crypto_market`   | Cleaned CoinGecko data    |
| `raw_binance_tickers`       | Raw Binance tickers       |
| `processed_binance_tickers` | Processed Binance tickers |
| `raw_wazirx_tickers`        | Raw WazirX tickers        |
| `processed_wazirx_tickers`  | Processed WazirX tickers  |

---

## 🛡️ **Containerization**

We use **Docker Compose** to orchestrate:

* **MongoDB** (port `27017`)
* **PostgreSQL** (Airflow backend)
* **Airflow Webserver** (port `8080`)
* **Airflow Scheduler**
* **Streamlit Dashboard** (port `8501`)

---

## ⚡ **How to Run the Project**

1️⃣ **Clone the repository**

```bash
git clone <repo_url>
cd Project_Batch_ETL/pipeline_orquestation
```

2️⃣ **Initialize Airflow DB**

```bash
docker compose run --rm webserver airflow db init
```

3️⃣ **Create Airflow Admin User**

```bash
docker compose run --rm webserver airflow users create \
    --username airflow \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password airflow
```

4️⃣ **Start the containers**

```bash
docker compose up --build
```

✅ **Access Airflow UI**: [http://localhost:8080](http://localhost:8080)
✅ **Access Streamlit App**: [http://localhost:8501](http://localhost:8501)
✅ **MongoDB Compass**: `mongodb://root:example@localhost:27017/project_db?authSource=admin`

---