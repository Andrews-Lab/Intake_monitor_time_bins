# BioDaq Food and Water Intake Monitor Time Bins 🐁

### Overview

__BioDaq Food and Water Intake Monitor__

The [BioDaq Food and Water Intake Monitor](https://researchdiets.com/biodaq) allows food and water levels in each rodent cage to be measured at all times.
This gives greater temporal resolution to food and water intake data, compared to data obatined through manual weighing.

__Purpose__

This code organises the excel output files from the BioDaq Food and Water Intake Monitor into time bins. <br>
It can also group the time binned data by individual stats and animals.

__Preview of the graphical user interface__

<p align="center">
  <img src="https://user-images.githubusercontent.com/101311642/205285449-ec27c443-c094-4660-999e-f5159e5d0a20.png" width="440">
</p><br/>

__Input and output data__

<p align="center">
  <img src="https://user-images.githubusercontent.com/101311642/205290754-cb911936-6727-47ce-bef5-65f2e03f62c4.png" width="530">

![image](https://user-images.githubusercontent.com/101311642/205290778-ba64a4a6-e492-4bb9-8248-488847fa3e0d.png)

### Installation

Install [Anaconda Navigator](https://www.anaconda.com/products/distribution). <br>
Open Anaconda Prompt (on Mac open terminal and install X-Code when prompted). <br>
Download this repository to your home directory by typing in the line below.
```
git clone https://github.com/Andrews-Lab/Intake_monitor_time_bins.git
```
Change the directory to the place where the downloaded folder is. <br>
```
cd Intake_monitor_time_bins
```

Create a conda environment and install the dependencies.
```
conda env create -n IMTB -f Dependencies.yaml
```

### Usage
Open Anaconda Prompt (on Mac open terminal). <br>
Change the directory to the place where the git clone was made.
```
cd Intake_monitor_time_bins
```

Activate the conda environment.
```
conda activate IMTB
```

Run the codes.
```
python Intake_monitor.py
```

### Guide

View the guide about [how to analyse your intake monitor data](How_to_use_intake_monitor_codes.pdf).

<br>

### Acknowledgements

__Author:__ <br>
[Harry Dempsey](https://github.com/H-Dempsey) (Andrews lab and Foldi lab) <br>

__Credits:__ <br>
Nikita Bajaj, Sarah Lockie, Zane Andrews <br>

__About the labs:__ <br>
The [Andrews lab](https://www.monash.edu/discovery-institute/andrews-lab) investigates how the brain senses and responds to hunger. <br>
The [Foldi lab](https://www.monash.edu/discovery-institute/foldi-lab) investigates the biological underpinnings of anorexia nervosa and feeding disorders. <br>
