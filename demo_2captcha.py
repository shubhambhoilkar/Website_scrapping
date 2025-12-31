import sys
import os
from dotenv import load_dotenv
from twocaptcha import TwoCaptcha

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
image_path = "captch_image.png"
api_key = os.getenv("new_2CAPTCHA_API")
solver = TwoCaptcha(api_key)
try:
    result = solver.normal(image_path)
except Exception as e:
    sys.exit(e)

else:
    sys.exit("solved: "+ str(result))
