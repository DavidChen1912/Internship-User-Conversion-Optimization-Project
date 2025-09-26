# Internship – i-TRUE @cosme  
<img src="docs/@cosme.png" alt="@cosme logo" width="70%" />
**User Conversion Optimization Project**

## ⚠️ Disclaimer  
This repository documents my internship at **i-TRUE @cosme**. Due to an **NDA**, I cannot provide the original internal datasets. Instead, I used publicly available @cosme URLs as the content basis for GPT-generated synthetic data, reconstructing the dataset structure. **No proprietary or confidential company data is included.**

---

## 📖 Introduction  
**@cosme** is the largest cosmetics information platform in Taiwan, where users frequently browse and share product reviews, often leading to purchase intent. The leadership team sought to better understand behavioral differences across customer segments and identify patterns of high-value customers.  

This project analyzed **individual user browsing paths** to uncover the **key webpages** and **browsing paths** that most strongly influenced conversions. Based on these insights, We provided business recommendations to optimize the customer journey and improve conversion rates.  

The full project pipeline and documentation can be found under the [`/docs`](./docs) directory.  

---

## 🛠️ Scripts  

- **`execute.py`**: Runs the complete analysis pipeline  
- **`preprocessing.py`**: Transforms internal datasets into user browsing paths  
- **`feature_select.py`**: Identifies the most influential webpages for conversion  
- **`conversion_analysis.py`**: Outputs the most valuable browsing paths and conversion analyses  

---

## 🚀 Usage  

Run the full pipeline with one command:  

```
python execute.py --data=example
```

#### Notes:
- **`data`** must match the structure of example.csv
- The one-click execution uses generalized parameters. For custom experiments, run each module separately.

## 🗂️ Preprocessing

Convert internal datasets into user browsing paths:

```
python preprocessing.py --data=example --output=paths
```

#### Notes:
- **`data`**: input dataset
- **`output`**: name for the transformed paths dataset (saved in [`/outputs`](./outputs))


## 🔎 Feature Selection

Identify the top 5 influential webpages

```
python feature_select.py --data=paths --classification_data_name=conversion --feature_data_name=top5_features
```

#### Notes:
- Input: browsing path dataset (**`data`**)
- Output: two datasets (**`classification_data_name`** and **`feature_data_name`**) stored in [`/outputs`](./outputs)

## 📊 Conversion Analysis

Generate high-value browsing paths and conversion-rate reports 

```
python conversion_analysis.py --paths_data_name=paths --classification_data_name=conversion --feature_data_name=top5_features
```

#### Notes:
- Requires three inputs: paths data, classification_data, and feature_data


  









