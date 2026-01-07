
# Parameter - functional relationships
Parameters = {
'conc'     : {'dynamic':'model_glm','params':['STIM0', 'STIM1', 'constant']},
'gamma'    : 'fixed',
'sigma'    : 'fixed',
'eps'      : 'fixed',
'baseline' : 'fixed',
'Phi_0'    : 'fixed',
'Phi_1'    : 'fixed'
}

# Bounds on free fitted parameters
Bounds = {
'gamma' : (0,None),
'sigma' : (0,None),
'constant' : (0,None),
'baseline' : (0, 0)
}

# Dynamic models
from numpy import dot
def model_glm(p,t):
    return dot(t,p)

# Dynamic model gradients
def model_glm_grad(p,t):
    return t.T
