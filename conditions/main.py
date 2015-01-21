# -*- coding: utf-8 -*-

import argparse

class Poly3(object):
  def __init__(self, x):
    self.x2 = x[0]
    self.x1 = x[1]
    self.x0 = x[2]
  def get(self, value):
    return self.x0 + self.x1*value + self.x2*value**2

def main():
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('temperature', metavar='temp', type=float,
                     help='a temperature, °F')
  parser.add_argument('humidity', metavar='humid', type=float,
                     help='relative hunidity, %')
  args = parser.parse_args()


  the_answer = []
  if args.temperature > FITTED_CELL.get(args.humidity):
    the_answer.append("too warm")
  elif args.temperature < FITTED_FLOOR.get(args.humidity):
    the_answer.append("too cold")
  if args.humidity > RIGHT_BOUND:
    the_answer.append("too humid")
  elif args.humidity < LEFT_BOUND:
    the_answer.append("too dry")
  if len(the_answer) == 0:
    the_answer.append("comfortable")

  print(" and ".join(the_answer))


FITTED_CELL = Poly3((8.56167979e-04, -2.64973753e-01, 9.35694751e+01))
FITTED_FLOOR = Poly3((1.48215223e-03, -2.45788714e-01, 7.83357743e+01))
LEFT_BOUND = 30
RIGHT_BOUND = 80

main()