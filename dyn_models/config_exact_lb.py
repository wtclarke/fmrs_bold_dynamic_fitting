
# Parameter - functional relationships
Parameters = {
'conc'     : {'dynamic':'model_glm1','params':['STIM0', 'STIM1', 'constant']},
'gamma'    : {'dynamic':'model_glm2','params':['const_lb', 'bold_lb']},
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
'const_lb' : (None, None)
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

# Init functions for the lorentzian linebroadening
from functools import partial
from scipy.optimize import minimize
from scipy.stats import norm
import numpy as np

def torbit_negloglike(
        y: np.ndarray,
        pred: np.ndarray,
        sigma: float,
        censor_point: float = 0.0) -> float:
    """Calculate the negative log-likelihood for a torbit model

    :param y: Data to fit
    :type y: np.ndarray
    :param pred: fit prediction
    :type pred: np.ndarray
    :param sigma: estimate of noise standard deviation
    :type sigma: float
    :param censor_point: Point at which model is censored (clipped), defaults to 0.0
    :type censor_point: float, optional
    :return: Negative log-likelihood
    :rtype: float
    """
    # mask for uncensored (observed above the censor point)
    uncensored = y > censor_point
    censored = ~uncensored

    # contribution from uncensored: log pdf at observed y
    ll_unc = norm.logpdf(
        y[uncensored],
        loc=pred[uncensored],
        scale=sigma)

    # contribution from censored: log CDF at censor_point
    # P(y* <= censor_point) = Phi((censor_point - mu)/sigma)
    ll_cens = norm.logcdf(
        censor_point,
        loc=pred[censored],
        scale=sigma)

    # Return negative log-likelihood
    return -(np.sum(ll_unc) + np.sum(ll_cens))

def torbit_min(params, tvar, x0, censor_point=0.0):
    func = partial(model_glm2, t=tvar)

    def loss(x):
        pred = np.maximum(func(x[:-1]), censor_point)
        sigma = np.exp(x[-1])
        return torbit_negloglike(params, pred, sigma, censor_point=censor_point)
    
    bounds = ((None, None), (None, None), (None, None))
    return minimize(loss,
                    x0,
                    bounds=bounds).x

def model_glm2_init(y, t):
    lstsq_init = np.linalg.lstsq(
        t[:, -2:],
        y,
        rcond=None)[0]
    
    log_sigma_init = np.log(np.std(y - t[:, -2:] @ lstsq_init))
    x0_torbit = np.concatenate([lstsq_init, [log_sigma_init]])

    return torbit_min(
        y,
        t[:, -2:],
        x0_torbit,
        censor_point=0.0)[:-1]