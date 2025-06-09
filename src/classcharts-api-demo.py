from classcharts_api import StudentClient
from datetime import datetime

code = input("Enter your ClassCharts Pupil Code: ")
dob = input("Enter your date of birth in the format YYYY-MM-DD: ")

client = StudentClient(code=code, dob=dob)

name = client.get_account_data()["data"]["user"]["first_name"]
print(f"Hi {name}!")

lessons = client.get_lessons("2025-06-08")["data"]
if len(lessons) > 0:
    print("---YOUR TIMETABLE FOR TODAY---")
    for lesson in lessons:
        start_time = datetime.fromisoformat(lesson["start_time"])
        subject = lesson["subject_name"]
        teacher = lesson["teacher_name"]
        room = lesson["room_name"]
        print(f"{start_time.strftime("%H:%M")}: {subject} with {teacher} in {room}")
    print("------------------------------")
else:
    print("You have no lessons today :)")