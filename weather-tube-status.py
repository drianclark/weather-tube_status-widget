#!/usr/bin/python3
# stolen from user viyoriya from discuss.getsol.us

import requests
import subprocess
from time import sleep

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   
def get_weather():
    weather_res = requests.get('https://wttr.in?format="%l:+%C+%f"')
    if weather_res.status_code != 200:
        print('Error fetching weather')
        
    weather = weather_res.text[1:-1].replace('+', '')
    
    return weather

def get_lines_status():
    tfl_res = requests.get('https://api.tfl.gov.uk/Line/Mode/tube%2Cdlr%2Coverground/Status?detail=true')
    lines_status = tfl_res.json()

    if tfl_res.status_code != 200:
        print('Error fetching tube status')
        
    return lines_status

def construct_lines_status_block():
    lines_status = get_lines_status()
    
    lines_status_block_array = []
    max_line_length = max(len(line["name"]) for line in lines_status)
    max_line_status_length = 0
    
    for line_status in lines_status:
        status_string = f'{line_status["name"]:{max_line_length + 2}} ==>   {line_status["lineStatuses"][0]["statusSeverityDescription"]}'
        lines_status_block_array.append(status_string)
        max_line_status_length = max(max_line_status_length, len(status_string))
            
    justified_lines_status_block = [
        line.ljust(max_line_status_length, ' ') for line in lines_status_block_array]
    
    return justified_lines_status_block

def construct_widget():
    # terminal dimensions
    height, width = map(int, subprocess.check_output(['stty', 'size']).split())
    OUTPUT_HEIGHT = 16
        
    newlines_to_add = height - OUTPUT_HEIGHT
        
    weather = get_weather()
    lines_status_block = construct_lines_status_block()
        
    print('\n' * (newlines_to_add//2))
    print(color.BOLD + weather.center(width) + color.END)
    print()
    for line_status in lines_status_block:
        print(line_status.center(width))
    print('\n' * (newlines_to_add//2))

    

def main():
    output = None

    while True:
        # if there were any changes to the widget, rewrite
        if construct_widget() != output:
            # clear terminal
            subprocess.run(['clear'])
            output = construct_widget()
            print(output)
        
        sleep(60)
            
main()