# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 11:25:32 2018

@author: Masha
"""
import classes as myClass

def X_n(pos, spd, a, length, tistep):
    val_n = []
    for i in range(length):    
        val_n.append(pos[i] + spd[i]*tistep + 0.5*a[i]*tistep**2 )

    return val_n


def V_n(spd, a_n, a_n1, length, tistep):
    val_n = []
    for i in range(length):  
        val_n.append(spd[i] + 0.5*(a_n[i] + a_n1[i])*tistep)
            
    return val_n
 


def Calculate(x_n, y_n, z_n, u_n, v_n, w_n, m_n, timerStep):
    
    G = 6.67408 * (10 ** -9)       
    
            
    ax_n = []
    ay_n = []
    az_n = []
    for px, py, pz in zip(x_n, y_n, z_n):            
        part = myClass.Position(px, py, pz)
        ax = []
        ay = []
        az = []
        for _px, _py, _pz, m in zip(x_n, y_n, z_n, m_n): 
            module = part.Module(myClass.Position(_px, _py, _pz))**3
            if module > 0:
                ax.append(G*m * (_px - px) / module)
                ay.append(G*m * (_py - py) / module)
                az.append(G*m * (_pz - pz) / module)

        ax_n.append(sum(ax))
        ay_n.append(sum(ay))
        az_n.append(sum(az))
        
    leng = len(x_n)
    
    x_n1 = X_n(x_n, u_n, ax_n, leng, timerStep)
    y_n1 = X_n(y_n, v_n, ay_n, leng, timerStep)
    z_n1 = X_n(z_n, w_n, az_n, leng, timerStep)
        
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
               
        
    u_n1 = V_n(u_n, ax_n, ax_n1, leng, timerStep)
    v_n1 = V_n(v_n, ay_n, ay_n1, leng, timerStep)
    w_n1 = V_n(w_n, az_n, az_n1, leng, timerStep)
        
   
    return [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] 
        
    

def CalculateSolar(x_n, y_n, z_n, u_n, v_n, w_n, m_n, timerStep):
    
    G = 6.67408 * (10 ** -11)        
 
                    
    ax_n = []
    ay_n = []
    az_n = []
    for px, py, pz in zip(x_n, y_n, z_n):            
        part = myClass.Position(px, py, pz)
        ax = []
        ay = []
        az = []
        for _px, _py, _pz, m in zip(x_n, y_n, z_n, m_n): 
            module = part.Module(myClass.Position(_px, _py, _pz))**3
            if module > 0:
                ax.append(G*m * (_px - px) / module)
                ay.append(G*m * (_py - py) / module)
                az.append(G*m * (_pz - pz) / module)

        ax_n.append(sum(ax))
        ay_n.append(sum(ay))
        az_n.append(sum(az))
            
    leng = len(x_n)
     
    x_n1 = X_n(x_n, u_n, ax_n, leng, timerStep)
    y_n1 = X_n(y_n, v_n, ay_n, leng, timerStep)
    z_n1 = X_n(z_n, w_n, az_n, leng, timerStep)
        
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
            
    u_n1 = V_n(u_n, ax_n, ax_n1, leng, timerStep)
    v_n1 = V_n(v_n, ay_n, ay_n1, leng, timerStep)
    w_n1 = V_n(w_n, az_n, az_n1, leng, timerStep)
                    
    return [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] 