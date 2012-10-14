from pyo import *
import time

s = Server().boot()
s.start()

wav = SquareTable()

# env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
# met = Metro(.125, 12).play()
# amp = TrigEnv(met, table=env, mul=.2)
# pit = TrigXnoiseMidi(met, dist=4, x1=10, scale=1, mrange=(48,84))

a = Osc(table=wav, freq=440, mul=1).out()
time.sleep(2)
a.stop()
time.sleep(2)

#s.gui(locals())
