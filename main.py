from bs4 import BeautifulSoup
from pygame import mixer 

import requests as req 
import time 

ALARM_FILE = "alarm.mp3"
# IAT Applicant login links
IAT = "https://cdn.digialm.com/EForms/configuredHtml/2245/98100/login.html"
IAT2 = "https://g06.tcsion.com//EForms/loginAction.do?subAction=ViewLoginPage&formId=98100&orgId=2245"
IAT_EDIT_APPL = "https://cdn.digialm.com/EForms/editApplication.do"
# NEST Applicant login links
NEST = "https://cdn3.digialm.com/EForms/configuredHtml/1834/97119/login.html"

def play_alarm():
	'''
	Play the alarm sound 3 times
	'''
	mixer.init()
	mixer.music.load(ALARM_FILE)
	mixer.music.set_volume(1.0)	# max volume
	mixer.music.play(loops=3)

	try:
		while mixer.music.get_busy():
			time.sleep(1)
	except KeyboardInterrupt:
		mixer.music.stop()

def validate_response(response_text):
	'''
	Validate the HTML response by categorizing it as one of 
	> Form Expired Page
	> Login Active page
	> Unknown (none of the above two)
	'''
	try:
		soup = BeautifulSoup(response_text, 'html.parser')

		title = soup.title.string.strip()
		form = soup.form

		loginNotOpen = soup.find(id='LoginNotOpen')				# unique to expired form
		loginCaptchaHolder = soup.find(id='loginCaptchaHolder')	# unique to active login 

		if 	(	# attributes of active login page present
				title == "Applicant Login" and 
				form and form['name'] == "loginForm" and
				not loginNotOpen and
				loginCaptchaHolder
			):
			print("Login Page is Active!")
			return 1

		elif (	# attributes of inactive login page present
				title == "Date Expired" and 
				not form and
				loginNotOpen and
				not loginCaptchaHolder
				):
			print("Login page inactive", end=" | ")
			return 0 

		else:
			print(f"Unknown Response Type:\n\ttitle:{title}\n\tform:{form} \
				\n\tLoginNotOpen:{loginNotOpen}\n\tloginCaptchaHolder:{loginCaptchaHolder}\n")
			return 0

	except Exception as e:
		print(f"Unexpected Exception Raised: {e}")


def main(sleep_bw_reqs=60, save_last_response=False):

	while (r := req.get(IAT, timeout=5)).status_code == req.codes.ok:

		contents = r.text.strip(" \n\t")

		if save_last_response:
			with open(f"last_response.html", 'w') as f:
				f.write(contents)

		readable_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(time.time()))

		if validate_response(contents) == 1:
			print(f">>> SITE IS UPDATED! Time: {readable_time}\n")
			play_alarm()
			break

		print(f"Code {r.status_code}: No changes at {readable_time}")

		time.sleep(sleep_bw_reqs)

	else:
		print(f"Status Code NOT OK: {r.status_code}")
		r.raise_for_status()


if __name__ == "__main__":
	main(save_last_response=True)
	
