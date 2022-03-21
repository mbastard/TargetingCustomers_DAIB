# This python file contains functions for generating plots


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import math as math

# Set palette for colors
#mypalette = ["#008248", "#604c4c", "#eac784", "#f0cddb", "#6B9997"]#Old
mypalette = ["#0b84a5", "#f6c85f", "#6f4e7c", "#9dd866", "#ca472f", "#ffa056","#8dddd0"]
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

    ax.set_xlabel("Component number")
    ax.set_ylabel("Percentage of explained variance")
    plt.title('Scree plot of explained variance');
    
# Function generating scree-plot
def screePlot_2axis(profile, var_explained=0.8, filename=""):
    
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
        
    fig, ax1 = plt.subplots(figsize=(10,6))    
    
    color = 'tab:blue'
    ax1.set_xlabel('Component number')
    ax1.set_ylabel('Explained variance per component (%)', color=color)
    ax1.bar(ind, vals, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(False)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:green'
    
    
    ax2.set_ylabel('Cumulated explained variance (%)', color=color)  # we already handled the x-label with ax1
    ax2.plot(ind, cumvals, color=color)
    ax2.scatter(ind, cumvals, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    ax1.set_ylim(0,0.4)
    ax2.set_ylim(0,1.2)
    
    
    for i, txt in enumerate(cumvals):
        ax2.annotate(str(int(round(cumvals[i],2)*100)) + "%", (ind[i], cumvals[i]+0.05), rotation=90, color=color)
    
    
    
    plt.title('Scree plot of explained variance');
    
    if filename != "":
        fig.savefig(filename+".png", dpi=200) 

    
    

# Function plotting the number of customers by clusters
def customersByClusters(profile, kmeans_clusters, filename=""):
    df = profile.copy().reset_index()
    df['cluster'] = kmeans_clusters
    ax = sns.countplot(x='cluster', data=df, palette=mypalette)
    ax.set_title('Customers by cluster');
    
    for p in ax.patches:
        ax.annotate(p.get_height(), (p.get_x()+0.3, p.get_height()+50))
    
    
    fig = ax.get_figure()
    if filename != "":
        fig.savefig(filename+".png", dpi=200) 

# Function plotting a collection of informative variable subplots for final interpretation of the different clusters.
# Each subplot shows how one variable is distributed across clusters.
def barPlotGrid(profile, kmeans_clusters, filename="", opt_col_order=[]):
      
    df = profile.copy()    
    
    if len(opt_col_order)==0:
        opt_col_order = list(df.columns)
        opt_col_order.remove("id_membership")
    
    
    #Remove prep_ in column names
    for ind, column in enumerate(df):
        if 'prep_' in column:
            new_col = column.replace("prep_", "", 1)
            df.rename(columns = {column:new_col}, inplace = True)
            # find the index
            i = opt_col_order.index(column)
            opt_col_order = opt_col_order[:i]+[new_col]+opt_col_order[i+1:]
    
    #sns.set_theme(style="darkgrid")
    sns.set_style("whitegrid")
    df['cluster'] = kmeans_clusters
    df = df.melt(id_vars=['id_membership', 'cluster'])
    df = df.query('cluster != -1').groupby(['cluster', 'variable']).mean().reset_index()
    
    
    g = sns.FacetGrid(df, col='variable', hue='cluster', col_wrap=3, height=2, sharey=False, palette=mypalette, 
                      col_order=opt_col_order)
    g = g.map(plt.bar, 'cluster', 'value').set_titles("{col_name}")
    if filename != "":
        g.savefig(filename+".png")  

        
                
# bar plot function printing values 
def f(cluster,value, **kwargs):
    ax = plt.bar(x=cluster,height=value,**kwargs)
    
    #plt.xticks(list(range(len(cluster))), list(range(len(cluster))))
    #l = cluster.shape[0]
    #plt.xticks(list(range(l)))
    
    for i in range(len(cluster)):
        plt.annotate(str(round(value.values[i],2)), xy=(cluster.values[i],0), ha='center', va='bottom',rotation=90)
        #plt.annotate(str(round(value.values[i],2)), xy=(cluster.values[i],value.values[i]), ha='center', va='bottom')
        #plt.ylabel("test")
    
    
# Function plotting a collection of informative variable subplots for final interpretation of the different clusters.
# Each subplot shows how one variable is distributed across clusters.
def barPlotGrid_values(profile, kmeans_clusters, filename="", opt_col_order=[], sharey_lst=[],ylabel_lst=[]):
    
    df = profile.copy() 
      
    if len(opt_col_order)==0:
        opt_col_order = list(df.columns)
        opt_col_order.remove("id_membership")
    
    
    #Remove prep_ in column names
    for ind, column in enumerate(df):
        if 'prep_' in column:
            new_col = column.replace("prep_", "", 1)
            df.rename(columns = {column:new_col}, inplace = True)
            # find the index
            if column in opt_col_order:
                i = opt_col_order.index(column)
                opt_col_order = opt_col_order[:i]+[new_col]+opt_col_order[i+1:]    
        
           
    df['cluster'] = kmeans_clusters
    df = df.melt(id_vars=['id_membership', 'cluster'])
    df = df.query('cluster != -1').groupby(['cluster', 'variable']).mean().reset_index()
    
    nb_clust = len(df["cluster"].unique())
        
    
    #l=l
    #plt.subplots(1, l)
    
    
    col_wrap=3
    l = math.ceil(len(opt_col_order)/col_wrap)
    j=0
    k=col_wrap
    
    #if len(sharey_lst)!=l:
    #    [True]*l
           
    for i in range(l):
        #plt.subplot(1, l, i+1)
            
        g = sns.FacetGrid(df, col='variable', hue='cluster', col_wrap=col_wrap, height=2, sharey=sharey_lst[i], palette=mypalette, 
                      col_order=opt_col_order[j:k])
        #g = g.map(plt.bar, 'cluster', 'value').set_titles("{col_name}")
        g = g.map(f, 'cluster', 'value').set_titles("{col_name}")
        
        if len(ylabel_lst) != 0:
            g.set(ylabel=ylabel_lst[i])
        
        plt.xticks(list(range(nb_clust)))
        
        
        j=j+col_wrap
        k=k+col_wrap
        
        if filename != "":
            g.savefig(filename + "_" + str(i+1) + ".png", dpi=200)
            
    return df