
Provided files:
--------------

    1) supports.tsv: quantile ranking (support), cosine distance, z-scored cosine distance and enrichment scores for each edge in each metapath-dataset.
    2) metapath_counts.tsv: Number of edge counts supported by each metapath-dataset at different support score cutoffs.
    3) edge_recapitulation.tsv: Recapitulation score (AUROCs) for each metapath assessed as potential predictor of the given network.
    4) XXX_neighbours_recapitulation.tsv: Recapitulation score (AUROCs) for each metapath assessed as potential predictor of similar interactors in the network.
    5) canvas.png: Figure summarizing all the results. A legend of the figure can be found below.
    6) edges.tsv.gz: List of edges used by the BQsupports (after removing duplications).
    7) README.txt: This README file.
    8) WARNINGS.txt (optional): Warnings that happened during the processing of the network (e.g. those steps that were skipped due to lack of data, if any).

    *Further details can be found at https://bioteque.irbbarcelona.org/about


Canvas Legend
--------------

    · · ·   · · · · · · ·
    · A ·   ·  C  ·  e  ·
· · · · · · · · · ·     ·
·           ·  D  ·  E  ·
·     B     · · · · · · ·
·           ·  F  ·  G  ·
· · · · · · · · · · · · ·

A) Color Legend of the figure showing the support score (quantile ranking).
   The lower (redder) the quantile ranking the higher the support score. Not covered edges are shown in white.

B) Heatmap showing the support score for all the given associations (y-axis) by the top 10 most supportive metapaths (x-axis).
   The last row shows the best quantile of the edge considering all the tested metapath.

C) The biggest pie chart (left) shows the number of associations supported at different quantile ranking cutoffs (provided in the color legend).
   The lower pie chart (right) shows the number of different entities (nodes) covered in this analysis.

D) Number of edges supported by at least one metapath across different support (quantile) scores.
   The 'expected support' line indicates the support achieved by the permuted networks, where network edges have been randomly shuffled N times.

E) Metapaths ranked according to their potential to be used as features for predicting new dataset-specific interactions.
   The analysis is run trying to recapitulate:
   --> (i) the provided network (black).
   --> (ii) pairs of nodes sharing a similar interaction profile (colored by entity). See legend (e).

F) Most supported input edges. The labels in the y-axis shows the index position (starting from 1) in the edges.tsv.gz file.

G) Metapath descriptors that most support the dataset.
        