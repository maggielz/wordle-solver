from datetime import datetime

def print_time(label="TIME"):
    now = datetime.now()
    print(f'{label}: {now.strftime("%I:%M:%S %p")}')