import matplotlib.pyplot as plt

class car:
   name = ""   #name of the car
   Cd = 0      #coefficient of drag, unitless
   Crr = 0     #coefficient of rolling resistance.
   Af = 0      #frontal area of the car
   M = 0       #Mass of the car in kg
   B = 0       #Battery capacity of the car in kWh
   IdlePow = 0 #Idle power, consumed by equipment, AC, etc.
   E = 0       #Battery capacity of the car in Joules.  Input as kWh and calc'd
   p = 1.2     #density of earth's atmosphere at sea level, kg/m^3
   g = 9.80665 #gravitational acceleration at sea level, m/s^2
   v = []
   R = []
   P = []
   
   def __init__(self,name,Cd,Crr,Af,M,B,IdlePow):
      self.name = name
      self.Cd = Cd
      if Crr > 0.014:
         warnings.warn("Typical rolling resistance is between 0.007 and 0.014, adjusting.")
         self.Crr = 0.014
      elif Crr < 0.007:
         warnings.warn("Typical rolling resistance is between 0.007 and 0.014, adjusting.")
         self.Crr = 0.007
      else:
         self.Crr = Crr
      self.Af = Af
      self.M = M
      self.B = B
      self.E = B*3.6e6
      self.IdlePow = IdlePow
   
   def P_cons(self,v):
      Cd = self.Cd
      Crr = self.Crr
      Af = self.Af
      N = self.M*self.g
      Pd = 0.5*self.p*Cd*Af*v**3    #(kg/m^3*m^2*(m/s)^3) = W
      Prr = N*Crr*v                 #(kg*m/s^2*m/s) = W
      return Pd+Prr+self.IdlePow
   
   def P_to_Range(self,P,v):
      return self.E*v/P*0.000621371
      

Bolt = car("Bolt EV",0.312,0.010,2.397,1616.15,60,1000)

f = open("Power.csv","w+")
f.write("Creating power curve for the following inputs:\n")
f.write("v(mph),P (W),Range (mi)\n")

for v in range(1,100):
   mps = v/2.23694
   P = Bolt.P_cons(mps)
   R = Bolt.P_to_Range(P,mps)
   f.write("{},{},{}\n".format(v,P,R))
   Bolt.v.append(v)
   Bolt.P.append(P)
   Bolt.R.append(R)
f.close

plt.plot(Bolt.v,Bolt.R)
plt.ylabel('Range (mi)')
plt.xlabel('Speed (mph)')
plt.show()