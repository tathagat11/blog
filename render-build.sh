#!/bin/bash

# Output the current Hugo version
hugo version

# Set Hugo version
HUGO_VERSION=0.125.7

# Check if hugo exists in the build cache
if [[ ! -f $XDG_CACHE_HOME/hugo ]]; then 
    echo "...Downloading Hugo $HUGO_VERSION" 
    mkdir -p ~/tmp 
    wget -q https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz -P ~/tmp
    
    cd ~/tmp
    echo "...Extracting Hugo" 
    tar -xzf hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz
    
    echo "...Moving Hugo to cache directory"
    mkdir -p $XDG_CACHE_HOME
    mv hugo $XDG_CACHE_HOME/hugo
    
    # Clean up
    rm -rf ~/tmp
    cd $HOME/project/src # Return to project directory
else 
    echo "...Using Hugo from build cache"
fi

# Output the new Hugo version
$XDG_CACHE_HOME/hugo version

# Build the site
$XDG_CACHE_HOME/hugo --theme PaperMod --gc --minify