import gradio as gr
import yfinance as yf
import ollama
from datetime import date
import plotly.graph_objects as go

def get_stock_data(ticker, start_date, end_date):
    """Fetch historical stock data from Yahoo Finance"""
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    return df


def analyze_stock(df):
    """Perform basic technical analysis (modified for Plotly)"""
    # Keep existing calculations
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df.reset_index()


def get_llm_recommendation(stock_data, model_name):
    """Get investment recommendation from local LLM"""
    prompt = f"""Analyze this stock data and provide investment advice. 
    Recent price: {stock_data['Close'].iloc[-1]:.2f}
    50-day MA: {stock_data['MA50'].iloc[-1]:.2f}
    200-day MA: {stock_data['MA200'].iloc[-1]:.2f}
    RSI: {stock_data['RSI'].iloc[-1]:.2f}

    Consider technical indicators and provide a recommendation to Buy, Hold, or Sell.
    Explain your reasoning in 3-4 sentences."""

    response = ollama.generate(model=model_name, prompt=prompt)
    return response['response']


def stock_analysis(ticker, start_date, end_date, model_name):
    try:
        df = get_stock_data(ticker, start_date, end_date)
        if df.empty:
            return "No data found", "", ""

        analyzed_df = analyze_stock(df)
        recommendation = get_llm_recommendation(analyzed_df, model_name)

        # Create interactive Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=analyzed_df['Date'],
            y=analyzed_df['Close'],
            name='Close Price',
            hovertemplate="Date: %{x}<br>Price: $%{y:.2f}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=analyzed_df['Date'],
            y=analyzed_df['MA50'],
            name='50-day MA',
            line=dict(dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=analyzed_df['Date'],
            y=analyzed_df['MA200'],
            name='200-day MA',
            line=dict(dash='dash')
        ))

        fig.update_layout(
            title=f'{ticker} Price Analysis',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            hovermode='x unified',
            showlegend=True
        )

        return analyzed_df, fig, recommendation

    except Exception as e:
        return str(e), "", ""



# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Stock Analysis AI Advisor 📈🤖")

    with gr.Row():
        ticker = gr.Textbox(label="Stock Ticker (e.g., AAPL)", value="AAPL")
        start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", value="2020-01-01")
        end_date = gr.Textbox(
            label="End Date (YYYY-MM-DD)",
            value=date.today().strftime('%Y-%m-%d')
        )
        model_name = gr.Dropdown(
            label="LLM Model",
            choices=["llama3.1", "deepseek-r1:14b", "phi4"],
            value="deepseek-r1:14b"
        )

    analyze_btn = gr.Button("Analyze Stock")

    with gr.Row():
        data_out = gr.Dataframe(label="Stock Data", interactive=False)
        plot_out = gr.Plot(label="Interactive Price Chart")

    recommendation_out = gr.Textbox(label="AI Recommendation", interactive=False)

    analyze_btn.click(
        fn=stock_analysis,
        inputs=[ticker, start_date, end_date, model_name],
        outputs=[data_out, plot_out, recommendation_out]
    )

if __name__ == "__main__":
    demo.launch()