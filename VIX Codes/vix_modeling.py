import numpy as np



def poly_ols_sde(data, terms = 2):
    """
    poly_ols_SDE is a function that uses a polynomial SDE form to model data.
    The functional form of the model is defined as
        dX_t = (a*x**2+b*x+c) * dt
    where:
        The highest order term is determined by the terms parameter

    Args:
        data (dataFrame): The time series data to be used for this differential equation model
        terms (int, optional): The degree of the leading term in the polynomial. Defaults to 2.

    Returns:
        list: Output is the coefficients for the model such as a,b,c from the example form above.
    """

    dt = (data[1,1]-data[0,1])
    n = len(data[:,0])
    x = data[:,0] # Original data
    dx = np.zeros((n, 1)) # Differntial series
    mod = np.zeros((n, terms)) # Model data
            
    for i in range(0,n-1):
        dx[i+1] = (x[i+1] - x[i])/dt
        for j in range(0, terms):
            mod[i+1,j] = x[i]**j
    
    return np.linalg.inv(mod.T @ mod) @ np.dot(mod.T, dx)



def poly_ols(data, terms = 2):
    """
    poly_ols_SDE is a function that uses a polynomial SDE form to model data.
    The functional form of the model is defined as
        dX_t = (a*x**2+b*x+c) * dt
    where:
        The highest order term is determined by the terms parameter

    Args:
        data (dataFrame): The time series data to be used for this differential equation model
        terms (int, optional): The degree of the leading term in the polynomial. Defaults to 2.

    Returns:
        list: Output is the coefficients for the model such as a,b,c from the example form above.
    """
    n = len(data[:,0])
    x_mod = np.zeros((n, terms))
    
    for i in range(0,n):
        for j in range(0, terms):
            x_mod[i,j] = data[i,0]**j
    
    return np.linalg.inv(x_mod.T @ x_mod) @ np.dot(x_mod.T, data[:,1])



def noise_modeler(data, beta, bins=1000, terms=1):
    dt = (data[1,1]-data[0,1])
    n = len(data[:,0])
    x_noi = np.np.zeros((n, 1))
    noise = np.zeros((bins, 2))
    
    for i in range(1, n):
        Est = 0
        for j in range(0, len(beta)):
            Est += beta[j] * data[i-1,0]**j * dt
        x_noi[i] = data[i,0] - data[i-1,0] - Est
    
    per = np.linspace(5, 95, (bins+1))
    bin_edges = np.percentile(data[:,0], per)
    masks = {}
    for i in range(0, bins):
        mask = (data[:,0] >= bin_edges[i]) & (data[:,0] <= bin_edges[i+1])
        masks[f'bin_{i}'] = [data[mask,0], x_noi[mask]]
    
    for i in range(0, bins):
        noise[i,0] = masks[f'bin_{i}'][0].mean()
        noise[i,1] = (masks[f'bin_{i}'][1].var()/dt)**(1/2)
    beta = poly_ols(noise, terms=terms)
    return beta

