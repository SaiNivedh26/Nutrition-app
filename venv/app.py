import streamlit as st
import google.generativeai as gemini
import os
from dotenv import load_dotenv
load_dotenv() #we'll load all env variables
from PIL import Image

gemini.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gem_response(input_prompt,image):
    model=gemini.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("OOPS ! ..... File not found")
    

st.set_page_config(page_title="Calories Advsior",page_icon="./my_img.jpeg")
st.header("Nutrition checker app by Sai")
uploaded_file = st.file_uploader("Choose an image..: ",type=["jpj","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)

submit=st.button("Tell me about Total calories in this food item")

input_prompt = """
You are an expert in nutritionist, you need to see the foodn item from the image
and calculate the total calories, also provided details of every food items with calory intake
in the below format

1. Item 1 - number of calories
2. Item 2 - number of calories
---
---

Finally you can mention whether the food is healthy or not healthy and mention that too.
mention the percentage split of ratio of carbohydrate,fats,fibres,sugars and other things required in diet


"""

if submit:
     with st.spinner('Calculating calories...'):
        image_data = input_image_setup(uploaded_file)
        response = get_gem_response(input_prompt,image_data)
     st.header("Response is ")
     st.write(response)