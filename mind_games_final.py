import numpy as np
import matplotlib.pyplot as plt
from icecream import ic 
import sys
import copy 

from IPython import get_ipython

print("\033[H\033[J"); 
get_ipython().run_line_magic('matplotlib', 'qt')



# I numeri sulle carte vanno da 1 a N_max
N_max = 100

# Numero di giocatori
n_gioc = 2

# Ogni giocatore ha in mano (n_carte_mani) carte
n_carte_mano = 5

# Array controllo frequenze carte
control = np.zeros(N_max)

n_carte_tot = n_gioc * n_carte_mano


#%% Calcoli

# Variabili varie

count_1 = 0
count_2 = 0    
sum_max_salto_in = 0
sum_max_salto_ex = 0
sum2_max_in = 0
sum2_max_ex = 0

media = 0
media_2 = 0

# Istogramma probabilità dei salti
prob_ex = np.zeros(N_max)
prob_in = np.zeros(N_max)

# Istogrammi g(r)
g_r = np.zeros(N_max)

N_rip = 10000


# Ciclo principale
for index in range(N_rip):
# while True :
    
    # N_rip += 1
        
    # if  ( N_rip > 10000 and  ( (np.std(control) / np.mean(control)) < 0.01) ):
    #     break
    
    # Mostra l'avanzamento del programma
    if N_rip % 10000 == 0:
        print('*', end='')
    
    # Pesca le carte, inizializza le mani di ogni giocatore e riordinale
    carte_tot = list(np.random.permutation(100)[:n_carte_tot] + 1)
    mani = []
    n_min = 0
    
    for i in range(0, n_gioc):
        mano = carte_tot[ n_min : n_min + n_carte_mano ]
        mani.append( mano )
        n_min += n_carte_mano
    
    for i in range(0, n_gioc):
        mani[i].sort()
    
    carte_tot.sort()

    # Array controllo
    for x in carte_tot:
        control[x-1] += 1
        
    



    # Conta, per ogni mano, quante carte dell'altra sono a differenza +-1 e +-2
    # Inoltre, calcola g(r) esterna
    for i in range(0, n_gioc):
        for j in range(i, n_gioc):
            if i != j:
                for x in mani[i]:
                    for y in mani[j]:
                        delta = abs(x-y)
                        if delta == 1:
                            count_1 += 1
                        if delta == 2:
                            count_2 += 1
                        g_r[delta] += 1
              
                        
    # Conta il salto massimo interno: per ogni mazzo, guarda la distanza massima interna
    # Inoltre, calcola g(r) interna
    max_salto_in = 0
    for i in range(0, n_gioc):
        for x in range(0, n_carte_mano-1):
            delta = mani[i][x+1] - mani[i][x]
            prob_in[delta] += 1
            if delta > max_salto_in:
                max_salto_in = delta     
        sum_max_salto_in += max_salto_in
        sum2_max_in      += max_salto_in**2
        max_salto_in = 0


    # Conta il salto massimo esterno: per ogni carta di un mazzo, guarda la distanza massima con le carte dell'altro mazzo
    max_salto_ex = 0
    for i in range(0, n_gioc):
        for j in range(0, n_gioc):
            if i != j:
                for x in mani[i]:
                    for y in mani[j]:
                        if( y > x ):
                            delta = y-x
                            prob_ex[delta] += 1
                            if( y-x > max_salto_ex ):
                                max_salto_ex = delta
                            break
                sum_max_salto_ex += max_salto_ex
                sum2_max_ex      += max_salto_ex**2


    # Media e deviazione standard della differenza tra le carte di tutti i mazzi
    delta = 0
    for x in range(0, n_carte_tot-1):
        delta = carte_tot[x+1] - carte_tot[x]
        media += delta
        media_2 += delta**2
        

#%% Stampa risultati


control /= N_rip

media /= ( (n_carte_tot-1) * N_rip )
media_2 /= ( (n_carte_tot-1) * N_rip )

dev_std = np.sqrt( media_2 - media**2 )

count_1 /= (N_rip)
count_2 /= (N_rip)

prob_ex /= np.sum(prob_ex)
prob_in /= np.sum(prob_in)

g_r /= N_rip



# Dati
print( "\nMedia control: %.4f (teorica è %.4f)" % (np.mean(control), 0.01 * (n_gioc * n_carte_mano) ) )
print( "Dev_std control: %.4f" % np.std(control) )
print( "Rapporto: %.4e" % ( np.std(control)/np.mean(control) ) )


print( "\nMedia dei salti: %.5f (teorica è %.5f)" % ( media, N_max/( n_gioc * n_carte_mano) ) )
print( "Dev_std salti: %.5f" % dev_std )
print( "Rapporto dev_std-media: %.3f\n" % (dev_std / media) )

