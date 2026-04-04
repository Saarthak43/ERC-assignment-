## ANSWER 3 

```cpp
import numpy as np ## calculation of FFT
import matplotlib.pyplot as plt ## plotting of graphs 
from scipy.io import wavfile ## scipy library to read and write wav files
import os ## create direcrtory for plots
os.makedirs("plots", exist_ok=True)
##load the file
sample_rate, data = wavfile.read("corrupted.wav")## reads the corrupted file
data = data.astype(float)
```
In this block of code we are importing different kinds of libraries such as 

> import numpy as np
NumPy is a maths library for Python, we'll use it here for FFT calculations .
as np is used so that we write np instead of numpy everytime .

> import matplotlib.pyplot as plt
Matplotlib is a graph-plotting library. It lets us draw charts and visualise our data.

> from scipy.io import wavfile
SciPy is a scientific computing library
we are not importing everything from this library but only wavfile which lets us read and write .wav files - essentially the sound files

> import os
OS stands for Operating System. basically powers on the python

> os.makedirs("plots") — creates a folder called plots where all our graph images will be saved
exist_ok=True — means "if the folder already exists, don't crash, just continue". Without this, the code would throw an error if you ran it a second time.

### THE VARIABLES 

sample_rate — stores how many samples exist per second 

data — stores the actual raw audio as a big list of numbers
