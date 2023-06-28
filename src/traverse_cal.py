from datetime import datetime

start = datetime(2011,10,1)
end = datetime(2011,10,15)

end_date_str = f'{end.year}-{end.month}'
start_date_str = f'{start.year}-{start.month}'

start_month = start.month
start_year = start.year

# Starting YYYY-mm
# Increment mm by one, until mm == 13.
# then Increment YYYY by 1, set mm == 1.
# until YYYY-mm equals end date

months = [ start_date_str ]

while start_date_str != end_date_str:
    print("Incrementing!")
    if start_month == 12:
        start_month = 1
        start_year = start_year + 1
    else:
        start_month = start_month + 1
    start_date_str = f'{start_year}-{start_month}'
    print(start_date_str)
    months.append(start_date_str)

return months