#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import datetime
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_file('design.kv')


class LoginScreen(Screen):
    def signup(self):
        self.manager.current = 'signup_screen'


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        with open('users.json', 'w') as file:
            json.dump(users, file)

        self.manager.current = 'sign_up_screen_success'


class SignUpScreenSuccess(Screen):
    def go_back(self):
        self.manager.current = 'login_screen'


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
