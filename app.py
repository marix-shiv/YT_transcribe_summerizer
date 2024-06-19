import streamlit as st
from dotenv import load_dotenv

load_dotenv() #load all the enviorment variables

import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a youtube video summarizer you will be 
taking the transcript text and summerizing the entire video
 and providing the important summary in points within 350 words and at last add 
 a conclusion.
 Please provide the summary of the text given here: """

#Getting the transcript form YT videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        return e


#Getting the summary based on Google gemini pro 
def generate_gemini_content(transcript_text,prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text



st.title("Youtube Transcript Summarizer")
youtube_link = st.text_input("Enter the Youtube video link")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)
    else:
        st.write("No transcript found for the given video link.")