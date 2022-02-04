# Instructions to set up your environment

Here are some instructions explaining how to create the conda environment with the necessary packages.

In your terminal, run the following commands:

1. Create new environement called "daib"

$conda create -y --name daib python=3.8

2. Activate new environment 

$source activate daib # Old conda

$conda activate daib # New conda 

3. Install packages contained in the requirements.txt file 

$pip install -r requirements.txt 

# Instructions while updating the environment (i.e. using new libraries or packages)

1. Update the requirements.txt file while mentioning the new libraries you have been using
