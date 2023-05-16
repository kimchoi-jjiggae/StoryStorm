
import os
# from elevenlabs import generate, play

import replicate
import streamlit as st
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
# from elevenlabs import generate, play


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
eleven_api_key = os.getenv("ELEVEN_API_KEY")

llm = OpenAI(temperature=0.9)

def generate_story(text):
    """Generate a story using the langchain library and OpenAI's GPT-3 model."""
    prompt = PromptTemplate(
        input_variables=["text"],
        template=""" 
        You are a female asian with this resume: MICHELLE E. CHOI 
choi.michelle.12@gmail.com ⋅ (310)-775-7048 

EDUCATION 
Harvard University, Cambridge, MA 
A.B., Fall 2016. Major: Organismic & Evolutionary Biology. Minor: Computer Science. GPA: 3.99. Summa cum laude. Phi Beta Kappa, Harvard-Radcliffe chapter. 

Harvard Business School, Cambridge MA. Class of 2023, on leave for career opportunities.		

EDUCATION 
Blockchain Non-Profit Consulting: Freelance					          January 2021 - August 2022
Launched non-profit fundraiser for a museum (The Lobkowicz Collections), by hosting a conference & digital art gallery in Prague Castle. Digital art sales generated sufficient revenue to fund 7 years of restoration ($300k). Managed & recruited 5-person team to deploy PR (published in Bloomberg, Decrypt, Coindesk, CNBC), social media (Discord, Twitter, Instagram), and technical implementation (e.g. customized SmartContracts via Manifold, platform interfacing & pricing with SuperRare & OpenSea). Invited to speak on Laura Shin’s Unchained & at Harvard Blockchain Conference.

Detect										     August 2020 - December 2020 Product Manager 
Led product development of a molecular COVID-19 diagnostic test intended for at-home use. Drove regulatory, clinical,  quality, software, hardware, supply chain, R&D (e.g. assay) and commercial teams to build a product in pursuit of FDA  Emergency Use Authorization. Built distributed workstreams to enable scaled usability testing of software and hardware. 

Verily Life Sciences/Google Health 							July 2018 - August 2020 
     Product Manager 
Managed infrastructure software development on the Automatic Retinal Disease Assessment team, which has launched a  machine learning (ML) model to detect diseases that cause preventable blindness in India, Thailand & the EU. Developed and executed roadmaps for regulatory approval (CE and FDA) of ML models and other Class 1 & 2 medical devices. Led partnerships with commercial and university partners to launch tele-medicine screening pilots in the US and the UK. Drove shared ML labeling infrastructure product development (e.g. analysis tooling, databases) across Google Brain, Verily, and Deepmind engineering teams. Team transferred from Verily to Google Health’s artificial intelligence division in 2020.

Google 											August 2017 - July 2018 
Associate Product Manager 
Managed product development of the Google Maps initiative to surface events (e.g. parades, concerts) to users. Designed and drove implementation of software architecture to auto-moderate event content (e.g. photos) submitted by users to the Maps database. Launched iOS & Android features to enrich users’ experiences with events (e.g. sharing, navigation).

Google  											Summer 2016 
Associate Product Manager Intern 
Rebuilt the user communication system on Project Fi, Google’s mobile virtual network operator. Developed a system to dynamically generate previously static Android & web notifications, increasing the flexibility & efficiency of alerts & billing.

The Westly Group 										Summer 2015 
Venture Summer Intern 
Analyzed the product viability and industry fit of prospective cleantech companies after sourcing and evaluation.

Formlabs 3D Printing Company  								2014-2015 	
Marketing Summer Intern and Part-Time Associate 
Restructured Formlabs’ AdWords strategy to reduce CPA of printer sales by 5-fold in 2 months.

Harvard College Mentors for Urban Debate 							2012-2016 	Founder and President 
Developed accessible mentorship for urban high schoolers by launching debate programs in Boston & Asia. 

SKILLS 
Technical: C, PHP/MySQL, HTML, CSS, React, JavaScript, D3, Python, TypeScript, Matlab, Solidity.
Language: Proficiency in Spanish (focus in medical Spanish developed during clinical shadowing work in Chile) & Korean.
 
        Generate a script to answer this interview question about your background: {text}.
                 """
    )
    story = LLMChain(llm=llm, prompt=prompt)
    return story.run(text=text)


def generate_audio(text):
    """Convert the generated story to audio using the Eleven Labs API."""
    # audio = generate(text=text, voice=voice, api_key=eleven_api_key)
    import requests

    # streaming chunk size
    CHUNK_SIZE = 1024

    XI_API_KEY = "52595903f763f2b4f5e0d520a225b018"


    url = "https://api.elevenlabs.io/v1/text-to-speech/W9AqZKoLZscRHWjcPSkk"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": XI_API_KEY
    }

    data = {
    "text": text,
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
    }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    # return audio


def generate_images(story_text):
    """Generate images using the story text using the Replicate API."""
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={"prompt": story_text}
    )
    return output


def app():
    st.title("Story Storm")

    with st.form(key='my_form'):
        text = st.text_input(
            "Enter a word to generate a story",
            max_chars=None,
            type="default",
            placeholder="What would you like to ask Michelle",
        )
        options = ["Michelle", "Antoni", "Arnold", "Adam", "Domi", "Elli", "Josh", "Rachel", "Sam"]
        voice = st.selectbox("Select a voice", options)

        if st.form_submit_button("Submit"):
            with st.spinner('Generating answer...'):
                story_text = generate_story(text)
                print(story_text)
                generate_audio(story_text)

            st.audio('./output.mp3', format='audio/mp3')
            images = generate_images(story_text)
            for item in images:
                st.image(item)

    if not text or not voice:
        st.info("Please enter a word and select a voice")


if __name__ == '__main__':
    app()