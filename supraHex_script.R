#! /opt/software/R/3.3.2/bin/R

args = commandArgs(trailingOnly=TRUE)

#################### (I) Load the package and import data ####################

if("supraHex" %in% rownames(installed.packages()) == FALSE) {
	source("http://bioconductor.org/biocLite.R")
	biocLite("supraHex")
	biocLite("hexbin")
	biocLite("methods")
}

library(supraHex)

# import datafile
input <- read.table(file=args[1], row.names= 1, header=T, sep="\t", check.names=F)

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

visHexMulComp(sMap, title.rotate=10, zlim=c(0,1), colormap="jet")#colormap =  “rainbow”, “jet”, “bwr”, “gbr”, “wyr”, “br”, “yr”
system('mv Rplots.pdf SupraHex_visHexMulComp.pdf')
dev.off()

sWriteData(sMap, data, filename="PyClone_cellular_prevalence.supraHex.txt")

#################### (III) Visualise the map ####################
###including built-in indexes, data hits/distributions, distance between map nodes, and codebook matrix
visHexMapping(sMap, mappingType="indexes")
system('mv Rplots.pdf SupraHex_visHexMapping_index.pdf')
dev.off()
# As you have seen, the smaller hexagons in the supra-hexagonal map are indexed as follows: 
#start from the center, and then expand circularly outwards, and for each circle increase in an anti-clock order.

visHexMapping(sMap, mappingType="hits")
system('mv Rplots.pdf SupraHex_visHexMapping_hits.pdf')
dev.off()
# As you have seen, the number represents how many input data vectors (mutations) are hitting each hexagon, 
#the size of which is proportional to the number of hits.

visHexMapping(sMap, mappingType="dist")
system('mv Rplots.pdf SupraHex_visHexMapping_dist.pdf')
dev.off()
# As you have seen, map distance tells how far each hexagon is away from its neighbors, 
#and the size of each hexagon is proportional to this distance.

visHexPattern(sMap, plotType="lines")
system('mv Rplots.pdf SupraHex_visHexPattern_lines.pdf')
dev.off()
# As you have seen, line plot displays the patterns associated with the codebook matrix. 
# If multple colors are given, the points are also plotted. 
# When the pattern involves both positive and negative values, zero horizental line is also shown.

visHexPattern(sMap, plotType="bars")
system('mv Rplots.pdf SupraHex_visHexPattern_bars.pdf')
dev.off()
# As you have seen, bar plot displays the patterns associated with the codebook matrix. 
#When the pattern involves both positive and negative values, the zero horizental line is in the middle of the hexagon; 
#otherwise at the top of the hexagon for all negative values, and at the bottom for all positive values.


#################### (IV) Perform partitioning operation on the map  ####################
### to obtain continuous clusters (i.e. mutation meta-clusters) as they are different from mutation clusters in an individual map node

sBase <- sDmatCluster(sMap)
myColor <- c("transparent", "black")
border.color <- myColor[sBase$bases%%2 + 1] ## the hexagon frame according to mete-clusters
visDmatCluster(sMap,sBase, gp=grid::gpar(cex=1.5, font=2, col="blue"), colormap="jet", area.size=0.95, border.color=border.color) #colormap =  “rainbow”, “jet”, “bwr”, “gbr”, “wyr”, “br”, “yr”

system('mv Rplots.pdf SupraHex_visDmatCluster.pdf')
dev.off()

sWriteData(sMap, data, sBase, filename="PyClone_cellular_prevalence.supraHex_base.txt")
# As you have seen, each cluster is filled with the same continuous color, and the cluster index is marked in the seed node. 
#An output txt file PyClone_cellular_prevalence.supraHex_base.txt. 
#This file has 1st column for your input data ID (an integer; otherwise the row names of input data matrix),
#and 2nd column for the corresponding index of best-matching hexagons (i.e. mutation clusters), 
#and 3rd column for the cluster bases (i.e. mutation meta-clusters). You can also force the input data to be output.

