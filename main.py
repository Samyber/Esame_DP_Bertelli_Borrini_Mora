import itertools
import os
import sys

import networkx as nx

def addEdges(G, k, l, n):
    """
    Funzione che ha il compito di aggiungere gli archi al grafo per anonimizzarlo.

    :param G: Grafo da anonimizzare
    :param k: Privacy parameter
    :param l: Privacy parameter
    :param n: Numero di nodi del grafo
    :return: Grafo aumentato
    """
    G2 = G.copy()
    flag = 1
    dist = 1

    # Lista di liste che tiene traccia dei nodi già visitati partendo da ogni nodo di partenza
    node_viewed = list()
    # Lista di liste che contiene i nodi ad una certa distanza dai vari nodi di partenza
    neig = list()

    nodes = list(G.nodes)

    if l == 1:
        # Inizializzazione di node_viewed e neig
        for i in range(0, n):
            node_viewed.append(list(G.adj[nodes[i]]))
            node_viewed[i].append(nodes[i])
            neig.append(list(G.adj[nodes[i]]))

        while flag == 1 and dist < n-1:
            flag = 0

            # Aggiornamento di neig e node_viewd
            for i in range(0, n):
                actual_neig2 = list()
                actual_neig = neig[i]
                actual_node_viewed = node_viewed[i]
                for j in range(0, len(actual_neig)): # Scorro vicini dei nodi presenti dentro actual_neig[i]
                    vertex = actual_neig[j]
                    tmp = list(G.adj[vertex])
                    for z in range(0, len(tmp)):
                        if not(tmp[z] in actual_node_viewed): # Controllo che nodo non sia stato già visitato
                            actual_neig2.append(tmp[z])
                            actual_node_viewed.append(tmp[z])
                actual_node_viewed = list(dict.fromkeys(actual_node_viewed)) # Rimuovo eventuali ripetizioni.
                actual_neig2 = list(dict.fromkeys(actual_neig2)) # Rimuovo eventuali ripetizioni.
                neig[i] = actual_neig2
                node_viewed[i] = actual_node_viewed

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

        # Inizializzazione di node_viewed e neig
        for i in range(0, n):
            list1 = list()
            list1.append(nodes[i])
            node_viewed.append(list1)
            list2 = list()
            list2.append(nodes[i])
            neig.append(list2)

        while flag == 1 and dist < n:
            flag = 0
            # Aggiornamento di neig e node_viewd
            for i in range(0, n):
                actual_neig2 = list()
                actual_neig = neig[i]
                actual_node_viewed = node_viewed[i]
                for j in range(0, len(actual_neig)):
                    vertex = actual_neig[j]
                    tmp = list(G.adj[vertex])
                    for z in range(0, len(tmp)):
                        if not(tmp[z] in actual_node_viewed):
                            actual_neig2.append(tmp[z])
                            actual_node_viewed.append(tmp[z])
                actual_node_viewed = list(dict.fromkeys(actual_node_viewed))
                actual_neig2 = list(dict.fromkeys(actual_neig2))
                neig[i] = actual_neig2
                node_viewed[i] = actual_node_viewed

            for i in range(0, n):
                Ng_i = Ng[i]
                v = neig[i] # lista dei nodi a distanza dist dal nodo i
                if check_privacy(G2, Ng_i, k):
                    for j in range(0, len(v)):
                        node_1 = v[j]
                        for z in range(0, len(Ng_i)):
                            node_2 = Ng_i[z]
                            if node_1 != node_2:
                                if G2.has_edge(node_1, node_2):
                                    if G2[node_1][node_2]['weight'] > 0:
                                        G2[node_1][node_2]['weight'] -= 1
                                else:
                                    G2.add_edge(node_1, node_2)
                                    G2[node_1][node_2]['weight'] = n - 1
                        if not (check_privacy(G2, Ng_i, k)):
                            break
                    flag = 1
            dist += 1
    return G2

