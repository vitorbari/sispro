#!/usr/bin/env python

"""GyroCube.py: Draws a rotating 3d cube with the data read from the gyro sensor."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Leonel Machava", "Marcin Polaczyk", "Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

import time
import sys, pygame
from operator import itemgetter

from classes.Point3D import Point3D


class Simulation:
    def __init__(self, win_width=640, win_height=480):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("SISPRO")

        self.myfont = pygame.font.SysFont(None, 24)

        self.logo = pygame.image.load("images/raspi.bmp")
        self.logo_rect = self.logo.get_rect()

        self.clock = pygame.time.Clock()

        self.vertices = [
            Point3D(-1, 1, -1),
            Point3D(1, 1, -1),
            Point3D(1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, 1, 1),
            Point3D(1, 1, 1),
            Point3D(1, -1, 1),
            Point3D(-1, -1, 1)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (0, 4, 5, 1), (3, 2, 6, 7)]

        # Define colors for each face
        self.colors = [(171, 0, 51), (227, 0, 64), (77, 0, 25), (190, 0, 51), (99, 156, 30), (116, 183, 34)]

        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0

    def run(self, file):

        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0

        with open(file) as fp:
            for line in fp:

                time.sleep(0.2)

                line = line.split(';')

                self.angleX = float(line[0])
                self.angleY = float(line[1])
                self.angleZ = float(line[2])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                self.screen.fill((0, 0, 0))

                label = self.my_font.render("SISPRO  |  X: %0.2f Y: %0.2f z:Z%0.2f" % (self.angleX, self.angleY, self.angleZ), 1, (255, 255, 255))
                self.screen.blit(label, (10, 10))

                label = self.my_font.render("Caue Diego", 1, (255, 255, 255))
                self.screen.blit(label, (10, 30))

                label = self.my_font.render("Felipe Tassoni", 1, (255, 255, 255))
                self.screen.blit(label, (10, 50))

                label = self.my_font.render("Jose Rodrigo", 1, (255, 255, 255))
                self.screen.blit(label, (10, 70))

                label = self.my_font.render("Vitor Bari Buccianti", 1, (255, 255, 255))
                self.screen.blit(label, (10, 90))

                self.screen.blit(self.logo, (580, 10))

                # It will hold transformed vertices.
                t = []

                for v in self.vertices:
                    # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                    r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
                    # Transform the point from 3D to 2D
                    p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                    # Put the point in the list of transformed vertices
                    t.append(p)

                # Calculate the average Z values of each face.
                avg_z = []
                i = 0
                for f in self.faces:
                    z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                    avg_z.append([i, z])
                    i = i + 1

                # Draw the faces using the Painter's algorithm:
                # Distant faces are drawn before the closer ones.
                for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                    face_index = tmp[0]
                    f = self.faces[face_index]
                    pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                                 (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                                 (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                                 (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                    pygame.draw.polygon(self.screen, self.colors[face_index], pointlist)

                pygame.display.flip()

