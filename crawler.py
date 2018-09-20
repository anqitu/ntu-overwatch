import os
import sched
import time
import sys
from urllib import request
from time import gmtime, strftime

DOWNLOAD_INTERVAL_SECONDS = 3 * 60
DOWNLOAD_DIRECTORY = "cam_images"
CAM_BASE_IMAGE_URL = "https://webcam.ntu.edu.sg/upload/slider/"
CAM_LOCATIONS = [
    "fastfood",
    "foodcourt",
    "lwn-inside",
    "quad",
    "onestop_sac",
    "WalkwaybetweenNorthAndSouthSpines",
]

# DO NOT MODIFY THE CONSTANTS BELOW
CAM_LOCATION_IMG_URLS = {title: "{}{}.jpg".format(CAM_BASE_IMAGE_URL, title) for title in CAM_LOCATIONS}
PID_FILE = "./ntuoverwatch.pid"
TIMESTAMP_FORMAT = "%Y-%m-%d-%H-%M-%S"

def init_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
    for location in CAM_LOCATIONS:
        if not os.path.exists(os.path.join(path, location)):
            os.mkdir(os.path.join(path, location))

def downlad_images(scheduler):
    timestamp = strftime(TIMESTAMP_FORMAT, gmtime())
    download_count = 0
    for location in CAM_LOCATION_IMG_URLS:
        try:
            image_url = CAM_LOCATION_IMG_URLS[location]
            image_path = os.path.join(DOWNLOAD_DIRECTORY, location, "{}.jpg".format(timestamp))
            request.urlretrieve(image_url, image_path)
            download_count += 1
        except Exception as e:
            print("Failed to download {}: {}".format(image_url, str(e)))
    print("{} - Downloaded {} images".format(timestamp, download_count))
    s.enter(DOWNLOAD_INTERVAL_SECONDS, 1, downlad_images, (scheduler,))

if __name__ == "__main__":

    timestamp = strftime(TIMESTAMP_FORMAT, gmtime())
    if os.path.isfile(PID_FILE):
        print("A crawler instance is already running!")
        sys.exit()
    pid = str(os.getpid())
    open(PID_FILE, 'w').write("{}\n{}".format(timestamp, pid))

    print("-" * 40)
    print("NTU OVERWATCH")
    print("-" * 40)

    print("Initializing directories...")
    init_path(DOWNLOAD_DIRECTORY)
    print("- Directory set: {}".format(DOWNLOAD_DIRECTORY))

    print("Starting scheduler...")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(0, 1, downlad_images, (s,))
    print("- Download interval set: {} S".format(DOWNLOAD_INTERVAL_SECONDS))

    print("\nOverwatch at your service!")
    try:
        s.run()
    except KeyboardInterrupt:
        print("\nCrawler shutting down...")
    finally:
        os.unlink(PID_FILE)
