
<h1 align="center">
  <br>
  <a href="https://interactibot.streamlit.app/"><img src="\resources\app_logo.png" alt="InteractiBot" width="600"></a>
</h1>

<h4 align="center">An innovative Streamlit application that allows users to interact with their uploaded CSV/JSON and PDF files, leveraging LIDA for data visualization and Langchain for document interaction.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#setup">Setup</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
</p>

https://github.com/Samm58/InteractiBot/assets/141254721/748cacba-8517-4707-b762-1a88ee67ce22

## Key Features

* **Interactive File Upload**: Upload CSV/JSON or PDF files and interact with them directly within the application
* **LIDA Integration**: Utilize LIDA for automatic generation of visualizations and infographics from CSV/JSON data.
  - Get a quick summary of your uploaded CSV/JSON data.
  - Explore your data based on 2 set of potential goals or user queries.
  - Generate visulization on selected goals or user queries.
* **Langchain Integration**: Use Langchain for interacting with uploaded PDF files.
  - Have a conversation with your uploaded PDF, powered by OpenAI’s language model.
* **Streamlit Community Cloud**: Published on Streamlit’s community cloud, making it accessible for anyone to try out.

## Setup

1. Clone this repository
```bash
git clone https://github.com/Samm58/InteractiBot
```
2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Obtain an API key from OpenAI and add it to the .env file in the project directory
```bash
OPENAI_API_KEY= "your_secret_api_key"
```

## How to Use

1. Ensure all dependecies are installed and OpenAI API key have been added
   
2. Run the `app.py` file
```bash
streamlit run app.py
```

3. The app will launched in your default browser
4. Select which file option you would like to interact with
5. Load the file on the sidebar
6. Start interact with your file

## Credits

This software uses the following open source packages:

- [Streamlit](https://streamlit.io/)
- [LIDA](https://microsoft.github.io/lida/)
- [Langchain](https://www.langchain.com/)

## Related

[InteractiBot](https://interactibot.streamlit.app/) - Web version of InteractiBot

