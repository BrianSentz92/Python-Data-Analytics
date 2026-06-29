import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


def get_period():
    """Prompt the user to select a time period."""

    print("\nSelect a Time Period")
    print("-------------------------")
    print("1. 1 Month")
    print("2. 3 Months")
    print("3. 6 Months")
    print("4. 1 Year")
    print("5. 5 Years")

    choice = input("\nSelection: ")

    periods = {
        "1": "1mo",
        "2": "3mo",
        "3": "6mo",
        "4": "1y",
        "5": "5y"
    }

    return periods.get(choice, "1y")


def download_stock_data(symbol, period):
    """Download historical stock data."""

    ticker = yf.Ticker(symbol)

    history = ticker.history(period=period)

    return history


def display_statistics(symbol, history):
    """Display summary statistics."""

    current_price = history["Close"].iloc[-1]
    highest_price = history["High"].max()
    lowest_price = history["Low"].min()
    average_close = history["Close"].mean()
    average_volume = history["Volume"].mean()

    total_return = (
        (history["Close"].iloc[-1] - history["Close"].iloc[0])
        / history["Close"].iloc[0]
    ) * 100

    print("\n")
    print("=" * 45)
    print(f"{symbol} STOCK SUMMARY")
    print("=" * 45)

    print(f"Current Price     : ${current_price:.2f}")
    print(f"Highest Price     : ${highest_price:.2f}")
    print(f"Lowest Price      : ${lowest_price:.2f}")
    print(f"Average Close     : ${average_close:.2f}")
    print(f"Average Volume    : {average_volume:,.0f}")
    print(f"Trading Days      : {len(history)}")
    print(f"Total Return      : {total_return:.2f}%")

    print("=" * 45)


def plot_stock(symbol, history):
    """Plot the historical closing price."""

    plt.figure(figsize=(12, 6))

    plt.plot(
        history.index,
        history["Close"],
        linewidth=2,
        label="Closing Price"
    )

    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():

    print("=" * 45)
    print("        STOCK MARKET ANALYZER")
    print("=" * 45)

    symbol = input("\nEnter Stock Ticker: ").upper()

    period = get_period()

    print("\nDownloading live market data...\n")

    history = download_stock_data(symbol, period)

    if history.empty:
        print("No data found.")
        return

    display_statistics(symbol, history)

    plot_stock(symbol, history)


if __name__ == "__main__":
    main()