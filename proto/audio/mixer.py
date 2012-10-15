from pyo import *
s = Server().boot()
s.start()
a = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.2)
b = FM(carrier=200, ratio=[.5013,.4998], index=6, mul=.2)
c = FM(carrier=400, ratio=[.5013,.4998], index=6, mul=.2)
d = FM(carrier=2000, ratio=[.5013,.4998], index=6, mul=.2)
mm = Mixer(outs=3, chnls=2, time=.025)
fx1 = Disto(mm[0], drive=.9, slope=.9, mul=.1).out()
fx2 = Freeverb(mm[1], size=.8, damp=.8, mul=.5).out()
fx3 = Harmonizer(mm[2], transpo=1, feedback=.75, mul=.5).out()
mm.addInput(0, a)
mm.addInput(1, b)
mm.addInput(2, c)
# mm.addInput(3, d)
mm.setAmp(0,0,.5)
mm.setAmp(0,1,.5)
mm.setAmp(1,2,.5)
mm.setAmp(1,1,.5)
mm.setAmp(2,0,.5)
mm.setAmp(2,1,.5)
mm.setAmp(3,0,.5)
mm.setAmp(3,0,.5)
s.gui(locals())