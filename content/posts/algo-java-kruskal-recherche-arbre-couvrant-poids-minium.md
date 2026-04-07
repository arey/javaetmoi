---
_edit_last: "1"
_thumbnail_id: "1760"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png
  title: 300px-Minimum_spanning_tree.svg
author: admin
categories:
  - retour-d'expérience
featureImage: /wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png
featureImageAlt: 300px-Minimum_spanning_tree.svg
date: "2017-09-16T10:28:59+00:00"
thumbnail: /wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png
guid: http://javaetmoi.com/?p=1759
parent_post_id: null
post_id: "1759"
post_views_count: "12755"
summary: |-
  [![Arbre couvrant de poids minimum](http://javaetmoi.com/wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png)](http://javaetmoi.com/wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png)

  Faisant partie des [algorithmes de la théorie des graphes](https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Algorithme_de_la_th%C3%A9orie_des_graphes "Catégorie:Algorithme de la théorie des graphes"), l' [algorithme de Kruskal](https://fr.wikipedia.org/wiki/Algorithme_de_Kruskal) permet de rechercher un arbre recouvrant de poids minimum.

  Une application pratique de l'algorithme de Kruskal consiste à relier tous les ordinateurs d'un même réseau local avec une longueur optimale de fibre optique.

  Dans ce billet, vous trouverez une implémentation Java de cet algorithme. Il m'aura permis de résoudre le [problème Fibre Optique donné en finale du concours du Meilleur Dev de France 2017](https://www.isograd.com/FR/solutionconcours.php).
tags:
  - algorithme
  - java
title: Implémentation Java de l'algorithme de Kruskal
url: /2017/09/algo-java-kruskal-recherche-arbre-couvrant-poids-minium/

---
[![Arbre couvrant de poids minimum](/wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png)](/wp-content/uploads/2017/09/300px-Minimum_spanning_tree.svg_.png)

Faisant partie des [algorithmes de la théorie des graphes](https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Algorithme_de_la_th%C3%A9orie_des_graphes "Catégorie:Algorithme de la théorie des graphes"), l'[algorithme de Kruskal](https://fr.wikipedia.org/wiki/Algorithme_de_Kruskal) permet de rechercher un arbre recouvrant de poids minimum.

Une application pratique de l'algorithme de Kruskal consiste à relier tous les ordinateurs d'un même réseau local avec une longueur optimale de fibre optique.

Dans ce billet, vous trouverez une implémentation Java de cet algorithme. Il m'aura permis de résoudre le [problème Fibre Optique donné en finale du concours du Meilleur Dev de France 2017](https://www.isograd.com/FR/solutionconcours.php).

```java
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class KruskalAlgo {

    /**
     * Détermine l'arbre couvrant de poids minimum (ARPM) à partir d'un graphe connexe non-orienté et pondéré.
     * <p>
     * Utilise l'algorithme de Kruskal
     * @see https://fr.wikipedia.org/wiki/Algorithme_de_Kruskal
     *
     * @param vertices graphe constitué d'un ensemble de points dans un plan à 2 dimensions.
     * @return arrêtes de l'arbre couvrant de poids minimum dans ce graphe.
     */
    static List<Edge> compute(List<Vertex> vertices) {

        // Calcule les arêtes et leur poids
        List<Edge> allEdges = new ArrayList<>();
        for (int i = 0; i < vertices.size(); i++) {
            for (int j = i + 1; j < vertices.size(); j++) {
                allEdges.add(new Edge(vertices.get(i), vertices.get(j)));
            }
        }

        // Tri par poids ascendant
        allEdges.sort(Comparator.comparingDouble(Edge::getWeight));

        // Applique l'algo de Kruskal
        List<Edge> graph = new ArrayList<>();
        int i = 0;
        while (graph.size() < vertices.size() - 1) {
            Edge edge = allEdges.get(i++);
            int id1 = edge.u.clusterId;
            int id2 = edge.v.clusterId;
            // L'arête est ajouté au compute si ses 2 sommets n'appartiennent pas au même réseau
            if (id1 != id2) {
                graph.add(edge);
                // Regroupe les sommets des 2 réseaux venant d'être reliés
                for (Vertex v : vertices)
                    if (v.clusterId == id2) {
                        v.clusterId = id1;
                    }
            }
        }

        return graph;
    }

    static class Vertex {

        static int NEX_ID = 0;

        private final int x;

        private final int y;

        private int clusterId = NEX_ID++;

        Vertex(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }

    static class Edge {

        private final Vertex u;

        private final Vertex v;

        private final double weight;

        Edge(Vertex v1, Vertex v2) {
            this.u = v1;
            this.v = v2;
            this.weight = Math.hypot(Math.abs(v1.x - v2.x), Math.abs(v1.y - v2.y));
        }

        double getWeight() {
            return weight;
        }
    }

    public static void main(String args[]) throws FileNotFoundException {
        List<Vertex> vertices = new ArrayList<>();
        vertices.add(new Vertex(0, 2));
        vertices.add(new Vertex(0, 0));
        vertices.add(new Vertex(1, 1));
        vertices.add(new Vertex(2, 1));
        vertices.add(new Vertex(3, 2));
        vertices.add(new Vertex(4, 2));
        vertices.add(new Vertex(3, 0));

        List<Edge> graph = KruskalAlgo.compute(vertices);

        System.out.println(graph.stream().mapToDouble(Edge::getWeight).sum()); // 7.656854249492381
    }
}
```
