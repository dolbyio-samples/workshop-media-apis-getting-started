#A helper function file for "Workshop Part 1"
#Questions: @BradenRiggs1

import shutil
import time
import requests


def start_job(dolbyio_mapi_key, target_audio_file):
    #Starts a Dolby.io Enhance job 
    #dolbyio_mapi_key: Your unique Media API Key.
    #target_audio_file: The audio file targeted for enhancement.
    #Return: The file output location, the Enhance job ID

    body = {
    "input" : {"url":target_audio_file,
    "region": {
        "start": 0,
        "end": 12}
    },
    "output" : "dlb://out/test_1-enhanced.wav",
    "content" : {
        "type": "mobile_phone"},
    }

    url = "https://api.dolby.com/media/enhance"

    headers = {
    "x-api-key": dolbyio_mapi_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
    }

    response = requests.post(url, json=body, headers=headers)
    print(response.json())
    print("Enhance job has started.")
    job_id = response.json()["job_id"]


    return body["output"], job_id

def check_job(dolbyio_mapi_key, job_id):
    #Checks the staus of the Dolby.io Enhance job 
    #dolbyio_mapi_key: Your unique Media API Key.
    #job_id: The job id of the Enhance job

    print("Enhance job is running:")
    url = "https://api.dolby.com/media/enhance"
    while True:

        headers = {
        "x-api-key": dolbyio_mapi_key,
        "Content-Type": "application/json",
        "Accept": "application/json"}

        params = {"job_id": job_id}

        response = requests.get(url, params=params, headers=headers)
        print(response.json()["status"])

        if response.json()["status"] == "Success":
            print("Enhance job is complete.")
            break
        time.sleep(5)
    

def download_file(dolbyio_mapi_key, out_file):
    #Downloads the results of a Dolby.io Enhance job
    #dolbyio_mapi_key: Your unique Media API Key.
    #out_file: The file output location
    #Return: The downloaded file location

    url = "https://api.dolby.com/media/output"
    headers = {
        "x-api-key": dolbyio_mapi_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    args = {"url": out_file,}

    with requests.get(url, params=args, headers=headers, stream=True) as response:
        response.raise_for_status()
        response.raw.decode_content = True
        print("Downloading corrected audio")
        with open("test_1-enhanced.wav", "wb") as output_file:
            shutil.copyfileobj(response.raw, output_file)
    return "test_1-enhanced.wav"
