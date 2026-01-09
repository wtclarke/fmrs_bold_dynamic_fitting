
# Parameter - functional relationships
Parameters = {
'conc'     : {'dynamic':'model_glm1','params':['STIM0', 'STIM1', 'constant']},
'gamma'    : {'dynamic':'model_glm2','params':['bold_lb',]},
'sigma'    : 'fixed',
'eps'      : 'fixed',
'baseline' : 'fixed',
'Phi_0'    : 'fixed',
'Phi_1'    : 'fixed'
}

import numpy as np
# Bounds on free fitted parameters
Bounds = {
'sigma' : (0,None),
'constant' : (0,None),
'baseline' : (0, 0),
'bold_lb'  : (np.pi, np.pi)
}

# Dynamic models
from numpy import dot
def model_glm1(p,t):
    return dot(t[:, :3],p)

# Dynamic model gradients
def model_glm1_grad(p,t):
    return t[:, :3].T

def model_glm2(p,t):
    return dot(t[:, -1:],p)

# Dynamic model gradients
def model_glm2_grad(p,t):
    return t[:, -1:].T

# Init functions for the lorentzian linebroadening
def model_glm2_init(y, t):    
    return np.pi