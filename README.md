# ClassCharts API for Python
An unofficial python wrapper for the ClassCharts API, making it easier for you to make requests.

There is a usage example included called `classcharts_api_demo.py`. It logges you in as a student and tells you your timetable for the current day.

You can view the API docs here: [API Docs](https://classchartsapi.github.io/api-docs/)
# How to use
You must have the classcharts_api.py in an accessable place by your script.
## Logging in - Student Client
```python
from classcharts_api import StudentClient

client = StudentClient(code="<Pupil Code>", dob="<DOB in YYYY-MM-DD>")
```
## Logging in - Parent Client
```python
from classcharts_api import ParentClient

client = ParentClient(email="example@example.com", password="<Password>")
```
### To use parent client
To use the API with a parent account, it must know which pupil to get data for. Do this with:
```python
client.select_pupil(123456)
```
You can run this multiple times.

Replace '123456' with the student ID (not code) that is found with:
```python
client.list_pupils()
```
# Methods
If there is an error, the method will return the error given in the response. If it is a success, the response will be returned.

In all appropriate methods, `from_date` and `to_date` are not required and will default to Jan 1 1970 and the current day.

## Account data
```python
client.get_account_data()
```
Returns information about the logged in account (parent or student) and what access they have.
## Revalidating Session ID
```python
client.get_new_session_id()
```
This also returns the new session ID as a string.
## Attendance
```python
client.get_attendance(from_date="YYYY-MM-DD", to_date="YYYY-MM-DD")
```
## Activity
```python
client.get_activity(from_date="YYYY-MM-DD", to_date="YYYY-MM-DD", last_id=0)
```
`last_id` is not required here
## Announcements
```python
client.get_announcements(from_date="YYYY-MM-DD", to_date="YYYY-MM-DD")
```
## Behaviour
```python
client.get_behaviour(from_date="YYYY-MM-DD", to_date="YYYY-MM-DD")
```
## Classes
```python
client.get_classes()
```
## Detentions
```python
client.get_detentions()
```
## Homework Tasks
```python
client.get_homework_tasks(from_date="YYYY-MM-DD", to_date="YYYY-MM-DD")
```
## Lessons
```python
client.get_lessons(date="YYYY-MM-DD")
```
Date defaults to current date so is not required

# Student Specific Methods
The following methods only work when logged in as a student

## Pupil Code
```python
client.get_student_code(dob="YYYY-MM-DD")
```
## List Rewards
```python
client.list_rewards()
```
## Purchase Rewards
```python
client.purchase_reward(item_id=123456)
```
## Mark Homework as Completed
```python
client.tick_homework(task_id=123456)
```
`task_id` found in "data", "id" from response from `get_homework_tasks()`.

Running this request again will untick the homework task.

## Mark homework as Seen
```python
client.mark_homework_as_seen(task_status_id=123456)
```
A task cannot be marked as uncompleted by running this request again.

Note that the `task_status_id` is different from `task_id` - the value for `task_status_id` can be found under "data", "status", "id". I have no idea why there are two IDs for the same task.

# Parent Specific Methods
The following methods only work when logged in as a parent.

## Select Pupil
```python
client.select_pupil(student_id=123456)
```
This can be run multiple times.
## Change Password
```python
client.change_password(old="<Current-Password>", new="<New-Password>")
```
## Add Parent Behaviour Point
```python
client.add_parent_behaviour_point(behaviour_id=123456)
```
`behaviour_id` is not required.
## Remove Parent Behaviour Point
```python
client.remove_parent_behaviour_point(behaviour_id=123456)
```
`behaviour_id` is not required.
## List Parent Behaviour Points
```python
client.list_parent_behaviour()
```
## List Pupils
```python
client.list_pupils()
```