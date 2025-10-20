import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize
import re


def main():
    """
    Enhanced AI to Human text converter with MAXIMUM humanization effectiveness.
    Uses aggressive parameters optimized for best AI detection bypass based on 2025 research.
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
        .success-box {
            background-color: #d4edda;
            border-left: 4px solid #28a745;
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
        • <em>Aggressively</em> converting sentences to passive voice<br>
        • <em>Extensively</em> replacing words with synonyms for maximum humanization<br>
        • Varying sentence structure for natural flow</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Advanced options in expander (optional toggles only)
    with st.expander("⚙️ Optional Features", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            remove_ai_words = st.checkbox("Remove Common AI Words", value=True, 
                                         help="Removes 50+ overused AI words like 'delve', 'robust', 'leverage'")
            fix_spacing = st.checkbox("Fix Punctuation Spacing", value=True,
                                     help="Removes extra spaces before punctuation marks")
        
        with col2:
            vary_sentence = st.checkbox("Vary Sentence Structure", value=True,
                                       help="Mix sentence lengths for natural flow")
            add_contractions = st.checkbox("Add Natural Contractions", value=True,
                                          help="Makes text more conversational")

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
    if st.button("🚀 Transform to Academic Style", type="primary", use_container_width=True):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Transforming text with maximum humanization..."):
                # Input stats
                input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # MAXIMUM EFFECTIVENESS PARAMETERS - Aggressive mode settings
                # Based on 2025 research: higher probabilities = more aggressive humanization
                humanizer = AcademicTextHumanizer(
                    p_passive=0.7,              # 70% passive voice (aggressive)
                    p_synonym_replacement=0.8,  # 80% synonym replacement (very aggressive)
                    p_academic_transition=0.6   # 60% academic transitions (high)
                )
                
                # Transform with MAXIMUM settings enabled
                transformed = humanizer.humanize_text(
                    user_text,
                    use_passive=True,      # Always enabled for max effect
                    use_synonyms=True      # Always enabled for max effect
                )

                # Post-processing enhancements (always apply if enabled)
                if fix_spacing:
                    transformed = fix_punctuation_spacing(transformed)
                
                if remove_ai_words:
                    transformed = replace_ai_words(transformed)
                
                if vary_sentence:
                    transformed = improve_sentence_variety(transformed)
                
                if add_contractions:
                    transformed = add_natural_contractions(transformed)

                # Final cleanup - ensure no double spaces or punctuation issues
                transformed = final_cleanup(transformed)

                # Output
                st.markdown("<div class='success-box'>✅ <b>Transformation Complete!</b></div>", unsafe_allow_html=True)
                st.subheader("Transformed Text:")
                st.write(transformed)

                # Download button
                st.download_button(
                    label="📥 Download Transformed Text",
                    data=transformed,
                    file_name="humanized_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                # Output stats with better formatting
                output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                st.markdown("---")
                st.subheader("📊 Transformation Statistics")
                
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

                # AI word comparison
                input_ai_words = len(detect_ai_words(user_text))
                output_ai_words = len(detect_ai_words(transformed))
                
                if input_ai_words > 0:
                    reduction_pct = int((1 - output_ai_words/input_ai_words) * 100) if input_ai_words > 0 else 0
                    st.success(f"🎯 AI Word Reduction: {input_ai_words} → {output_ai_words} ({reduction_pct}% reduction)")
                else:
                    st.info("ℹ️ No common AI words detected in input text")

    st.markdown("---")
    st.caption("💡 **Tip:** This tool uses aggressive humanization parameters optimized for maximum effectiveness based on 2025 research.")


def fix_punctuation_spacing(text):
    """
    Fix spacing issues around punctuation marks.
    Removes spaces before punctuation and ensures single space after.
    """
    # Remove spaces before punctuation
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)
    
    # Ensure single space after punctuation (if followed by word)
    text = re.sub(r'([,.!?;:])\s*([A-Za-z])', r'\1 \2', text)
    
    # Fix quotes - remove space before opening quotes and after closing quotes
    text = re.sub(r'\s+(["\'"])', r'\1', text)
    text = re.sub(r'(["\'"])\s+', r'\1 ', text)
    
    # Fix apostrophes - remove spaces around apostrophes in contractions
    text = re.sub(r'\s+\'', r"'", text)
    text = re.sub(r'\'\s+', r"' ", text)
    
    # Fix multiple spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Fix spaces at start/end of lines
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text.strip()


def detect_ai_words(text):
    """
    Detect common AI-overused words in the text.
    Comprehensive list based on 2025 research on AI detection patterns.
    """
    ai_words = {
        # Verbs commonly overused by AI
        'delve', 'delving', 'delved', 'delves',
        'leverage', 'leveraging', 'leveraged', 'leverages',
        'utilize', 'utilizing', 'utilized', 'utilizes', 'utilisation', 'utilization',
        'harness', 'harnessing', 'harnessed', 'harnesses',
        'optimize', 'optimizing', 'optimized', 'optimizes', 'optimisation', 'optimization',
        'facilitate', 'facilitating', 'facilitated', 'facilitates',
        'unlock', 'unlocking', 'unlocked', 'unlocks',
        'embark', 'embarking', 'embarked', 'embarks',
        'revolutionize', 'revolutionizing', 'revolutionized', 'revolutionizes',
        'underscore', 'underscoring', 'underscored', 'underscores',
        'navigate', 'navigating', 'navigated', 'navigates',
        'orchestrate', 'orchestrating', 'orchestrated', 'orchestrates',
        'streamline', 'streamlining', 'streamlined', 'streamlines',
        
        # Adjectives commonly overused by AI
        'robust', 'comprehensive', 'innovative', 'cutting-edge', 'seamless',
        'pivotal', 'intricate', 'multifaceted', 'dynamic', 'paramount',
        'groundbreaking', 'state-of-the-art', 'transformative', 'unparalleled',
        'meticulous', 'holistic', 'strategic', 'vital', 'crucial',
        'noteworthy', 'remarkable', 'significant', 'substantial',
        
        # Phrases and nouns
        'realm', 'landscape', 'tapestry', 'paradigm', 'framework',
        'ecosystem', 'synergy', 'methodology', 'implications', 'nuances',
        'cornerstone', 'linchpin', 'testament', 'plethora', 'myriad',
        'facet', 'facets', 'aspect', 'aspects',
        
        # Corporate speak
        'game-changer', 'game-changing', 'actionable', 'insights', 
        'endeavor', 'endeavors', 'scalability', 'scalable'
    }
    
    text_lower = text.lower()
    detected = set()
    
    for word in ai_words:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            detected.add(word)
    
    return detected


def replace_ai_words(text):
    """
    Replace common AI words with more natural alternatives.
    Comprehensive replacements based on 2025 humanization best practices.
    """
    replacements = {
        # Verbs
        r'\bdelve into\b': 'explore',
        r'\bdelve\b': 'explore',
        r'\bdelving\b': 'exploring',
        r'\bdelved\b': 'explored',
        r'\bdelves\b': 'explores',
        
        r'\bleverage\b': 'use',
        r'\bleveraging\b': 'using',
        r'\bleveraged\b': 'used',
        r'\bleverages\b': 'uses',
        
        r'\butilize\b': 'use',
        r'\butilizing\b': 'using',
        r'\butilized\b': 'used',
        r'\butilizes\b': 'uses',
        r'\butilisation\b': 'use',
        r'\butilization\b': 'use',
        
        r'\bharness\b': 'use',
        r'\bharnessing\b': 'using',
        r'\bharnessed\b': 'used',
        
        r'\boptimize\b': 'improve',
        r'\boptimizing\b': 'improving',
        r'\boptimized\b': 'improved',
        r'\boptimizes\b': 'improves',
        r'\boptimisation\b': 'improvement',
        r'\boptimization\b': 'improvement',
        
        r'\bfacilitate\b': 'help',
        r'\bfacilitating\b': 'helping',
        r'\bfacilitated\b': 'helped',
        r'\bfacilitates\b': 'helps',
        
        r'\bunderscore\b': 'highlight',
        r'\bunderscoring\b': 'highlighting',
        r'\bunderscored\b': 'highlighted',
        r'\bunderscores\b': 'highlights',
        
        r'\bstreamline\b': 'simplify',
        r'\bstreamlining\b': 'simplifying',
        r'\bstreamlined\b': 'simplified',
        r'\bstreamlines\b': 'simplifies',
        
        r'\bnavigate\b': 'handle',
        r'\bnavigating\b': 'handling',
        r'\bnavigated\b': 'handled',
        r'\bnavigates\b': 'handles',
        
        r'\borchestrate\b': 'organize',
        r'\borchestrating\b': 'organizing',
        r'\borchestrated\b': 'organized',
        r'\borchestrates\b': 'organizes',
        
        # Adjectives
        r'\brobust\b': 'strong',
        r'\bcomprehensive\b': 'complete',
        r'\bseamless\b': 'smooth',
        r'\bpivotal\b': 'important',
        r'\bintricate\b': 'complex',
        r'\bmultifaceted\b': 'varied',
        r'\bdynamic\b': 'active',
        r'\bparamount\b': 'essential',
        r'\bgroundbreaking\b': 'new',
        r'\bcutting-edge\b': 'advanced',
        r'\bstate-of-the-art\b': 'modern',
        r'\btransformative\b': 'major',
        r'\bunparalleled\b': 'unique',
        r'\bmeticulous\b': 'careful',
        r'\bholistic\b': 'complete',
        r'\bstrategic\b': 'planned',
        
        # Nouns
        r'\brealm\b': 'field',
        r'\blandscape\b': 'field',
        r'\btapestry\b': 'mix',
        r'\bparadigm\b': 'model',
        r'\bframework\b': 'structure',
        r'\becosystem\b': 'system',
        r'\bsynergy\b': 'cooperation',
        r'\bmethodology\b': 'method',
        r'\bcornerstone\b': 'foundation',
        r'\blinchpin\b': 'key element',
        r'\btestament\b': 'proof',
        
        # Phrases
        r'\bactionable insights\b': 'useful information',
        r'\bgame-changing\b': 'innovative',
        r'\bgame-changer\b': 'innovation',
        r'\ba plethora of\b': 'many',
        r'\ba myriad of\b': 'many',
    }
    
    for pattern, replacement in replacements.items():
        # Case-insensitive replacement while preserving sentence start capitalization
        def replace_func(match):
            original = match.group(0)
            if original[0].isupper():
                return replacement.capitalize()
            return replacement
        
        text = re.sub(pattern, replace_func, text, flags=re.IGNORECASE)
    
    return text


def improve_sentence_variety(text):
    """
    Add variety to sentence structure to make text more natural.
    Combines short sentences and breaks up overly long ones.
    """
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    
    if len(sentences) < 2:
        return text
    
    # Simple heuristic: if we have many short sentences, occasionally combine them
    improved = []
    i = 0
    while i < len(sentences):
        current = sentences[i]
        
        # If current sentence is very short and next exists and is also short, combine with 'and'
        if i + 1 < len(sentences):
            current_words = len(current.split())
            next_words = len(sentences[i + 1].split())
            
            if current_words < 8 and next_words < 8 and len(improved) % 3 == 0:
                # Combine occasionally for variety
                combined = current.rstrip('.!?') + ', and ' + sentences[i + 1][0].lower() + sentences[i + 1][1:]
                improved.append(combined)
                i += 2
                continue
        
        improved.append(current)
        i += 1
    
    return ' '.join(improved)


def add_natural_contractions(text):
    """
    Add contractions to make text sound more conversational and human-like.
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
        r'\bwhere is\b': "where's",
        r'\bI am\b': "I'm",
        r'\byou are\b': "you're",
        r'\bwe are\b': "we're",
        r'\bthey are\b': "they're",
        r'\bhe is\b': "he's",
        r'\bshe is\b': "she's",
    }
    
    for pattern, replacement in contractions.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def final_cleanup(text):
    """
    Final pass to ensure text is perfectly formatted with no spacing issues.
    """
    # Remove any remaining double spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Ensure proper spacing after punctuation
    text = re.sub(r'([.!?,;:])([A-Za-z])', r'\1 \2', text)
    
    # Remove space before punctuation one more time
    text = re.sub(r'\s+([.!?,;:])', r'\1', text)
    
    # Fix any issues with quotes
    text = re.sub(r'\s+"', r'"', text)
    text = re.sub(r'"\s+', r'" ', text)
    
    # Clean up line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    return text.strip()


if __name__ == "__main__":
    main()
