#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA for PIMLIG/LIG/CNRS- 10/12/2018

#################################
## GLOBAL LIBS
import sys
import math
import platform as pl
import numpy    as np

try:
    from OpenGL.GL      import *
    from OpenGL.GLU     import *
    from OpenGL.GLUT    import *
    from OpenGL.GL      import shaders
except:
    print ('''ERROR: PyOpenGL not installed properly.''')

#################################
## LOCAL LIBS
if __name__ == '__main__':
    from libs import shader             as sh
    from libs import projector          as pr
else:
    from .libs import shader             as sh
    from .libs import projector          as pr

def wire_cube(pos, edge):
    p = np.array(pos)
    e = edge/2.
    return [    [pos + np.array([-e, -e, e])],
                [pos + np.array([e, -e, e])],
                [pos + np.array([e, -e, e])],
                [pos + np.array([e, e, e])],
                [pos + np.array([e, e, e])],
                [pos + np.array([-e, e, e])],
                [pos + np.array([-e, e, e])],
                [pos + np.array([-e, -e, e])],

                [pos + np.array([-e, -e, -e])],
                [pos + np.array([e, -e, -e])],
                [pos + np.array([e, -e, -e])],
                [pos + np.array([e, e, -e])],
                [pos + np.array([e, e, -e])],
                [pos + np.array([-e, e, -e])],
                [pos + np.array([-e, e, -e])],
                [pos + np.array([-e, -e, -e])],

                [pos + np.array([-e, -e, -e])],
                [pos + np.array([-e, -e, e])],
                [pos + np.array([e, -e, -e])],
                [pos + np.array([e, -e, e])],
                [pos + np.array([e, e, -e])],
                [pos + np.array([e, e, e])],
                [pos + np.array([-e, e, -e])],
                [pos + np.array([-e, e, e])]    ]


class hellocube:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.cube_shader = sh.shader()
        self.projo = pr.projector(position = [0, 0, 2])

    def init_GL(self):
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


    def init_shader(self):

        ##########################
        # general vertex array object
        print('\n\tGenerating vao...', end='')
        sys.stdout.flush()
        try:
            vao = glGenVertexArrays(1)
            glBindVertexArray(vao)
            print('\tOk')
            sys.stdout.flush()
        except ValueError:
            print()
            print()
            print(ValueError)
            print()
            sys.exit()

        ##########################
        # simple cube
        self.cube_vbo           = glGenBuffers(1)
        self.cube_vertices      = np.array(wire_cube([0,0,0], 1))
        self.cube_shader.attr_vertices = sh.new_attribute_index()

        ## CALLBACKS -------
        #update arrays callback
        def _update_arrays():
            sh.bind(self.cube_vbo, self.cube_vertices, self.cube_shader.attr_vertices, 3, GL_FLOAT)
        self.cube_shader.update_arrays = _update_arrays

        # display callback
        def cube_display():
            self.cube_shader.update_projections(self.projo.projection(), self.projo.modelview())
            glDrawArrays(GL_LINES, 0, len(self.cube_vertices))
        self.cube_shader.display = cube_display
        ## CALLBACKS -------

        #first array update
        self.cube_shader.update_arrays()

        #Loading shader files
        print('\tCube shader...', end='')
        self.cube_shader.sh = sh.create('./shaders/cube.vert',None,'./shaders/cube.frag', [self.cube_shader.attr_vertices], ['in_vertex'])
        if not self.cube_shader.sh:
            exit(1)
        print('\t\tOk')
        sys.stdout.flush()


    def start(self):

        #Glut Init
        try:
            glutInit()
        except Exception as e:
            print(e)
            sys.exit()

        if pl.system() == 'Darwin': #Darwin: OSX
            glutInitDisplayString('double rgba samples=8 core depth')
        else:   #Other: Linux
            try:
                glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_MULTISAMPLE | GLUT_DEPTH)
            except Exception as e:
                print('Issue detected')
                print(e)
                sys.exit()

        glutInitWindowSize (800, 600)
        glutCreateWindow ('Basic OGL')
        self.init_GL()
        self.init_shader()
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutMouseFunc(self.mouse_clicks)
        glutMotionFunc(self.mouse_motion)
        glutReshapeFunc(self.reshape)
        glutMainLoop()


    def display(self):
        glClearColor(.31,.63,1.0,1.0)
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        sh.display_list([self.cube_shader])
        glutSwapBuffers()


    def mouse_clicks(self, button, state, x, y):
        self.mouse = [x, y]

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.imode = 'rotation'
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.imode = 'none'


    def mouse_motion(self, x, y):
        dx, dy = x - self.mouse[0], y - self.mouse[1]
        self.mouse = [x, y]
        if self.imode == 'rotation':
            self.projo.rotate_h(-dx/glutGet(GLUT_WINDOW_WIDTH)*math.pi)
            self.projo.rotate_v(-dy/glutGet(GLUT_WINDOW_HEIGHT)*math.pi)
        glutPostRedisplay()


    def keyboard(self, key, x, y):
        if key == b'\x1b':
            sys.exit()

        elif key == b't':
            self.resize(400, 200)


    def resize(self, w, h):
        glutReshapeWindow(w, h)


    def reshape(self, w, h):
        glViewport(0,  0,  w,  h);
        self.projo.ratio = w/float(h)
        glutPostRedisplay()



if __name__ == '__main__':
    bogl = hellocube(800, 600)
    bogl.start()
