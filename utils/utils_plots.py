# This python file contains functions for generating plots


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

# Set palette for colors
mypalette = ["#008248", "#604c4c", "#eac784", "#f0cddb", "#6B9997"]
mypalette_d = ["#cce6da", "#66b491", "#008248"]
genders = ["#8700f9", "#00c4a9", "#4462D1"]

# Function generating scree-plot
def screePlot(profile, var_explained=0.8):
    
    profile = profile.set_index("id_membership") # set id_membership as index
    
    # Apply feature scaling - leaving variances unequal is equivalent to putting more weight on variables with smaller variance
    scaler = StandardScaler().fit(profile)
    profile_scaled = scaler.transform(profile)
    
    # Apply dimensionality reduction -  k-means algorithm is both more effective and more efficient with a small number of dimensions
    # Use PCA to reduce dimensionality
    
    pca = PCA()
    X_pca = pca.fit_transform(profile_scaled)
    
    # Scree plot (variance explained by each principal component)
    num_components=len(pca.explained_variance_ratio_)
    ind = np.arange(num_components)
    vals = pca.explained_variance_ratio_
    cumvals = np.cumsum(vals)

    plt.figure(figsize=(10,6))

    ax = sns.barplot(ind, vals, ci=None, palette=mypalette[:1])
    ax2 = sns.lineplot(ind, cumvals, ci=None, color="black")
    ax.grid(b=True, which='major', linewidth=0.5)

    ax.set_xlabel("Principal component")
    ax.set_ylabel("Variance explained (%)")
    plt.title('Explained variance per principal component');
    

# Function plotting the number of customers by clusters
def customersByClusters(profile, kmeans_clusters, filename=""):
    df = profile.copy().reset_index()
    df['cluster'] = kmeans_clusters
    ax = sns.countplot(x='cluster', data=df, palette=mypalette)
    ax.set_title('Customers by cluster');
    fig = ax.get_figure()
    if filename != "":
        fig.savefig(filename+".png") 
    
# Function plotting a collection of informative variable subplots for final interpretation of the different clusters.
# Each subplot shows how one variable is distributed across clusters.
def barPlotGrid(profile, kmeans_clusters, filename=""):
    df = profile.copy()
    df['cluster'] = kmeans_clusters
    df = df.melt(id_vars=['id_membership', 'cluster'])
    df = df.query('cluster != -1').groupby(['cluster', 'variable']).mean().reset_index()
    
    g = sns.FacetGrid(df, col='variable', hue='cluster', col_wrap=5, height=2, sharey=False, palette=mypalette)
    g = g.map(plt.bar, 'cluster', 'value').set_titles("{col_name}")
    if filename != "":
        g.savefig(filename+".png")  
    