import os
import humanize
import crawler
import time
from time import strptime, gmtime, mktime

def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return humanize.naturalsize(total_size)

def get_file_count(path):
    return sum([len(files) for r, d, files in os.walk(path)])

def get_time_elapsed(since):
    now = gmtime()
    elapsed = mktime(now) - mktime(since)
    return humanize.naturaltime(elapsed)

if __name__ == "__main__":

    if os.path.isfile(crawler.PID_FILE):
        with open(crawler.PID_FILE) as pid_file:
            pid_data = pid_file.readlines()
            uptime = strptime(pid_data[0].strip(), crawler.TIMESTAMP_FORMAT)
            print("Status: RUNNING")
            print("Up Since: {}".format(get_time_elapsed(uptime)))
    else:
        print("Status: DOWN")
        

    current_size = get_size(crawler.DOWNLOAD_DIRECTORY)
    print('Current Size: {}'.format(current_size))

    images_count = get_file_count(crawler.DOWNLOAD_DIRECTORY)
    print('Images Downloaded: {}'.format(images_count))
    
