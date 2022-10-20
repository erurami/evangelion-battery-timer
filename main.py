# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:16:27 2021

@author: kozu_
"""

import pygame
import psutil
import os
import random
import ctypes
import win32gui
import win32con

def absolute_path_maker(relative_path):
    """　images\\????.png"""
    return os.path.join(os.getcwd(), relative_path)

pygame.init()

icon = pygame.image.load(absolute_path_maker("images\\icon.png"))

screen=pygame.display.set_mode((500,200), pygame.RESIZABLE)
pygame.display.set_caption("主電源供給システム")
pygame.display.set_icon(icon)
myclock=pygame.time.Clock()#時計を設定
myfont_small_small=pygame.font.Font(None,16)
myfont_small=pygame.font.Font(absolute_path_maker("clockfont.ttf"),40)
myfont=pygame.font.Font(absolute_path_maker("clockfont.ttf"),65)
myfont_big=pygame.font.Font(absolute_path_maker("clockfont.ttf"),100)
myfont_big_big=pygame.font.Font(absolute_path_maker("clockfont.ttf"),200)

wallpaper = pygame.image.load(absolute_path_maker("images\\wallpaper.png"))
battery_image = pygame.image.load(absolute_path_maker("images\\battery.png"))
plugged_image = pygame.image.load(absolute_path_maker("images\\plugged.png"))
stop_image = pygame.image.load(absolute_path_maker("images\\stop.png"))
slow_image = pygame.image.load(absolute_path_maker("images\\slow.png"))
normal_image = pygame.image.load(absolute_path_maker("images\\normal.png"))
racing_image = pygame.image.load(absolute_path_maker("images\\racing.png"))
unplugged_message = pygame.image.load(absolute_path_maker("images\\message_unplugged.png"))
plugged_message = pygame.image.load(absolute_path_maker("images\\message_plugged.png"))
warning_image = pygame.image.load(absolute_path_maker("images\\warning.png"))

set_top = True

if set_top == True: 
    hwnd = ctypes.windll.user32.FindWindowW(0, '主電源供給システム')
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


state = "normal"
score = 0

battery_sensor = psutil.sensors_battery()

symbol_bright = 255

class main_vars:
    def __init__(self):
        global state
        macine_details = psutil.sensors_battery()
        cpu_details = psutil.cpu_percent()
        self.plugged_in = macine_details.power_plugged
        self.state = "normal"
        self.remain_time = macine_details.secsleft * 10
        if self.plugged_in == True:
            state = "plugged"
        else:
            state = "unplugged"
        if cpu_details >= 90:
            self.state = "racing"
        elif cpu_details >= 30:
            self.state = "normal"
        elif cpu_details >=15:
            self.state = "slow"
        else:
            self.state = "stop"
        if self.plugged_in == False:
            self.remain_miliseconds = self.remain_time % 10
            self.remain_seconds = int(self.remain_time / 10) % 60
            self.remain_minutes = int(self.remain_time / 600) % 60
            self.remain_hours = int(self.remain_time / 36000)
            self.remain_miliseconds = str(self.remain_miliseconds)
            if len(str(self.remain_seconds)) == 1:
                self.remain_seconds = "0" + str(self.remain_seconds)
            else:
                self.remain_seconds = str(self.remain_seconds)
            if len(str(self.remain_minutes)) == 1:
                self.remain_minutes = "0" + str(self.remain_minutes)
            else:
                self.remain_minutes = str(self.remain_minutes)
            if len(str(self.remain_hours)) == 1:
                self.remain_hours = "0" + str(self.remain_hours)
            else:
                self.remain_hours = str(self.remain_hours)
        self.cpu_details_recent = []
    def update(self):
        cpu_details = psutil.cpu_percent()
        macine_details = psutil.sensors_battery()
        self.cpu_details_recent.append(cpu_details)
        if len(self.cpu_details_recent) >= 100:
            del self.cpu_details_recent[0]
        cpu_details = sum(self.cpu_details_recent) / len(self.cpu_details_recent)
        if cpu_details >= 90:
            self.state = "racing"
        elif cpu_details >= 10:
            self.state = "normal"
        elif cpu_details >=5:
            self.state = "slow"
        else:
            self.state = "stop"
        global state
        if self.plugged_in == False:
            if macine_details.power_plugged == True:
                self.plugged_in = True
                state = "plugged_effect"
            self.remain_time -= 1
            error_remain_time = macine_details.secsleft * 10 - self.remain_time
            if abs(error_remain_time) >= 600:
                global substate
                substate = "change_time"
                self.remain_time = macine_details.secsleft * 10
            self.remain_miliseconds = self.remain_time % 10
            self.remain_seconds = int(self.remain_time / 10) % 60
            self.remain_minutes = int(self.remain_time / 600) % 60
            self.remain_hours = int(self.remain_time / 36000)
            self.remain_miliseconds = str(self.remain_miliseconds)
            if len(str(self.remain_seconds)) == 1:
                self.remain_seconds = "0" + str(self.remain_seconds)
            else:
                self.remain_seconds = str(self.remain_seconds)
            if len(str(self.remain_minutes)) == 1:
                self.remain_minutes = "0" + str(self.remain_minutes)
            else:
                self.remain_minutes = str(self.remain_minutes)
            if len(str(self.remain_hours)) == 1:
                self.remain_hours = "0" + str(self.remain_hours)
            elif len(str(self.remain_hours)) >= 3:
                self.remain_hours = str(self.remain_hours)[-2:]
            else:
                self.remain_hours = str(self.remain_hours)
        if self.plugged_in == True:
            if macine_details.power_plugged == False:
                self.plugged_in = False
                state = "unplugg_effect"

def shuffle(list):
    already_selected = []
    retval = []
    for index in range(len(list)):
        serect = random.choice(list)
        while True:
            if serect in already_selected:
                serect = random.choice(list)
                pass
            else:
                retval.append(serect)
                already_selected.append(serect)
                break
    return retval


main_var = main_vars()
print(state)
substate = None
warning_positions = [(-40,-5),(-40,65),(-40,135),
                     (20,-40),(20,30),(20,100),(20,170),
                     (80,-5),(80,135),
                     (140,-40),(140,170),
                     (200,-5),(200,135),
                     (260,-40),(260,170),
                     (320,-5),(320,135),
                     (380,-40),(380,30),(380,100),(380,170),
                     (440,-5),(440,65),(440,135)]

while state != "end":
    if state == "plugged":
        symbol_bright = 0
        while state == "plugged":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = "end"
            main_var.update()
            screen.blit(wallpaper,(0,0))
            screen.blit(plugged_image,(0,0))
            symbol_bright -= 20
            if symbol_bright <= 0:
                symbol_bright = 255
            screen.blit(myfont.render("88",True,(symbol_bright/2,symbol_bright/1.5,symbol_bright)),(38,60))
            screen.blit(myfont.render("88",True,(symbol_bright/2,symbol_bright/1.5,symbol_bright)),(146,60))
            screen.blit(myfont.render("88",True,(symbol_bright/2,symbol_bright/1.5,symbol_bright)),(253,60))
            screen.blit(myfont_small.render("8",True,(symbol_bright/2,symbol_bright/1.5,symbol_bright)),(358,85))
            screen.blit(myfont.render(":",True,(symbol_bright/2,symbol_bright/1.5,symbol_bright)),(138,60))
            screen.blit(myfont.render(":",True,(symbol_bright/2,symbol_bright/1.5,symbol_bright)),(246,60))
            pygame.display.flip()
            myclock.tick(10)
    
    if state == "unplugged":
        print(state)
        symbol_bright = 255
        effect_change_time = False
        effect_time = 0
        while state == "unplugged":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = "end"
            main_var.update()
            
            screen.blit(wallpaper,(0,0))
            if main_var.state == "stop":
                screen.blit(stop_image,(0,0))
            if main_var.state == "slow":
                screen.blit(slow_image,(0,0))
            if main_var.state == "normal":
                screen.blit(normal_image,(0,0))
            if main_var.state == "racing":
                screen.blit(racing_image,(0,0))
            screen.blit(battery_image,(0,0))
            if substate == "change_time":
                effect_time = 0
                effect_change_time = True
                substate = None
            effect_time += 1
            if effect_change_time:
                if effect_time % 2 == 1:
                    symbol_bright = 0
                else:
                    symbol_bright = 255
                if effect_time >= 6:
                    effect_change_time = False
            screen.blit(myfont.render(main_var.remain_hours,True,(symbol_bright,symbol_bright / 5,symbol_bright / 5)),(38,60))
            screen.blit(myfont.render(main_var.remain_minutes,True,(symbol_bright ,symbol_bright / 5 ,symbol_bright / 5 )),(146,60))
            screen.blit(myfont.render(main_var.remain_seconds,True,(symbol_bright ,symbol_bright / 5 ,symbol_bright / 5 )),(253,60))
            screen.blit(myfont_small.render(main_var.remain_miliseconds,True,(symbol_bright ,symbol_bright / 5 ,symbol_bright / 5 )),(355,83))
            screen.blit(myfont.render(":",True,(symbol_bright,symbol_bright / 5 ,symbol_bright / 5 )),(138,60))
            screen.blit(myfont.render(":",True,(symbol_bright ,symbol_bright / 5 ,symbol_bright / 5 )),(246,60))
            pygame.display.flip()
            myclock.tick(10)
    
    if state == "unplugg_effect":
        effect_time = 0
        UNPLG_EFCTTIME = 15
        drawed_warning = set()
        shuffled_warning = shuffle(warning_positions)
        # state = "unplugged"
        effect_stage = "warning_hex"
        while state == "unplugg_effect":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = "end"
            screen.fill((0,0,0))
            screen.blit(unplugged_message,(0,0))
            for pos in drawed_warning:
                screen.blit(warning_image,pos)
            try:
                for i in range(2):
                    drawed_warning.add(shuffled_warning[effect_time*2 - i])
            except:
                effect_stage = "change_warning_photo"
                effect_stage_time = 0
            effect_time += 1
            if effect_time == UNPLG_EFCTTIME:
                state = "unplugged"
            pygame.display.flip()
            myclock.tick(10)
    
    if state == "plugged_effect":
        effect_time = 0
        PLG_EFCTTIME = 15
        drawed_warning = set()
        for warning_pos in warning_positions:
            drawed_warning.add(warning_pos)
        shuffled_warning = shuffle(warning_positions)
        # state = "unplugged"
        effect_stage = "warning_hex"
        while state == "plugged_effect":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = "end"
                    screen.fill((0,0,0))
            screen.blit(plugged_message,(0,0))
            for pos in drawed_warning:
                screen.blit(warning_image,pos)
            try:
                for i in range(3):
                    drawed_warning.remove(shuffled_warning[effect_time*3 - i])
            except: pass
            effect_time += 1
            if effect_time == PLG_EFCTTIME:
                state = "plugged"
            pygame.display.flip()
            myclock.tick(10)
    
pygame.quit()
