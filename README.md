<div align="center">
  <img src="https://github.com/user-attachments/assets/85bfbd12-2889-42ba-be05-41c8c12404e3" alt="Project Logo" width="250"/>
</div>

<p align="center">
  <a href="TBU"> 📃 Paper </a> | 
  <a href="[https://link-to-playground.com](https://www.youtube.com/watch?v=jtZO6_l66JI)"> 🎦 Demo </a>
</p>

https://github.com/user-attachments/assets/7c099a92-05b2-4b24-855d-dc52407b16b1

## SummPilot: Bridging Efficiency and Customization for Interactive Summarization System

**SummPilot** is a web application built with Flask that offers customizable and interactive summarization of multiple documents. It allows users to generate initial summaries and then personalize them to meet their specific needs. It features two modes: **Basic Mode**, which provides automatic summarization, and **Advanced Mode**, which enables user-driven customization, offering different approaches to the summarization process.

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Summary Evaluation](#summary-evaluation)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Build Your Own SummPilot

### Install Dependencies

```bash
git clone https://github.com/Jungmin-YUN-0/SummPilot.git
cd SummPilot
pip install -r requirements.txt
```

### Usage
To run the application locally:
```bash
python run.py
```
You can access the application by opening your web browser and navigating to `http://localhost:8080`.

If needed, you can modify the host and port settings by editing the following code:
```bash
if __name__ == "__main__":
  app.run(host='localhost', port=8080, debug=True) # for localhost
```

### Environment Setup

- Open the app.py file and set a secure value for app.secret_key:

```bash
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key
```

- Ensure all necessary files and directories are in place, including templates, static assets, and the `THEME` directory.


### OpenAI API Key Setup
To use the OpenAI-compatible APIs with SummPilot, follow these steps to set up your OpenAI API key:

1. Open the `summarization.py` and `summary_evaluation.py` files in your preferred text editor.

2. In each file, locate the following code snippet:
 ```python
   # Please enter your API key
   # openai.api_key = "your_openai_api_key_here"
```

3. Uncomment the openai.api_key line and replace the "your_openai_api_key_here" text with your actual OpenAI API key.

By completing these steps, you'll have successfully configured SummPilot to use your OpenAI API key for its summarization and evaluation functionalities.

