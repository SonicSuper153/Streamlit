import streamlit as st
from pytube import YouTube
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_url):
    yt = YouTube(video_url)
    transcript = ""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_url)
    except:
        st.error("Could not fetch the transcript. Ensure the video has English captions.")
    return transcript


qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')



st.title('YouTube Transcript Q&A')

video_url = st.text_input('Enter YouTube video URL:')

if st.button('Fetch Transcript'):
    if video_url:
        transcript = get_transcript(video_url)
        if transcript:
            st.subheader('Transcript')
            st.text_area('Transcript', value=transcript, height=300)
    else:
        st.error("Please enter a YouTube video URL.")

question = st.text_input('Enter your question:')

if st.button('Get Answer'):
    if video_url and transcript:
        context = transcript
        result = qa_pipeline(question=question, context=context)
        answer = result['answer']

        st.subheader('Answer')
        st.write(answer)
    else:
        st.error("Please fetch the transcript first.")

