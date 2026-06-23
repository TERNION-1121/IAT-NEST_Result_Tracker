from bs4 import BeautifulSoup
from os import system
from pygame import mixer 

import argparse
import requests as req 
import time 

ALARM_FILE = "alarm.mp3"
URL = {	
		'IAT' : "https://g06.tcsion.com//EForms/loginAction.do?subAction=ViewLoginPage&formId=98100&orgId=2245",
		'NEST':	"https://g06.tcsion.com//EForms/loginAction.do?subAction=ViewLoginPage&formId=97119&orgId=1834"
		}

def play_alarm():
	'''
	Play the alarm sound indefinitely until KeyboardInterrupt
	'''
	mixer.init()
	mixer.music.load(ALARM_FILE)
	mixer.music.set_volume(1.0)	# max volume
	mixer.music.play(loops=-1)	# play indefinitely

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

def tracker(exam: str, sleep_interval=60, save_last_response=False):

	while (r := req.get(URL[exam], timeout=5)).status_code == req.codes.ok:

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

		time.sleep(sleep_interval)

	else:
		print(f"Status Code NOT OK: {r.status_code}")
		r.raise_for_status()

def main():
	system("cls||clear") # clear terminal screen before execution

	parser = argparse.ArgumentParser(
						description='Track the status of the applicant login page for IISER Aptitude Test (IAT) and/or National Entrance Screening Test (NEST) exams using a simple Python script and notify the user upon encountering desirable changes.',
						epilog='Made by TERNION, for the community')

	parser.add_argument('exam', choices=['IAT', 'NEST'])
	parser.add_argument('-s', '--save', action='store_true', help="externally save the html response body pertaining to the last url request")
	parser.add_argument('-t', '--interval', type=int, default=60, help='time interval between successive url requests')

	args = parser.parse_args()

	tracker(exam=args.exam, sleep_interval=args.interval, save_last_response=args.save)


if __name__ == "__main__":
	main()
