from classcharts_api import StudentClient

code = input("Enter your ClassCharts Pupil Code: ")
dob = input("Enter your date of birth in the format YYYY-MM-DD: ")

client = StudentClient(code=code, dob=dob)

name = client.get_account_data()["data"]["user"]["first_name"]
print(f"Hi {name}!")

lessons = client.get_lessons()["data"]
meta = client.get_lessons()["meta"]

if len(lessons) > 0:
    print("---YOUR TIMETABLE FOR TODAY---")
    
    for lesson in lessons:
        period_num = lesson["period_number"]
        for period in meta["periods"]:
            if period["number"] == period_num:
                start_time = period['start_time'][:5]
        subject = lesson["subject_name"]
        teacher = lesson["teacher_name"]
        room = lesson["room_name"]
        
        print(f"{start_time}: {subject} with {teacher} in {room}")
        
    print("------------------------------")
else:
    print("You have no lessons today :)")