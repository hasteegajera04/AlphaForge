# AlphaForge — Quantitative Trading Data Pipeline

> An end-to-end data pipeline for quantitative trading research: ingesting market data, engineering 50+ technical indicator features, and storing everything in a queryable SQLite warehouse — built as a foundation for backtesting and ML-driven strategy research.

## Overview

AlphaForge automates the unglamorous but critical first stage of any quant workflow: getting raw market data into a clean, feature-rich, analysis-ready form. It pulls historical price data, computes a broad library of technical indicators, and persists everything to SQLite so downstream research (backtesting, ML models, signal analysis) can query a single reliable source of truth instead of re-deriving features every time.

This project is part of a broader quant finance portfolio, built alongside study of *Advances in Financial Machine Learning* (López de Prado), and designed to reflect the kind of data infrastructure used in real quant research and trading desks.

## Features

- **Data ingestion** — automated retrieval of historical market/price data
- **SQLite storage layer** — structured, queryable warehouse for raw and engineered data
- **50+ technical indicators** — momentum, trend, volatility, and volume-based features engineered from raw OHLCV data
- **Modular pipeline design** — ingestion, feature engineering, and storage are decoupled stages, making it straightforward to extend with new data sources or indicators

## Tech Stack

- **Python** — core pipeline logic
- **SQLite** — data storage
- **Pandas / NumPy** — data manipulation and feature computation

## Project Structure

```
quant-data-pipeline/
├── data_ingestion/       # Scripts to pull and update raw market data
├── feature_engineering/  # Technical indicator computation (~50 features)
├── storage/              # SQLite schema, load/query utilities
├── notebooks/            # Exploratory analysis (if applicable)
├── requirements.txt
└── README.md
```
*(Update this tree to match your actual folder layout — happy to regenerate once you share it.)*

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
git clone https://github.com/hasteegajera04/quant-data-pipeline.git
cd quant-data-pipeline
pip install -r requirements.txt
```

### Usage
```bash
# Run data ingestion
python data_ingestion/fetch_data.py

# Generate technical indicator features
python feature_engineering/build_features.py

# Query the resulting SQLite database
python storage/query_example.py
```
*(Replace with your actual entry-point scripts and filenames.)*

## Roadmap

- [ ] Backtesting engine integration
- [ ] ML model training on engineered features
- [ ] Risk framework / portfolio-level metrics
- [ ] Live data feed support

## Reference

Built with concepts from Marcos López de Prado's *Advances in Financial Machine Learning*.

## Author

**Hastee Gajera** — B.Tech CSE + MBA (Integrated), Nirma University
Data Analytics Intern @ Xtin Capitals

---
*This is a portfolio/research project and not intended for live trading use.*
