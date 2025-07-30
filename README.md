# BRICS Protocol Investment Dashboard

A professional due diligence and monitoring dashboard for early investors in the $BRICS synthetic credit protocol.

## 🚀 Features

- **📊 Real-time $BRICS Price Monitoring** - Yield-inclusive pricing with volatility simulation
- **📈 Portfolio Analytics** - Risk analysis, tranching, and obligor performance
- **💰 Unit Economics** - Token mechanics, yield breakdown, and cash flow waterfall
- **🔍 Advanced Analytics** - VaR, stress testing, concentration risk, correlation matrix
- **📋 Compliance & Documentation** - Regulatory tracking, audit trail, document management
- **🔌 API Integration** - Bank data stream simulation and data quality metrics
- **🤖 AI/ML Analytics** - Credit risk models, yield forecasting, and backtesting
- **⚡ Performance Monitoring** - System and process metrics
- **🎨 Modern UI/UX** - Sidebar navigation, grid layout, and professional design

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yomarfrancisco/brics-mvp.git
   cd brics-mvp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run dashboard/app.py --server.port 8501 --server.address localhost
   ```

4. **Open in your browser:**  
   [http://localhost:8501](http://localhost:8501)

## 📁 Project Structure

```
brics-mvp/
├── dashboard/          # Streamlit application
│   └── app.py         # Main dashboard file
├── engine/             # Core analytics modules
│   ├── advanced_analytics.py
│   ├── api_integration.py
│   ├── ml_predictions.py
│   ├── performance_monitor.py
│   └── report_generator.py
├── data/               # Mock data files
│   ├── mock_brics_price.csv
│   ├── mock_company_summary.csv
│   └── ...
├── docs/               # Documentation and compliance
│   └── compliance_tracker.py
├── tests/              # Test scripts
│   └── test_dashboard.py
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎯 Key Features

### Dashboard Pages
- **Dashboard** - Executive summary with prominent price display
- **Unit Economics** - Token mechanics and yield breakdown
- **Portfolio Analysis** - Risk structure and obligor analysis  
- **Advanced Analytics** - Risk analytics and performance monitoring
- **Compliance & Docs** - Compliance tracking and documentation
- **API Integration** - Connection status and data quality
- **AI/ML Analytics** - Credit risk models and yield forecasting

### Technical Highlights
- **Real-time Data Simulation** - Ultra-fast price updates with volatility
- **Yield-Inclusive Pricing** - $1.00 peg + yield components + volatility
- **Risk Analytics** - VaR, stress testing, concentration risk (HHI)
- **ML Predictions** - XGBoost credit risk, yield forecasting
- **Performance Monitoring** - System metrics, uptime tracking
- **Professional UI** - Grid-based layouts, section cards, responsive design

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and test
3. Commit: `git commit -m "Add new feature"`
4. Push: `git push origin feature/new-feature`
5. Create pull request

## 📊 Data Sources

The dashboard currently uses mock data for demonstration:
- **$BRICS Price Data** - Historical price with yield components
- **Company Summary** - Obligor profiles and credit metrics
- **Portfolio Tranching** - Risk structure and exposure
- **Protocol Metrics** - APY, capital efficiency, weighted PD
- **Risk Outputs** - XGBoost predictions and risk scores
- **Transactions** - Extended transaction history
- **Waterfall** - Cash flow distribution

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Yomar Francisco** - [@yomarfrancisco](https://github.com/yomarfrancisco)

## 🙏 Acknowledgments

- Built for institutional due diligence and investor monitoring
- Designed for early-stage synthetic credit protocol analysis
- Focus on professional presentation and data clarity

---

**Note:** This dashboard is designed for due diligence and monitoring purposes, not for trading. Past performance does not guarantee future results. 