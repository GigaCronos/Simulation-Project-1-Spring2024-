from math import log, log1p
from random import uniform
from re import L
from matplotlib import pyplot as plt
import numpy as np

def G(ratio :float):#exponencial distribution generator
    d=-1/ratio*log(uniform(0,1)+1e-100)
    return d

def T(Ts,Rat_Mi,Rat_Ma,alfa:int , beta:int):
    rest=Ts-int(Ts/(alfa+beta))*(alfa+beta)
    rat=0 #lamda(Ts)
    Ts=Ts+G(Rat_Ma)
    if(rest<alfa):
        rat=Rat_Mi+((Rat_Ma-Rat_Mi)/alfa)*rest
    else:
        rest-=alfa
        rat=Rat_Ma-((Rat_Ma-Rat_Mi)/beta)*rest
    if(uniform(0,1)<=rat/Rat_Ma):
        return Ts
    else:
        return T(Ts,Rat_Mi,Rat_Ma,alfa,beta)


def Simulate(Rat_Mi,Rat_Ma,alfa,beta,G_rat,Break_MaxTime,maxSimTime):
    curT=0
    nextArrive=T(curT,Rat_Mi,Rat_Ma,alfa,beta)
    nextTask=0
    cont=int(0)
    onBreakTime=0
    while(min(nextArrive,nextTask)<maxSimTime):
        if(nextArrive<=nextTask):
            cont+=1
            curT=nextArrive
            nextArrive=T(curT,Rat_Mi,Rat_Ma,alfa,beta)
        else:
            curT=nextTask
            if(cont==0):
                nextTask=curT+uniform(0,Break_MaxTime)
                onBreakTime+=min(nextTask-curT,maxSimTime-curT)    
            else:
                cont-=1
                nextTask=curT+G(G_rat)

    return onBreakTime

def EstimateBreakTime(Rat_Mi,Rat_Ma,alfa,beta,G_rat,Break_MaxTime,maxSimTime):
    mean=0
    for _ in range(0,500):
        mean+=Simulate(Rat_Mi,Rat_Ma,alfa,beta,G_rat,Break_MaxTime,maxSimTime)
    mean/=50
    return mean

def main():
    print(EstimateBreakTime(4,19,5,5,25,0.3,100))
    
if(__name__ == "__main__"):
    main()