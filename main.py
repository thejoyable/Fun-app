import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize



def main():
    """
    The `main` function sets up a Streamlit page for transforming user-provided text into a more formal
    academic style by expanding contractions, adding academic transitions, and optionally converting
    sentences to passive voice or replacing words with synonyms.
    """
    # Download NLTK resources if needed
    download_nltk_resources()

    # Configure Streamlit page
    st.set_page_config(
        page_title="From AI to Human Written For Soumya ka dost... 😂😁 ",
        page_icon="😂",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Made with and Assembled by JOY': "# Made with and Assembled by JOY'!!!!!! YAYYYY"
        }
    )

    # --- Custom CSS for Title Centering and Additional Styling ---
    st.markdown(
        """
        <style>
        /* Center the main title */
        .title {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            margin-top: 0.5em;
        }
        /* Center the subtitle / introduction block */
        .intro {
            text-align: left;
            line-height: 1.6;
            margin-bottom: 1.2em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Title / Intro ---
    st.markdown("<div class='title'>🧔🏻‍♂️Humanize AI🤖 Generated text</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='intro'>
        <p><b>This app transforms your text into a more formal academic style by:<b><br>
        • Expanding contractions<br>
        • Adding academic transitions<br>
        • <em>Optionally</em> converting some sentences to passive voice<br>
        • <em>Optionally</em> replacing words with synonyms for a more formal tone.</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Checkboxes
    use_passive = st.checkbox("Enable Passive Voice Transformation", value=False)
    use_synonyms = st.checkbox("Enable Synonym Replacement", value=False)

    # Text input
    user_text = st.text_area("Enter your text here:")

    # File upload
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # Button
    if st.button("Transform to Academic Style"):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Transforming text..."):
                # Input stats
                input_word_count = len(word_tokenize(user_text,language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # Transform
                humanizer = AcademicTextHumanizer(
                    p_passive=0.3,
                    p_synonym_replacement=0.3,
                    p_academic_transition=0.4
                )
                transformed = humanizer.humanize_text(
                    user_text,
                    use_passive=use_passive,
                    use_synonyms=use_synonyms
                )

                # Output
                st.subheader("Transformed Text:")
                st.write(transformed)

                # Output stats
                output_word_count = len(word_tokenize(transformed,language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                st.markdown(
                    f"**Input Word Count**: {input_word_count} "
                    f"| **Sentence Count**: {input_sentence_count}  "
                    f"| **Output Word Count**: {output_word_count} "
                    f"| **Sentence Count**: {output_sentence_count}"
                )

    st.markdown("---")


if __name__ == "__main__":
    main()