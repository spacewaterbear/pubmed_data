import random

def return_video_list():
    with open("./images/url_videos.txt", "r") as file:
        video_list = file.readlines()
    return video_list

def return_one_random_url():
    random_video_url_list = return_video_list()
    random_video_url = random.choice(random_video_url_list)
    return random_video_url


