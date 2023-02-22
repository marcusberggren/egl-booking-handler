import time

import pyautogui

bnr_egl = '503300003258'
amount = '3'
equ = '45G1'
weight = '25000'

tol = 'NLEMX'
shipper = 'XCL'


pyautogui.click(r'png\bnr_search_bar_empty.png')
pyautogui.write(bnr_egl)
pyautogui.press('enter')
pyautogui.move(xOffset=0, yOffset=200)

bnr_exists = None

while bnr_exists == None:
    bnr_exists = pyautogui.locateOnScreen(r'png\bnr_exists.png', minSearchTime=10)

if bnr_exists:
    pyautogui.click(r'png\bnr_exists.png', duration=0.2)
    pyautogui.click(r'png\bnr_edit.png', duration=0.5)

bnr_edit_panel = None

while bnr_edit_panel == None:
    bnr_edit_panel = pyautogui.locateOnScreen(r'png\bnr_edit_panel.png', minSearchTime=10)

if bnr_edit_panel:
    pyautogui.click(r'png\equ_tally_out.png')
    pyautogui.rightClick()
    time.sleep(0.5)
    pyautogui.move(xOffset=10, yOffset=10)
    pyautogui.leftClick()

equ_edit_panel = None

while equ_edit_panel == None:
    equ_edit_panel = pyautogui.locateOnScreen(r'png\equ_edit_panel.png', minSearchTime=10)

if equ_edit_panel:
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