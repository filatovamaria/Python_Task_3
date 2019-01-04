# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 22:13:41 2018

@author: Masha
"""
import classes as myClass

def X_n(pos, spd, a, tistep):
    val_n = [x + u*tistep + 0.5*a*tistep**2 
            for x, u, a in zip(pos, spd, a)]
    return val_n

def V_n(spd, a_n, a_n1, tistep):
    val_n = [u + 0.5*(an + an1)*tistep
            for u, an, an1 in zip(spd, a_n, a_n1)]
    return val_n
 


def Calculate(particle_list, timerStep):
    G = 6.67408 * (10 ** -9)
        
    x_n = []
    y_n = []
    z_n = []
    u_n = []
    v_n = []
    w_n = []
    m_n = []
    col_n = []        
        
    for partic in particle_list:
        for par in particle_list:
            if (partic.position.Module(par.position) > 0) & (partic.position.Module(par.position) < (partic.m + par.m) / 100.0):
                if partic.m > par.m:
                    partic.m += par.m
                else:
                    partic.alive = False

                        
        if (partic.alive):
            x_n.append(partic.x)
            y_n.append(partic.y)
            z_n.append(partic.z)
            u_n.append(partic.u)
            v_n.append(partic.v)
            w_n.append(partic.w)
            m_n.append(partic.m)
            col_n.append(partic.color)
                
    length = len(x_n)      
            
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

        
    

def CalculateSolar(particle_list, timerStep):
    G = 6.67408 * (10 ** -11)
        
    constRadius = 14959787070
    constMass = 5.9726 * 10**24
        
    x_n = [p.x * constRadius for p in particle_list]
    y_n = [p.y * constRadius for p in particle_list]
    z_n = [p.z * constRadius for p in particle_list]
    position = [myClass.Position(x, y, z) for x, y, z in zip(x_n, y_n, z_n)]
    u_n = [p.u for p in particle_list]
    v_n = [p.v for p in particle_list]
    w_n = [p.w for p in particle_list]
    m_n = [p.m * constMass for p in particle_list]
    col_n = [p.color for p in particle_list]        
                        
    length = len(x_n) 
                    
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

