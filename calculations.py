# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 22:54:31 2018

@author: Masha
"""

import multi as multi
import verlet as verlet
import cyth as cyth
import classes as myClass

class Calculations:
        
    def CalculateVerlet(particle_list, timerStep, timer):
        return verlet.Calculate(particle_list, timerStep, timer)     
                    
        
    
    def CalculateVerletSolar(particle_list, timerStep, timer):
        return verlet.CalculateSolar(particle_list, timerStep, timer)  
    
    
    

    
    
    def CalculateOdeint(particle_list, timer_step, timer):
#        G = 6.67408 * (10 ** -9)
#        
#        x_n = []
#        y_n = []
#        z_n = []
#        u_n = []
#        v_n = []
#        w_n = []
#        m_n = []
#        col_n = []        
#        
#        for partic in particle_list:
#            for par in particle_list:
#                if (partic.position.Module(par.position) > 0) & (partic.position.Module(par.position) < (partic.m + par.m) / 100.0):
#                    if partic.m > par.m:
#                        partic.m += par.m
#                    else:
#                        partic.alive = False
#                        
#            if (partic.alive):
#                x_n.append(partic.x)
#                y_n.append(partic.y)
#                z_n.append(partic.z)
#                u_n.append(partic.u)
#                v_n.append(partic.v)
#                w_n.append(partic.w)
#                m_n.append(partic.m)
#                col_n.append(partic.color)
#                
#        length = len(x_n) 
#        if length < 2:
#            print('stop')
#            timer.stop()   
#            
#        v = Symbol('v')
#        m = Symbol('m', Positive=True)
#        x = Symbol("x")
#        t = Symbol("t", Positive=True)
#            
#        def dxdt(v):
#            return v
#        
#        def dvdt(m, r1, r2):
#            mr12 = r1.Module()
#            return dv
#    
#        z1 = [0, 0.00]
#        v = odeint(dvdt, z1, t, args = (m, r_i, r_j))
#
#        
#        _particle_list = []
#        for i in range(length):
#            position = myClass.Position(x_n1[i] / constRadius, y_n1[i] / constRadius, z_n1[i] / constRadius)
#            velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
#            _particle_list.append(myClass.Particle(position, velocity, m_n[i] / constMass, col_n[i]))
           
        return 
    
    def CalculateOdeintSolar(particle_list, timer_step, timer):
        
        return
    
    
    def CalculateParallSolar(particle_list, timerStep, timer):
        return multi.CalculateSolar(particle_list, timerStep, timer)
    
     
    def CalculateParall(particle_list, timerStep, timer):
        return multi.Calculate(particle_list, timerStep, timer) 
        
        
    def CalculateCythonSolar(particle_list, timer_step, timer):
#        constRadius = 14959787070
#        constMass = 5.9726 * 10**24
#        
#        x_n = [p.x * constRadius for p in particle_list]
#        y_n = [p.y * constRadius for p in particle_list]
#        z_n = [p.z * constRadius for p in particle_list]
#        position = [myClass.Position(x, y, z) for x, y, z in zip(x_n, y_n, z_n)]
#        u_n = [p.u for p in particle_list]
#        v_n = [p.v for p in particle_list]
#        w_n = [p.w for p in particle_list]
#        m_n = [p.m * constMass for p in particle_list]
#        col_n = [p.color for p in particle_list]        
#                            
#        length = len(x_n) 
#        if length < 9:
#            print('stop')
#            timer.stop() 
#        else:
#            x_n1, y_n1, z_n1, u_n1, v_n1, w_n1 = cyth.Calculate(x_n, y_n, z_n, u_n, v_n, w_n, m_n, col_n)
#            _particle_list = []
#            for i in range(length):
#                position = myClass.Position(x_n1[i] / constRadius, y_n1[i] / constRadius, z_n1[i] / constRadius)
#                velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
#                _particle_list.append(myClass.Particle(position, velocity, m_n[i] / constMass, col_n[i]))
#                            
#        return _particle_list  
        return
    
    
    def CalculateCython(particle_list, timer_step, timer):
#        x_n = []
#        y_n = []
#        z_n = []
#        u_n = []
#        v_n = []
#        w_n = []
#        m_n = []
#        col_n = []        
#            
#        for partic in particle_list:
#            for par in particle_list:
#                if (partic.position.Module(par.position) > 0) & (partic.position.Module(par.position) < (partic.m + par.m) / 100.0):
#                    if partic.m > par.m:
#                        partic.m += par.m
#                    else:
#                        partic.alive = False
#        
#                            
#            if (partic.alive):
#                x_n.append(partic.x)
#                y_n.append(partic.y)
#                z_n.append(partic.z)
#                u_n.append(partic.u)
#                v_n.append(partic.v)
#                w_n.append(partic.w)
#                m_n.append(partic.m)
#                col_n.append(partic.color)
#                    
#        length = len(x_n) 
#        if length < 2:
#            print('stop')
#            timer.stop() 
#        else:
#            x_n1, y_n1, z_n1, u_n1, v_n1, w_n1 = cyth.Calculate(x_n, y_n, z_n, u_n, v_n, w_n, m_n, col_n)
#            _particle_list = []
#            for i in range(length):
#                position = myClass.Position(x_n1[i], y_n1[i], z_n1[i])
#                velocity = myClass.Velocity(u_n1[i], v_n1[i], w_n1[i])
#                _particle_list.append(myClass.Particle(position, velocity, m_n[i], col_n[i]))
#        
#        return _particle_list
        return
