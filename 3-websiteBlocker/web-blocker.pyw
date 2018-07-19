# Block websites in working hours
import time
from datetime import datetime as dt

host_path = r"C:\Windows\System32\drivers\etc"
redirect = "127.0.0.1"
website_list = ["www.facebook.com", "www.twitter.com"]

actualHour = dt.now()
d = dt.now()
while True:
    with open(host_path, 'r+') as host_file:
        # If actualHour between 9 and 18
        if dt(d.year, d.month, d.day, 9) < actualHour < dt(d.year, d.month, d.day, 18):
            print('Working hour')

            # Add website to host file
            content = host_file.read()
            for website in website_list:
                if website in content:
                    pass
                else:
                    host_file.write("\n" + redirect + " " + website)
        else:
            print('Fun hour')

            # Append from first line of hosts file any line that doesn't contain a website blocked to this file.
            content = host_file.readlines()
            host_file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    host_file.write(line)
            # Truncate old content
            host_file.truncate()
    print(content)
    time.sleep(60)