print('Numero di coppie a distanza 1 tra i mazzi: '+str(count_1 ) )
print('Numero di coppie a distanza 2 tra i mazzi: '+str(count_2 ) )
print('Totale: '+str(count_1 + count_2) + '\n')


print('Max salto medio interno: %.3f' % (sum_max_salto_in / (n_gioc * N_rip) ) )
print('Dev_std max salto interno: %.3f' % ( np.sqrt( sum2_max_in/(n_gioc * N_rip) - sum_max_salto_in**2 / (n_gioc * N_rip)**2 )) )

print('Max salto medio esterno: %.3f' %(sum_max_salto_ex / (n_gioc * N_rip) ) )
print('Dev_std max salto esterno: %.3f' %( np.sqrt( sum2_max_ex/(n_gioc * N_rip) - sum_max_salto_ex**2 / (n_gioc * N_rip)**2 )) + '\n')


#%% Grafici

delta_n = np.linspace(1, 100, num=100)

fig1 = plt.figure( figsize = (8,6), dpi = 140)                        
plt.plot(delta_n, prob_ex, linewidth = 0, color = 'r', linestyle = "none", marker = '.', markersize = 8, label ='Esterna ') 
plt.plot(delta_n, prob_in, linewidth = 0, color = 'b', linestyle = "none", marker = '.', markersize = 8, label ='Interna ') 

plt.title('Frequenza relativa in funzione del salto\n %i giocatori, %i carte in mano' % (n_gioc, n_carte_mano), fontweight = "bold", fontsize = 18)
plt.xlabel(' $\Delta$n ', fontsize = 14, rotation = 0)
plt.ylabel(' Freq ', fontweight = "bold", fontsize = 14, rotation = 90)
plt.legend( loc = 'upper right', frameon = True, framealpha = 1, fancybox = 0, edgecolor = 'k')
plt.grid(True, color = 'k', alpha = 0.3)
plt.xticks( fontsize = 14, rotation = 0)
plt.yticks( fontsize = 14, rotation = 0)
plt.show()


# fig2 = plt.figure( figsize = (12,6), dpi = 140)                        

# plt.title('\"Probabilità\" $interna$ in funzione del salto', fontweight = "bold", fontsize = 18)
# plt.xlabel(' $\Delta$n ', fontsize = 14, rotation = 0)  
# plt.ylabel(' Prob ', fontweight = "bold", fontsize = 14, rotation = 90)
# plt.legend( loc = 'upper right', frameon = True, framealpha = 1, fancybox = 0, edgecolor = 'k')
# plt.grid(True, color = 'k', alpha = 0.3)
# plt.xticks( fontsize = 14, rotation = 0)
# plt.yticks( fontsize = 14, rotation = 0)


# fig2 = plt.figure( figsize = (8,6), dpi = 140)                        
# plt.plot(delta_n[prob_ex > 0 and prob_in > 0], np.log(prob_ex[prob_ex > 0 and prob_in > 0]), linewidth = 0, color = 'r', linestyle = "none", marker = '.', markersize = 5, label ='Esterna ') 
# plt.plot(delta_n[prob_ex > 0 and prob_in > 0], np.log(prob_in[prob_ex > 0 and prob_in > 0]), linewidth = 0, color = 'b', linestyle = "none", marker = '.', markersize = 5, label ='Interna ') 


# plt.title('Log frequenza relativa in funzione del salto', fontweight = "bold", fontsize = 18)
# plt.xlabel(' $\Delta$n ', fontsize = 14, rotation = 0)    #  
# plt.ylabel(' Log(freq) ', fontweight = "bold", fontsize = 14, rotation = 90)
# plt.legend( loc = 'upper right', frameon = True, framealpha = 1, fancybox = 0, edgecolor = 'k')
# plt.grid(True, color = 'k', alpha = 0.3)
# plt.xticks( fontsize = 14, rotation = 0)
# plt.yticks( fontsize = 14, rotation = 0)

fig3 = plt.figure( figsize = (8,6), dpi = 140)                        
plt.plot(delta_n[delta_n % 1 == 0], g_r[delta_n % 1 == 0], linewidth = 0, color = 'b', linestyle = "none", marker = '.', markersize = 8, label ='g(r)') 

plt.title('g(r)\n %i giocatori, %i carte in mano' % (n_gioc, n_carte_mano), fontweight = "bold", fontsize = 18)
plt.xlabel(' $\Delta$n ', fontsize = 14, rotation = 0)
plt.ylabel(' g(r) ', fontweight = "bold", fontsize = 14, rotation = 90)
plt.legend( loc = 'upper right', frameon = True, framealpha = 1, fancybox = 0, edgecolor = 'k')
plt.grid(True, color = 'k', alpha = 0.3)
plt.xticks( fontsize = 14, rotation = 0)
plt.yticks( fontsize = 14, rotation = 0)
plt.show()



#%% TODO: g(r) tra le carte; array controllo per gestire; 



