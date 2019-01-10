# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 22:13:07 2018

@author: Masha
"""
import threading

from math import sqrt


class myThreadX(threading.Thread):
    
    def __init__(self, _id, pos, spd, a, tistep):
        threading.Thread.__init__(self)
        self.threadID = _id
        self.pos = pos
        self.spd = spd
        self.a = a
        self.tistep = tistep
        self.value = 0
        
    def run(self):
        self.value = X_n(self.pos, self.spd, self.a, self.tistep)
        
    def Value(self):
        return self.value

class myThreadV(threading.Thread):
    
    def __init__(self, _id, spd, a1, a2, tistep):
        threading.Thread.__init__(self)
        self.threadID = _id
        self.spd = spd
        self.a1 = a1
        self.a2 = a2
        self.tistep = tistep
        self.value = 0
        
    def run(self):
        self.value = V_n(self.spd, self.a1, self.a2, self.tistep)
        
    def Value(self):
        return self.value
 
 
def X_n(pos, spd, a, tistep):
    val_n = [x + u*tistep + 0.5*a*tistep**2 
            for x, u, a in zip(pos, spd, a)]
    return val_n

def V_n(spd, a_n, a_n1, tistep):
    val_n = [u + 0.5*(an + an1)*tistep
            for u, an, an1 in zip(spd, a_n, a_n1)]
    return val_n
 

def Module(x1, y1, z1, x2, y2, z2):
	return sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)



def Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timerStep):
  
    ax_n = []
    ay_n = []
    az_n = []
    for px, py, pz in zip(x_n, y_n, z_n):            
        ax = []
        ay = []
        az = []
        for _px, _py, _pz, m in zip(x_n, y_n, z_n, m_n): 
            module = Module(px, py, pz, _px, _py, _pz)**3
            if module > 0:
                ax.append(G*m * (_px - px) / module)
                ay.append(G*m * (_py - py) / module)
                az.append(G*m * (_pz - pz) / module)

        ax_n.append(sum(ax))
        ay_n.append(sum(ay))
        az_n.append(sum(az))

      
    thread1 = myThreadX(1, x_n, u_n, ax_n, timerStep)
    thread2 = myThreadX(2, y_n, v_n, ay_n, timerStep)
    thread3 = myThreadX(3, z_n, w_n, az_n, timerStep)
        
    thread1.start()
    thread2.start()
    thread3.start()
    
    x_n1 = thread1.Value()
    y_n1 = thread2.Value()
    z_n1 = thread3.Value()  
 
    thread1.join()
    thread2.join()
    thread3.join() 

    ax_n1 = []
    ay_n1 = []
    az_n1 = []
    for px, py, pz in zip(x_n1, y_n1, z_n1):

        ax = []
        ay = []
        az = []
        for _px, _py, _pz, m in zip(x_n1, y_n1, z_n1, m_n):

            module = Module(px, py, pz, _px, _py, _pz)**3
            if module > 0:
                ax.append(G*m * (_px - px) / module)
                ay.append(G*m * (_py - py) / module)
                az.append(G*m * (_pz - pz) / module)

        ax_n1.append(sum(ax))
        ay_n1.append(sum(ay))
        az_n1.append(sum(az))

    thread11 = myThreadV(4, u_n, ax_n, ax_n1, timerStep)
    thread21 = myThreadV(5, v_n, ay_n, ay_n1, timerStep)
    thread31 = myThreadV(6, w_n, az_n, az_n1, timerStep)
        
    thread11.start()
    thread21.start()
    thread31.start()
  
    u_n1 = thread11.Value()
    v_n1 = thread21.Value()
    w_n1 = thread31.Value()
    
    thread11.join()
    thread21.join()
    thread31.join()


    return [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1]         
    

    
