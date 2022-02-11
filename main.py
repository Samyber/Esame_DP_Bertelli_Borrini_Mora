# Questa è solo una prova
import itertools
import os
import sys

import networkx as nx

def addEdges(G, k, l, n):
    G2 = G.copy()
    flag = 1
    dist = 1

    node_viewed = list()
    neig = list()
    #neig2 = list()

    nodes = list(G.nodes)
    #print(list(G.adj[nodes[4]]))

    if l == 1:

        for i in range(0, n):
            # node_viewed[i] = list(G.adj[nodes[i]])
            node_viewed.append(list(G.adj[nodes[i]]))
            node_viewed[i].append(nodes[i])
            # neig[i] = list(G.adj[nodes[i]])
            # neig2[i] = list()
            neig.append(list(G.adj[nodes[i]]))
            # neig2.append(list())

        while flag == 1 and dist < n-1:
            flag = 0

            for i in range(0, n):
                actual_neig2 = list()
                actual_neig = neig[i]
                actual_node_viewed = node_viewed[i]
                for j in range(0, len(actual_neig)): # Scorro vicini dei nodi presenti dentro actual_neig[i]
                    vertex = actual_neig[j]
                    tmp = list(G.adj[vertex]) # G invece di G2
                    for z in range(0, len(tmp)):
                        if not(tmp[z] in actual_node_viewed): # Controllo che nodo non sia stato già visitato
                            actual_neig2.append(tmp[z])
                            actual_node_viewed.append(tmp[z])
                actual_node_viewed = list(dict.fromkeys(actual_node_viewed)) # Rimuovo eventuali ripetizioni.
                actual_neig2 = list(dict.fromkeys(actual_neig2)) # Rimuovo eventuali ripetizioni.
                #neig2[i] = actual_neig2
                neig[i] = actual_neig2
                node_viewed[i] = actual_node_viewed

            #print(neig)
            #print(node_viewed)

            # FINO QUI VA

            for i in range(0, n): # Scorre tutti i nodi del grafo
                node_i = nodes[i]
                actual_neig = neig[i]
                if len(G2.adj[node_i]) < k:
                    for j in range(0, len(actual_neig)):
                        node_j = actual_neig[j]
                        if G2.has_edge(node_i, node_j):
                            if G2[node_i][node_j]['weight'] > 0:
                                G2[node_i][node_j]['weight'] -= 1
                        else:
                            G2.add_edge(node_i, node_j)
                            G2[node_i][node_j]['weight'] = n - 1
                    flag = 1
            dist += 1
    else:
        # Caso l > 1

        Ng = list() # Lista contenente nella cella i i vicini del nodo i
        for i in range(0, n):
            Ng.append(list(G.adj[nodes[i]]))

        #controlli = list()
        for i in range(0, n):
            list1 = list()
            list1.append(nodes[i])
            node_viewed.append(list1)
            list2 = list()
            list2.append(nodes[i])
            neig.append(list2)
            #controlli.append(True)

        while flag == 1 and dist < n:
            flag = 0

            # TODO Cambia i nomi? Usa V'?

            for i in range(0, n):
                actual_neig2 = list()
                actual_neig = neig[i]
                actual_node_viewed = node_viewed[i]
                for j in range(0, len(actual_neig)):
                    vertex = actual_neig[j]
                    tmp = list(G.adj[vertex]) # G invece di G2
                    for z in range(0, len(tmp)):
                        if not(tmp[z] in actual_node_viewed):
                            actual_neig2.append(tmp[z])
                            actual_node_viewed.append(tmp[z])
                actual_node_viewed = list(dict.fromkeys(actual_node_viewed))
                actual_neig2 = list(dict.fromkeys(actual_neig2))
                #neig2[i] = actual_neig2
                neig[i] = actual_neig2
                node_viewed[i] = actual_node_viewed

            for i in range(0, n):
                Ng_i = Ng[i]
                v = neig[i]
                if check_privacy(G2, Ng_i, k):
                    #controllo = True  # variabile che serve per bloccare la creazione di nuovi archi se viene soddisfatta il privacy check. Continuo a diminuire il costo di quelli già esistenti
                    for j in range(0, len(v)):
                        node_1 = v[j]
                        for z in range(0, len(Ng_i)):
                            node_2 = Ng_i[z]
                            if node_1 != node_2:
                                if G2.has_edge(node_1, node_2):
                                    if G2[node_1][node_2]['weight'] > 0:
                                        G2[node_1][node_2]['weight'] -= 1
                                else:
                                    #if controlli[i]:
                                    G2.add_edge(node_1, node_2)
                                    G2[node_1][node_2]['weight'] = n - 1
                        if not (check_privacy(G2, Ng_i, k)):
                            break
                            #controlli[i] = False
                            #print(controlli)
                    flag = 1
            dist += 1

    return G2

