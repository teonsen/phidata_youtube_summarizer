from textwrap import dedent
from phi.llm.groq import Groq
from phi.assistant import Assistant

def get_chunk_summarizer(
    model: str = "llama-3.1-70b-versatile",
    language: str = "English",
    debug_mode: bool = True,
) -> Assistant:
    """Get a Groq Research Assistant."""

    instructions = [
        "You will be provided with a youtube video transcript.",
        "Carefully read the transcript a prepare thorough report of key facts and details.",
        "Provide as many details and facts as possible in the summary.",
        "Your report will be used to generate a final New York Times worthy report.",
        "Give the section relevant titles and provide details/facts/processes in each section.",
        "REMEMBER: you are writing for the New York Times, so the quality of the report is important.",
        "Make sure your report is properly formatted and follows the <report_format> provided below.",
    ]
    #if language != "English":
    #    instructions.append(f"DO NOT FORGET: Translate the report into {language}.")

    if language == "日本語":
        instructions = [
            "あなたにはYouTube動画のトランスクリプトが提供されます。",
            "トランスクリプトを注意深く読み、重要な事実や詳細を含む徹底的なレポートを作成してください。",
            "可能な限り多くの詳細と事実を要約に含めてください。",
            "あなたのレポートは最終的なニューヨークタイムズにふさわしいレポートを生成するために使用されます。",
            "セクションに関連するタイトルを付け、それぞれのセクションに詳細/事実/プロセスを提供してください。",
            "ニューヨークタイムズのために執筆していることを忘れないでください。レポートの質が重要です。",
            "レポートが適切にフォーマットされ、以下の<report_format>に従っていることを確認してください。",
        ]

    return Assistant(
        name="groq_youtube_pre_processor",
        llm=Groq(model=model),
        description="You are a Senior NYT Reporter tasked with summarizing a youtube video.",
        instructions=instructions,
        add_to_system_prompt=dedent(
            """<report_format>
            ### Overview
            {give an overview of the video}

            ### Section 1
            {provide details/facts/processes in this section}

            ... more sections as necessary...

            ### Takeaways
            {provide key takeaways from the video}
            </report_format>"""
        ),
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )

def get_video_summarizer(
    model: str = "llama-3.1-70b-versatile",
    language: str = "English",
    debug_mode: bool = True,
) -> Assistant:
    """Get a Groq Research Assistant."""

    instructions = [
        "You will be provided with:",
        "  1. Youtube video link and information about the video",
        "  2. Pre-processed summaries from junior researchers.",
        "Carefully process the information and think about the contents",
        "Then generate a final New York Times worthy report in the <report_format> provided below.",
        "Make your report engaging, informative, and well-structured.",
        "Break the report into sections and provide key takeaways at the end.",
        "Make sure the title is a markdown link to the video.",
        "Give the section relevant titles and provide details/facts/processes in each section.",
        "REMEMBER: you are writing for the New York Times, so the quality of the report is important.",
    ]

    # This does not work propery.
    #if language != "English":
    #    instructions.append(f"DO NOT FORGET: Translate the report into {language}.")

    # Works well
    if language == "日本語":
        instructions = [
            "あなたには以下が提供されます:",
            "  1. YouTube動画のリンクと動画に関する情報",
            "  2. ジュニアリサーチャーからの事前処理された要約",
            "情報を注意深く処理し、内容について考えてください",
            "その後、以下の<report_format>で最終的なニューヨークタイムズにふさわしいレポートを生成してください。",
            "レポートを魅力的で、情報豊かで、よく構成されたものにしてください。",
            "レポートをセクションに分け、最後に重要なポイントを提供してください。",
            "タイトルが動画へのマークダウンリンクであることを確認してください。",
            "セクションに関連するタイトルを付け、それぞれのセクションに詳細/事実/プロセスを提供してください。",
            "ニューヨークタイムズのために執筆していることを忘れないでください。レポートの質が重要です。",
            "レポートは日本語で出力してください。",
        ]

    return Assistant(
        name="groq_video_summarizer",
        llm=Groq(model=model),
        description="You are a Senior NYT Reporter tasked with writing a summary of a youtube video.",
        instructions=instructions,
        add_to_system_prompt=dedent(
            """<report_format>
            ## Video Title with Link
            {this is the markdown link to the video}

            ### Overview
            {give a brief introduction of the video and why the user should read this report}
            {make this section engaging and create a hook for the reader}

            ### Section 1
            {break the report into sections}
            {provide details/facts/processes in this section}

            ... more sections as necessary...

            ### Takeaways
            {provide key takeaways from the video}

            Report generated on: {Month Date, Year (hh:mm AM/PM)}
            </report_format>"""
        ),
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )