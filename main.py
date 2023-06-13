import simcx
from simcx.simulators import FunctionIterator, Simulator
from simcx.visuals import TimeSeries
from pylab import *
import matplotlib.pyplot as plt

# Initial population
p0 = 3
a0 = 2
b0 = 1

# Test parameter (initial)
a1 = 1.5
a2 = 0.5
b1 = 1.8
b2 = 0.6
np = 4/7
wa = 2/7
wb = 1/7

def predator(p,a,b):
    return -p * np + p * wa * a + p * wb * b

def prey_A(a,p):
    return a * a1 - a * a2 * p

def prey_B(b,p):
    return b * b1 - b2 * b * p

class MyIterator(Simulator):
    def __init__(self, func1, func2, func3, initial_state1, initial_state2, initial_state3, Dt):
        super(MyIterator, self).__init__()
        self.initial_state1 = initial_state1
        self.initial_state2 = initial_state2
        self.initial_state3 = initial_state3

        self._state1 = initial_state1
        self._state2 = initial_state2
        self._state3 = initial_state3

        self.func1 = func1
        self.func2 = func2
        self.func3 = func3

        self.i = 0
        self.x = [0]
        self.y = [[initial_state1], [initial_state2], [initial_state3]]
        self.sum = [initial_state2 + initial_state3]
        self.Dt = Dt

    def step(self, delta=0):
        
        old_state_1 = self._state1
        self._state1 = self.y[0][-1] + self.func1(self._state1,self._state2,self._state3) * self.Dt
        self._state2 = self.y[1][-1] + self.func2(self._state2,old_state_1) * self.Dt
        self._state3 = self.y[2][-1] + self.func3(self._state3,old_state_1) * self.Dt

        if(self._state1 < 0):
            self._state1 = 0
        if(self._state2 < 0):
            self._state2 = 0
        if(self._state3 < 0):
            self._state3 = 0
        
        self.y[0].append(self._state1)
        self.y[1].append(self._state2)
        self.y[2].append(self._state3)
        self.sum.append(self._state2 + self._state3)

        # print for checking on population
        if self.i == 1 or self.i == 2 or self.i == 75 or self.i == 100:
            print("\n   Predator Pop: ", self.y[0][-1])
            print("\n   Prey A Pop: ", self.y[1][-1])
            print("\n   Prey B Pop: ", self.y[2][-1])

        self.x += [self.x[-1] + self.Dt]
        self.i += 1
    def reset(self):
        self._state1 = self.initial_state1
        self._state2 = self.initial_state2
        self._state3 = self.initial_state3
        self.Dt = Dt
        self.x = [0]
        self.y = [[self.initial_state1],[self.initial_state2],[self.initial_state3]]
        self.sum = [self.initial_state1 + self.initial_state2]

class MyVisual(simcx.MplVisual):
    def __init__(self, sim):
        super(MyVisual, self).__init__(sim)
        self.ax = self.figure.add_subplot(111)
        self.l, = self.ax.plot(self.sim.x, self.sim.y[0], '-b')
        self.l1, = self.ax.plot(self.sim.x, self.sim.y[1], '-r')
        self.l2, = self.ax.plot(self.sim.x, self.sim.y[2], '-g')

    def draw(self):
        self.l.set_data(self.sim.x, self.sim.y[0])
        self.l1.set_data(self.sim.x, self.sim.y[1])
        self.l2.set_data(self.sim.x, self.sim.y[2])
        self.ax.relim()
        self.ax.autoscale_view()

class PhaseSpace(simcx.MplVisual):
    def __init__(self, sim):
        super().__init__(sim)
        self.ax = self.figure.add_subplot(111)
        self.l, = self.ax.plot(self.sim.x, self.sim.y[0], '-b')
        self.l1, = self.ax.plot(self.sim.x, self.sim.y[1], '-r')
        self.l2, = self.ax.plot(self.sim.x, self.sim.y[2], '-g')
        self.i = 0

    def draw(self):
        #self.l.set_data(self.sim.y[1], self.sim.y[0])
        #self.l1.set_data(self.sim.y[2], self.sim.y[0])
        #self.l2.set_data(self.sim.y[0], self.prey)
        #self.i += 1
        self.l2.set_data(self.sim.sum, self.sim.y[0])
        self.ax.relim()
        self.ax.autoscale_view()


if __name__ == "__main__":
    
    ############################
    ### SIMCX BLOCK
    ############################
    
    Dt = 0.1

    
    display = simcx.Display()
    simulate = MyIterator(predator, prey_A, prey_B, p0, a0, b0, Dt)
    #print(simulate.initial_state1)
    visualize = MyVisual(simulate)
    preys = []
    for i in range(len(simulate.y[0])):
        preys.append(simulate.y[1][i] + simulate.y[2][i])
    #visualize = PhaseSpace(simulate)

    display.add_simulator(simulate)
    display.add_visual(visualize)

    simcx.run()
    
    
    ############################
    ### MATPLOTLIB BLOCK
    ############################
    
    '''
    matplotlib.use('TkAgg')
    simulate = MyIterator(predator, prey_A, prey_B, p0, a0, b0, Dt)
    [simulate.step() for i in range(800)]


    x = simulate.y[1]
    y = simulate.y[2]
    z = simulate.y[0]
    preys = []
    for i in range(len(simulate.y[0])):
        preys.append(simulate.y[1][i] + (simulate.y[2][i])/2)

    #plot simulation
    plt.plot(simulate.x,z,color='b',label='Predators')
    plt.plot(simulate.x,x,color='r',label='Prey A')
    plt.plot(simulate.x,y,color='g',label='Prey B')
   
    #plot phase space
    #plt.plot(y,z)
    #plt.axvline(x=8, color='r', linestyle='-')
    #plt.axhline(y=3, color='g', linestyle='-')
    #plt.plot(2,3,'ro',label='Fixed Point') 
  
    plt.legend()
    plt.show()
    '''