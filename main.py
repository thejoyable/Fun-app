import streamlit as st
import re
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize, sent_tokenize
import random


def fix_punctuation_spacing(text):
    """
    Remove extra spaces before and after punctuation marks.
    Fixes issues like: "my name is don . Hey" -> "my name is don. Hey"
    """
    # Remove spaces before punctuation (.,!?;:)
    text = re.sub(r'\s+([.,!?;:\'")\]])', r'\1', text)
    
    # Remove spaces after opening punctuation (['"(])
    text = re.sub(r'([\["\'\(])\s+', r'\1', text)
    
    # Ensure single space after sentence-ending punctuation
    text = re.sub(r'([.!?])\s*', r'\1 ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Clean up any trailing/leading whitespace
    text = text.strip()
    
    return text


def add_sentence_variety(text):
    """
    Add natural sentence length variation to avoid AI detection patterns.
    AI-generated text often has uniform sentence lengths.
    """
    sentences = sent_tokenize(text)
    varied_sentences = []
    
    for i, sent in enumerate(sentences):
        words = sent.split()
        # Randomly combine short sentences or split long ones
        if len(words) < 8 and i < len(sentences) - 1 and random.random() > 0.6:
            # Occasionally combine with next sentence using transition
            transitions = ['moreover', 'additionally', 'furthermore', 'likewise']
            varied_sentences.append(sent.rstrip('.') + ', ' + random.choice(transitions).lower())
        else:
            varied_sentences.append(sent)
    
    return ' '.join(varied_sentences)


def add_perplexity_variations(text):
    """
    Increase perplexity (word unpredictability) to make text less AI-detectable.
    This adds natural variations in word choice.
    """
    # Add occasional contractions for naturalness
    contractions = {
        'is not': "isn't", 'are not': "aren't", 'was not': "wasn't",
        'were not': "weren't", 'have not': "haven't", 'has not': "hasn't",
        'had not': "hadn't", 'will not': "won't", 'would not': "wouldn't",
        'do not': "don't", 'does not': "doesn't", 'did not': "didn't",
        'cannot': "can't", 'could not': "couldn't", 'should not': "shouldn't"
    }
    
    for formal, informal in contractions.items():
        # Randomly apply contractions (50% chance for more natural feel)
        if random.random() > 0.5:
            text = re.sub(r'\b' + formal + r'\b', informal, text, flags=re.IGNORECASE)
    
    return text


def remove_ai_patterns(text):
    """
    Remove common AI-generated text patterns that trigger detection.
    """
    # Reduce repetitive starting patterns
    text = re.sub(r'\b(In conclusion|To summarize|In summary|Overall),?\s+', '', text, flags=re.IGNORECASE)
    
    # Remove overly formal academic hedging
    text = re.sub(r'\b(It is important to note that|It should be noted that)\b', '', text, flags=re.IGNORECASE)
    
    # Reduce excessive use of "the fact that"
    text = re.sub(r'\bthe fact that\b', 'that', text, flags=re.IGNORECASE)
    
    return text


def enhance_readability(text):
    """
    Improve readability by breaking overly long sentences and fixing flow.
    """
    sentences = sent_tokenize(text)
    enhanced = []
    
    for sent in sentences:
        words = sent.split()
        # Split very long sentences (>30 words)
        if len(words) > 30:
            # Find a natural breaking point (coordinating conjunctions)
            for i, word in enumerate(words):
                if word.lower() in ['and', 'but', 'or', 'so', 'yet'] and i > 15:
                    first_part = ' '.join(words[:i]) + '.'
                    second_part = ' '.join(words[i+1:])
                    enhanced.extend([first_part, second_part])
                    break
            else:
                enhanced.append(sent)
        else:
            enhanced.append(sent)
    
    return ' '.join(enhanced)


def advanced_humanize_pipeline(text, use_passive, use_synonyms, humanizer):
    """
    Advanced humanization pipeline combining multiple techniques.
    """
    # Step 1: Original humanization
    text = humanizer.humanize_text(text, use_passive=use_passive, use_synonyms=use_synonyms)
    
    # Step 2: Add sentence variety
    text = add_sentence_variety(text)
    
    # Step 3: Increase perplexity with natural variations
    text = add_perplexity_variations(text)
    
    # Step 4: Remove AI detection patterns
    text = remove_ai_patterns(text)
    
    # Step 5: Enhance readability
    text = enhance_readability(text)
    
    # Step 6: Fix punctuation spacing (YOUR REQUESTED FIX)
    text = fix_punctuation_spacing(text)
    
    return text


def main():
    """
    Enhanced Streamlit app for transforming AI-generated text into human-like academic writing.
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

    # Caption / footer line
    st.caption("Made with and assembled by joy 💫")

    # --- Custom CSS for styling ---
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            margin-top: 0.5em;
        }
        .intro {
            text-align: left;
            line-height: 1.6;
            margin-bottom: 1.2em;
        }
        .feature-badge {
            display: inline-block;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            margin: 2px;
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
        <p><b>🚀 Enhanced AI Humanizer with Advanced Features:</b><br>
        • <span class='feature-badge'>NEW</span> Fix punctuation spacing issues automatically<br>
        • <span class='feature-badge'>NEW</span> Add sentence variety to avoid detection<br>
        • <span class='feature-badge'>NEW</span> Increase perplexity with natural variations<br>
        • <span class='feature-badge'>NEW</span> Remove common AI writing patterns<br>
        • Expand contractions & add academic transitions<br>
        • Optional passive voice transformation<br>
        • Optional synonym replacement for formal tone<br>
        • Enhanced readability optimization</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for advanced options
    with st.sidebar:
        st.header("⚙️ Transformation Settings")
        
        # Basic options
        use_passive = st.checkbox("Enable Passive Voice Transformation", value=False, 
                                   help="Converts some active sentences to passive voice for academic tone")
        use_synonyms = st.checkbox("Enable Synonym Replacement", value=False,
                                    help="Replaces words with more formal synonyms")
        
        st.markdown("---")
        st.subheader("🔧 Advanced Options")
        
        # Advanced options
        fix_spacing = st.checkbox("Fix Punctuation Spacing", value=True,
                                  help="Removes extra spaces before/after punctuation marks")
        add_variety = st.checkbox("Add Sentence Variety", value=True,
                                  help="Varies sentence length to appear more natural")
        add_perplexity = st.checkbox("Increase Perplexity", value=True,
                                     help="Adds natural variations to avoid AI detection")
        remove_patterns = st.checkbox("Remove AI Patterns", value=True,
                                      help="Eliminates common AI-generated text patterns")
        enhance_read = st.checkbox("Enhance Readability", value=True,
                                   help="Breaks long sentences for better flow")
        
        # Transformation strength
        st.markdown("---")
        strength = st.slider("Transformation Strength", 0.0, 1.0, 0.5,
                            help="Higher = more aggressive humanization")

    # Text input
    user_text = st.text_area("Enter your text here:", height=200,
                            placeholder="Paste your AI-generated text here...")

    # File upload
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # Transform button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        transform_button = st.button("🎯 Transform to Human Writing", use_container_width=True)

    if transform_button:
        if not user_text.strip():
            st.warning("⚠️ Please enter or upload some text to transform.")
        else:
            with st.spinner("🔄 Transforming text with advanced AI humanization..."):
                # Input stats
                input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # Initialize humanizer with adjusted probabilities based on strength
                humanizer = AcademicTextHumanizer(
                    p_passive=0.2 + (strength * 0.3),
                    p_synonym_replacement=0.2 + (strength * 0.3),
                    p_academic_transition=0.3 + (strength * 0.4)
                )

                # Apply transformations based on user selections
                if add_variety or add_perplexity or remove_patterns or enhance_read:
                    transformed = advanced_humanize_pipeline(user_text, use_passive, use_synonyms, humanizer)
                else:
                    transformed = humanizer.humanize_text(user_text, use_passive=use_passive, use_synonyms=use_synonyms)
                
                # Apply punctuation spacing fix if enabled
                if fix_spacing:
                    transformed = fix_punctuation_spacing(transformed)

                # Display results
                st.success("✅ Transformation Complete!")
                
                # Output in expandable section
                with st.expander("📄 Transformed Text", expanded=True):
                    st.write(transformed)
                
                # Download button
                st.download_button(
                    label="📥 Download Transformed Text",
                    data=transformed,
                    file_name="humanized_text.txt",
                    mime="text/plain"
                )

                # Statistics comparison
                output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                # Display stats in columns
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Input Words", input_word_count)
                with col2:
                    st.metric("Output Words", output_word_count, 
                             delta=output_word_count - input_word_count)
                with col3:
                    st.metric("Input Sentences", input_sentence_count)
                with col4:
                    st.metric("Output Sentences", output_sentence_count,
                             delta=output_sentence_count - input_sentence_count)

    # Footer with tips
    st.markdown("---")
    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        **For Academic Writing:**
        - Enable passive voice transformation
        - Enable synonym replacement
        - Set transformation strength to 0.6-0.8
        
        **For Natural Casual Writing:**
        - Keep passive voice disabled
        - Enable perplexity increase
        - Set transformation strength to 0.3-0.5
        
        **To Avoid AI Detection:**
        - Enable all advanced options
        - Use transformation strength 0.7-1.0
        - Run the text through multiple times if needed
        
        **Punctuation Fix:**
        - Automatically removes spaces like "word ." → "word."
        - Fixes apostrophes: "don ' t" → "don't"
        - Normalizes spacing around all punctuation marks
        """)


if __name__ == "__main__":
    main()
