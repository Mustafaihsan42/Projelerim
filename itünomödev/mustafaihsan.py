# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m0qIhRbi6XNxr29Qg2ovrEuA9Z9Mt9-T
"""

import threading
import time
import random
from multiprocessing import Process, Queue
#araç sınıfı tanımı
class Vehicle:
  def __init__(self,vehicle_number):
    self.vehicle_number=vehicle_number
    self.position=[1.2, 3.4]
    self.velocity=[3.5, 6.4]
#kinematik verileri rastgele değiştiriyoruz
  def update_kinematics(self):
    self.position[0] += self.velocity[1]
    self.position[1] += self.velocity[0]
    self.velocity[1] = random.uniform(-2,3)
    self.velocity[0] =random.uniform(-2,3)

  def get_kinematics(self):
    return {
        'number': self.vehicle_number,
        'position': self.position,
        'velocity': self.velocity
    }
#iki araç için alt sınıf
class Quadcopter(Vehicle):
  def __init__(self,vehicle_number):
    super().__init__(vehicle_number)

class FixedWingDrone(Vehicle):
  def __init__(self,vehicle_number):
    super().__init__(vehicle_number)

#araçların kinematik verilerinin güncellenmesi
def vehicle_thread(vehicle,queue):
  while True:
    vehicle.update_kinematics()
    kinematics_data=vehicle.get_kinematics()
    queue.put(kinematics_data)
    time.sleep(1)

#Kontrol merkezi kısmı
def control_center(queue):
  while True:
   while not queue.empty():
    data=queue.get()
    print(f"Araç Durum Güncellemesi - Araç Numarası: {data['number']}, Araç Hızı: {data['velocity']}, Araç Konumu: {data['position']}")
    time.sleep(1)

#ana süreç başlatma

if __name__=='__main__':
  queue=Queue()

#araçları tanımla
vehicles = [
    Quadcopter(vehicle_number=1),
    FixedWingDrone(vehicle_number=2)
]

#araçlar için thread oluşturma
threads = []
for vehicle in vehicles:
  x= threading.Thread(target=vehicle_thread,args=(vehicle,queue))
  threads.append(x)
  x.start()

#kontrol merkezinin sürecini başlattığımız kısım
control_center_process=Process(target=control_center,args=(queue,))
control_center_process.start()

#iş sürecinin olumlu akması için parçacıkların tamamlanmasını beklediğimiz kısım
for x in threads:
    x.join()


control_center_process.join()