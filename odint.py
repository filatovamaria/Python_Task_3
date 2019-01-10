from math import sqrt
from numpy import linspace
from scipy.integrate import odeint



def Calculate(G, x_n, y_n, z_n, u_n, v_n, w_n, m_n, timerStep):
  
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
                if module > 0:
                    ax_sum += G * m_n[j] * (x[j] - x[i]) / module
                    ay_sum += G * m_n[j] * (y[j] - y[i]) / module
                    az_sum += G * m_n[j] * (z[j] - z[i]) / module
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
 