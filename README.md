# Progetto Singolo FIA
## Problem:
>a competizione avrà luogo su un task di Radiomica. 
> 
>Per Radiomica si intende l'analisi delle immagini mediche volta ad ottenere, tramite opportuni metodi 
matematici e l'uso del calcolatore, informazioni di tipo quantitativo da queste non rilevabili tramite 
la loro semplice osservazione visiva da parte dell'operatore [Wikipedia]. 
> 
>L’obiettivo del progetto consiste nell’analizzare dati che provengono da 79 pazienti anonimizzati dai 
quali sono state acquisite immagini TAC del distretto anatomico dell’addome. 
> 
>A tutti i 79 pazienti è stata inizialmente diagnosticata una neoplasia maligna alla prostata  e si sono 
>sottoposti ad una prostatectomia radicale. 
>Successivamente, durante un esame di “controllo” nel quale sono state raccolte le TAC in analisi, in 
>45 dei pazienti è stata riscontrata una recidiva del tumore. 
> 
>Si chiede di sviluppare un sistema in IA che, utilizzando il dato acquisito in questa visita di controllo, 
>predica la presenza di recidiva del tumore. 
## Solution:

I have developed a program which will process the data from a table and try to predict the chances of having a recessive tumor. The program works in three steps:
1. **Data preprocessing:**
   - Importing dataset
   - Cleaning NaNs
   - Normalisation
   - Feature Selection
2. **Classification:** We have three available models:
   - Support Vector Machine
   - K Nearest Neighbour
   - Logistic Regression
3. **Evaluation:**
   - Calculates confussion matrix
   - Calculates some basic metrics
   - Saves the results in a JSON file

## Installation
In order to run the program we can make use of this script:
```
git clone https://github.com/KosmicKatXV/progetto-singolo-FIA.git
cd progetto-singolo-FIA
pip install -r requirements.txt
python main.py
```

## Usage

This program provides a list of arguments to use:
- `-h, --help`: short explanation of arguments
- `-f  FILENAME, --filename FILENAME`:dataset file name
- `-n NEIGHBOURS, --neighbours NEIGHBOURS`: number of neighbours for KNN
- `-ts TESTSIZE, --testsize TESTSIZE`: percentage of dataset for test data
- `-m MODEL, --model MODEL`: which model to choose:
   - svm
   - knn
   - lr
- `-r REGULARISATION, --regularisation REGULARISATION`: regularisation parameter for svm.
- `-p PENALTY, --penalty PENALTY`: penalty parameter for logistic regression
- `-v, --verbose`: prints data during the run
- `-c, --cache`: caches progress in case of interruption and attempts to find already cached progress
- `-o OUTPUT, --output OUTPUT`:results location, defaults in `results/`