# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 11:25:32 2018

@author: Masha
"""
import classes as myClass
import numpy as np

def X_n(double[:] pos, double[:] spd, double[:] a, int length, int tistep):
    cdef double[:] val_n = np.zeros(length)
    cdef int i = 0
    for i in range(length):    
        val_n[i] = pos[i] + spd[i]*tistep + 0.5*a[i]*tistep**2 

    return val_n


def V_n(double[:] spd, double[:] a_n, double[:] a_n1, int length, int tistep):
    cdef double[:] val_n = np.zeros(length)
    cdef int i = 0
    for i in range(length):  
        val_n[i] = spd[i] + 0.5*(a_n[i] + a_n1[i])*tistep
            
    return val_n
 


cpdef Calculate():
    
    cdef int G = 6.67408 * (10 ** -9)
        
    
            
    ax_n = []
    ay_n = []
    az_n = []
    for px, py, pz in zip(x_n, y_n, z_n):            
        part = myClass.Position(px, py, pz)
        ax = []
        ay = []
        az = []
        for p in particle_list:
            module = part.Module(p.position)**3
            if module > 0:
                ax.append(G*p.m * (p.x - px) / module)
                ay.append(G*p.m * (p.y - py) / module)
                az.append(G*p.m * (p.z - pz) / module)

        ax_n.append(sum(ax))
        ay_n.append(sum(ay))
        az_n.append(sum(az))
    
    x_n1 = X_n(x_n, u_n, ax_n, timerStep)
    y_n1 = X_n(y_n, v_n, ay_n, timerStep)
    z_n1 = X_n(z_n, w_n, az_n, timerStep)
        
    ax_n1 = []
    ay_n1 = []
    az_n1 = []
    for px, py, pz in zip(x_n1, y_n1, z_n1):
        part = myClass.Position(px, py, pz)
        ax = []
        ay = []
        az = []
        for x, y, z, m in zip(x_n1, y_n1, z_n1, m_n):
            p = myClass.Position(x, y, z) 
            module = part.Module(p)**3
            if module > 0:
                ax.append(G*m * (x - px) / module)
                ay.append(G*m * (y - py) / module)
                az.append(G*m * (z - pz) / module)
                
        ax_n1.append(sum(ax))
        ay_n1.append(sum(ay))
        az_n1.append(sum(az))
            
    u_n1 = V_n(u_n, ax_n, ax_n1, timerStep)
    v_n1 = V_n(v_n, ay_n, ay_n1, timerStep)
    w_n1 = V_n(w_n, az_n, az_n1, timerStep)
        
    _particle_list = []
    for i in range(length):
        position = myClass.Position(x_n1[i], y_n1[i], z_n1[i])
        velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
        _particle_list.append(myClass.Particle(position, velocity, m_n[i], col_n[i]))
    return _particle_list   
        
    

cdef CalculateSolar(particle_list, timerStep, timer):
    G = 6.67408 * (10 ** -11)        
 
                    
    ax_n = []
    ay_n = []
    az_n = []
    for px, py, pz in zip(x_n, y_n, z_n):
        part = myClass.Position(px, py, pz)
        
        ax = [G*m * (p.x - px) / part.Module(p)**3 
               for p,m in zip(position, m_n)
               if part.Module(p) > 0]
        ax_n.append(sum(ax))
        
        ay = [G*m * (p.y - py) / part.Module(p)**3 
               for p,m in zip(position, m_n)
               if part.Module(p) > 0]
        ay_n.append(sum(ay))
        
        az = [G*m * (p.z - pz) / part.Module(p)**3 
               for p,m in zip(position, m_n) 
               if part.Module(p) > 0]
        az_n.append(sum(az))
            
    x_n1 = X_n(x_n, u_n, ax_n, timerStep)
    y_n1 = X_n(y_n, v_n, ay_n, timerStep)
    z_n1 = X_n(z_n, w_n, az_n, timerStep)
        
    ax_n1 = []
    ay_n1 = []
    az_n1 = []
    for px, py, pz in zip(x_n1, y_n1, z_n1):
        part = myClass.Position(px, py, pz)
        ax = []
        ay = []
        az = []
        for x, y, z, m in zip(x_n1, y_n1, z_n1, m_n):
            p = myClass.Position(x, y, z) 
            module = part.Module(p)**3
            if module > 0:
                ax.append(G*m * (x - px) / module)
                ay.append(G*m * (y - py) / module)
                az.append(G*m * (z - pz) / module)
                
        ax_n1.append(sum(ax))
        ay_n1.append(sum(ay))
        az_n1.append(sum(az))
            
    u_n1 = V_n(u_n, ax_n, ax_n1, timerStep)
    v_n1 = V_n(v_n, ay_n, ay_n1, timerStep)
    w_n1 = V_n(w_n, az_n, az_n1, timerStep)
        
    _particle_list = []
    for i in range(length):
        position = myClass.Position(x_n1[i] / constRadius, y_n1[i] / constRadius, z_n1[i] / constRadius)
        velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
        _particle_list.append(myClass.Particle(position, velocity, m_n[i] / constMass, col_n[i]))
                    
    return _particle_list  