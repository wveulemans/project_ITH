#################### (I) Load the package and import data ####################
library(supraHex)

# import datafile
getwd()
setwd("/home/Ward/Ward_stage/b/")
input <- read.table(file="supraHex_input_b.tsv", row.names= 1, header=T, sep="\t", check.names=F)

# extract the mean cellular prevalence of the n mutations X n samples
odd_indexes <- seq(1,ncol(input)-1,2) # only odd indexes (excluding the last column)
data <- input[,odd_indexes]

# check data dimensions and types
dim(data)
str(data)

# get familiar with data (looking at the first few rows of matrix)
head(data)


#################### (II) Train the supra-hexagonal map with input data only ####################
sMap <- sPipeline(data)
visHexMulComp(sMap, title.rotate=10, zlim=c(0,1), colormap="darkgreen-lightgreen-lightpink-darkred")
dev.copy(png,'SupraHex_visHexMulComp.png')
dev.off()

sWriteData(sMap, data, filename="PyClone_cellular_prevalence.supraHex.txt")


#################### (III) Visualise the map ####################
###including built-in indexes, data hits/distributions, distance between map nodes, and codebook matrix

visHexMapping(sMap, mappingType="indexes")
dev.copy(png,'SupraHex_visHexMapping_index.png')
dev.off()
# As you have seen, the smaller hexagons in the supra-hexagonal map are indexed as follows: 
#start from the center, and then expand circularly outwards, and for each circle increase in an anti-clock order.

visHexMapping(sMap, mappingType="hits")
dev.copy(png,'SupraHex_visHexMapping_hits.png')
dev.off()
# As you have seen, the number represents how many input data vectors (mutations) are hitting each hexagon, 
#the size of which is proportional to the number of hits.

visHexMapping(sMap, mappingType="dist")
dev.copy(png,'SupraHex_visHexMapping_dist.png')
dev.off()
# As you have seen, map distance tells how far each hexagon is away from its neighbors, 
#and the size of each hexagon is proportional to this distance.

visHexPattern(sMap, plotType="lines")
dev.copy(png,'SupraHex_visHexPattern_lines.png')
dev.off()
# As you have seen, line plot displays the patterns associated with the codebook matrix. 
# If multple colors are given, the points are also plotted. 
# When the pattern involves both positive and negative values, zero horizental line is also shown.

visHexPattern(sMap, plotType="bars")
dev.copy(png,'SupraHex_visHexPattern_bars.png')
dev.off()
# As you have seen, bar plot displays the patterns associated with the codebook matrix. 
#When the pattern involves both positive and negative values, the zero horizental line is in the middle of the hexagon; 
#otherwise at the top of the hexagon for all negative values, and at the bottom for all positive values.


#################### (IV) Perform partitioning operation on the map  ####################
### to obtain continuous clusters (i.e. mutation meta-clusters) as they are different from mutation clusters in an individual map node

sBase <- sDmatCluster(sMap)
myColor <- c("transparent", "black")
border.color <- myColor[sBase$bases%%2 + 1] ## the hexagon frame according to mete-clusters
visDmatCluster(sMap,sBase, gp=grid::gpar(cex=1.5, font=2, col="blue"), colormap="PapayaWhip-pink-Tomato", area.size=0.95, border.color=border.color)
dev.copy(png,'SupraHex_visDmatCluster.png')
dev.off()

sWriteData(sMap, data, sBase, filename="PyClone_cellular_prevalence.supraHex_base.txt")
# As you have seen, each cluster is filled with the same continuous color, and the cluster index is marked in the seed node. 
#An output txt file PyClone_cellular_prevalence.supraHex_base.txt. 
#This file has 1st column for your input data ID (an integer; otherwise the row names of input data matrix),
#and 2nd column for the corresponding index of best-matching hexagons (i.e. mutation clusters), 
#and 3rd column for the cluster bases (i.e. mutation meta-clusters). You can also force the input data to be output.

sWriteData(sMap, data, sBase, filename="PyClone_cellular_prevalence.supraHex_base_2.txt", keep.data=T)
output <- visDmatHeatmap(sMap, data, sBase, base.separated.arg=list(col="black"), base.legend.location="bottomleft", colormap="darkgreen-lightgreen-lightpink-darkred", KeyValueName="Cellular prevalence", labRow=NA, keep.data=T, srtCol=20)
# As you have seen, heatmap is used to visualise cellular prevalence patterns seen within each meta-cluster/base. 
#Row side bar indicates the mutation meta-clusters/bases. 
#The returned variable "output" (NOT a txt file) has 1st column for your input data ID (an integer; otherwise the row names of input data matrix), 
#and 2nd column for the corresponding index of best-matching hexagons (i.e. mutation clusters),
#and 3rd column for the cluster bases (i.e. mutation meta-clusters). 
#Note: it has rows in the same order as visualised in the heatmap


#################### (V) Reorder the taxonomy-specific components of the map  ####################
### to delineate relationships between taxonomy

sReorder <- sCompReorder(sMap, metric="euclidean")
visCompReorder(sMap, sReorder, title.rotate=10, zlim=c(0,1), colormap="darkgreen-lightgreen-lightpink-darkred")
dev.copy(png,'SupraHex_visCompReorder.png')
dev.off()
# As you have seen, reordered components of trained map is displayed. 
#Each component illustrates a sample-specific map and is placed within a two-dimensional rectangular lattice. 
#Across components/samples, mutations with similar cellular prevalence patterns are mapped onto the same position of the map. 
#Geometric locations of components delineate relationships between components/samples, 
#that is, samples with the similar cellular prevalence profiles are placed closer to each other.


#################### (VI) Build and visualise the bootstrapped tree ####################

tree_bs <- visTreeBootstrap(t(data))
# As you have seen, neighbour-joining tree is constructed based on pairwise euclidean distance matrices between samples. 
#The robustness of tree branching is evaluated using bootstraping. 
#In internal nodes (also color-coded), the number represents the proportion of bootstrapped trees that support the observed internal branching. 
#The higher the number, the more robust the tree branching. 100 means that the internal branching is always observed by resampling characters.