sWriteData(sMap, data, sBase, filename="PyClone_cellular_prevalence.supraHex_base_2.txt", keep.data=T)
output <- visDmatHeatmap(sMap, data, sBase, base.separated.arg=list(col="black"), base.legend.location="bottomleft", colormap="jet", KeyValueName="Cellular prevalence", labRow=NA, keep.data=T, srtCol=20)#colormap =  “rainbow”, “jet”, “bwr”, “gbr”, “wyr”, “br”, “yr”

system('mv Rplots.pdf SupraHex_visDmatHeatmap.pdf')
dev.off()
# As you have seen, heatmap is used to visualise cellular prevalence patterns seen within each meta-cluster/base. 
#Row side bar indicates the mutation meta-clusters/bases. 
#The returned variable "output" (NOT a txt file) has 1st column for your input data ID (an integer; otherwise the row names of input data matrix), 
#and 2nd column for the corresponding index of best-matching hexagons (i.e. mutation clusters),
#and 3rd column for the cluster bases (i.e. mutation meta-clusters). 
#Note: it has rows in the same order as visualised in the heatmap


#################### (V) Reorder the taxonomy-specific components of the map  ####################
### to delineate relationships between taxonomy

sReorder <- sCompReorder(sMap, metric="euclidean")
visCompReorder(sMap, sReorder, title.rotate=10, zlim=c(0,1), colormap="jet") #colormap =  “rainbow”, “jet”, “bwr”, “gbr”, “wyr”, “br”, “yr”

system('mv Rplots.pdf SupraHex_visCompReorder.pdf')
dev.off()
# As you have seen, reordered components of trained map is displayed. 
#Each component illustrates a sample-specific map and is placed within a two-dimensional rectangular lattice. 
#Across components/samples, mutations with similar cellular prevalence patterns are mapped onto the same position of the map. 
#Geometric locations of components delineate relationships between components/samples, 
#that is, samples with the similar cellular prevalence profiles are placed closer to each other.


#################### (VI) Build and visualise the bootstrapped tree ####################

tree_bs <- visTreeBootstrap(t(data))
system('mv Rplots.pdf SupraHex_visTreeBootstrap.pdf')
dev.off()
# As you have seen, neighbour-joining tree is constructed based on pairwise euclidean distance matrices between samples. 
#The robustness of tree branching is evaluated using bootstraping. 
#In internal nodes (also color-coded), the number represents the proportion of bootstrapped trees that support the observed internal branching. 
#The higher the number, the more robust the tree branching. 100 means that the internal branching is always observed by resampling characters.


#################### TimeScape ####################

hc = hclust(dist(t(data)))
sample_time_order = hc$labels[c(hc$order)]
dist_matrix = as.matrix(dist(t(data)))

tmp_time = 0
for (sample in sample_time_order){
#print(sample)
get_index_first = which(sample==sample_time_order)
get_index_last = get_index_first+1
sample_first = sample_time_order[get_index_first]
sample_last = sample_time_order[get_index_last]
sample_dist_samples = dist_matrix[sample_first,sample_last]
#print(sample_dist_samples)

print(paste(c(sample, tmp_time)))
tmp_time = tmp_time + sample_dist_samples
print(tmp_time)
}

#################################################
file <- read.csv('PyClone_cellular_prevalence.supraHex_base_2.txt', sep='\t', header=TRUE)
clone_id <- file[,3]


mut_id <- strsplit(as.character(file[,1]), ":")
matrix(unlist(mut_id), ncol=5, byrow=TRUE)
chrom <- matrix(unlist(chromosome), ncol=5, byrow=TRUE)[,4]

coord <- matrix(unlist(mut_id), ncol=5, byrow=TRUE)[,5]





head(data)
clonal_prev  <- data.frame(timepoint=character(), clone_id=character(), clonal_prev=numeric(), stringsAsFactors=FALSE) 
tree_edges  <- data.frame(source=character(), target=character(), stringsAsFactors=FALSE) 
mutations <- data.frame(chrom=character(), coord=numeric(), clone_id=character(),  timepoint=character(), VAF=numeric(), stringsAsFactors=FALSE)








