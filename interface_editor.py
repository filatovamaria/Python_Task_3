from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint, Qt

import OpenGL.GLU as glu
import OpenGL.GL as gl

import sys, math
import random
import time

import interface
import classes as myClass
import calculations as calc

class InterfaceEditor(QtWidgets.QMainWindow, interface.Ui_MainWindow, QtWidgets.QOpenGLWidget):
   
    _particle_list = []
       
    def __init__(self):
        super().__init__()
        self.xRot = 0
        self.yRot = 0
        self.zoom = 200
        self.lastPos = QPoint()
        self._color = QtGui.QColor(255, 0, 0)
        self._m = 0
        self._dt = 1000
        self.started = True
        
        self.setupUi(self)
        self.initSliderMass()
        self.initTextEdits()
        self.timer = QtCore.QTimer() 
        self.timer.timeout.connect(self.draw)         
        
        self.horizontalSlider.valueChanged[int].connect(self.slider_mass)
        self.pushButton_2.clicked.connect(self.button_add)
        self.pushButton_color.clicked.connect(self.button_selectColor)
        self.initComboBox()
        self.initComboBox2()
        self.comboBox.currentIndexChanged.connect(self.combobox_methodChoice)
         
        self.checkBox.stateChanged.connect(self.checkbox_solarSystemExample) 
        self.checkbox_solarSystemExample()
        self.comboBox_2.currentIndexChanged.connect(self.combobox_numberChoice)

    def initTextEdits(self):
        self.textEdit.setText('50')
        self.textEdit_2.setText('-80')
        self.textEdit_3.setText('90')
        self.textEdit_4.setText('0.001')
        self.textEdit_5.setText('0.001')
        self.textEdit_6.setText('-0.001')

    
    def initSliderMass(self):
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(200)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(1)
        self.slider_mass()
        
        
    def initComboBox(self):
        self.comboBox.addItem("Пользовательское")
        self.comboBox.addItem("100")
        self.comboBox.addItem("200")
        self.comboBox.addItem("400")
        self.comboBox.addItem("1000")
        self.comboBox.setCurrentIndex(1)        
        
        
    def initComboBox2(self):
        self.comboBox_2.addItem("odeint")
        self.comboBox_2.addItem("Верле")
        self.comboBox_2.addItem("Параллельный Верле")
        self.comboBox_2.addItem("Cython Верле")
        #self.comboBox_2.addItem("CUDA Верле")
        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.setEnabled(True)
        
    def slider_mass(self):
        self._m = self.horizontalSlider.value() * 5.0
        self.label_13.setText(str(self._m / 10))
        
    
    def button_selectColor(self):
        qcolor = QtWidgets.QColorDialog.getColor()
        p = self.widget.palette()
        self._color = QColor(qcolor)
        p.setColor(QtGui.QPalette.Background, QColor(qcolor))
        self.widget.setPalette(p)
        self.widget.show()
        
        
    def button_add(self):
        global _particle_list
        
        x = float(self.textEdit.toPlainText())
        y = float(self.textEdit_2.toPlainText())
        z = float(self.textEdit_3.toPlainText())
        emitter = myClass.Position(x, y, z)
        
        u = float(self.textEdit_4.toPlainText()) / 1000.0
        v = float(self.textEdit_5.toPlainText()) / 1000.0
        w = float(self.textEdit_6.toPlainText()) / 1000.0
        velocity = myClass.Velocity(u, v, w)

        _particle_list.append(myClass.Particle(emitter, velocity, self._m, self._color.getRgbF()))     
        if (self.timer.isActive()):
            self.openGLWidget.update()
        
        
    def combobox_methodChoice(self):
        self.timer.stop()
        self.started = True
        self.calculate()
        self.timer.start(self._dt)
        
    
    def combobox_numberChoice(self):

        self.timer.stop()
        global _particle_list        
        self.zoom = 1000
        
        self.groupBox_4.setEnabled(False)
        rang = 0
        if self.comboBox.currentIndex() == 4:
            rang = 1000
        elif self.comboBox.currentIndex() == 1:
            rang = 100
        elif self.comboBox.currentIndex() == 2:
            rang = 200
        elif self.comboBox.currentIndex() == 3:
            rang = 400
        else:
            rang = 3 
            self.groupBox_4.setEnabled(True)

        _particle_list = []
        _particle_list.append(myClass.Particle(myClass.Position(0, 0, 0), myClass.Velocity(0, 0, 0), 3000, [255, 0, 0]))
                
        for i in range(1, rang):
            _particle_list.append(
                    myClass.Particle(myClass.Position(random.randint(-500, 500), random.randint(-500, 500), random.randint(-500, 500)), myClass.Velocity(random.randint(-5, 5) / 10000.0, random.randint(-5, 5) / 10000.0, random.randint(-5, 5) / 10000.0), random.uniform(100, 1000), [random.uniform(0.3, 0.9), random.uniform(0.3, 0.9), random.uniform(0.3, 0.9)]))
        self.started = True
        self.timer.start(self._dt)
        if (self.timer.isActive()):
            self.openGLWidget.update()
        
            
            
    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()            
            self.setXRotation(self.xRot + dy / 100)
            self.setYRotation(self.yRot - dx / 100)

            self.lastPos = event.pos()
            self.openGLWidget.update()
            
            
    def setXRotation(self, angle):
        if angle != self.xRot:
            self.xRot = angle

    def setYRotation(self, angle):
        if angle != self.yRot:
            self.yRot = angle
            
            
    def wheelEvent(self, event):  
        if (self.zoom >= 20) & (self.zoom <= 2000):
            self.zoom += event.angleDelta().y() / 10
            self.openGLWidget.update()
        elif self.zoom < 20:
            self.zoom = 20
        else:
            self.zoom = 2000
            
              
            
    def checkbox_solarSystemExample(self):        
        if self.checkBox.isChecked():
            self.groupBox_4.setEnabled(False)
            self.comboBox.setEnabled(False)
            global _particle_list
            _particle_list = []
            #Sun
            _particle_list.append(myClass.Particle(myClass.Position(0, 0, 0), myClass.Velocity(0, 0, 0), 332900, [1, 0.8, 0]))
            #Mercury
            _particle_list.append(myClass.Particle(myClass.Position(3.87, 0, 0), myClass.Velocity(0, 47360, 0), 0.055, [0.7, 0.6, 0.6]))
            #Venus
            _particle_list.append(myClass.Particle(myClass.Position(7.233, 0, 0), myClass.Velocity(0, 35020, 0), 0.815, [0.9, 0.8, 0.7]))
            #Earth
            _particle_list.append(myClass.Particle(myClass.Position(10, 0, 0), myClass.Velocity(0, 29783, 0), 1, [0.4, 0.6, 0.8]))
            #Mars
            _particle_list.append(myClass.Particle(myClass.Position(15.24, 0, 0), myClass.Velocity(0, 24100, 0), 0.107, [1, 0.5, 0]))
            #Jupiter
            _particle_list.append(myClass.Particle(myClass.Position(52, 0, 0), myClass.Velocity(0, 13070, 0), 318, [1, 0.8, 0.6]))
            #Saturn
            _particle_list.append(myClass.Particle(myClass.Position(100, 0, 0), myClass.Velocity(0, 9690, 0), 95, [0.8, 0.7, 0.1]))
            #Uran
            _particle_list.append(myClass.Particle(myClass.Position(192.3, 0, 0), myClass.Velocity(0, 6810, 0), 14.6, [0.6, 0.65, 1]))
            #Neptune
            _particle_list.append(myClass.Particle(myClass.Position(301, 0, 0), myClass.Velocity(0, 5430, 0), 17.1, [0.1, 0.3, 1]))
            #No Pluto :G
            self.timer.start(self._dt)
            self.zoom = 280
            self._dt = 10000
        else:
            self._dt = 5000
            self.comboBox.setEnabled(True)
            self.combobox_numberChoice()
            
            
        
    def calculate(self):        
        global _particle_list
        start_time = time.time()
        
        if (self.comboBox_2.currentIndex() == 0):
            if self.checkBox.isChecked():
                _particle_list = calc.Calculations.CalculateOdeintSolar(_particle_list, self._dt, self.timer)
            else:
                _particle_list = calc.Calculations.CalculateOdeint(_particle_list, self._dt, self.timer)
        
        elif (self.comboBox_2.currentIndex() == 1):
            if self.checkBox.isChecked():
                _particle_list = calc.Calculations.CalculateVerletSolar(_particle_list, self._dt, self.timer)
            else:
                _particle_list = calc.Calculations.CalculateVerlet(_particle_list, self._dt, self.timer)
        
        elif (self.comboBox_2.currentIndex() == 2):
            if self.checkBox.isChecked():
                _particle_list = calc.Calculations.CalculateParallSolar(_particle_list, self._dt, self.timer)
            else:
                _particle_list = calc.Calculations.CalculateParall(_particle_list, self._dt, self.timer)
        
        else:
            if self.checkBox.isChecked():
                _particle_list = calc.Calculations.CalculateCythonSolar(_particle_list, self._dt, self.timer)
            else:
                _particle_list = calc.Calculations.CalculateCython(_particle_list, self._dt, self.timer)
        
        if self.started:
            print("--- %s seconds ---" % (time.time() - start_time))
            self.started = False
        
        if (self.timer.isActive()):
            self.openGLWidget.update()
            
            
    def setupGL(self):
        print("setupGL")
        self.windowsHeight = self.openGLWidget.height()
        self.windowsWidth = self.openGLWidget.width()

        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.windowsWidth, self.windowsHeight)
        self.openGLWidget.initializeGL = self.initializeGL
        self.openGLWidget.paintGL = self.paintGL        


    def paintGL(self):
        self.loadScene() 
        
        # camera rotation
        rad = self.zoom
        x_cam = rad * math.sin(self.yRot) * math.cos(self.xRot)
        y_cam = rad * math.sin(self.yRot) * math.sin(self.xRot)
        z_cam = rad * math.cos(self.yRot) 
        glu.gluLookAt(x_cam, y_cam, z_cam, 0, 0, 0, 0, 1, 0)
        
        
        if self.timer.isActive():
            self.draw()
            self.calculate()

        
    def draw(self):
        global _particle_list

        #Solar system drawing
        if self.checkBox.isChecked():
            #Sun
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[0].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[0].color)
            gl.glTranslatef(_particle_list[0].x, _particle_list[0].y, _particle_list[0].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[0].m / 120000.0, 16, 16) 
            gl.glTranslatef(-_particle_list[0].x, -_particle_list[0].y, -_particle_list[0].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Mercury
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[1].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[1].color)
            gl.glTranslatef(_particle_list[1].x, _particle_list[1].y, _particle_list[1].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[1].m * 10, 16, 16) 
            gl.glTranslatef(-_particle_list[1].x, -_particle_list[1].y, -_particle_list[1].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Venus
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[2].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[2].color)
            gl.glTranslatef(_particle_list[2].x, _particle_list[2].y, _particle_list[2].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[2].m, 16, 16) 
            gl.glTranslatef(-_particle_list[2].x, -_particle_list[2].y, -_particle_list[2].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Earth
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[3].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[3].color)
            gl.glTranslatef(_particle_list[3].x, _particle_list[3].y, _particle_list[3].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[3].m, 16, 16) 
            gl.glTranslatef(-_particle_list[3].x, -_particle_list[3].y, -_particle_list[3].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Mars
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[4].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[4].color)
            gl.glTranslatef(_particle_list[4].x, _particle_list[4].y, _particle_list[4].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[4].m * 7, 16, 16) 
            gl.glTranslatef(-_particle_list[4].x, -_particle_list[4].y, -_particle_list[4].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
                
            #Jupiter
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[5].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[5].color)
            gl.glTranslatef(_particle_list[5].x, _particle_list[5].y, _particle_list[5].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[5].m / 30.0, 16, 16) 
            gl.glTranslatef(-_particle_list[5].x, -_particle_list[5].y, -_particle_list[5].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Saturn
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[6].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[6].color)
            gl.glTranslatef(_particle_list[6].x, _particle_list[6].y, _particle_list[6].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[6].m / 12.0, 16, 16) 
            gl.glTranslatef(-_particle_list[6].x, -_particle_list[6].y, -_particle_list[6].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Uran
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[7].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[7].color)
            gl.glTranslatef(_particle_list[7].x, _particle_list[7].y, _particle_list[7].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[7].m / 2.3, 16, 16) 
            gl.glTranslatef(-_particle_list[7].x, -_particle_list[7].y, -_particle_list[7].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
            
            #Neptune
            gl.glPushMatrix()
            sphere = glu.gluNewQuadric()  
            gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[8].color)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[8].color)
            gl.glTranslatef(_particle_list[8].x, _particle_list[8].y, _particle_list[8].z)
            glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
            glu.gluSphere(sphere, _particle_list[8].m / 3.2, 16, 16) 
            gl.glTranslatef(-_particle_list[8].x, -_particle_list[8].y, -_particle_list[8].z)
            gl.glPopMatrix()
            glu.gluDeleteQuadric(sphere)
          
        #other
        else:
            _particle_list = [p for p in _particle_list if p.alive == True]
            for i in range(len(_particle_list)):
                if ((_particle_list[i].x > -2000)&(_particle_list[i].x < 2000)
                   &(_particle_list[i].y > -2000)&(_particle_list[i].y < 2000)
                   &(_particle_list[i].z > -2000)&(_particle_list[i].z < 2000)):
                    gl.glPushMatrix()
                    sphere = glu.gluNewQuadric()  
                    gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, _particle_list[i].color)
                    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, _particle_list[i].color)
                    gl.glTranslatef(_particle_list[i].x, _particle_list[i].y, _particle_list[i].z)
                    glu.gluQuadricDrawStyle(sphere, glu.GLU_FILL)        
                    glu.gluSphere(sphere, _particle_list[i].m / 100.0, 16, 16) 
                    gl.glTranslatef(-_particle_list[i].x, -_particle_list[i].y, -_particle_list[i].z)
                    gl.glPopMatrix()
                    glu.gluDeleteQuadric(sphere)   
                else:
                    _particle_list[i].alive = False
                    
        label = str(len(_particle_list))
        self.label_12.setText(label)
        
        

    def initializeGL(self):
        print("initializeGL")
        gl.glEnable(gl.GL_CULL_FACE)
        #gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)        
        gl.glEnable(gl.GL_NORMALIZE) 

        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [100,100,100,1])
        gl.glLightf(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.1)
        gl.glLightf(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPOT_DIRECTION, [0,1,1]);
        gl.glLighti(gl.GL_LIGHT0, gl.GL_SPOT_EXPONENT, 1); 
        gl.glLighti(gl.GL_LIGHT0, gl.GL_SPOT_CUTOFF, 45);
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        

    def loadScene(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        x, y, width, height = gl.glGetDoublev(gl.GL_VIEWPORT)
        glu.gluPerspective(
            90,  # field of view in degrees
            width / float(height or 1),  # aspect ratio
            .25,  # near clipping plane
            2000,  # far clipping plane
        )       


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceEditor()
    window.setupGL()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()