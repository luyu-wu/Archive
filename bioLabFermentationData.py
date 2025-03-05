import matplotlib.pyplot as plt
import numpy as np

sample_1 = np.array([0,7.5,11.2,10.2])
sample_2 = np.array([0,6.5,9.2,12.2])
sample_3 = np.array([0,6.0,8.2,9.0])
sample_4 = np.array([0,7.4,8.9,11])
control = np.array([0,0,0,0])

days = np.array([0,7,11,18])


plt.errorbar(days,sample_1,label="Sample 1",fmt="o",alpha=0.5)
plt.errorbar(days,sample_2,label="Sample 2",fmt="s",alpha=0.5)
plt.errorbar(days,sample_3,label="Sample 3",fmt="^",alpha=0.5)
plt.errorbar(days,sample_4,label="Sample 4",fmt="D",alpha=0.5)
plt.errorbar(days,control,label="Control",fmt="x",alpha=0.5)



plt.errorbar(days,np.average([sample_1,sample_2,sample_3,sample_4],axis=0),yerr=np.std([sample_1,sample_2,sample_3,sample_4],axis=0),capsize=2,fmt="*-",color="black")

plt.xlabel("Time (days)")
plt.ylabel("Alcohol Content (%)")
plt.title("Data for Room Samples")
plt.legend()
plt.grid()
plt.show()
