import time

import pyautogui

bnr_egl = '503300003037'
amount = '35'
equ = '45G1'
weight = '27000'

tol = 'NLEMX'
shipper = 'XCL'

"""
Kan vara bättre att använda 'locateCenterOnScreen() istället för 'click' och png-fil?
Och inkludera region=x, x, x, x
samt grayscale=True
"""


pyautogui.click(r'png\bnr_search_bar_empty.png')
pyautogui.write(bnr_egl)
pyautogui.press('enter')
pyautogui.move(xOffset=0, yOffset=200)

time.sleep(2)
bnr_exists = None

while bnr_exists == None:
    bnr_exists = pyautogui.locateOnScreen(r'png\bnr_exists2.png', minSearchTime=10)

if bnr_exists:
    pyautogui.click(r'png\bnr_exists2.png', duration=0.2)
    pyautogui.click(r'png\bnr_edit.png', duration=0.5)

#time.sleep(2)
bnr_edit_panel = None
bnr_edit_panel_dark = None

while bnr_edit_panel == None and bnr_edit_panel_dark == None:
    bnr_edit_panel = pyautogui.locateOnScreen(r'png\bnr_edit_panel.png')
    bnr_edit_panel_dark = pyautogui.locateOnScreen(r'png\bnr_edit_panel_dark.png')

if bnr_edit_panel or bnr_edit_panel_dark:
    pyautogui.click(r'png\equ_tally_out.png')
    pyautogui.rightClick()
    time.sleep(0.5)
    pyautogui.move(xOffset=10, yOffset=10)
    pyautogui.leftClick()

#time.sleep(2)
equ_edit_panel = None
equ_edit_panel_dark = None

while equ_edit_panel == None and equ_edit_panel_dark == None:
    equ_edit_panel = pyautogui.locateOnScreen(r'png\equ_edit_panel.png')
    equ_edit_panel = pyautogui.locateOnScreen(r'png\equ_edit_panel_dark.png')

if equ_edit_panel or equ_edit_panel_dark:
    pyautogui.write(amount)
    pyautogui.press('tab')
    time.sleep(0.1)
    pyautogui.press('tab')
    time.sleep(0.1)
    pyautogui.write(equ)
    time.sleep(0.2)
    pyautogui.press('tab')
    pyautogui.click(r'png\equ_weight.png')
    pyautogui.move(xOffset=200, yOffset=4)
    time.sleep(0.1)
    pyautogui.leftClick()
    with pyautogui.hold('ctrl'):
        pyautogui.press('a')
    pyautogui.press('backspace')
    pyautogui.write(weight)