def check_privacy(G2, Ng_i, k):
    neig_com = list() # Lista di liste dei vicini di Ng_i (vicini di vi)

    for i in range(0, len(Ng_i)):
        neig_com.append(list(G2.adj[Ng_i[i]]))

    common = dict()
    for i in range(0, len(neig_com)):
        neig = neig_com[i]
        for j in range(0, len(neig)):
            node = neig[j]
            if node in common:
                common[node] += 1
            else:
                common[node] = 1

    count = 0
    occurency = list(common.values())
    for i in range(0, len(occurency)):
        if occurency[i] == len(Ng_i):
            count += 1

    if count >= k:
        return False
    else:
        return True

def removeEdges(G, G2, k, l):
    G3 = G2.copy()

    edges = sorted(G2.edges(data=True), key=lambda t: t[2].get('weight', 1))
    edges = list(edges)
    edges.reverse()

    #print("------------------>",list(G3.edges.data()))

    # TODO Ottimizza?
    edges = [elem for elem in edges if elem[2]['weight'] > 0]

    #print("------------------>", list(edges))

    for i in range(0, len(edges)):
        node_1 = edges[i][0]
        node_2 = edges[i][1]

        if l == 1:
            if len(G3.adj[node_1]) > k and len(G3.adj[node_2]) > k:
                G3.remove_edge(node_1, node_2)
        else:
            cost = edges[i][2]['weight']
            G3.remove_edge(node_1, node_2)
            if isSafe(G, G2, G3, node_1, node_2, k, l):
                G2.remove_edge(node_1, node_2)
            else:
                G3.add_edge(node_1, node_2)
                G3[node_1][node_2]['weight'] = cost

    return G3

def isSafe(G, G2, G3, node_1, node_2, k, l):
    Ng_i = list(G.adj[node_1])
    Ng_j = list(G.adj[node_2])
    Ng2_vj = list(G2.adj[node_2])
    Ng2_vi = list(G2.adj[node_1])

    for i in range(0, len(Ng_i)):
        Ng_ni = list(G.adj[Ng_i[i]])
        V_i = list()
        for j in range(0, len(Ng_ni)):
            node = Ng_ni[j]
            if node in Ng2_vj:
                V_i.append(node)

        minim = min(l, len(V_i))

        if check_edge(V_i, minim, k, node_1, G3):
            return False

    for i in range(0, len(Ng_j)):
        Ng_nj = list(G.adj[Ng_j[i]])
        V_i = list()
        for j in range(0, len(Ng_nj)):
            node = Ng_nj[j]
            if node in Ng2_vi:
                V_i.append(node)

        minim = min(l, len(V_i))

        if check_edge(V_i, minim, k, node_2, G3):
            return False

    return True


