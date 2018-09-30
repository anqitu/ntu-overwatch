# NTU Overwatch Tagger

## Usage

1. Move the images you need to tag inside the `/images` folder
2. Install `flask` with `pip install flask`
3. Run the app with `python app.py`
4. View the app from your browser by going to `127.0.0.1:5000`
5. Tag the count as the number of people in the image accordingly
6. Results will automatically be written to a file called `tagging.csv`

## FAQ

1. I've incorrectly tagged an image. How can I go back to the previous image?
> You can't. You have to edit the entry in the tagging.csv manually. The latest entry should be at the bottom of the file.

2. I gotta go and I need to pause this for awhile. Will my progress be affected?
> The results are appended to the file after every tagging of an image. You can safely kill the server with `ctrl+c` and run it again later if you wish to resume your tagging. It should bring you back to the last image you were left with when you open it again.
