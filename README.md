# Animesh Basak - Portfolio

This is the portfolio website of Animesh Basak, showcasing his skills, experience, and projects. The website includes a chatbot feature that allows users to interact and ask questions about Animesh's resume and projects.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [License](#license)

## Introduction

This portfolio website is designed to highlight the skills and experiences of Animesh Basak. It includes sections for an introduction, skills, resume, contact information, and a chatbot for interactive queries.

## Features

- **Introduction**: Overview of Animesh's background and expertise.
- **Skills**: List of technical skills and proficiencies.
- **Resume**: Downloadable resume and project highlights.
- **Contact**: Links to social media profiles and email.
- **Chatbot**: Interactive chatbot to answer questions about Animesh's resume and projects.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/AnimeshBasak-14/portfolio.git
    cd portfolio
    ```

2. Navigate to the [chatbot](http://_vscodecontentref_/0) directory and install the required Python packages:
    ```sh
    cd chatbot
    pip install -r requirements.txt
    ```

3. Create a [.env](http://_vscodecontentref_/1) file in the [chatbot](http://_vscodecontentref_/2) directory and add your environment variables:
    ```env
    HF_TOKEN="your_huggingface_token"
    GROQ_API_KEY="your_groq_api_key"
    ```

4. Start the Flask server:
    ```sh
    python app.py
    ```

5. Open [index.html](http://_vscodecontentref_/3) in your browser to view the portfolio website.

## Usage

- **Chatbot**: Navigate to the Chatbot section and interact with the chatbot by typing your questions in the input box and clicking "Send".
- **Resume**: Download the resume by clicking the "Download My Resume" button in the Resume section.
- **Contact**: Use the provided links to connect with Animesh on LinkedIn, GitHub, or via email.

## Project Structure
portfolio/
├── chatbot/
│   ├── __pycache__/
│   ├── .env
│   ├── app.py
│   ├── requirements.txt
├── img/
├── pages/
│   ├── chatbot.html
│   ├── contact.html
│   ├── introduction.html
│   ├── resume.html
│   ├── skills.html
├── script.js
├── styles.css
├── index.html



## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, Python
- **Libraries**: Langchain, Chroma, HuggingFace, PyPDF2
- **Styling**: Poppins font, Font Awesome icons

## Deployment

This project is deployed using Netlify. To deploy your own version, follow these steps:

1. Create a Netlify account at [Netlify](https://www.netlify.com/).
2. Connect your GitHub repository to Netlify.
3. Configure the build settings:
    - Build command: `npm run build` (if applicable)
    - Publish directory: [portfolio](http://_vscodecontentref_/4) (root directory)
4. Deploy the site.

For more detailed instructions, refer to the [Netlify documentation](https://docs.netlify.com/).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
