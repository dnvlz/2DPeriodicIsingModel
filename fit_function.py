import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np

xdata = np.arange(1,20,1)
# Datos obtenidos del cálculo de la función de correlación
ydata=[41.605,38.7675,37.115,35.825,34.71,34.17,33.3475,32.79,32.1125,32.245,32.1125,32.79,33.3475,34.17,34.71,35.825,37.115,38.7675,41.605]

# Función a ajustar
def func(x,a,b):
    return a*np.cosh((x-10)/b)

# Código para encontrar parámetros a y b que ajustan curva
popt, pcov = opt.curve_fit(func, xdata, ydata)

#Gráficas
plt.plot(xdata, func(xdata, *popt), 'r-',label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
plt.plot(xdata,ydata,'.k')
plt.xlabel('Distance |i-j|')
plt.ylabel('Correlation')
plt.legend()
plt.show()