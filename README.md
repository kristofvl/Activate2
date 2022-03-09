# Activity Analysis throughout the day using wearables (Step Counting and Walking Detection)

Activate2 Dataset consisting of Day-Long Recordings stored in CSV Folder 

A dataset for analyzing activity throughout the day with wearables.

To run the experiment, simply clone this repository and execute the exp.py script:

> python exp.py <kbd>Return</kbd>

The class and functions are declared in Act.py

# Organisation

* `_CSV` contains the dataframes for 27 Participants from 001 to 033
* `_Fig` contains the plots of accelerometer values, steps, walking, and steps/min for all the participants
* `_Pkl` contains the Pkl files of the dataframes and the Walking Segment CSV files
 


## License

This content is distributed with a [Creative Commons Zero v1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/).

The person who associated a work with this deed has dedicated the work to the public domain by waiving all of his or her rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

- In no way are the patent or trademark rights of any person affected by CC0, nor are the rights that other persons may have in the work or in how the work is used, such as publicity or privacy rights.
- Unless expressly stated otherwise, the person who associated a work with this deed makes no warranties about the work, and disclaims liability for all uses of the work, to the fullest extent permitted by applicable law.
 - When using or citing the work, you should not imply endorsement by the author or the affirmer.


## Step Detection and Walking Detection Consists of 4 Steps:

1. Modules and Repository Import
2. Class and Function Declarations
3. Data Exploration and Analysis
4. Data Visualization

After importing the necessary modules and cloning the repository for the CSV files, optimal parameters are used to detect the step. From the steps detected, a sliding window approach is used to ascertain walking within a particular window. The data (accelerometer values, steps, walking segments) are then plotted in the form of a time series graph.

The python notebook `Steps_and_Walking_Detection_v1.ipynb` can be found in the repository.

To run this notebook in colab, simply open the file and click on the **Open In Colab** Badge (<a href="https://colab.research.google.com/github/kristofvl/Activate2/blob/main/Steps_and_Walking_Detection_v1.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a> ) present at the top in the notebook.

 ## Result Plots for two cases

Plot for ID: 006

![006](https://user-images.githubusercontent.com/85766211/157211750-0ad83f9f-f198-4f35-8004-16652c31b7bb.png)



Plot for ID: 013

![013](https://user-images.githubusercontent.com/85766211/157211777-68bca3ea-1f28-4438-a387-ea09044937b9.png)

