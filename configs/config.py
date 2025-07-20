import os
import dspy
from dotenv import load_dotenv

load_dotenv()

lm = dspy.LM('gemini/gemini-2.0-flash', api_key = os.getenv("API_KEY"))
dspy.configure(lm=lm)