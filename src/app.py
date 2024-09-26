import streamlit as st
from phi.tools.youtube_tools import YouTubeTools
from assistant import get_chunk_summarizer, get_video_summarizer  # type: ignore
from dotenv import load_dotenv

# Read the .env file
load_dotenv()

st.set_page_config(
    page_title="Youtube Video Summaries",
    page_icon=":orange_heart:",
)
st.title("Youtube Video Summaries powered by Groq")
st.markdown("##### :orange_heart: built using [phidata](https://github.com/phidatahq/phidata)")

def main() -> None:
    # Get model
    llm_model = st.sidebar.selectbox(
        "Select Model", options=["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "gemma2-9b-it", "mixtral-8x7b-32768"]
    )
    # Set assistant_type in session state
    if "llm_model" not in st.session_state:
        st.session_state["llm_model"] = llm_model
    elif st.session_state["llm_model"] != llm_model:
        st.session_state["llm_model"] = llm_model
        st.rerun()

    # Get chunker limit
    chunker_limit = st.sidebar.slider(
        ":heart_on_fire: Words in chunk",
        min_value=1000,
        max_value=10000,
        value=4500,
        step=500,
        help="Set the number of characters to chunk the text into.",
    )

    # Get video url
    video_url = st.sidebar.text_input(":video_camera: Video URL")

    language_dict = {
        'English': 'en',
        '日本語': 'ja'
    }
    language_options = []
    for language in language_dict.keys():
        language_options.append(language)

    # Get input language selection
    video_language = st.sidebar.selectbox(
        "Video Language", options=language_options
    )

    # Get output language selection
    language_to_translate = st.sidebar.selectbox(
        "Translate into :", options=language_options
    )

    generate_report = st.sidebar.button("Generate Summary")
    if generate_report:
        st.session_state["youtube_url"] = video_url

    if "youtube_url" in st.session_state:
        _url = st.session_state["youtube_url"]
        youtube_tools = YouTubeTools(languages=[language_dict[video_language]])
        video_captions = None
        video_summarizer = get_video_summarizer(model=llm_model, language=language_to_translate)

        with st.status("Parsing Video", expanded=False) as status:
            with st.container():
                video_container = st.empty()
                video_container.video(_url)

            video_data = youtube_tools.get_youtube_video_data(_url)
            with st.container():
                video_data_container = st.empty()
                video_data_container.json(video_data)
            status.update(label="Video", state="complete", expanded=False)

        with st.status("Reading Captions", expanded=False) as status:
            video_captions = youtube_tools.get_youtube_video_captions(_url)
            with st.container():
                video_captions_container = st.empty()
                video_captions_container.write(video_captions)
            status.update(label="Captions processed", state="complete", expanded=False)

        if not video_captions:
            st.write("Sorry could not parse video. Please try again or use a different video.")
            return

        chunks = []
        num_chunks = 0

        words = video_captions.split()
        for i in range(0, len(words), chunker_limit):
            num_chunks += 1
            chunks.append(" ".join(words[i : (i + chunker_limit)]))

        if num_chunks > 1:
            chunk_summaries = []
            for i in range(num_chunks):
                with st.status(f"Summarizing chunk: {i+1}", expanded=False) as status:
                    chunk_summary = ""
                    chunk_container = st.empty()
                    chunk_summarizer = get_chunk_summarizer(model=llm_model, language=video_language)
                    chunk_info = f"Video data: {video_data}\n\n"
                    chunk_info += f"{chunks[i]}\n\n"
                    for delta in chunk_summarizer.run(chunk_info):
                        chunk_summary += delta  # type: ignore
                        chunk_container.markdown(chunk_summary)
                    chunk_summaries.append(chunk_summary)
                    status.update(label=f"Chunk {i+1} summarized", state="complete", expanded=False)

            with st.spinner("Generating Summary"):
                summary = ""
                summary_container = st.empty()
                video_info = f"Video URL: {_url}\n\n"
                video_info += f"Video Data: {video_data}\n\n"
                video_info += "Summaries:\n\n"
                for i, chunk_summary in enumerate(chunk_summaries, start=1):
                    video_info += f"Chunk {i}:\n\n{chunk_summary}\n\n"
                    video_info += "---\n\n"

                for delta in video_summarizer.run(video_info):
                    summary += delta  # type: ignore
                    summary_container.markdown(summary)
        else:
            with st.spinner("Generating Summary"):
                summary = ""
                summary_container = st.empty()
                video_info = f"Video URL: {_url}\n\n"
                video_info += f"Video Data: {video_data}\n\n"
                video_info += f"Captions: {video_captions}\n\n"

                for delta in video_summarizer.run(video_info):
                    summary += delta  # type: ignore
                    summary_container.markdown(summary)
    else:
        st.write("Please provide a video URL or click on one of the trending videos.")

    st.sidebar.markdown("---")
    if st.sidebar.button("Restart"):
        st.rerun()

main()