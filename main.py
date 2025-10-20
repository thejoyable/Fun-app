import streamlit as st
import re
import random
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize, sent_tokenize

try:
    import language_tool_python
    GRAMMAR_CHECKER_AVAILABLE = True
except ImportError:
    GRAMMAR_CHECKER_AVAILABLE = False


def fix_punctuation_spacing(text):
    """
    Fix spacing issues around punctuation marks to ensure grammatically correct spacing.
    Removes extra spaces before punctuation and ensures proper spacing after.
    """
    # Remove spaces before punctuation marks
    text = re.sub(r'\s+([.,;:!?\'\")])', r'\1', text)
    
    # Remove spaces after opening punctuation
    text = re.sub(r'([\(\[\{\"\'"])\s+', r'\1', text)
    
    # Ensure single space after sentence-ending punctuation if followed by text
    text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
    
    # Ensure single space after commas, semicolons, colons if followed by text
    text = re.sub(r'([,;:])\s*([^\s])', r'\1 \2', text)
    
    # Remove multiple consecutive spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Fix common contractions spacing
    text = re.sub(r"\s+('\s*[tsmredvl]{1,3})\b", r"\1", text, flags=re.IGNORECASE)
    
    # Clean up leading/trailing whitespace
    text = text.strip()
    
    return text


def add_natural_imperfections(text):
    """
    Add subtle human-like imperfections and variations to bypass AI detection.
    Based on Reddit research: unique phrases, varied structures, and natural flow.
    """
    sentences = sent_tokenize(text)
    modified_sentences = []
    
    # Casual transitional phrases that sound human
    casual_transitions = [
        "Actually, ", "In fact, ", "Interestingly, ", "Notably, ",
        "It's worth noting that ", "To be fair, ", "In reality, ",
        "Essentially, ", "Basically, ", "In other words, ",
        "That said, ", "On the other hand, ", "At the same time, "
    ]
    
    # Casual connecting phrases
    mid_sentence_connectors = [
        " - which is important - ", " (which matters here) ", 
        " - and this is key - ", ", importantly, ", 
        ", interestingly enough, ", " - worth mentioning - "
    ]
    
    for i, sentence in enumerate(sentences):
        modified = sentence
        
        # Add casual transitions to some sentences (not all)
        if i > 0 and random.random() < 0.25:  # 25% chance
            transition = random.choice(casual_transitions)
            modified = transition + modified
        
        # Insert mid-sentence connectors occasionally
        if random.random() < 0.15 and ',' in modified:  # 15% chance
            parts = modified.split(',', 1)
            if len(parts) == 2:
                connector = random.choice(mid_sentence_connectors)
                modified = parts[0] + connector + parts[1]
        
        # Add subtle contractions occasionally (more human-like)
        contraction_map = {
            ' is not ': " isn't ", ' are not ': " aren't ",
            ' was not ': " wasn't ", ' were not ': " weren't ",
            ' have not ': " haven't ", ' has not ': " hasn't ",
            ' do not ': " don't ", ' does not ': " doesn't ",
            ' did not ': " didn't ", ' will not ': " won't ",
            ' would not ': " wouldn't ", ' should not ': " shouldn't ",
            ' cannot ': " can't ", ' could not ': " couldn't "
        }
        
        if random.random() < 0.20:  # 20% chance to add contraction
            for formal, casual in contraction_map.items():
                if formal in modified.lower():
                    modified = re.sub(formal, casual, modified, flags=re.IGNORECASE, count=1)
                    break
        
        modified_sentences.append(modified)
    
    return ' '.join(modified_sentences)


