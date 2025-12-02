import pyautogui
import ollama
from ollama import chat
from ollama import Client
import mss
import numpy as np
import easyocr#
import time
import requests
import re
import os
import webbrowser
import keyboard


client = Client()
time.sleep(3)

# Screen capture region
monitor = {"top": 350, "left": 50, "width": 950, "height": 450}
question = {"top": 350, "left": 50, "width": 1100, "height": 450}
reader = easyocr.Reader(['en'], gpu=True)

i = 1
while i < 6:
    time.sleep(2)
    # Capture screen
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)[:, :, :3][:, :, ::-1]  # BGRA->RGB

    # OCR
    keyboard.press('alt')
    # Press and release Tab
    keyboard.press_and_release('tab')
    # Release Alt
    keyboard.release('alt')

    results = reader.readtext(img)
    ocr_text = " ".join([text for _, text, _ in results])

    query = ocr_text
    webbrowser.open(f"https://www.google.com/search?q={query}")

    time.sleep(6)

    with mss.mss() as sct:
        qscreenshot = sct.grab(question)

    keyboard.press('alt')
    # Press and release Tab
    keyboard.press_and_release('tab')
    # Release Alt
    keyboard.release('alt')

    results2 = reader.readtext(img)
    ocr_text2 = " ".join([text for _, text, _ in results])

    print("OCR text:", ocr_text)

    # AI system prompt
    SYSTEM_PROMPT = (
        "Look at the question and options and determine which choice is correct. "
        "search up the answer to the question"
            
    
        "Only output the number corresponding to the correct choice, e.g., '1', '2', '3', or '4'. "
        "Respond with only the one number corresponding to the correct choice that is closest to answer when searching up question. "
        "Answer correctly. "

    )

    response = client.chat(
        model="qwen3:30b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": ocr_text2},
            {"role": "user", "content": ocr_text}
        ],
        options = {"web_search": True}
    )



    # Extract AI text
    try:
        ai_text = response.message.content.strip()
        ai_text_clean = "".join(c for c in ai_text if c.isdigit())
        aifeedback = int(ai_text_clean) if ai_text_clean else 5
    except Exception as e:
        print("Error parsing AI response:", e)
        aifeedback = 0


    # Click the correct choice
    choice_positions = {1: 460, 2: 510, 3: 560, 4: 600, 5: 660}
    doublelinechoice_positions = {1: 480, 2: 530, 3: 580, 4: 620, 5: 680}

    if aifeedback in choice_positions:
        pyautogui.moveTo(500, choice_positions[aifeedback], duration=0.5)
        pyautogui.click()
        pyautogui.moveTo(500, doublelinechoice_positions[aifeedback] , duration=0.5)
        pyautogui.click()
    elif aifeedback not in choice_positions:
        print("Invalid answer, pausing.")
        continue
    else:
        print("Cannot find answer. AI response:", ai_text)


    time.sleep(1)
    pyautogui.moveTo(500, 730, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(500, 760, duration=0.5)
    pyautogui.click()
