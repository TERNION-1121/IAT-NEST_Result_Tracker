# IAT-NEST Result Tracker
Track the status of the applicant login page for _IISER Aptitude Test_ **(IAT)** and/or _National Entrance Screening Test_ **(NEST)** exams using a simple Python script and notify the user upon encountering desirable changes.

Inspired from [DikshitRJ/fackNTA](https://github.com/DikshitRJ/fackNTA)

```bash
Login page inactive | Code 200: No changes at Tue, 16 Jun 2026 12:16:09
Login page inactive | Code 200: No changes at Tue, 16 Jun 2026 12:17:10
Login page inactive | Code 200: No changes at Tue, 16 Jun 2026 12:18:10
Login page inactive | Code 200: No changes at Tue, 16 Jun 2026 12:19:10
Login Page is Active!
>>> SITE IS UPDATED! Time: Tue, 16 Jun 2026 12:20:11
```
> Sample terminal output when the Applicant Login Form goes active 

## Working
The script looks for specific signatures within the response HTML fetched from the Applicant Login Page's URL for the respective exam (either IAT or NEST).
Since all exam related activities like candidate registration, portal for changes, admit card release, response sheet release, and scorecard declaration — all happen on the same Applicant Portal, it is reasonable to track the changes in the response body of the corresponding exam's Applicant Login page. Also since the 
body engaged in providing these online services is the same for both IAT and NEST — TCSion — therefore the script works equally well for tracking major exam related events for both IAT and NEST.

> [!IMPORTANT] 
> The script only notifies the user whether the Applicant Login Form has gone live or not. It can very well be the case that the login form has gone live however the form is not accepting any responses i.e. it leads you to an error page despite filling in your login details. In such cases, the fact that the Applicant Login page's title has changed from "Date Expired" to "Applicant Login" is an affirmative sign indicating that the Form might be going live soon!

## How to Use
- Python3.12+ is required
- Download/Clone this GitHub Repository
- Navigate to the repository directory on your device
- Install the requirements using the following terminal command :
    `pip install -r requirements.txt` 
- Run the script:
    `python main.py`
    > use `python3 main.py` on Linux/MacOS

The script sends a request to the corresponding exam's Applicant Login URL once every minute (this duration can be changed in the code). Upon confirmation that the Applicant Login Form has gone live — an alert is displayed on the terminal and an alarm sound is played alongside that.
> You can change your alarm sound by recording your own alarm sound and saving it in the directory of the repository with the name `alarm.mp3`

## End Notes
The plan is to convert this script into a simple Command Line Interface (CLI) so that users can easily choose between IAT/NEST and also configure some settings at their own convenience without playing with the code directly. 

Meaningful contributions towards this project are appreciated and welcomed!
