from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.urls import path
from datetime import datetime
import time
import requests
import json
from django.views.decorators.csrf import csrf_exempt

# import RPi.GPIO as GPIO

# PIR_SENSOR_PIN = 4
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)

# Create your views here.
def home(request):
    return render(request, "home.html")


@api_view(['GET'])
def motion_detected(request):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%I:%M %p')
    # Loop to send the notification every 10 seconds, 4 times
    for i in range(4):
        send_push_notification(title=f"Motion Detected {i+1}", body=f"Location: Office  Time: {formatted_time}")
        print(f"Notification {i+1} sent")
        time.sleep(10)  # Wait for 10 seconds before sending the next notification

    return JsonResponse({'message': 'Push notifications sent 4 times!'})

    # current_time = datetime.now().strftime('%I:%M %p')
    
    # # Motion detection logic
    # try:
    #     print("Starting motion detection...")
    #     motion_detected_count = 0
        

    #     if GPIO.input(PIR_SENSOR_PIN):
    #         motion_detected_count += 1
    #         # Send push notification
    #         send_push_notification(
    #             title=f"Motion Detected {motion_detected_count}",
    #             body=f"Location: Office  Time: {current_time}"
    #         )
    #         print(f"Notification {motion_detected_count} sent.")
    #         time.sleep(10)  # Wait for 10 seconds before checking again
    #     else:
    #         time.sleep(1)  # Wait a moment to avoid excessive CPU usage

    # except KeyboardInterrupt:
    #     print("Motion detection terminated.")
    # finally:
    #     GPIO.cleanup()  # Clean up GPIO settings

    # return JsonResponse({'message': 'Push notifications sent!'})



def send_push_notification(title, body):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Content-Type": "application/json",
        "Accept": 'application/json',
    }

    # Hardcoded Expo push token for your React Native app
    push_token = "ExponentPushToken[wkpAV-AHN5ifQ-X48fi3Nr]"  # Replace with your actual token

    data = {
        "to": push_token,
        "sound": "default",
        "title": title,
        "body": body,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")
