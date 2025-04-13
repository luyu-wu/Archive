import numpy as np
import matplotlib.pyplot as plt

fig,ax = plt.subplots()

concentrations = np.array([0,0.2,0.4,0.6,0.8,1.0])
mass_change = np.array([20.62473153,0.2654137606,-11.42192361,-25.01852079,-33.01744722,-27.53562677])
st = np.array([4.679832065,11.37014266,3.285282466,2.280116734,3.96945238,6.781351649])
ax.errorbar(concentrations[:-1],mass_change[:-1],yerr=st[:-1],fmt='o',label="Averaged Data")
ax.errorbar(concentrations[-1],mass_change[-1],yerr=st[-1],fmt='o',alpha=0.3,label="Removed Data")
a,b = np.polyfit(concentrations[:-1],mass_change[:-1],1)
ax.plot(concentrations,a*concentrations + b, ls="--",color='#089FFF',alpha=0.8,label="LoBF")

print(a,b,-b/a)
ax.legend()
ax.set_title("Relative Mass Change")
ax.set_ylim(-40,40)
ax.set_xlabel(r'Sucrose Concentrations ($M$)')
ax.set_ylabel("Mass Change (%)")
ax.grid(True, linestyle='--', which='major',color='grey', alpha=.25)


plt.tight_layout()
plt.show()
