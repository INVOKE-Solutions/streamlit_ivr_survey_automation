# **🪐 Streamlit Survey Automation**

---

## **Technologies Used 🔧**

<div>
    <h1 style="text-align: center;">Data Cleaning and Analysis with Streamlit, FastAPI, and Docker</h1>
    <img style="text-align: left" src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="10%" alt="Streamlit Logo" />
    <img style="text-align: left" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="10%" alt="FastAPI Logo" />
    <img style="text-align: left" src="https://img.icons8.com/color/48/000000/docker.png" width="10%" alt="Docker Logo" />
    <img style="text-align: left" src="https://img.icons8.com/color/48/000000/python.png" width="10%" alt="Python Logo" />
</div>
<br>

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ivr-cleaning-automation.streamlit.app/)

---

## **📋 Table of Contents**

1. [Overview](#overview)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Usage](#usage)
   - [IVR Data Cleaner & Pre-Processor App](#ivr-data-cleaner--pre-processor-app)
   - [Questionnaire Definer](#questionnaire-definer)
   - [Keypresses Decoder](#keypresses-decoder)
   - [FastAPI App Integration](#fastapi-app-integration)
5. [Contributing](#contributing)
6. [License](#license)

---

## **1. Overview 📖**

The **IVR Data Processing Suite** is a comprehensive toolset designed for cleaning and processing IVR (Interactive Voice Response) data (the campaign data) . It utilizes a combination of Streamlit and FastAPI to provide an intuitive user interface for file uploads, data cleaning, questionnaire definition, keypress decoding, and data analysis. The suite is split into three main components: IVR Data Cleaner & Pre-Processor App, Questionnaire Definer, and Keypresses Decoder, which are built to work seamlessly together or as standalone modules.

---

## **2. Getting Started 🚀**

### **Prerequisites**

- Docker
- Python 3.8 or newer

### **Installation**

1. **Clone the Repository**

   Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Build the Docker Container**

   Navigate to the project directory and build the Docker container:
   ```bash
   docker build -t ivr-data-suite .
   ```

3. **Run the Docker Container**

   Run the Docker container:
   ```bash
   docker run -p 8501:8501 ivr-data-suite
   ```

---

## **3. Project Structure 📂**

```
.
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── .streamlit
│   └── secrets.toml
├── fastapiapp
│   ├── dockerfile
│   ├── security_utils.py
│   ├── test.db
│   ├── app
│   │   ├── main.py
│   │   └── modules
│   │       ├── aws_utils.py
│   │       ├── crud.py
│   │       ├── data_cleaner_utils_page1.py
│   │       ├── dependencies.py
│   │       ├── keypress_decoder_utils_page3.py
│   │       ├── questionnaire_utils_page2.py
│   │       ├── schemas.py
│   │       └── ...
│   ├── tests
│   │   └── tests_main.py
│   └── images
│       └── invoke_logo.png
└── mainapp
    ├── 1_IVR_Data_Cleaner_Pre_Processor_App.py
    ├── modules
    │   ├── data_cleaner_utils_page1.py
    │   ├── keypress_decoder_utils_page3.py
    │   ├── questionnaire_utils_page2.py
    │   └── security_utils.py
    └── pages
        ├── 2_Questionnaire_Definer.py
        └── 3_Keypresses_Decoder.py
```

This structure organizes the Streamlit apps and FastAPI backend, providing clear modularity and separation of concerns for different functionalities.

---

## **4. Usage 📊**

### **IVR Data Cleaner & Pre-Processor App**

- **Objective**: To clean and preprocess IVR data for analysis.
- **Features**: Upload IVR files, visualize basic statistics, download cleaned data, and manage phone numbers for future sampling.

### **Questionnaire Definer**

- **Objective**: To define and structure the questionnaire from IVR campaigns.
- **Features**: Upload script files, parse questions and answers, rename data columns, and prepare data for further processing.

### **Keypresses Decoder**

- **Objective**: To decode and categorize keypress responses from IVR campaigns.
- **Features**: Upload script or JSON files for decoding, classify responses, and download the decoded data for analysis.

### **FastAPI App Integration**

- **Objective**: To integrate the Streamlit apps with a FastAPI backend for advanced data processing and storage capabilities.
- **Setup**: Refer to the `fastapiapp` directory and Dockerfile for setup and deployment instructions.

---

## **5. Contributing 🤝**

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'feat: add AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

---

## **6. License 📜**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
