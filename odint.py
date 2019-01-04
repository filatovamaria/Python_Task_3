# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 09:53:39 2018

@author: Masha
"""

import numpy
import math
from sympy import lambdify, Symbol
from scipy.integrate import odeint

import classes as myClass

def Calculate(particle_list, timer_step, timer):
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
    if length < 2:
        print('stop')
        timer.stop()   
        
    v = Symbol('v')
    m = Symbol('m', Positive=True)
    x = Symbol("x")
    t = Symbol("t", Positive=True)
        
    def dxdt(v):
        return v
    
    def dvdt(m, r1, r2):
        mr12 = r1.Module()
        return dv
    
    x = []
    y = []
    z = []
    u = []
    v = []
    w = []
    for i in range(length):
        par = myClass.Particle(x_n[i], y_n[i], z_n[i])
        modul =  
        

    z1 = [0, 0.00]
    v = odeint(dvdt, z1, t, args = (m, r_i, r_j))

    
    _particle_list = []
    for i in range(length):
        position = myClass.Position(x[i], y[i], z[i])
        velocity = myClass.Velocity(u[i], v[i], w[i])
        _particle_list.append(myClass.Particle(position, velocity, m_n[i], col_n[i]))
    return _particle_list

def CalculateSolar():
    return  
    