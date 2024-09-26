# phidata-youtube-summarizer

A Streamlit application that generates summaries of YouTube videos using various language models powered by Groq.

## Features

- Summarize YouTube videos by providing their URLs
- Choose from multiple language models (llama-3.1-70b-versatile, llama-3.1-8b-instant, llama3-70b-8192, gemma2-9b-it, mixtral-8x7b-32768)
- Adjust the chunk size for processing video captions
- Support for different input and output languages
- Ability to summarize longer videos by processing them in multiple chunks
- Display video metadata and captions

## Requirements

- rye
- Python 3.8+
- Streamlit
- phidata library
- python-dotenv
- groq API-KEY

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   rye sync
   ```
3. Set up your environment variables in a `.env` file (see `.env.sample` for reference)
4. Get your own groq API-KEY and paste it on the `.env` file

## Usage

1. Run the Streamlit app:
   ```
   rye run streamlit run src/app.py
   ```
2. Open the provided URL in your web browser
3. Enter a YouTube video URL in the sidebar
4. Select your desired language model and settings
5. Click "Generate Summary" to process the video and view the results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [LICENSE](LICENSE) file.

## Acknowledgements

This project is built using [phidata](https://github.com/phidatahq/phidata) and powered by Groq language models.
