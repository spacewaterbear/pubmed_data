from datetime import datetime
def to_datetime(dico):
    date_time_str = f"{dico['Year']}-{dico['Month']}-{dico['Day']}"
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    return date_time_obj

