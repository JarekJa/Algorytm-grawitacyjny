from random import uniform
import math
import matplotlib.pyplot as plt
from numpy import transpose



class GSA(object):
    def __init__(self, G, n, tab_roz):
        self.agenci = self.generój_agentów( n, tab_roz)
        self.G=G
        self.G0=G
        self.n=n
        self.v=[]
        for i in range(n):
            self.v.append([0, 0])



    def generój_agentów(self, n, tab_roz):
        agenci = []
        for i in range(n):
            wiersz = []
            wiersz.append(round(uniform(tab_roz[0][0], tab_roz[0][1]),2))
            wiersz.append(round(uniform(tab_roz[1][0], tab_roz[1][1]), 2))
            agenci.append(wiersz)

        rys=transpose(agenci)
        plt.plot(rys[0],rys[1],'o')
        plt.show()
        return agenci
    def funkcja(self,x,y):
        if x==0:
            return 100000
        else:
            return math.fabs(math.cos(2**x+y**2)*x+y**3/x)
    def oblicz_masy(self,agenci,n):
        masy=[]
        sort_agenci=[]
        sort_prędkości = []
        pom=self.funkcja(agenci[0][0],agenci[0][1])
        sort_agenci.append(agenci[0])
        sort_prędkości.append(self.v[0])
        masy.append(pom)
        for i in range(1,n):
            npom=self.funkcja(agenci[i][0],agenci[i][1])
            j=0
            p = True
            while j<i and p:
                if masy[j]>npom:
                    masy.insert(j,npom)
                    sort_agenci.insert(j,agenci[i])
                    sort_prędkości.insert(j,self.v[i])
                    p=False
                j=j+1
            if p:
                masy.append(npom)
                sort_agenci.append(agenci[i])
                sort_prędkości.append(self.v[i])
        self.v=sort_prędkości
        self.agenci=sort_agenci
        fun_nlep=masy[0]
        fun_ngor=masy[len(masy)-1]
        print(fun_nlep)
        M=[]
        suma=0
        for i in range(n):
            pomM=(masy[i]-fun_ngor)/(fun_nlep-fun_ngor)
            M.append(pomM)
            suma+=pomM
        masy=[]
        for i in range(n):
            masy.append(M[i]/suma)
        return masy,fun_nlep
    def oblicz_odległość(self,agent1,agent2):
        odległość=math.sqrt((agent1[0]-agent1[1])**2+(agent2[0]-agent2[1])**2)
        return odległość
    def wylicz_siły(self,agenci,masy,n):
        F=[]
        for i in range(n):
            pom=[]
            x=0
            y=0
            for j in range(n):
                if i!=j:
                    war=self.G*(masy[i]*masy[j])/(self.oblicz_odległość(agenci[i],agenci[j])+0.1)*(-1)
                    pomlos=uniform(0,1)
                    x+=war*(agenci[i][0]-agenci[j][0])*pomlos
                    y+=war * (agenci[i][1] - agenci[j][1])*pomlos
                else:
                    x=0
                    y=0
            pom.append(x)
            pom .append(y)
            F.append(pom)
        return F
    def wykonaj(self,ite):
        fun_naj=100000
        for i in range(ite) or fun_naj!=0:
            a=[]
            masy,fun_naj=self.oblicz_masy(self.agenci,self.n)
            F=self.wylicz_siły(self.agenci,masy,self.n)
            for j in range(self.n):
                pom=[]
                if masy[j]!=0:
                    pom.append(F[j][0]/masy[j])
                    pom.append(F[j][1] / masy[j])
                else:
                    pom=[0,0]
                a.append(pom)
            new_agęci=[]
            for j in range(self.n):
                pom = []
                losowa=uniform(0, 1)
                pomx=self.v[j][0] * losowa + a[j][0]
                pomy=self.v[j][1] * losowa + a[j][1]
                pom.append(self.agenci[j][0]+pomx)
                pom.append(self.agenci[j][1] + pomy)
                self.v[j][0]=pomx
                self.v[j][1]=pomy
                new_agęci.append(pom)


            self.G=self.G0*math.e**(-(ite/4)*i/ite)
            self.agenci=new_agęci

        rys = transpose(self.agenci)
        plt.plot(rys[0], rys[1], 'o')
        plt.show()
        return fun_naj,self.agenci[0]



roz= GSA(5,1000,[[-10,10],[-10,10]])
print(roz.wykonaj(1000))



