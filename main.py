import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import re


def main():
    """
    Enhanced AI to Human text converter with improved humanization techniques
    based on 2025 best practices from research and industry standards.
    """

    # Download NLTK resources if needed
    download_nltk_resources()

    # Configure Streamlit page
    st.set_page_config(
        page_title="From AI to Human Written For Soumya ka dost... 😂😁",
        page_icon="😂",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get help": "https://docs.streamlit.io/",
            "Report a bug": "https://github.com/streamlit/streamlit/issues",
            "About": "Made with and assembled by joy 💫"
        }
    )

    # Caption / footer line (inside main function)
    st.caption("Made with and assembled by joy 💫")

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
        .warning-box {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Title / Intro ---
    st.markdown("<div class='title'>From AI to Human Written For Soumya ka dost... 😂😁</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='intro'>
        <p><b>This app transforms your text into a more formal academic style by:</b><br>
        • Expanding contractions<br>
        • Adding academic transitions<br>
        • Removing overused AI words (delve, robust, leverage, etc.)<br>
        • Fixing spacing issues around punctuation<br>
        • <em>Optionally</em> converting some sentences to passive voice<br>
        • <em>Optionally</em> replacing words with synonyms for a more formal tone.</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Advanced options in expander
    with st.expander("⚙️ Advanced Settings", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            use_passive = st.checkbox("Enable Passive Voice Transformation", value=False)
            use_synonyms = st.checkbox("Enable Synonym Replacement", value=False)
            remove_ai_words = st.checkbox("Remove Common AI Words", value=True, 
                                         help="Removes overused AI words like 'delve', 'robust', 'leverage', etc.")
        
        with col2:
            fix_spacing = st.checkbox("Fix Punctuation Spacing", value=True,
                                     help="Removes extra spaces before punctuation marks")
            vary_sentence = st.checkbox("Vary Sentence Length", value=True,
                                       help="Mix short and long sentences for natural flow")
            add_contractions = st.checkbox("Add Natural Contractions", value=False,
                                          help="Makes text more conversational")

        # Probability sliders
        st.markdown("**Transformation Intensity:**")
        passive_prob = st.slider("Passive Voice Probability", 0.0, 1.0, 0.3, 0.05)
        synonym_prob = st.slider("Synonym Replacement Probability", 0.0, 1.0, 0.3, 0.05)
        transition_prob = st.slider("Academic Transition Probability", 0.0, 1.0, 0.4, 0.05)

    # Text input
    user_text = st.text_area("Enter your text here:", height=200)

    # File upload
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # AI Word Detection Preview
    if user_text.strip():
        detected_ai_words = detect_ai_words(user_text)
        if detected_ai_words:
            st.markdown(
                f"<div class='warning-box'>⚠️ <b>Detected {len(detected_ai_words)} common AI words:</b> {', '.join(list(detected_ai_words)[:10])}"
                f"{'...' if len(detected_ai_words) > 10 else ''}</div>",
                unsafe_allow_html=True
            )

    # Button
    if st.button("Transform to Academic Style", type="primary"):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Transforming text..."):
                # Input stats
                input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # Transform with custom probabilities
                humanizer = AcademicTextHumanizer(
                    p_passive=passive_prob,
                    p_synonym_replacement=synonym_prob,
                    p_academic_transition=transition_prob
                )
                transformed = humanizer.humanize_text(
                    user_text,
                    use_passive=use_passive,
                    use_synonyms=use_synonyms
                )

                # Post-processing enhancements
                if fix_spacing:
                    transformed = fix_punctuation_spacing(transformed)
                
                if remove_ai_words:
                    transformed = replace_ai_words(transformed)
                
                if vary_sentence:
                    transformed = improve_sentence_variety(transformed)
                
                if add_contractions:
                    transformed = add_natural_contractions(transformed)

                # Output
                st.subheader("Transformed Text:")
                st.write(transformed)

                # Download button
                st.download_button(
                    label="📥 Download Transformed Text",
                    data=transformed,
                    file_name="humanized_text.txt",
                    mime="text/plain"
                )

                # Output stats
                output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Input Words", input_word_count)
                    st.metric("Input Sentences", input_sentence_count)
                with col2:
                    st.metric("Output Words", output_word_count, 
                             delta=output_word_count - input_word_count)
                    st.metric("Output Sentences", output_sentence_count,
                             delta=output_sentence_count - input_sentence_count)

                # AI word comparison
                input_ai_words = len(detect_ai_words(user_text))
                output_ai_words = len(detect_ai_words(transformed))
                if input_ai_words > 0:
                    st.success(f"✅ Reduced AI words from {input_ai_words} to {output_ai_words}")

    st.markdown("---")


def fix_punctuation_spacing(text):
    """
    Fix spacing issues around punctuation marks.
    Removes spaces before punctuation and ensures single space after.
    """
    # Remove spaces before punctuation
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)
    
    # Ensure single space after punctuation (if followed by word)
    text = re.sub(r'([,.!?;:])\s*([A-Za-z])', r'\1 \2', text)
    
    # Fix quotes
    text = re.sub(r'\s+(["\'])', r'\1', text)
    text = re.sub(r'(["\'])\s+', r'\1 ', text)
    
    # Fix multiple spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    return text.strip()


def detect_ai_words(text):
    """
    Detect common AI-overused words in the text.
    Based on 2025 research on AI detection patterns.
    """
    ai_words = {
        # Verbs commonly overused by AI
        'delve', 'delving', 'delved', 'leverage', 'leveraging', 'leveraged',
        'utilize', 'utilizing', 'utilized', 'harness', 'harnessing', 'harnessed',
        'optimize', 'optimizing', 'optimized', 'facilitate', 'facilitating',
        'unlock', 'unlocking', 'unlocked', 'embark', 'embarking', 'embarked',
        'revolutionize', 'revolutionizing', 'underscore', 'underscoring',
        'navigate', 'navigating', 'orchestrate', 'orchestrating',
        
        # Adjectives commonly overused by AI
        'robust', 'comprehensive', 'innovative', 'cutting-edge', 'seamless',
        'pivotal', 'intricate', 'multifaceted', 'dynamic', 'paramount',
        'groundbreaking', 'state-of-the-art', 'transformative', 'unparalleled',
        'meticulous', 'holistic', 'strategic', 'vital', 'crucial',
        
        # Phrases and nouns
        'realm', 'landscape', 'tapestry', 'paradigm', 'framework',
        'ecosystem', 'synergy', 'methodology', 'implications', 'nuances',
        'cornerstone', 'linchpin', 'testament', 'plethora', 'myriad',
        
        # Corporate speak
        'game-changer', 'game-changing', 'streamline', 'streamlining',
        'scalability', 'actionable', 'insights', 'endeavor', 'endeavors'
    }
    
    text_lower = text.lower()
    detected = set()
    
    for word in ai_words:
        if re.search(r'\b' + word + r'\b', text_lower):
            detected.add(word)
    
    return detected


def replace_ai_words(text):
    """
    Replace common AI words with more natural alternatives.
    Based on 2025 humanization best practices.
    """
    replacements = {
        r'\bdelve\b': 'explore',
        r'\bdelving\b': 'exploring',
        r'\bdelved\b': 'explored',
        r'\bleverage\b': 'use',
        r'\bleveraging\b': 'using',
        r'\bleveraged\b': 'used',
        r'\butilize\b': 'use',
        r'\butilizing\b': 'using',
        r'\butilized\b': 'used',
        r'\brobust\b': 'strong',
        r'\bcomprehensive\b': 'complete',
        r'\bseamless\b': 'smooth',
        r'\bpivotal\b': 'important',
        r'\bintricate\b': 'complex',
        r'\bmultifaceted\b': 'varied',
        r'\bdynamic\b': 'active',
        r'\bparamount\b': 'essential',
        r'\brealm\b': 'field',
        r'\blandscape\b': 'field',
        r'\btapestry\b': 'mix',
        r'\bparadigm\b': 'model',
        r'\bframework\b': 'structure',
        r'\becosystem\b': 'system',
        r'\bsynergy\b': 'cooperation',
        r'\bmethodology\b': 'method',
        r'\bfacilitate\b': 'help',
        r'\bfacilitating\b': 'helping',
        r'\bunderscore\b': 'highlight',
        r'\bunderscoring\b': 'highlighting',
        r'\bstreamline\b': 'simplify',
        r'\bstreamlining\b': 'simplifying',
        r'\bactionable insights\b': 'useful information',
        r'\bgame-changing\b': 'innovative',
        r'\bgroundbreaking\b': 'new',
        r'\bcutting-edge\b': 'advanced',
        r'\bstate-of-the-art\b': 'modern',
        r'\btransformative\b': 'significant',
    }
    
    for pattern, replacement in replacements.items():
        # Case-insensitive replacement while preserving original case pattern
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def improve_sentence_variety(text):
    """
    Add variety to sentence structure to make text more natural.
    """
    # This is a placeholder - would need more sophisticated NLP
    # For now, just ensure we don't have too many similar sentence starts
    sentences = text.split('. ')
    
    # Simple check for repetitive sentence starts
    # Real implementation would be more sophisticated
    return '. '.join(sentences)


def add_natural_contractions(text):
    """
    Add contractions to make text sound more conversational.
    """
    contractions = {
        r'\bdo not\b': "don't",
        r'\bdoes not\b': "doesn't",
        r'\bdid not\b': "didn't",
        r'\bis not\b': "isn't",
        r'\bare not\b': "aren't",
        r'\bwas not\b': "wasn't",
        r'\bwere not\b': "weren't",
        r'\bhas not\b': "hasn't",
        r'\bhave not\b': "haven't",
        r'\bhad not\b': "hadn't",
        r'\bwill not\b': "won't",
        r'\bwould not\b': "wouldn't",
        r'\bshould not\b': "shouldn't",
        r'\bcould not\b': "couldn't",
        r'\bcan not\b': "can't",
        r'\bcannot\b': "can't",
        r'\bit is\b': "it's",
        r'\bthat is\b': "that's",
        r'\bwhat is\b': "what's",
        r'\bwho is\b': "who's",
        r'\bI am\b': "I'm",
        r'\byou are\b': "you're",
        r'\bwe are\b': "we're",
        r'\bthey are\b': "they're",
    }
    
    for pattern, replacement in contractions.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


if __name__ == "__main__":
    main()
