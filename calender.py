import calendar

def print_calendar(year, month):
    """Prints a calendar for the specified month and year."""
    print(calendar.month(year, month))

# Get input from the user
year = int(input("Enter the year: "))
month = int(input("Enter the month (1-12): "))

# Print the calendar
print_calendar(year, month)