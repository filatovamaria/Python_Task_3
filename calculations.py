# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 22:54:31 2018

@author: Masha
"""
import classes as myClass

#import odint as odi
import verlet as ver
import multi as mul
#import opcl as ocl
#import cyth as cyt

import time


def Calculate(mytype, particle_list, timer_step):
    G = 6.67408 * (10 ** -9)
    times = []
    
    for i in range(5):
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
        _particle_list = []
        if length < 2:
            print('stop')
        else:
            x_n1 = []
            y_n1 = []
            z_n1 = []
            u_n1 = []
            v_n1 = []
            w_n1 = []
            
            start_time = time.time()
            
            if (mytype == 0):
                print('Odeint')
                [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = CalculateOdeint(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
            elif (mytype == 1):
                print('Verlet')
                [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = ver.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
            elif (mytype == 2):
                print('Threads')
                [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = mul.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
            elif (mytype == 3):
                print('OpenCL')
                #[x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = ocl.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
            else:
                print('Cython')
                #[x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = cyt.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
            
            times.append(time.time() - start_time)
            
            for i in range(length):
                position = myClass.Position(x_n1[i], y_n1[i], z_n1[i])
                velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
                _particle_list.append(myClass.Particle(position, velocity, m_n[i], col_n[i]))           
        
        
    return times

        
        
def CalculateSolar(mytype, particle_list, timer_step):
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
    _particle_list = []
    if length < 9:
        print('stop')
    else:  
        x_n1 = []
        y_n1 = []
        z_n1 = []
        u_n1 = []
        v_n1 = []
        w_n1 = []
        if (mytype == 0):
            print('Odeint')
            [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = CalculateOdeint(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
        elif (mytype == 1):
            print('Verlet')
            [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = ver.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
        elif (mytype == 2):
            print('Threads')
            [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = mul.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
        elif (mytype == 3):
            print('OpenCL')
            #[x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = ocl.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
        else:
            print('Cython')
            #[x_n1, y_n1, z_n1, u_n1, v_n1, w_n1] = cyt.Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timer_step)
            
            
        for i in range(length):
            position = myClass.Position(x_n1[i] / constRadius, y_n1[i] / constRadius, z_n1[i] / constRadius)
            velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
            _particle_list.append(myClass.Particle(position, velocity, m_n[i] / constMass, col_n[i]))
                        
    return _particle_list



from math import sqrt
from numpy import linspace
from scipy.integrate import odeint



def CalculateOdeint(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timerStep):
  
    length = len(x_n)
    times = linspace(0, timerStep, 2)
    
    def gravitySystem(_y, t):
        
        x = []
        y = []
        z = []
        u = []
        v = []
        w = []
        for i in range(length):
            u.append(_y[6*i])
            v.append(_y[6*i + 1])
            w.append(_y[6*i + 2])            
            
            x.append(_y[6*i + 3])
            y.append(_y[6*i + 4])
            z.append(_y[6*i + 5])
        
        gsys = []        

        for i in range(length): 
            #dr/dt = v
            gsys.append(u[i])
            gsys.append(v[i])
            gsys.append(w[i])
            
            #dv/dt = sum
            ax_sum = 0
            ay_sum = 0
            az_sum = 0
            for j in range(length):
                module = sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2 + (z[i] - z[j])**2)**3
                const = G * m_n[j]
                if module > 0:
                    ax_sum += const * (x[j] - x[i]) / module
                    ay_sum += const * (y[j] - y[i]) / module
                    az_sum += const * (z[j] - z[i]) / module
            gsys.append(ax_sum)
            gsys.append(ay_sum)
            gsys.append(az_sum)

        return gsys
    
    
    prev = []
    for i in range(length): 
        prev.append(u_n[i])
        prev.append(v_n[i])
        prev.append(w_n[i])
        
        prev.append(x_n[i])
        prev.append(y_n[i])
        prev.append(z_n[i])   
        
    res = odeint(gravitySystem, prev, times)

    x_n1 = []
    y_n1 = [] 
    z_n1 = [] 
    u_n1 = [] 
    v_n1 = [] 
    w_n1 = []
    for i in range(length):
        u_n1.append(res[1, 6*i])
        v_n1.append(res[1, 6*i + 1])
        w_n1.append(res[1, 6*i + 2])
        x_n1.append(res[1, 6*i + 3])
        y_n1.append(res[1, 6*i + 4])
        z_n1.append(res[1, 6*i + 5])

    return [x_n1, y_n1, z_n1, u_n1, v_n1, w_n1]      