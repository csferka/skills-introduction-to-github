import tkinter as tk
from tkinter import  messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global variables to store expense data
expenses = []
total_expense = 0

# Email and API keys
MY_EMAIL = "feruzbekpirmatov04@gmail.com"  # Replace with your email
PASSWORD = "smjo oiww coht kkwz"          # Replace with your email password
NEWS_API_KEY = "ce635da561564859a1323f1bd239468c"
STOCK_API_KEY = "RUGC94P0ZABE02F7" #Replace this with your own api stock key
#https://www.alphavantage.co/support/#api-key here

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def add_item():
    global total_expense
    try:
        item = entry_name.get()
        quantity = int(entry_quantity.get())
        cost = float(entry_cost_per_unit.get())
        total = quantity * cost
        expenses.append((item, quantity, cost, total))

        # Update the table
        expenses_table.insert("", "end", values=(item, quantity, cost, total))

        # Update the total expense
        total_expense += total
        total_label.config(text=f"Total Expenses: ${total_expense:.2f}")

        # Clear entry fields
        entry_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_cost_per_unit.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid quantity and cost.")

def analyze_expenses():
    if not expenses:
        messagebox.showinfo("No Data", "No expenses to analyze.")
        return

    # Prepare data for the pie chart
    items = [expense[0] for expense in expenses]
    totals = [expense[3] for expense in expenses]

    # Create the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(totals, labels=items, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution")
    plt.show()

def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_cost_per_unit.delete(0, tk.END)

def clear_expenses():
    global expenses, total_expense
    expenses = []
    total_expense = 0
    expenses_table.delete(*expenses_table.get_children())
    total_label.config(text=f"Total Expenses: ${total_expense:.2f}")

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

        if abs(diff_percent) >0:
            articles = fetch_news(stock_name)
            email_body = f"Stock: {stock_name}\nPrice Change: {diff_percent}%\n\n" + "\n\n".join(articles)
            send_email(f"Stock Update: {stock_name}", email_body, recipient_email)
        else:
            messagebox.showinfo("No Significant Change", "Price change is less than 5%.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Unified GUI Setup
root = tk.Tk()
root.title("Unified App")
root.geometry("800x600")
root.configure(background="#6AB187")
# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)
# Expense Tracker Tab
expense_frame = tk.Frame(notebook, bg="#6AB187")
notebook.add(expense_frame, text="Expense Tracker")
# Expense Tracker Components
expense_title = tk.Label(expense_frame, text="Expense Tracker", background="#6AB187", font=("Arial", 16, "bold"))
expense_title.pack(pady=10)
tk.Label(expense_frame, text="Item", background="#6AB187").pack(pady=5)
entry_name = tk.Entry(expense_frame)
entry_name.pack(pady=5)
tk.Label(expense_frame, text="Quantity", background="#6AB187").pack(pady=5)
entry_quantity = tk.Entry(expense_frame)
entry_quantity.pack(pady=5)
tk.Label(expense_frame, text="Cost Per Unit", background="#6AB187").pack(pady=5)
entry_cost_per_unit = tk.Entry(expense_frame)
entry_cost_per_unit.pack(pady=5)
frame1 = tk.Frame(expense_frame, bg="#6AB187")
tk.Button(frame1, text="Add Item", background="#6AB187", command=add_item).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="Clear Inputs", background="#6AB187", command=clear_inputs).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="Clear Expenses", background="#6AB187", command=clear_expenses).pack(side=tk.LEFT, padx=5)
frame1.pack(pady=10)
tk.Label(expense_frame, text="Expenses", background="#6AB187").pack(pady=5)
columns = ("Item", "Quantity", "Unit Cost", "Total")
expenses_table = ttk.Treeview(expense_frame, columns=columns, show="headings")
for col in columns:
    expenses_table.heading(col, text=col)
expenses_table.pack(pady=5, fill=tk.BOTH, expand=True)

total_label = tk.Label(expense_frame, text=f"Total Expenses: ${total_expense:.2f}", background="#6AB187", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

tk.Button(expense_frame, text="Analyse", background="#6AB187", command=analyze_expenses).pack(pady=10)

# Stock Market Analyzer Tab
stock_frame = tk.Frame(notebook, bg="#6AB187")
notebook.add(stock_frame, text="Stock Market Analyzer")

stock_title = tk.Label(stock_frame, text="Stock Market Analyzer", background="#6AB187", font=("Arial", 16, "bold"))
stock_title.pack(pady=10)

tk.Label(stock_frame, text="Stock Name:", background="#6AB187").pack(pady=10)
entry_stock_name = tk.Entry(stock_frame, width=30)
entry_stock_name.pack(pady=5)

tk.Label(stock_frame, text="Recipient Email:", background="#6AB187").pack(pady=10)
entry_email = tk.Entry(stock_frame, width=30)
entry_email.pack(pady=5)

tk.Button(stock_frame, text="Analyze and Send", background="#6AB187", command=analyze_and_send).pack(pady=20)

# Run the application
root.mainloop()

