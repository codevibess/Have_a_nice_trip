import datetime

#  this function convert date form UNIX format to UTC
def convert_date_to_UTC(date):
    return datetime.datetime.fromtimestamp(
        int(date)
    ).strftime('%Y-%m-%d')