import tkinter as tk
from tkinter import messagebox
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Environment variables for sensitive data
MY_EMAIL = "feruzbekpirmatov04@gmail.com"  # Replace with your email
PASSWORD = "zppb hufu opfc toxw"          # Replace with your email password
NEWS_API_KEY = "ce635da561564859a1323f1bd239468c"
STOCK_API_KEY = "360NFMD8R53PSCZ0"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def fetch_stock_data(stock_name):
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_name,
        "apikey": STOCK_API_KEY
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    return data_list

def fetch_news(company_name):
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": company_name
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    articles = response.json()["articles"][:3]
    return [
        f"Headline: {article['title']}\nURL: {article['url']}\nAuthor: {article.get('author', 'N/A')}"
        for article in articles
    ]

def send_email(subject, body, recipient_email):
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)

            msg = MIMEMultipart()
            msg['From'] = MY_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
            connection.send_message(msg)
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

def analyze_and_send():
    stock_name = entry_stock_name.get().strip()
    recipient_email = entry_email.get().strip()

    if not stock_name or not recipient_email:
        messagebox.showerror("Input Error", "Both stock name and recipient email are required.")
        return

    try:
        data_list = fetch_stock_data(stock_name)
        yesterday_data = data_list[0]
        day_before_yesterday_data = data_list[1]

        yesterday_closing_price = float(yesterday_data["4. close"])
        day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

        difference = yesterday_closing_price - day_before_yesterday_closing_price
        diff_percent = round((difference / yesterday_closing_price) * 100, 2)

        if abs(diff_percent) > 0:
            articles = fetch_news(stock_name)
            email_body = f"Stock: {stock_name}\nPrice Change: {diff_percent}%\n\n" + "\n\n".join(articles)
            send_email(f"Stock Update: {stock_name}", email_body, recipient_email)
        else:
            messagebox.showinfo("No Significant Change", "Price change is less than 5%.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("Stock Market Analyzer")
root.geometry("500x400")
root.configure(background="#6AB187")

# Stock name input
label_stock_name = tk.Label(root, text="Stock Name:", background="#6AB187")
label_stock_name.pack(pady=10)
entry_stock_name = tk.Entry(root, width=30)
entry_stock_name.pack(pady=5)

# Recipient email input
label_email = tk.Label(root, text="Recipient Email:", background="#6AB187")
label_email.pack(pady=10)
entry_email = tk.Entry(root, width=30)
entry_email.pack(pady=5)

# Analyze and Send button
analyze_button = tk.Button(root, text="Analyze and Send", background="#6AB187", command=analyze_and_send)
analyze_button.pack(pady=20)

root.mainloop()
