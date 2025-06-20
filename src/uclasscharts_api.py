import urequests
import utime

BASE_URL = "https://www.classcharts.com/apiv2student"

def current_date():
  localtime = utime.localtime()
  year = str(localtime[0])
  month = str(localtime[1])
  day = str(localtime[2])
  
  if len(month) == 1:
    month = f"0{month}"
  
  if len(day) == 1:
    day = f"0{day}"
  
  return f"{day}-{month}-{year}"

class GlobalClient:
  def __init__(self, session_id, student_id):
    self.session_id = session_id
    self.student_id = student_id

  def _ping(self):
      url = f"{BASE_URL}/ping"
      body = "include_data=true"
      headers = {
          "Authorization": f"Basic {self.session_id}",
          "Content-Type": "application/x-www-form-urlencoded"
      }
      response = urequests.post(url, data=body, headers=headers)
      data = response.json()
      return response, data

  def get_account_data(self):
      response, data = self._ping()
      if response.status_code == 200:
          return data
      raise Exception(data["error"])

  def get_new_session_id(self):
      response, data = self._ping()
      if response.status_code == 200:
          self.session_id = data["meta"]["session_id"]
          return self.session_id
      raise Exception(data["error"])

  def get_attendance(self, from_date="1970-01-01",to_date=current_date()):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/attendance/{self.student_id}?from={from_date}&to={to_date}"
      headers = {
          "Authorization" : f"Basic {self.session_id}",
      }

      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

  def get_activity(self, from_date="1970-01-01", to_date=current_date(), last_id=None):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      if last_id:
        url = f"{BASE_URL}/activity/{self.student_id}?from={from_date}&to={to_date}&last_id={last_id}"
      else:
        url = f"{BASE_URL}/activity/{self.student_id}?from={from_date}&to={to_date}"
      headers = {
        "Authorization": f"Basic {self.session_id}"
      }
      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

  def get_announcements(self):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/announcements/{self.student_id}"
      headers = {
        "Authorization": f"Basic {self.session_id}"
      }
      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

  def get_badges(self):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/eventbadges/{self.student_id}"
      headers = {
        "Authorization": f"Basic {self.session_id}"
      }
      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:  
        raise Exception(data["error"])

  def get_behaviour(self, from_date="1970-01-01", to_date=current_date()):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/behaviour/{self.student_id}?from={from_date}&to={to_date}"
      headers = {
        "Authorization": f"Basic {self.session_id}"
      }
      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

  def get_classes(self):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/classes/{self.student_id}"
      headers = {
        "Authorization": f"Basic {self.session_id}"
      }
      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:  
        raise Exception(data["error"])

  def get_detentions(self):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/detentions/{self.student_id}"
      headers = {
        "Authorization": f"Basic {self.session_id}"
      }
      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

  def get_homework_tasks(self, from_date="1970-01-01",to_date=current_date(), display_date="issue_date"):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/homeworks/{self.student_id}?display_date={display_date}&from={from_date}&to={to_date}"
      headers = {
          "Authorization" : f"Basic {self.session_id}",
      }

      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:  
        raise Exception(data["error"])

  def get_lessons(self, date=current_date()):
    if not self.student_id:
      raise ValueError("No student selected")
    else:
      url = f"{BASE_URL}/timetable/{self.student_id}?date={date}"
      headers = {
          "Authorization" : f"Basic {self.session_id}",
      }

      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:  
        raise Exception(data["error"])

