import matplotlib.pyplot as plt
import numpy as np

# frequencies: start, end, spacing
f = np.arange(0,100000,50)
# mel scale equation per http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/
m = 1125 * np.log(1+f/700)
fig, ax = plt.subplots()
ax.plot(f,m)
ax.grid(linestyle=':')
plt.title('Mel Scale vs frequency')
plt.xlabel('frequency (Hz)')
plt.ylabel('mels')

plt.show()