def vary_sentence_structures(text):
    """
    Create burstiness by varying sentence lengths and structures.
    Mix short punchy sentences with longer complex ones.
    """
    sentences = sent_tokenize(text)
    if len(sentences) < 3:
        return text
    
    varied_sentences = []
    
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        word_count = len(words)
        
        # Occasionally split longer sentences (>25 words) into two shorter ones
        if word_count > 25 and random.random() < 0.30:
            # Find a good split point (after conjunctions or commas)
            split_points = [j for j, word in enumerate(words) if word.lower() in ['and', 'but', 'however', 'yet', 'so'] or word.endswith(',')]
            
            if split_points and len(split_points) > 0:
                mid_point = split_points[len(split_points)//2]
                first_half = ' '.join(words[:mid_point])
                second_half = ' '.join(words[mid_point:])
                
                # Clean up the split
                if first_half.endswith(','):
                    first_half = first_half[:-1]
                if not first_half.endswith('.'):
                    first_half += '.'
                
                second_half = second_half.strip(',').strip()
                if second_half and second_half[0].islower():
                    second_half = second_half[0].upper() + second_half[1:]
                if not second_half.endswith('.'):
                    second_half += '.'
                
                varied_sentences.append(first_half)
                varied_sentences.append(second_half)
                continue
        
        varied_sentences.append(sentence)
    
    return ' '.join(varied_sentences)


def add_perplexity_and_burstiness(text):
    """
    Implement high perplexity and burstiness as recommended by Reddit users.
    This significantly helps bypass AI detection.
    """
    # Replace some academic words with more varied/unexpected choices
    vocabulary_variations = {
        'utilize': ['use', 'employ', 'apply', 'leverage'],
        'demonstrate': ['show', 'reveal', 'illustrate', 'indicate'],
        'significant': ['important', 'major', 'substantial', 'considerable'],
        'investigate': ['examine', 'explore', 'look into', 'study'],
        'obtain': ['get', 'acquire', 'secure', 'gain'],
        'commence': ['begin', 'start', 'initiate', 'kick off'],
        'terminate': ['end', 'finish', 'conclude', 'wrap up'],
        'facilitate': ['help', 'enable', 'assist', 'make easier'],
        'implement': ['use', 'apply', 'put in place', 'deploy'],
        'comprehensive': ['complete', 'thorough', 'full', 'extensive']
    }
    
    words = text.split()
    modified_words = []
    
    for word in words:
        lower_word = word.lower().strip('.,;:!?')
        if lower_word in vocabulary_variations and random.random() < 0.40:
            replacement = random.choice(vocabulary_variations[lower_word])
            # Preserve original capitalization and punctuation
            if word[0].isupper():
                replacement = replacement.capitalize()
            # Preserve trailing punctuation
            trailing_punct = ''.join([c for c in word if c in '.,;:!?'])
            modified_words.append(replacement + trailing_punct)
        else:
            modified_words.append(word)
    
    return ' '.join(modified_words)


def remove_ai_telltale_phrases(text):
    """
    Remove phrases that AI detectors flag as typical AI-generated content.
    Based on Reddit discussions of common AI patterns.
    """
    # Phrases to avoid (common AI patterns)
    ai_phrases = [
        r'\bmeticulous(?:ly)?\b', r'\bmeticulously\b',
        r'\bcomplexities\b', r'\beverchanging\b', r'\bever-evolving\b',
        r'\btreasure trove\b', r'\bworld of\b',
        r'\bunlock the\b', r'\bunveil(?:ing)? secrets\b',
        r'\brobust\b', r'\bdelve\b', r'\bdel into\b',
        r'\bnavigat(?:e|ing) the landscape\b',
        r'\bIt is important to note that\b',
        r'\bIn conclusion\b', r'\bIn summary\b',
        r'\bvast array\b', r'\bmyriad of\b',
        r'\btapestry of\b', r'\bcrucial\b', r'\bpivotal\b'
    ]
    
    for phrase_pattern in ai_phrases:
        # Replace with more natural alternatives
        text = re.sub(phrase_pattern, lambda m: _get_natural_replacement(m.group()), text, flags=re.IGNORECASE)
    
    return text


def _get_natural_replacement(matched_text):
    """Get natural replacements for AI-like phrases"""
    replacements = {
        'meticulously': 'carefully',
        'meticulous': 'careful',
        'complexities': 'complexissues',
        'everchanging': 'changing',
        'ever-evolving': 'evolving',
        'treasure trove': 'collection',
        'unlock the': 'reveal the',
        'robust': 'strong',
        'delve': 'explore',
        'crucial': 'important',
        'pivotal': 'key'
    }
    
    lower_match = matched_text.lower().strip()
    if lower_match in replacements:
        result = replacements[lower_match]
        # Preserve capitalization
        if matched_text[0].isupper():
            result = result.capitalize()
        return result
    return ''  # Remove if no replacement


def check_and_correct_grammar(text):
    """
    Check and correct grammar using LanguageTool if available.
    Returns corrected text and list of corrections made.
    """
    if not GRAMMAR_CHECKER_AVAILABLE:
        return text, []
    
    try:
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        
        # Apply corrections automatically
        corrected_text = language_tool_python.utils.correct(text, matches)
        
        # Create a list of corrections for display
        corrections = []
        for match in matches:
            if match.replacements:
                corrections.append({
                    'original': text[match.offset:match.offset + match.errorLength],
                    'correction': match.replacements[0] if match.replacements else '',
                    'message': match.message
                })
        
        tool.close()
        return corrected_text, corrections
    except Exception as e:
        return text, []


def apply_comprehensive_humanization(text, humanizer):
    """
    Apply ALL humanization techniques in optimal order for maximum effectiveness.
    Based on Reddit research and proven bypass methods.
    """
    # Step 1: Remove AI telltale phrases first
    text = remove_ai_telltale_phrases(text)
    
    # Step 2: Initial transformation with optimized parameters
    transformed = humanizer.humanize_text(
        text,
        use_passive=True,
        use_synonyms=True
    )
    
    # Step 3: Add perplexity and burstiness (KEY for bypassing detection)
    transformed = add_perplexity_and_burstiness(transformed)
    
    # Step 4: Vary sentence structures (create burstiness)
    transformed = vary_sentence_structures(transformed)
    
    # Step 5: Add natural imperfections and casual elements
    transformed = add_natural_imperfections(transformed)
    
    # Step 6: Fix punctuation spacing issues
    transformed = fix_punctuation_spacing(transformed)
    
    # Step 7: Apply grammar correction last (ensures correctness)
    if GRAMMAR_CHECKER_AVAILABLE:
        transformed, corrections = check_and_correct_grammar(transformed)
    else:
        corrections = []
    
    return transformed, corrections


def main():
    """
    Advanced AI text humanizer that bypasses detection while maintaining academic quality.
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

    # --- Custom CSS for Title Centering and Additional Styling ---
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
        .correction-box {
            background-color: #f0f8ff;
            border-left: 4px solid #4CAF50;
            padding: 10px;
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
        <p><b>Advanced AI text humanizer with detection bypass:</b><br>
        • Removes AI-like phrases and patterns<br>
        • Adds high perplexity and burstiness (varied sentence structures)<br>
        • Includes natural imperfections and casual elements<br>
        • Balanced passive voice (~28%) for academic style<br>
        • Smart synonym replacement with varied vocabulary<br>
        • Automatic grammar correction and proper spacing<br>
        • Optimized to bypass GPTZero, Turnitin, and other detectors</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display grammar checker status
    if GRAMMAR_CHECKER_AVAILABLE:
        st.success("✓ Advanced grammar checking enabled")
    else:
        st.info("ℹ️ Install 'language-tool-python' for advanced grammar checking")

    # Text input
    user_text = st.text_area("Enter your text here:", height=200)

    # File upload
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # Button
    if st.button("Transform to Human-Like Text"):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Applying advanced humanization techniques..."):
                # Input stats
                input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # Transform with ALL humanization techniques
                # Optimized parameters based on extensive Reddit research
                humanizer = AcademicTextHumanizer(
                    p_passive=0.28,              # 28% passive voice (academic norm)
                    p_synonym_replacement=0.35,   # 35% synonym replacement (higher variety)
                    p_academic_transition=0.35    # 35% transitions (balanced)
                )
                
                transformed, corrections = apply_comprehensive_humanization(user_text, humanizer)

                # Output
                st.subheader("Humanized Text:")
                st.write(transformed)

                # Output stats
                output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Input Words", input_word_count)
                with col2:
                    st.metric("Input Sentences", input_sentence_count)
                with col3:
                    st.metric("Output Words", output_word_count)
                with col4:
                    st.metric("Output Sentences", output_sentence_count)

                # Display grammar corrections if any were made
                if GRAMMAR_CHECKER_AVAILABLE and corrections:
                    with st.expander(f"✓ {len(corrections)} grammar corrections applied"):
                        for i, correction in enumerate(corrections[:10], 1):
                            st.markdown(
                                f"**{i}.** '{correction['original']}' → '{correction['correction']}'  \n"
                                f"*{correction['message']}*"
                            )

                # Humanization techniques applied
                with st.expander("🎯 Humanization Techniques Applied"):
                    st.markdown("""
                    - ✓ Removed AI-telltale phrases (meticulous, robust, etc.)
                    - ✓ Added perplexity (varied vocabulary choices)
                    - ✓ Created burstiness (mixed sentence lengths)
                    - ✓ Included natural imperfections and casual elements
                    - ✓ Applied contractions and informal connectors
                    - ✓ Fixed punctuation spacing
                    - ✓ Grammar checked and corrected
                    """)

                # Download button
                st.download_button(
                    label="📥 Download Humanized Text",
                    data=transformed,
                    file_name="humanized_text.txt",
                    mime="text/plain"
                )

    st.markdown("---")
    st.caption("Made with and assembled by joy 💫")


if __name__ == "__main__":
    main()
