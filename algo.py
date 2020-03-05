from itertools import combinations_with_replacement
from scipy.optimize import linprog
import numpy as np

#ПЕРЕД ЗАПУСКОМ ИЛИ ПРОСМОТРОМ ОБЯЗАТЕЛЬНО ПОСМОТРЕТЬ файл input.txt
    
if __name__ == "__main__":
    
    #Считываем данные также как это указано в пояснени
    file = open('input.txt', 'r')
    outfile = open('output.txt', 'w')

    s = int(file.readline())

    tcount, ocount = [int(x) for x in file.readline().split()]

    techs = [int(t) for t in file.readline().split()]
    obs = [int(o) for o in file.readline().split()]

    maxtimes = [[int(h) for h in file.readline().split()] for r in range(tcount)]
    cvelos = [[int(v) for v in file.readline().split()] for r in range(tcount)]
    prices = [[int(p) for p in file.readline().split()] for r in range(tcount)]

    #Массив комбинаций оборудования и техники, которые доступны (Имеют в матрице ненулевое значение)
    t_combs = []
    
    for i in range(tcount):
        for j in range(ocount):
            if maxtimes[i][j] != 0:
                t_combs.append((i, j))
    
    #Высчитывание K из формулы для размешений с повторениями (A из N по K)
    n = len(t_combs)

    #Высчитывание K из формулы для размешений с повторениями (A из N по K)
    k = 0
    actt = 0
    acto = 0

    for i in range(tcount):
        p = 0
        for j in range(ocount):
            p = p + maxtimes[i][j]
        if p > 0:
            actt = actt + techs[i]

    for j in range(ocount):
        p = 0
        for i in range(tcount):
            p = p + maxtimes[i][j]
        if p > 0:
            acto = acto + obs[j]
            
    k = min(actt, acto)
    
    #Перебираем все возможные сочетания с повторениями и для каждой комбинации высчитываем
    #по симплекс методу нужные нам значения стоимости и времени
    res = None
    res_combs = None

    for i in range(k+1, 1, -1):
        w_combs = combinations_with_replacement(t_combs, i)

        #Подготовка параметров для для симплекс-алгоритма
        for j in w_combs:
            t = techs
            o = obs
            ps = []
            cs = []
            bs = [-1*s, ]
            flag = True
            
            gg = []
            for k in range(i):
                fr = j[k][0]
                sc = j[k][1]
                
                if t[fr] == 0 or o[sc] == 0:
                    flag = False
                    break
                    
                ps.append(prices[fr][sc])
                gg.append(-1*cvelos[fr][sc])
                bs.append(maxtimes[fr][sc])

            cs.append(gg)
            
            for k in range(len(ps)):
                cs.append([0]*len(ps))
                cs[k+1][k] = 1

            A = np.array(cs)
            b = np.array(bs)
            c = np.array(ps)

            if flag == False:
                continue
            else:
                #Здесь мы сравниваем между собой предыдущую комбинацию с мин. стоимости с текущей
                #и принимаем новую, если она дает меньший результат.

                ans = linprog(c, A_ub=A, b_ub=b,bounds=(0, None))

                if res == None:
                    res = ans
                else:
                    if ans.fun == res.fun:
                        if sum(ans.x) < sum(res.x):
                            res = ans
                            res_combs = j
                    elif ans.fun < res.fun:
                        res = ans
                        res_combs = j

    print("Pmin = ", res.fun, " rub")
    print("T = ", sum(res.x), " hours")
    print("Working units: ", res_combs)

