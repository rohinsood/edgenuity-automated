# Edgenuity Automated 😈
> 🏫 A browser script to automatically move to the next video/question when the video is complete or when the question is answered

> 🖊️ This helps students stay focused & productive throughout an activity & minimizes the time waste navigating between videos and questions

> NOTE: This script is not meant to be used to actually automate the process of completing an activity. It is meant to be used as a tool to boost productity and attentiveness. 
---
## Setup 💀
1. Clone the repository 
```cmd
git clone https://github.com/rohinsood/edgenuity-automated.git
```
3. Install the dependencies 
```cmd
pip install selenium webdriver_manager
```
4. Enter your MyPlan username and password on lines 1 and 2 of ```login.txt``` <br /><br />
![login.txt image](https://cdn.discordapp.com/attachments/882455696199807007/988711576137793536/unknown.png)

## Run 🥶
1. Open the folder of the repository ```cd .\path\to\edgenuity-automated```
2. Run ```Run.py``` 
```cmd
python Run.py
```
```OR```
```cmd
python3 Run.py
```
```OR```
```cmd
py Run.py
```
---
### Known Bugs 🤫
1. When logging in to MyPlan, sometimes the request takes too long & the script times out.
```cmd
FIX: Try cicking the Login button in the browser (This isn't reliable because timeouts can still occur due to human error)
FIX: Run the script again (Usually works another time around)
```
### Preview 🤑
![Question Frame Popup](https://cdn.discordapp.com/attachments/882455696199807007/988707957439090729/unknown.png)
_This shows the alert box that will appear when a question is detected, you must click 'OK' in order to answer the question_