def check_privacy(G2, Ng_i, k):
    """
    Funzione che controlla se tutti i vicini di vi in G condividono meno di k vicini comuni in G2

    :param G2: Grafo aumentato
    :param Ng_i: Nodi vicini al nodi i
    :param k: Privacy parameter
    :return: True se il controllo va a buon fine, False altrimenti.
    """
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
    """
    Funzione che ha il compito di rimuovere gli archi aggiunti dalla funzione addEdges che non sono necessari per
    rendere il grafo finale (k, l)-anonimo

    :param G: Grafo da anonimizzare
    :param G2: Grafo aumentato
    :param k: Privacy parameter
    :param l: Privacy parameter
    :return: Grafo (k, l)-anonimo
    """
    G3 = G2.copy()
    # Ordinamento degli archi in base al loro costo
    edges = sorted(G2.edges(data=True), key=lambda t: t[2].get('weight', 1))
    edges = list(edges)
    edges.reverse()
    # Consideriamo solo gli archi con costo positivo (archi aggiunti dalla funzione addEdges)
    edges = [elem for elem in edges if elem[2]['weight'] > 0]

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
    """
    Funzione che controlla se cancellando l'arco tra nodo_1 e nodo_2 il grafo finale rimane (k, l)-anonimo.

    :param G: Grafo da anonimizzare
    :param G2: Grafo aumentato
    :param G3: Grafo finale
    :param node_1: Nodo ad un estremo dell'arco
    :param node_2: Nodo ad un estremo dell'arco
    :param k: Privacy parameter
    :param l: Privacy parameter
    :return: True se è sicuro cancellare l'arco, False altrimenti
    """
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
        V_j = list()
        for j in range(0, len(Ng_nj)):
            node = Ng_nj[j]
            if node in Ng2_vi:
                V_j.append(node)

        minim = min(l, len(V_j))

        if check_edge(V_j, minim, k, node_2, G3):
            return False

    return True


def check_edge(V_i, minim, k, node_1, G3):
    """
    Funzione che controlla se esiste un subset di V_i al massimo minim elementi che contenga node_1 con meno di k
    vicini comuni

    :param V_i: Insieme che contiene i nodi vicini a vni in G che sono anche vicini di vj in G2
    :param minim: Grandezza massima del subset che si può considerare
    :param k: Privacy parameter
    :param node_1: Nodo che deve ssere presente nei subset che si considerano
    :param G3: Grafo finale
    :return: True se la condicione è verificata, False altrimenti
    """
    # Modifica apportata per provare a correggere l'algoritmo
    if len(V_i) == 1:
        return True

    # Prelevo solo i subset che contengono vi di minim elementi
    for subset in itertools.combinations(V_i, minim):
        if node_1 in subset:
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
            if count < k:
                return True
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

        G = nx.Graph()
        if os.path.exists(file_graph):
            with open(file_graph) as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            for line in content:
                names = line.split(" ")
                start_node = names[0]
                if start_node not in G:
                    G.add_node(start_node)
                for index in range(1, len(names)):
                    node_to_add = names[index]
                    if node_to_add not in G:
                        G.add_node(node_to_add)
                    G.add_edge(start_node, node_to_add)
        else:
            print("File path wrong!")
            sys.exit(1)

        nx.set_edge_attributes(G, values=-1, name='weight')
        if not(nx.is_connected(G)):
            print("The graph must be connected!")
            sys.exit(1)

        n = len(G.nodes)

        print("The number of nodes is ", n)

        G2 = addEdges(G, k, l, n)

        G3 = removeEdges(G, G2, k, l)

        # Sostituisco nomi nodi con id
        """
        nodes = list(G3.nodes)
        new_name_mapping = dict()
        for i in range(0, len(nodes)):
            new_name_mapping[nodes[i]] = i + 1

        G3 = nx.relabel_nodes(G3, new_name_mapping)
        """
        edges = list(G3.edges)
        edges_weight = list(G3.edges.values())

        count = 0
        # Stampa degli archi aggiunti dall'algoritmo
        for i in range(0, len(edges)):
            if edges_weight[i]['weight'] >= 0:
                print(edges[i])
                count += 1
        print(count)

        print("Delta APL = ", abs(nx.average_shortest_path_length(G3)-nx.average_shortest_path_length(G)))
        print("Delta ACC = ", abs(nx.average_clustering(G3) - nx.average_clustering(G)))