def check_edge(V_i, minim, k, node_1, G3):
    #neig = list() # Lista dei vicini dei nodi in V_i
    #for i in range(0, len(V_i)):
    #    neig.append(G3.adj[V_i[i]])

    # Prelevo solo i subset che contengono vi di minim elementi
    #list_subset = list()
    for subset in itertools.combinations(V_i, minim):
        if node_1 in subset:
            #list_subset.append(subset)
            neig = list()
            for j in range(0, len(subset)):
                neig.append(list(G3.adj[subset[j]]))

            common = dict()
            for z in range(0, len(neig)):
                actual_neig = neig[z]
                for h in range(0, len(actual_neig)):
                    node = actual_neig[h]
                    if node in common:
                        common[node] += 1
                    else:
                        common[node] = 1

            count = 0
            occurency = list(common.values())
            for i in range(0, len(occurency)):
                if occurency[i] == len(subset):
                    count += 1

            # TODO Cambia len(subset) con minim?

            if count < k:
                return True

    """
    for i in range(0, len(list_subset)):
        subset = list_subset[i]
        neig = list()
        for j in range(0, len(subset)):
            neig.append(list(G3.adj[subset[j]]))

        common = dict()
        for z in range(0, len(neig)):
            actual_neig = neig[z]
            for h in range(0, len(actual_neig)):
                node = actual_neig[h]
                if node in common:
                    common[node] += 1
                else:
                    common[node] = 1

        count = 0
        occurency = list(common.values())
        for i in range(0, len(occurency)):
            if occurency[i] == len(subset):
                count += 1

        # TODO Cambia len(subset) con minim?

        if count < k:
            return True
    """
    return False

if __name__ == '__main__':

        if len(sys.argv) < 4:
            print("The number of parameter passed is not correct!")
            sys.exit(1)

        file_graph = sys.argv[1]
        k = sys.argv[2]
        l = sys.argv[3]

        if k.isdigit() and l.isdigit():
            k = int(k)
            l = int(l)
        else:
            print("k and l must be integer values!")
            sys.exit(1)

        print("k=", k, " l=", l)

        """

        G = nx.Graph()

        G.add_node(1)
        G.add_node(2)
        G.add_node(3)
        G.add_node(4)
        G.add_node(5)
        G.add_edge(1, 2)
        G.add_edge(1, 3)
        G.add_edge(2, 4)
        G.add_edge(3, 5)

        #nx.set_edge_attributes(G, values=-1, name='weight')
  
        print(len(G.nodes))
        G2 = addEdges(G, k, l, len(G.nodes))
    
        edges = list(G2.edges)
        edges_weight = list(G2.edges.values())
    
        print(G2.edges.data())
    
    
    
        G3 = removeEdges(G, G2, k, l)
    
        for i in range(0, len(edges)):
            if edges_weight[i]['weight'] >= 0:
                print(edges[i])
    
        """

        G = nx.Graph()
    
        if os.path.exists(file_graph):
            # if file exist
            with open(file_graph) as f:
                content = f.readlines()
            # read each line
            content = [x.strip() for x in content]
            for line in content:
                # split name inside each line
                # names = line.split(",") # Split con ,
                names = line.split(" ") # Split con spazio
                start_node = names[0]
                if start_node not in G:
                    G.add_node(start_node)
                for index in range(1, len(names)):
                    node_to_add = names[index]
                    if node_to_add not in G:
                        G.add_node(node_to_add)
                    G.add_edge(start_node, node_to_add)
    


        nx.set_edge_attributes(G, values=-1, name='weight') # Assegno peso -1 a tutti gli archidel grafo

        if not(nx.is_connected(G)):
            print("The graph must be connected!")
            sys.exit(1)

        n = len(G.nodes)

        print("The number of nodes is ", n)

        #prova = G.adj[1]
        #print(G.edges)

        G2 = addEdges(G, k, l, n)

        G3 = removeEdges(G, G2, k, l)

        # Sostituisco nomi nodi con id

        nodes = list(G3.nodes)
        new_name_mapping = dict()
        for i in range(0, len(nodes)):
            new_name_mapping[nodes[i]] = i + 1

        G3 = nx.relabel_nodes(G3, new_name_mapping)

        edges = list(G3.edges)
        edges_weight = list(G3.edges.values())

        #print(G2.edges.data())

        #print(edges_weight)

        count = 0
        for i in range(0, len(edges)):
            if edges_weight[i]['weight'] >= 0:
                print(edges[i])
                count += 1
        print(count)



