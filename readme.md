# Stock Analysis AI Advisor 📈🤖

This project provides a web-based interface for analyzing stock data and receiving investment recommendations using a local Language Model (LLM). The application fetches historical stock data from Yahoo Finance, performs basic technical analysis, and generates investment advice based on the analysis.

## Features

- Fetch historical stock data from Yahoo Finance
- Perform basic technical analysis (e.g., moving averages, RSI)
- Generate investment recommendations using a local LLM
- Interactive Plotly charts for visualizing stock data

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/TsTsvetkoff/stock-analysis-ai-advisor.git
    cd stock-analysis-ai-advisor
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python my_llm.py
    ```

2. Open your web browser and navigate to the provided URL.

3. Enter the stock ticker, start date, end date, and select the LLM model. Click "Analyze Stock" to get the analysis and recommendation.

## Disclaimer

**This is not financial advice.** The recommendations provided by the AI are for informational purposes only and should not be considered as financial advice. Language models (LLMs) are in an experimental phase and their outputs may not be accurate or reliable. Do not risk your financial well-being based on the recommendations provided by this application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
