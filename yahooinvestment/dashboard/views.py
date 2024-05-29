from django.shortcuts import render
from .data_fetcher import fetch_all_stocks_data
import pandas as pd

def get_nearest_date(data, target_date):
    # Ensure both target_date and data.index are timezone-naive
    target_date = target_date.tz_localize(None) if target_date.tz is not None else target_date
    data.index = data.index.tz_localize(None) if data.index.tz is not None else data.index
    nearest_date = min(data.index, key=lambda x: abs(x - target_date))
    return nearest_date

def dashboard_view(request):
    stock_data = fetch_all_stocks_data()

    processed_data = {}
    total_value = 0
    colors = {
        'AAPL': 'rgba(75, 192, 192, 1)',
        'MSFT': 'rgba(54, 162, 235, 1)',
        'VTI': 'rgba(255, 206, 86, 1)',
    }

    target_date_1231 = pd.Timestamp('2023-12-31')
    target_date_331 = pd.Timestamp('2024-03-31')

    for ticker, info in stock_data.items():
        hist = info['history']
        shares = info['shares']
        beta = info['beta']

        nearest_date_1231 = get_nearest_date(hist, target_date_1231)
        nearest_date_331 = get_nearest_date(hist, target_date_331)

        hist['Investment Value'] = hist['Close'] * shares
        last_close = round(hist['Close'].loc[nearest_date_331], 2)
        last_day_change = round(((hist['Close'].loc[nearest_date_331] - hist['Close'].loc[nearest_date_331 - pd.Timedelta(days=1)]) / hist['Close'].loc[nearest_date_331 - pd.Timedelta(days=1)]) * 100, 2)
        last_3_months_change = round(((hist['Close'].loc[nearest_date_331] - hist['Close'].loc[nearest_date_1231]) / hist['Close'].loc[nearest_date_1231]) * 100, 2)
        
        processed_data[ticker] = {
            'history': hist.to_dict(orient='records'),
            'last_close': last_close,
            'last_day_change': last_day_change,
            'last_3_months_change': last_3_months_change,
            'beta': round(beta, 2) if isinstance(beta, (int, float)) else 'N/A',
            'color': colors.get(ticker, 'rgba(0, 0, 0, 1)'),
            'shares': shares,
        }
        total_value += last_close * shares

    line_chart_labels = stock_data['AAPL']['history'].index.strftime('%Y-%m-%d').tolist()
    pie_chart_data = [processed_data[ticker]['last_close'] * processed_data[ticker]['shares'] for ticker in processed_data]
    pie_chart_colors = [processed_data[ticker]['color'] for ticker in processed_data]

    context = {
        'data': processed_data,
        'total_value': round(total_value, 2),
        'line_chart_labels': line_chart_labels,
        'pie_chart_data': pie_chart_data,
        'pie_chart_colors': pie_chart_colors,
    }
    return render(request, 'dashboard/dashboard.html', context)
