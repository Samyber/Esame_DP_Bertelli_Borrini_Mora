# Questa è solo una prova
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
    print(list(G.adj[nodes[4]]))

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

            print(neig)
            print(node_viewed)

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
    neig_com = list()

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

    nx.set_edge_attributes(G, values=-1, name='weight')

    print(len(G.nodes))
    G2 = addEdges(G, k, l, len(G.nodes))

    edges = list(G2.edges)
    edges_weight = list(G2.edges.values())

    print(G2.edges.data())

    for i in range(0, len(edges)):
        if edges_weight[i]['weight'] >= 0:
            print(edges[i])

    G3 = removeEdges(G, G2, k, l)

    """
    if os.path.exists(file_graph):
        # if file exist
        with open(file_graph) as f:
            content = f.readlines()
        # read each line
        content = [x.strip() for x in content]
        for line in content:
            # split name inside each line
            names = line.split(",")
            start_node = names[0]
            if start_node not in G:
                G.add_node(start_node)
            for index in range(1, len(names)):
                node_to_add = names[index]
                if node_to_add not in G:
                    G.add_node(node_to_add)
                G.add_edge(start_node, node_to_add)
                
    nx.set_edge_attributes(G, values=-1, name='weight')

    if not(nx.is_connected(G)):
        print("The graph must be connected!")
        sys.exit(1)

    n = len(G.nodes)

    print("The number of nodes is ", n)

    G2 = addEdges(G,k,l,n)
    """
