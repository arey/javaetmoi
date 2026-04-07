---
_edit_last: "1"
_thumbnail_id: "1744"
_wp_old_slug: implementation-java-recursive-de-lalgorithme-dynamique-de-rendu-de-monnaie
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2017/07/300px-Rendu_monnaie.svg_.png
  title: 300px-Rendu_monnaie.svg
author: admin
categories:
  - retour-d'expérience
featureImage: /wp-content/uploads/2017/07/300px-Rendu_monnaie.svg_.png
featureImageAlt: 300px-Rendu_monnaie.svg
date: "2017-07-01T08:07:45+00:00"
guid: http://javaetmoi.com/?p=1742
parent_post_id: null
post_id: "1742"
post_views_count: "16406"
summary: |-
  [![](http://javaetmoi.com/wp-content/uploads/2017/07/300px-Rendu_monnaie.svg_.png)](http://javaetmoi.com/wp-content/uploads/2017/07/300px-Rendu_monnaie.svg_.png) Dans ce billet, j’ai eu l’envie de vous partager mon implémentation Java du très célèbre [problème du rendu de monnaie](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_rendu_de_monnaie) dont voici l’énoncé : étant donné un système de monnaie, comment rendre de façon optimale une somme donnée, c'est-à-dire avec le nombre minimal de pièces et de billets ?
  Par exemple, dans le système monétaire de l’Euro, la manière la plus optimale de rendre 6 euros consiste à rendre un billet de 5 € et une pièce de 1 €, même si d’autres combinaisons existent (ex : 3 x 2 € ou 6 x 1 €).

  Dans le cas d’un système monétaire non canonique, utiliser un [algorithme glouton](https://fr.wikipedia.org/wiki/Algorithme_glouton) ne donnera pas nécessairement un résultat optimal. Il est nécessaire de passer par la méthode algorithmique dite de [programmation dynamique](https://fr.wikipedia.org/wiki/Programmation_dynamique).
tags:
  - algorithme
  - java
title: Implémentation Java de l'algorithme de rendu de monnaie par programmation dynamique
url: /2017/07/algo-rendu-monnaie-programmation-dynamique-java/

---
[![](/wp-content/uploads/2017/07/300px-Rendu_monnaie.svg_.png)](/wp-content/uploads/2017/07/300px-Rendu_monnaie.svg_.png) Dans ce billet, j’ai eu l’envie de vous partager mon implémentation Java du très célèbre [problème du rendu de monnaie](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_rendu_de_monnaie) dont voici l’énoncé : étant donné un système de monnaie, comment rendre de façon optimale une somme donnée, c'est-à-dire avec le nombre minimal de pièces et de billets ?
Par exemple, dans le système monétaire de l’Euro, la manière la plus optimale de rendre 6 euros consiste à rendre un billet de 5 € et une pièce de 1 €, même si d’autres combinaisons existent (ex : 3 x 2 € ou 6 x 1 €).

Dans le cas d’un système monétaire non canonique, utiliser un [algorithme glouton](https://fr.wikipedia.org/wiki/Algorithme_glouton) ne donnera pas nécessairement un résultat optimal. Il est nécessaire de passer par la méthode algorithmique dite de [programmation dynamique](https://fr.wikipedia.org/wiki/Programmation_dynamique).

Voici l’ **implémentation Java récursive** par **programmation dynamique** de **rendu de monnaie**:

```java
package com.javaetmoi.algo;

import java.util.HashMap;
import java.util.Map;

/**
 * Résolution par programmation dynamique et récursivité du calcul de rendu de monnaie.
 */
public class AlgoRenduMonnaie {

    /**
     * Système de monnaie (exemple de l'Euro : [1, 2, 5, 10, 20, 50, 100, 200, 500])
     */
    private long[] pieces;

    /**
     * Cache des résultats intermédiaires.
     * <p>
     * Format : Map<Montant, Map<IndexPiece, RenduMonnaie>>
     */
    private Map<Long, Map<Integer, RenduMonnaie>> resultatsIntermediaires = new HashMap<>();

    /**
     * Constructeur
     *
     * @param pieces système de monnaire utilisé par l'algorithme.
     */
    public AlgoRenduMonnaie(long[] pieces) {
        this.pieces = pieces;
    }

    /**
     * Méthode principale exécutant l'algorithme de rendu de monnaie.
     * <p>
     * Cette méthode peut-être appelée plusieurs fois.
     * Elle réutilisera les résultats des précédents appels.
     *
     * @param montant somme à rendre
     * @return résultat optimal ou <code>null</code> si rendu de monnaie impossible
     */
    public RenduMonnaie calculerRenduMonnaieOptimal(long montant) {
        initResultatsIntermediaires();
        return calculeMonnaie(montant);
    }

    /**
     * Structure de données renvoyée par l'algorithme et également utilisée pour les calculs intermédiaires.
     */
    public class RenduMonnaie {

        private final long montant;
        /**
         * Pour chaque piece du systeme monétaire, conserve le nombre minimal de pieces à rendre pour le montant donné.
         */
        private final int[] nbPiecesARendre;

        /**
         * Constructeur pour un montant à 0.
         */
        RenduMonnaie() {
            this.montant = 0;
            this.nbPiecesARendre = new int[pieces.length];
        }

        RenduMonnaie(long montant, RenduMonnaie precedent, int indexPiece) {
            this.montant = montant;
            int length = precedent.nbPiecesARendre.length;
            nbPiecesARendre = new int[length];
            System.arraycopy(precedent.nbPiecesARendre, 0, nbPiecesARendre, 0, length);
            nbPiecesARendre[indexPiece]++;
        }

        public int[] getNbPiecesARendre() {
            return nbPiecesARendre;
        }

        public long getMontant() {
            return montant;
        }

        public int nbPieces() {
            int nbPieces = 0;
            for (int i = 0; i < pieces.length; i++) {
                nbPieces += nbPiecesARendre[i];
            }
            return nbPieces;
        }

        public String toString() {
            StringBuilder str = new StringBuilder();
            for (int i = 0; i < nbPiecesARendre.length; i++) {
                if (nbPiecesARendre[i] != 0) {
                    str.append(nbPiecesARendre[i]).append("x").append(pieces[i]).append("€ ");
                }
            }
            return str.toString();
        }
    }

    /**
     * Renvoie l'index de la pièce la plus proche d'un montant.
     */
    private Integer getIndexPieceMax(long montant) {
        Integer pieceMax = null;
        for (int i = 0; i < pieces.length; i++) {
            if (pieces[i] <= montant) {
                pieceMax = i;
            }
        }
        return pieceMax;
    }

    /**
     * Initialise le cache avec le 1er résultat : rendre un montant de zéro consiste à ne rendre aucune pièce.
     */
    private void initResultatsIntermediaires() {
        RenduMonnaie renduZero = new RenduMonnaie();
        Map<Integer, RenduMonnaie> zeroMap = new HashMap<>();
        for (int i = 0; i < pieces.length; i++) {
            zeroMap.put(i, renduZero);
        }
        resultatsIntermediaires.put(0L, zeroMap);
    }

    /**
     * Méthode appelée récursivement.
     *
     * @param montant somme à rendre
     * @return résultat optimal ou <code>null</code> si rendu de monnaie impossible
     */
    private RenduMonnaie calculeMonnaie(long montant) {
        Integer indexPieceMax = getIndexPieceMax(montant);
        if (indexPieceMax == null) {
            return null;
        }
        resultatsIntermediaires.putIfAbsent(montant, new HashMap<>());
        RenduMonnaie meilleurRendu = null;
        int meilleurePiece = -1;
        for (int indexPiece = indexPieceMax; indexPiece >= 0; indexPiece--) {
            long nouveauMontant = montant - pieces[indexPiece];
            resultatsIntermediaires.putIfAbsent(nouveauMontant, new HashMap<>());
            RenduMonnaie renduOptimal = resultatsIntermediaires.get(nouveauMontant).get(indexPiece);
            if (renduOptimal == null) {
                renduOptimal = calculeMonnaie(nouveauMontant);
            }
            if (renduOptimal != null) {
                if ((meilleurRendu == null) || (meilleurRendu.nbPieces() > renduOptimal.nbPieces())) {
                    meilleurRendu = renduOptimal;
                    meilleurePiece = indexPiece;
                }
            }
        }
        if (meilleurRendu != null) {
            meilleurRendu = new RenduMonnaie(montant, meilleurRendu, meilleurePiece);
            resultatsIntermediaires.get(montant).put(meilleurePiece, meilleurRendu);
        }
        return meilleurRendu;
    }
}
```

Le test unitaire JUnit associé valide différents cas de tests et documente son utilisation :

```java
package com.javaetmoi.algo;

import org.junit.Ignore;
import org.junit.Test;

import static org.junit.Assert.*;

public class MonnaieTest {

    @Test
    public void monnaie_2_5_10_montant_1() {
        calculerMonnaie(new long[]{2, 5, 10}, 1L, null);
    }

    @Test
    public void monnaie_2_5_10_montant_5() {
        calculerMonnaie(new long[]{2, 5, 10}, 5L, 1);
    }

    @Test
    public void monnaie_2_5_10_montant_6() {
        calculerMonnaie(new long[]{2, 5, 10}, 6L, 3);
    }

    @Test
    public void monnaie_2_5_10_montant_10() {
        calculerMonnaie(new long[]{2, 5, 10}, 10L, 1);
    }

    @Test
    public void monnaie_2_5_10_montant_37() {
        calculerMonnaie(new long[]{2, 5, 10}, 37L, 5);
    }

    @Test
    public void monnaie_1_3_4_montant_6() {
        calculerMonnaie(new long[]{1, 3, 4}, 6L, 2);
    }

    @Test
    @Ignore
    public void monnaie_1_2_5_10_20_50_100_200_500_montant_1989() {
        calculerMonnaie(new long[]{1, 2, 5, 10, 20, 50, 100, 200, 500}, 1989L, 11);
    }

    private void calculerMonnaie(long[] pieces, long montant, Integer nbPiecesAttendues) {
        AlgoRenduMonnaie algo = new AlgoRenduMonnaie(pieces);
        AlgoRenduMonnaie.RenduMonnaie rendu = algo.calculerRenduMonnaieOptimal(montant);

        if (nbPiecesAttendues == null) {
            assertNull(rendu);
            return;
        }
        assertNotNull(rendu);
        for (int i = 0; i < pieces.length; i++) {
            if (rendu.getNbPiecesARendre()[i] != 0) {
                System.out.println("Nombre de pièces de " + pieces[i] + " € : " + rendu.getNbPiecesARendre()[i]);
            }
        }

        assertEquals(montant, rendu.getMontant());
        assertEquals(nbPiecesAttendues.intValue(), rendu.nbPieces());
    }

}
```

Plus le système monétaire est dense et plus le montant à rendre est élevé, plus il y’a de chance que la récursivité provoque des débordements de pile d’appel (je vous invite à tester le test annoté avec @Ignore). Passer par une impléemntation itérative permettrait de résoudre ce problème.

Pour complexifier le problème, on pourrait tenir compte du nombre de pièces disponibles dans la caisse et adapter le rendu de monnaie en conséquences. La mise en cache des résultats intermédiaires ne serait alors plus possible.

Références :

- [Problème de rendu de monnaie](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_rendu_de_monnaie), Wikipedia
- Rendu de monnaie, bases de programmation dynamique, Jill-Jênn Vie & Clémence
- [Corrigé du contrôle des connaissances Algorithmique & Programmation (INF431)](http://www.enseignement.polytechnique.fr/informatique/INF431/X12-2013-2014/Annales/X11-2012-2013/cc2-corrige.pdf)
