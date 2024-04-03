import os
import streamlit as st
import pandas as pd
from lida import Manager, TextGenerationConfig, llm
from PIL import Image
from io import BytesIO
import base64
from goals import goals_to_html
from htmlTemplates import css

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

def csv_main():
    selected_dataset = None
    with st.sidebar:
        st.image("resources/app_logo.png")
        st.write("# 🗳️ Upload CSV/JSON File")
        uploaded_file = st.file_uploader("Upload your file here", type=["csv", "json"])
        if uploaded_file:
            if uploaded_file is not None:
            # Get the original file name and extension
                file_name, file_extension = os.path.splitext(uploaded_file.name)
                # Load the data depending on the file type
                if file_extension.lower() == ".csv":
                    data = pd.read_csv(uploaded_file)
                elif file_extension.lower() == ".json":
                    data = pd.read_json(uploaded_file)
                # Save the data using the original file name in the directory
                uploaded_file_path = os.path.join("file_uploaded", uploaded_file.name)
                data.to_csv(uploaded_file_path, index=False)
                selected_dataset = uploaded_file_path
                st.success("✅ File Uploaded!")

    if uploaded_file:
        # Data Summarization
        lida = Manager(text_gen = llm("openai"))
        textgen_config = TextGenerationConfig(n=1, 
                                            temperature=0.5, 
                                            model="gpt-3.5-turbo", 
                                            use_cache=True)
        st.markdown(css, unsafe_allow_html=True)
        st.markdown("<h2 class='my-header'> Data Summary </h2>", unsafe_allow_html=True)
        st.caption("An enriched representation of the data (with predicted semantic type and description (if any))")

        summary = lida.summarize(selected_dataset, summary_method="default", textgen_config=textgen_config)
        if "dataset_description" in summary:
            st.write(summary["dataset_description"])
        if "fields" in summary:
            fields = summary["fields"]
            nfields = []
            for field in fields:
                flatted_fields = {}
                flatted_fields["column"] = field["column"]
                for row in field["properties"].keys():
                    if row != "samples":
                        flatted_fields[row] = field["properties"][row]
                    else:
                        flatted_fields[row] = str(field["properties"][row])
                nfields.append(flatted_fields)
            nfields_df = pd.DataFrame(nfields)
            st.data_editor(nfields_df)
        else:
            st.write(str(summary))
        st.divider()

        # Goal Exploration
        st.markdown("<h2 class='my-header'> Goal Exploration </h2>", unsafe_allow_html=True)
        st.caption("A list of automatically generated data exploration goals (hypothesis) based on the data summary above")

        goals = lida.goals(summary, n=2, textgen_config=textgen_config)
        html_goals = goals_to_html(goals)
        for html_goal in html_goals:
            st.write(html_goal, unsafe_allow_html=True)
        st.divider()

        # Visualization Generation
        st.markdown("<h2 class='my-header'> Visualization Generation </h2>", unsafe_allow_html=True)
        st.caption("Select a button goal or query a new visualization goal to generate visualization")
        button1 = st.button("Goal 0")
        button2 = st.button("Goal 1")
        text_area = st.text_area("Query your new goals to generate visualization", height=100)
        button3 = st.button("Generate Graph")
        library = "matplotlib"
        if button1:
            textgen_config = TextGenerationConfig(n=1, temperature=0.5, use_cache=True)
            charts = lida.visualize(summary=summary, goal=goals[0], textgen_config=textgen_config, library=library)
            if charts:
                viz_titles = [f'Visualization {i+1}' for i in range(len(charts))]
                img_base64_string = charts[0].raster
                img = base64_to_image(img_base64_string)
                st.image(img, caption=viz_titles, use_column_width=True)
            else:
                st.error("No charts generated")

        if button2:
            textgen_config = TextGenerationConfig(n=1, temperature=0.5, use_cache=True)
            charts = lida.visualize(summary=summary, goal=goals[1], textgen_config=textgen_config, library=library)
            if charts:
                viz_titles = [f'Visualization {i+1}' for i in range(len(charts))]
                img_base64_string = charts[0].raster
                img = base64_to_image(img_base64_string)
                st.image(img, caption=viz_titles, use_column_width=True)
            else:
                st.error("No charts generated")
        
        if button3:
            if len(text_area) > 0:
                st.info("Your Query: " + text_area)
                lida = Manager(text_gen = llm("openai")) 
                textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                summary = lida.summarize(selected_dataset, summary_method="default", textgen_config=textgen_config)
                user_query = text_area
                charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)
            if charts:
                charts[0]
                image_base64 = charts[0].raster
                img = base64_to_image(image_base64)
                st.image(img)
            else:
                st.error("No charts generated. Try again with a better prompt")
