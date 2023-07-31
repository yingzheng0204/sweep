from param import *
from thermo import *
from state import *
import os

class Sweep:
   '''
   '''

   def __init__(self, d):
      old_cwd = os.getcwd()

      if os.path.isdir(d) == True:
         os.chdir(d)
      elif os.path.isfile(d) == True:
         p = Composite(d)
         for x,y in p.children.items():
            if x.rfind('Sweep') != -1:
               nd = old_cwd + '/' + y.baseFileName
               break
         try:
            os.chdir(nd)
         except:
            raise Exception('No Sweep block in the Param file')
      else:
         raise Exception('Not valid argument')

      filenames = []
      for file in os.listdir():
         if file.endswith('.dat'):
            filenames.append(file)
      filenames.sort()

      self.sweep = []
      for i in range(0, len(filenames)):
         s = State(filenames[i])
         self.sweep.append(s)

      os.chdir(old_cwd)

   def summary(self, l, index = False):
      n = len(l)

      summary = []

      for i in range(0, len(self.sweep)):
         if index == True:
            s = [i]
         else:
            s = []
         for j in range(0, n):
            a = self.sweep[i]
            string = 'a.' + l[j]
            try:
               val = eval(string)
            except RecursionError:
               raise Exception('Wrong command or values do not exist')
            s.append(val)
         summary.append(s)

      return summary

   def summaryString(self, l):
      n = len(l)

      summary = []

      for i in range(0, len(self.sweep)):
         s = [i]
         for j in range(0, n):
            a = self.sweep[i]
            string = 'a.' + l[j]
            try:
               val = eval(string)
            except RecursionError:
               raise Exception('Wrong command or values do not exist')
            s.append(val)
         summary.append(s)

      nl = [4]
      nameList = ['step']
      for i in range(0, n):
         index = l[i].rfind('.')
         name = l[i][index+1:]
         nameList.append(name)
         nl.append(len(name))

      valType = []
      for i in range(0, len(summary)):
         valType.append([])
         for j in range(0, len(summary[0])):
            valType[i].append(type(summary[i][j]))

      for i in range(0, len(summary)):
         for j in range(0, len(summary[0])):
            length = len(str(summary[i][j]))
            if (valType[i][j] == str) and (length > nl[j]):
               nl[j] = length
            if (valType[i][j] == float) and (13 > nl[j]):
               nl[j] = 13
            if (valType[i][j] == int) and (length > nl[j]):
               nl[j] = length


      summaryString = ' '
      for i in range(0, len(nameList)):
         stringFormat = '{:>' + str(nl[i]) + 's}'
         if i != len(nameList)-1:
            summaryString += stringFormat.format(nameList[i]) + '  '
         else:
            summaryString += stringFormat.format(nameList[i]) + '\n '

      for i in range(0, len(summary)):
         for j in range(0, len(summary[0])):
            if valType[i][j] == int:
               stringFormat = '{:>' + str(nl[j]) + '}'
               summaryString += stringFormat.format(summary[i][j])
            if valType[i][j] == float:
               stringFormat = '{:.7e}'
               val = stringFormat.format(summary[i][j])
               summaryString += val
            if valType[i][j] == str:
               stringFormat = '{:>' + str(nl[j]) + 's}'
               summaryString += stringFormat.format(summary[i][j])
            if j == len(summary[0])-1:
               summaryString += '\n '
            else:
               summaryString += '  '

      return summaryString

   def __getitem__(self, key):
      return self.sweep[key]

# s = Sweep('100')
s = Sweep('param100up')
# print(s.summary(['param.Mixture.ds', 'thermo.pressure', 'param.Domain.mode']))
print(s[0])
print(s.summary(['param.Mixture.ds', 'thermo.pressure', 'param.Domain.mode'], index = True))
print(s.summaryString(['param.Interaction.chi[0][1]', 'thermo.pressure', 'param.Domain.mode']))








