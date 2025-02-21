<div align="center">
  <img src="https://github.com/user-attachments/assets/85bfbd12-2889-42ba-be05-41c8c12404e3" alt="Project Logo" width="250"/>
</div>

<p align="center">
   📃 Paper | 
</p>

https://github.com/user-attachments/assets/7c099a92-05b2-4b24-855d-dc52407b16b1

---

### ✨ SummPilot: Bridging Efficiency and Customization for Interactive Summarization System

**SummPilot** is a web application built with Flask that offers customizable and interactive summarization of multiple documents. It allows users to generate initial summaries and then personalize them to meet their specific needs.

It features two modes: **Basic Mode**, which provides automatic summarization, and **Advanced Mode**, which enables user-driven customization, offering different approaches to the summarization process.

## Contents 📑
- [Features](#Features)
- [Install Dependencies](#1.-Install-Dependencies)
- [Usage](#2.-Usage)
- [Setup](#3.-Setup)
- [Citation](#Citation)


## Features
- **Graph Visualization**: Visualizes the relationships between entities in the input text as a semantic graph, helping users understand the structure and key connections within the text by illustrating how entities are interrelated.
- **Relation Extraction**: Identifies and extracts significant relationships between entities in the input text, highlighting how different entities are connected.
- **Entity Clustering**: Groups similar or related entities together to provide a clearer overview of the information by identifying and clustering references to the same entity.
- **User Commands**: Allows users to customize the generated summary to meet their specific needs by inputting text-based instructions or preferences.
- **Summary Evaluation**: Assesses the quality of the generated summary through metrics such as compression ratio, coverage, and factual consistency, ensuring the summary accurately reflects the original content. Possible Errors refer to potential inaccuracies or inconsistencies in the generated summary that may arise due to user intervention or model limitations.

---

## Build Your Own SummPilot ⚒️

### 1. Install Dependencies

```bash
# clone the code
git clone https://github.com/Jungmin-YUN-0/SummPilot.git
cd SummPilot

# prepare the environment
# create env using conda
conda create -n SummPilot
conda activate SummPilot

# install requirements
pip install -r requirements.txt
```

##

### 2. Usage
To run the application locally:
```bash
python run.py
```
You can access the application by opening your web browser and navigating to `http://localhost:8080`.  

&nbsp;

If needed, you can modify the host and port settings by editing the following code:
```bash
if __name__ == "__main__":
  app.run(host='localhost', port=8080, debug=True) # for localhost
```

##

### 3. Setup
#### 3-1. Environment Setup
Ensure all necessary files and directories are in place, including templates, static assets, and the `THEME` directory.  

&nbsp;

Open the run.py file and set a secure value for app.secret_key:
```bash
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key
```

&nbsp;

#### 3-2. OpenAI API Key Setup
To use the OpenAI-compatible APIs with SummPilot, follow these steps to set up your OpenAI API key:

1. Open the `summarization.py` and `summary_evaluation.py` files in your preferred text editor.

2. In each file, locate the following code snippet:
 ```python
   # Please enter your API key
   # openai.api_key = "your_openai_api_key_here"
```

3. Uncomment the openai.api_key line and replace the "your_openai_api_key_here" text with your actual OpenAI API key.

By completing these steps, you'll have successfully configured SummPilot to use your OpenAI API key for its summarization and evaluation functionalities.


---

## Citation
TBU

