import openai
import requests
import os
import streamlit as st
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
IFTTT_WEBHOOK_KEY = os.getenv("IFTTT_WEBHOOK_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="Personalized Market Content Generator", page_icon=":rocket:", layout="centered")

# Create three columns
col1, col2, col3 = st.columns([1, 3, 1])  # Adjust the width ratio as needed

# Place the image in the center column (col2)
with col2:
    st.image("team_logo.png")

st.title('Personalised Market Content Generator')


# st.sidebar.subheader("Select Platform:",divider='rainbow')

platform = st.sidebar.selectbox(
    "**Choose your platform:**",
    ("Instagram", "Facebook", "LinkedIn", "Twitter"),index=None,
)




content_type = st.sidebar.radio(
    "Select Content type:",
    ["Post Caption", "Comment", "Recommendation"],index=None,
)




goal = st.text_input("**Define the goal of the Content:**")

context = st.text_input("**Define the Context for the Content:**")

output_size = (st.slider("**Select the Content Word Count:**", 0, 500, 200, 50))

# content_level = st.radio(
#     "Select Content Category",
#     ["Creative", "Descriptive", "Logical", "Joyful"],index=None,
# )

platform = st.selectbox(
    "**Select your content category**",
    ("Creative", "Descriptive", "Logical", "Joyful"),index=None,
)

def load_model(prompt):
    with st.spinner('Generating the Content...'):
        # Using OpenAI's ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional in generating personalized marketing content"},
                {"role": "user", "content": prompt}],
            max_tokens=350,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

    if response.choices[0]:                                         # type: ignore
        output = response.choices[0].message['content']             # type: ignore
        return output
    else:
        st.error("Sorry, OpenAI didn't provide an answer.")

def main():
    try:
        if st.button("Generate", type="primary"):
            # Ensure all required inputs are provided
            if goal and context and platform and (content_type != None) and (content_level != None):  # type: ignore

                if (content_type != "Image (Coming Soon!)"):
                    # Construct the dynamic prompt based on user inputs
                    prompt = (
                        "Generate a " + str(content_type) + " for a post related to the " + str(context) +  # type: ignore
                        ". The goal of the post is " + str(goal) + ". Provide the content in only " + 
                        str(output_size) + " words. The " + str(content_type) + 
                        " will be posted on the platform " + str(platform) + 
                        ". Constraint: Provide content according to the prompt, no explanations or descriptions. "
                        "Give only the content in " + str(output_size) + " words."
                    )

                    output = load_model(prompt)

                    st.success("Here is Your Generated Content")
                    st.toast('Content Generated Successfully')
                    st.balloons()

                    container = st.container(border=True)
                    output2 = content_type + " in " + str(output_size) + " words."
                    container.subheader(output2)
                    container.write(output)

                else:
                    st.error("Can't Generate Image!, Select other Content Type")
                    st.toast('Image Generation is not Supported Yet!', icon='🚫')

            else:
                st.error("Enter Data Completely")
                st.toast('Fill All Values Completely', icon='🚫')

    except Exception as e:
        print(e)
        st.error("Sorry, the model didn't want to answer that!")

# footer_html = """<div style='text-align: center;'>
#   <p>Developed with ❤️ by Team SAS Alliance</p>
# </div>"""

# st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
