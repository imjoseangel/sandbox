#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import datetime
import glob
import json
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')


class LoginScreen(Screen):

    def signup(self):
        self.manager.current = 'signup_screen'

    def login(self, uname, pword):
        with open('users.json', encoding='UTF-8') as file:
            users = json.load(file)

        if uname in users and pword == users[uname]['password']:
            self.manager.current = 'login_screen_success'
            self.ids.error_label.text = ''
        else:
            self.ids.error_label.text = 'Invalid username or password'


class LoginScreenSuccess(Screen):

    def logout(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def enlighten(self, feel):
        feel = feel.lower()

        feelingsdata = glob.glob('quotes/*.txt')
        feelings = [Path(filename).stem for filename in feelingsdata]

        if feel in feelings:
            with open(f'quotes/{feel}.txt', encoding='UTF-8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = 'I don\'t know this feeling'


class SignUpScreen(Screen):

    def add_user(self, uname, pword):
        with open('users.json', encoding='UTF-8') as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        with open('users.json', 'w', encoding='UTF-8') as file:
            json.dump(users, file)

        self.manager.current = 'sign_up_screen_success'


class SignUpScreenSuccess(Screen):

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'


class RootWidget(ScreenManager):
    pass


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
