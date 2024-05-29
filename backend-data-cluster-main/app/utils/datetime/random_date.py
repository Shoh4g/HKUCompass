import random
from datetime import datetime, timedelta
import pytz

# Generate a random datetime in the last six months of current date, used for mock data.
def random_date_last_six_months():
    hong_kong_tz = pytz.timezone('Asia/Hong_Kong')
    end_date = datetime.now(tz=hong_kong_tz)
    start_date = end_date - timedelta(days=180)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date