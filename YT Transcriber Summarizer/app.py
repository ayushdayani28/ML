import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as yta
# Run the app
# userdata.get('secretName')
from dotenv import load_dotenv
import os
load_dotenv()
import webbrowser

# # Open in Chrome explicitly
# chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# webbrowser.get(chrome_path).open("http://localhost:8501")

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
prompt="You are a youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summaryin points within 200-250 words. Please provide the summary of the text given here:"
def generate_gemini_content(transcript_text, prompt):
  model=genai.GenerativeModel("gemini-pro")
  response=model.generate_content(prompt+transcript_text)
  return response.text

def extract_transcript_details(yt_url):
  try:
    video_id = yt_url.split("=")[1]
    transcript_text = yta.get_transcript(video_id)
    transcript = ""
    for i in transcript_text:
      transcript += " " + i["text"]
    return transcript
  except Exception as e:
    raise e

# The function to run the Streamlit app
def run_app():
    st.title("Youtube Transcript to Detailed Notes Converter")
    youtube_link = st.text_input("Enter Youtube Video Link:")
    
    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)

if __name__ == "__main__":
   run_app()