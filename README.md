# MSC-Project: AI-Powered Chatbot for University Websites

## Table of Contents

- [Abstract](#abstract)
- [Repository Overview](#repository-overview)
- [Project Objectives](#project-objectives)
- [Installation](#installation)
- [Usage](#usage)
- [Prototype Details](#prototype-details)
- [Images and Visuals](#images-and-visuals)
- [Results and Findings](#results-and-findings)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Abstract

University websites are essential platforms for providing critical information. However, they often suffer from issues such as fragmented navigation, lack of personalization, and poor search interfaces. This project addresses these challenges by developing an AI-powered chatbot using advanced Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) techniques. The chatbot is designed to dynamically retrieve and generate accurate, domain-specific responses for course-related queries, improving the user experience for prospective students and other stakeholders.

## Repository Overview

The repository contains all the necessary resources for developing, fine-tuning, and deploying the chatbot. It includes the following directories and files:

- **`Data_Cleaning_and_Data_Analysis`**: This folder contains the notebook used for cleaning the data and Exploratory Data Analysis is also included here.
- **`Google-Collab`**: This folder contains all the notebooks used for finetuning and testing large language model on Google Colab with GPU.
- ** `Large Language Models`**:  Finetuned Large Languge Models are very big in size. All the LLM's made in this project is hosted on Huggingface. These LLM's are: [Gemma-2-9b](https://huggingface.co/roger33303/gemma-2-9b-Instruct-Finetune-website-QnA), [Mistral-7b](https://huggingface.co/roger33303/mistral-7b-Instruct-Finetune-website-QnA), [Llama-3.2-3b](https://huggingface.co/roger33303/Best_Model-llama3.2-3b-Instruct-Finetune-website-QnA), [Llama-3.2-3b-GGUF-Model](https://huggingface.co/roger33303/Best_Model-llama3.2-3b-16bit-Instruct-Finetune-website-QnA-gguf), [Phi-3.5-mini-instruct](https://huggingface.co/roger33303/phi3.5-4b-Instruct-Finetune-website-QnA). [More Information](https://github.com/Abhinav330/MSC-Project/blob/main/Large%20Language%20Models/README.md).
- **`Web_Scraping`**: This folder contains Web scraping scripts for extracting university course data.
- **`prototype_website_chatbot`**: This folder contains the prototype implementation of the chatbot. **`app.py`**: The main Streamlit script for running the chatbot prototype.
- **`README.md`**: This documentation file.

## Project Objectives

1. **Development**: Implement an AI chatbot capable of delivering accurate and contextually relevant course-related information.
2. **Improving User Experience**: Simplify access to university course details through an intuitive conversational interface.
3. **Model Evaluation**: Fine-tune and evaluate LLMs like Mistral-7B, Gemma-2-9B, Phi-3.5, and Llama-3.2 using metrics such as ScarBLEU, CER, and Meteor.
4. **Demonstrate Applications**: Highlight the potential of AI chatbots in enhancing educational digital services.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Abhinav330/MSC-Project.git
   ```

2. **Navigate to the directory**:
   ```bash
   cd MSC-Project
   ```

3. **Set up a virtual environment (recommended)**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Prototype Application**:
   ```bash
   streamlit run app.py
   ```
   This script launches the chatbot interface using Streamlit, enabling users to interact with the chatbot for course-related queries.

2. **Test Data Cleaning and Analysis**:
   - Access the `Data_Cleaning_and_Data_Analysis` directory.
   - Use the provided Jupyter notebooks to explore data preparation steps.

3. **Web Scraping**:
   - Use the `Web_Scraping/scrape_uni` scripts to extract updated course data from the university website.

## Prototype Details

- **Core Functionality**: Implemented in `app.py`, this Streamlit script integrates fine-tuned LLMs to respond to user queries about course details dynamically.
- **Technologies**: The chatbot uses LangChain for conversational flow, ChromaDB for efficient data retrieval, and Streamlit for the UI.
- **Supported Models**: Fine-tuned versions of Mistral-7B, Gemma-2-9B, Llama-3.2, and Phi-3.5.

## Images and Visuals

### Prototype Screenshots


![Prototype Chat Interface](https://github.com/Abhinav330/MSC-Project/blob/main/img/Prototype.png)

*Figure 1: The chatbot responding to user queries.*

![EDA Visualization](https://github.com/Abhinav330/MSC-Project/blob/main/img/International%20fee%20distribution.png)

*Figure 2: Exploratory Data Analysis showing International fee distribution.*

## Results and Findings

1. **Model Performance**:
   - **Best Model**: Llama-3.2 demonstrated the highest accuracy and fluency.
   - **Metrics**: ScarBLEU, CER, and Meteor scores validated the model outputs.

2. **User Experience**:
   - Improved navigation and search efficiency on the university website.
   - Accurate, context-aware responses for course-related queries.

3. **Prototype Evaluation**:
   - Robust response handling for paraphrased and complex user questions.

## Contributing

We welcome contributions to improve the chatbot. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add your feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact Information

For any inquiries, please contact Abhinav via [abhinav33303@gmail.com](mailto:abhinav33303@gmail.com).

---

*This project is part of an MSc research initiative focused on improving digital services in higher education.*
