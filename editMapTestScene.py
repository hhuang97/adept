import os
import os.path
import sys

import numpy
import numpy.random

import pygame

from buffalo import utils
from buffalo.scene import Scene
from buffalo.label import Label
from buffalo.button import Button
from buffalo.input import Input
from buffalo.tray import Tray

from camera import Camera
from pluginManager import PluginManager

class CameraController:
    def __init__(self):
        self.fPos = (0.0, 0.0)
        self.pos = (int(self.fPos[0]), int(self.fPos[1]))
        self.xv, self.yv = 0.0, 0.0
        self.speed = 1.2
        self.shift_speed = self.speed * 5.0

    def update(self, keys):
        w, a, s, d, shift = (
            keys[pygame.K_w],
            keys[pygame.K_a],
            keys[pygame.K_s],
            keys[pygame.K_d],
            keys[pygame.K_LSHIFT],
        )

        if shift:
            speed = self.shift_speed
        else:
            speed = self.speed

        self.xv = 0.0
        self.yv = 0.0

        if w:
            self.yv -= speed
        if a:
            self.xv -= speed
        if s:
            self.yv += speed
        if d:
            self.xv += speed

        x, y = self.fPos
        x += self.xv
        y += self.yv
        self.fPos = x, y
        self.pos = (int(self.fPos[0]), int(self.fPos[1]))

class EditMapTestScene(Scene):
    def on_escape(self):
        sys.exit()

    def blit(self):
        Camera.blitView()

    def update(self):
        super(EditMapTestScene, self).update()
        keys = pygame.key.get_pressed()
        self.camera_controller.update(keys)
        Camera.update()

    def __init__(self):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 0, 255)
        PluginManager.loadPlugins()
        Camera.init()
        self.camera_controller = CameraController()
        Camera.lock(self.camera_controller)
        self.tool_tray = Tray(
            (utils.SCREEN_W - 270, 20),
            (250, 800),
            min_width=250, max_width=250,
            min_height=250, max_height=800,
        )
        self.tool_tray.labels.add(
            Label(
                (int(self.tool_tray.width / 2), 10),
                "Tool Tray",
                color=(255,255,255,255),
                x_centered=True,
                font="default18",
            )
        )
        self.tool_tray.buttons.add(
            Button(
                (int(self.tool_tray.width / 2), 50),
                "Yolo Doot Doot",
                color=(255,255,255,255),
                bg_color=(100,100,200,255),
                x_centered=True,
                font="default18",
            )
        )
        self.tool_tray.render()
        self.trays.add(self.tool_tray)
