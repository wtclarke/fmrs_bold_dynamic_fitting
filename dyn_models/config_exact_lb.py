
# Parameter - functional relationships
Parameters = {
'conc'     : {'dynamic':'model_glm1','params':['STIM0', 'STIM1', 'constant']},
'gamma'    : {'dynamic':'model_glm2','params':['constant', 'Lorentz_lb']},
'sigma'    : 'fixed',
'eps'      : 'fixed',
'baseline' : 'fixed',
'Phi_0'    : 'fixed',
'Phi_1'    : 'fixed'
}

# Bounds on free fitted parameters
Bounds = {
'sigma' : (0,None),
'constant' : (0,None),
}

# Dynamic models
from numpy import dot
def model_glm1(p,t):
    return dot(t[:, :3],p)

# Dynamic model gradients
def model_glm1_grad(p,t):
    return t[:, :3].T

def model_glm2(p,t):
    return dot(t[:, -2:],p)

# Dynamic model gradients
def model_glm2_grad(p,t):
    return t[:, -2:].T
