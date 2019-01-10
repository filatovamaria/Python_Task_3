# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 16:14:47 2019

@author: Masha
"""

import random

import classes as myClass
import calculations as calc

mytype = 1
rang = 100

_dt = 1000
isSolar = True


_particle_list = []

if isSolar:
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
else: 
    _particle_list.append(myClass.Particle(myClass.Position(0, 0, 0), myClass.Velocity(0, 0, 0), 3000, [255, 0, 0]))
                
    for i in range(1, rang):
        _particle_list.append(
                myClass.Particle(myClass.Position(random.randint(-500, 500), random.randint(-500, 500), random.randint(-500, 500)), myClass.Velocity(random.randint(-5, 5) / 10000.0, random.randint(-5, 5) / 10000.0, random.randint(-5, 5) / 10000.0), random.uniform(100, 1000), [random.uniform(0.3, 0.9), random.uniform(0.3, 0.9), random.uniform(0.3, 0.9)]))
   
if isSolar:
    _particle_list = calc.CalculateSolar(mytype, _particle_list, _dt)
else:
    times = calc.Calculate(mytype, _particle_list, _dt)
    
    print("--- %s seconds ---" % (sum(times)/5))