class StudentClient(GlobalClient):
    def __init__(self, code, dob):
        url = f"{BASE_URL}/login"
        code = code.upper()
        body = f"""code={code}&remember=true&recaptcha-token=no-token-available&dob={dob}"""
        headers = {
          "Content-Type": "application/x-www-form-urlencoded"
        }

        response = urequests.post(url, data=body, headers=headers)
        data = response.json()

        if data["success"] == 1:
          student_id = data["data"]["id"]
          session_id = data["meta"]["session_id"]
          super().__init__(session_id, student_id)
        else:
          raise Exception(data["error"])

    def get_student_code(self, dob):
      url = f"{BASE_URL}/getcode"
      body = f"""date={dob}"""
      headers = {
          "Authorization" : f"Basic {self.session_id}",
          "Content-Type": "application/x-www-form-urlencoded"
      }

      response = urequests.post(url, data=body, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data["data"]["code"].upper()
      else:
        raise Exception(data["error"])

    def list_rewards(self):
      url = f"{BASE_URL}/rewards/{self.student_id}"
      headers = {
          "Authorization" : f"Basic {self.session_id}",
      }

      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

    def purchase_reward(self, item_id):
      url = f"{BASE_URL}/purchase/{item_id}"
      body = f""""""
      headers = {
          "Authorization" : f"Basic {self.session_id}",
          "Content-Type": "application/x-www-form-urlencoded"
      }

      response = urequests.post(url, data=body, headers=headers)
      data = response.json()

      if data["success"] == 1:
        return data
      else:
        raise Exception(data["error"])

    def tick_homework(self, task_id):
      url = f"{BASE_URL}/homeworkticked/{task_id}?studentId={self.student_id}"
      headers = {
          "Authorization" : f"Basic {self.session_id}",
      }

      response = urequests.get(url, headers=headers)
      data = response.json()

      if data["success"] == 0:
        raise Exception(data["error"])
      
    def mark_homework_as_seen(self, task_status_id):
      url = f"{BASE_URL}/markhomeworkasseen/{task_status_id}"
      body = f"""pupil_id={self.student_id}"""
      headers = {
          "Authorization" : f"Basic {self.session_id}",
      }
      
      response = urequests.post(url, data=body, headers=headers)
      data = response.json()
      
      if data["success"] == 0:
        raise Exception(data["error"])
      
class ParentClient(GlobalClient):
  def __init__(self, email, password):
    url = f"{BASE_URL}/login"
    body = f"""email={email}&password={password}&remember=true&recaptcha-token=no-token-available"""
    headers = {
      "Content-Type": "application/x-www-form-urlencoded"
    }

    response = urequests.post(url, data=body, headers=headers)
    data = response.json()

    if data["success"] == 1:
      self.session_id = data["meta"]["session_id"]
      super().__init__(session_id=self.session_id, student_id=None)
    else:
      raise Exception(data["error"])

  def select_pupil(self, student_id):
    self.student_id = student_id

  def change_password(self, old, new):
    url = f"{BASE_URL}/password"
    body = f"""current={old}&new={new}&repeat={new}"""
    headers = {
      "Authorization": f"Basic {self.session_id}",
      "Content-Type": "application/x-www-form-urlencoded"
    }
    response = urequests.post(url, data=body, headers=headers)
    data = response.json()

    if data["success"] == 0:
      return data["error"]

  def add_parent_behaviour_point(self, behaviour_id=None):
    url = f"{BASE_URL}/addparentbehaviour/{self.student_id}"
    if behaviour_id:
      body = f"""behaviour_id={behaviour_id}"""
    else:
      body = """"""
    headers = {
      "Authorization": f"Basic {self.session_id}",
      "Content-Type": "application/x-www-form-urlencoded"
    }
    response = urequests.post(url, data=body, headers=headers)
    data = response.json()

    if data["success"] == 1:
      return data
    else:
      raise Exception(data["error"])

  def remove_parent_behaviour_point(self, behaviour_id=None):
    url = f"{BASE_URL}/deleteparentbehaviour/{self.student_id}"
    if behaviour_id:
      body = f"""behaviour_id={behaviour_id}"""
    else:
      body = """"""
    headers = {
      "Authorization": f"Basic {self.session_id}",
      "Content-Type": "application/x-www-form-urlencoded"
    }
    response = urequests.post(url, data=body, headers=headers)
    data = response.json()

    if data["success"] == 0:
      raise Exception(data["error"])

  def list_parent_behaviour(self):
    url = f"{BASE_URL}/parentbehaviours/{self.student_id}"
    headers = {
      "Authorization": f"Basic {self.session_id}",
      "Content-Type": "application/x-www-form-urlencoded"
    }
    response = urequests.get(url, headers=headers)
    data = response.json()

    if data["success"] == 1:
      return data
    else:
      raise Exception(data["error"])
    
  def list_pupils(self):
    url = f"{BASE_URL}/pupils"
    headers = {
        "Authorization" : f"Basic {self.session_id}",
    }

    response = urequests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
      return data
    else:
      raise Exception(data["error"])  

