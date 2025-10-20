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
    """Fix spacing issues around punctuation marks."""
    text = re.sub(r'\s+([.,;:!?\'\")])', r'\1', text)
    text = re.sub(r'([\(\[\{\"\'"])\s+', r'\1', text)
    text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
    text = re.sub(r'([,;:])\s*([^\s])', r'\1 \2', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r"\s+('\s*[tsmredvl]{1,3})\b", r"\1", text, flags=re.IGNORECASE)
    return text.strip()


def ultra_aggressive_phrase_destruction(text):
    """
    DESTROY every single AI-characteristic phrase and pattern.
    Most aggressive removal possible.
    """
    # Nuclear option - remove/replace EVERYTHING AI-like
    ai_destruction_map = {
        # Formal transitions (100% removal)
        r'\bfurthermore,?\b': '',
        r'\bmoreover,?\b': '',
        r'\badditionally,?\b': 'also,',
        r'\bconsequently,?\b': '',
        r'\btherefore,?\b': 'so',
        r'\bthus,?\b': 'so',
        r'\bhence,?\b': 'so',
        r'\baccordingly,?\b': '',
        r'\bnevertheless,?\b': 'but',
        r'\bnonetheless,?\b': 'but',
        
        # Verbose phrases (replace with shortest form)
        r'\bit is important to note that\b': '',
        r'\bit is worth noting that\b': '',
        r'\bit should be noted that\b': '',
        r'\bit is evident that\b': 'clearly',
        r'\bit is clear that\b': 'clearly',
        r'\bthis demonstrates that\b': 'this shows',
        r'\bthis illustrates that\b': 'this shows',
        r'\bthis indicates that\b': 'this shows',
        r'\bthis highlights that\b': 'this shows',
        r'\bthis reveals that\b': 'this shows',
        r'\bin conclusion,?\b': '',
        r'\bin summary,?\b': '',
        r'\bto summarize,?\b': '',
        r'\bto conclude,?\b': '',
        
        # AI favorite words (always replace)
        r'\bmeticulous(?:ly)?\b': 'careful',
        r'\brobust\b': 'strong',
        r'\bdelve into\b': 'look at',
        r'\bdelve\b': 'check',
        r'\bleverage\b': 'use',
        r'\bseamlessly\b': 'smoothly',
        r'\bpivotal\b': 'key',
        r'\bcrucial\b': 'key',
        r'\bvital\b': 'key',
        r'\bessential\b': 'needed',
        r'\bcritical\b': 'key',
        r'\bfundamental\b': 'basic',
        
        # Formal phrases
        r'\butilize\b': 'use',
        r'\bemploy\b': 'use',
        r'\bfacilitate\b': 'help',
        r'\bimplement\b': 'use',
        r'\bcommence\b': 'start',
        r'\bterminate\b': 'end',
        r'\bobtain\b': 'get',
        r'\bacquire\b': 'get',
        r'\bprovide\b': 'give',
        r'\bassist\b': 'help',
        r'\bensure\b': 'make sure',
        r'\bcomprehensive\b': 'full',
        r'\bsubstantial\b': 'big',
        r'\bconsiderable\b': 'big',
        r'\bnumerous\b': 'many',
        
        # Wordy constructions
        r'\bnavigat(?:e|ing) (?:the|this) (?:landscape|complexity|challenge)\b': 'handle',
        r'\btreasure trove of\b': '',
        r'\bunlock(?:ing)? the\b': 'reveal',
        r'\bvast array of\b': 'many',
        r'\bmyriad of\b': 'many',
        r'\bplethora of\b': 'many',
        r'\btapestry of\b': 'mix of',
        r'\blandscape of\b': 'area of',
        r'\brealm of\b': 'field of',
        
        # Sentence starters
        r'\bIn the context of\b': 'In',
        r'\bWith regards? to\b': 'About',
        r'\bIn terms of\b': 'For',
        r'\bIn the realm of\b': 'In',
        r'\bIn the world of\b': 'In',
        r'\bIn today\'s (?:digital )?age\b': 'Today',
        r'\bIn recent years\b': 'Lately',
        r'\bAt the end of the day\b': 'Finally',
        
        # Complex connectors
        r'\b(?:despite|in spite of) the fact that\b': 'though',
        r'\bdue to the fact that\b': 'because',
        r'\bin order to\b': 'to',
        r'\bfor the purpose of\b': 'to',
        r'\bwith the aim of\b': 'to',
    }
    
    for pattern, replacement in ai_destruction_map.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Clean up double spaces from removals
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\s+([.,;])', r'\1', text)
    
    return text


def complete_sentence_reconstruction(text):
    """
    COMPLETELY reconstruct sentences - change word order, split/combine aggressively.
    This is the nuclear option for sentence-level detection.
    """
    sentences = sent_tokenize(text)
    reconstructed = []
    
    i = 0
    while i < len(sentences):
        sent = sentences[i]
        words = sent.split()
        word_count = len(words)
        
        # Strategy 1: ALWAYS split sentences >20 words (not random, ALWAYS)
        if word_count > 20:
            # Find ANY break point
            break_words = ['and', 'but', 'while', 'though', 'since', 'because', 'although', 'where', 'when', 'if']
            for break_word in break_words:
                for j in range(8, word_count - 5):
                    if words[j].lower().rstrip('.,;') == break_word:
                        # SPLIT HERE
                        first = ' '.join(words[:j]).rstrip(',;') + '.'
                        second = ' '.join(words[j:]).lstrip(',; ')
                        if second and second[0].islower():
                            second = second[0].upper() + second[1:]
                        if not second.endswith('.'):
                            second += '.'
                        
                        reconstructed.append(first)
                        reconstructed.append(second)
                        i += 1
                        break
                else:
                    continue
                break
            else:
                # No break word found? Force split in middle
                mid = word_count // 2
                first = ' '.join(words[:mid]) + '.'
                second = ' '.join(words[mid:])
                if second and second[0].islower():
                    second = second[0].upper() + second[1:]
                if not second.endswith('.'):
                    second += '.'
                reconstructed.append(first)
                reconstructed.append(second)
                i += 1
            continue
        
        # Strategy 2: Combine short sentences (<10 words) with next
        if word_count < 10 and i < len(sentences) - 1:
            next_sent = sentences[i + 1]
            # Use casual connector
            connectors = [', and', ', but', ' because', ' since', ', so', ', yet']
            connector = random.choice(connectors)
            combined = sent.rstrip('.') + connector + ' ' + next_sent[0].lower() + next_sent[1:]
            reconstructed.append(combined)
            i += 2
            continue
        
        # Strategy 3: Reorder sentence components (change word order)
        if word_count > 12 and random.random() < 0.40:
            # Try to move dependent clauses around
            sent_lower = sent.lower()
            if ' which ' in sent_lower or ' that ' in sent_lower:
                # Try to restructure
                parts = re.split(r'(\s+which\s+|\s+that\s+)', sent, flags=re.IGNORECASE)
                if len(parts) >= 3:
                    # Reverse order sometimes
                    reordered = parts[2].rstrip('.') + ' ' + parts[0].strip()
                    if not reordered.endswith('.'):
                        reordered += '.'
                    sent = reordered
        
        reconstructed.append(sent)
        i += 1
    
    return ' '.join(reconstructed)


def nuclear_vocabulary_replacement(text):
    """
    NUCLEAR option - replace 85%+ of replaceable words.
    Maximum vocabulary diversity possible.
    """
    # MASSIVE vocabulary map
    mega_vocab_map = {
        # Level 1: Most common academic words
        'significant': ['big', 'major', 'key', 'large', 'important', 'notable'],
        'important': ['key', 'big', 'major', 'vital', 'critical', 'main'],
        'large': ['big', 'huge', 'major', 'substantial'],
        'small': ['little', 'tiny', 'minor', 'slight'],
        'various': ['many', 'different', 'several', 'diverse'],
        'different': ['other', 'separate', 'distinct', 'unique'],
        'numerous': ['many', 'lots of', 'plenty of', 'countless'],
        'multiple': ['many', 'several', 'various'],
        'several': ['many', 'some', 'a few'],
        
        # Level 2: Verbs
        'demonstrate': ['show', 'prove', 'display'],
        'indicate': ['show', 'suggest', 'point to'],
        'illustrate': ['show', 'display'],
        'reveal': ['show', 'expose', 'display'],
        'provide': ['give', 'offer', 'supply'],
        'enable': ['let', 'allow'],
        'assist': ['help', 'aid', 'support'],
        'examine': ['look at', 'check', 'review'],
        'analyze': ['look at', 'study', 'review'],
        'investigate': ['look into', 'check', 'study'],
        'establish': ['set up', 'create', 'form'],
        'develop': ['create', 'make', 'build'],
        'create': ['make', 'build', 'form'],
        'maintain': ['keep', 'preserve', 'uphold'],
        'enhance': ['improve', 'boost', 'better'],
        'increase': ['raise', 'boost', 'grow'],
        'decrease': ['lower', 'reduce', 'cut'],
        'reduce': ['cut', 'lower', 'shrink'],
        
        # Level 3: Adjectives
        'effective': ['good', 'useful', 'helpful'],
        'efficient': ['quick', 'fast', 'effective'],
        'appropriate': ['right', 'proper', 'suitable'],
        'adequate': ['enough', 'sufficient'],
        'substantial': ['large', 'big', 'major'],
        'considerable': ['large', 'big', 'major'],
        'potential': ['possible', 'likely'],
        'possible': ['potential', 'feasible'],
        'necessary': ['needed', 'required'],
        'required': ['needed', 'necessary'],
        'specific': ['particular', 'certain', 'exact'],
        'particular': ['specific', 'certain', 'special'],
        'general': ['common', 'usual', 'typical'],
        'common': ['usual', 'typical', 'normal'],
        'unique': ['special', 'distinct', 'one-of-a-kind'],
        
        # Level 4: Adverbs
        'particularly': ['especially', 'notably'],
        'specifically': ['especially', 'in particular'],
        'generally': ['usually', 'typically', 'often'],
        'typically': ['usually', 'normally', 'often'],
        'currently': ['now', 'today', 'at present'],
        'previously': ['before', 'earlier'],
        'subsequently': ['later', 'after', 'then'],
        'ultimately': ['finally', 'in the end'],
        'approximately': ['about', 'around', 'roughly'],
        'significantly': ['greatly', 'largely', 'majorly'],
        'considerably': ['greatly', 'largely'],
        'extremely': ['very', 'really', 'highly'],
        'relatively': ['fairly', 'quite', 'somewhat'],
        
        # Level 5: Nouns
        'aspect': ['part', 'side', 'element'],
        'component': ['part', 'piece', 'element'],
        'element': ['part', 'piece', 'component'],
        'factor': ['element', 'part', 'aspect'],
        'issue': ['problem', 'matter', 'concern'],
        'challenge': ['problem', 'difficulty', 'issue'],
        'advantage': ['benefit', 'plus', 'upside'],
        'disadvantage': ['drawback', 'downside', 'con'],
        'benefit': ['advantage', 'plus', 'gain'],
        'impact': ['effect', 'influence'],
        'effect': ['impact', 'result', 'outcome'],
        'result': ['outcome', 'effect'],
        'outcome': ['result', 'effect'],
        'method': ['way', 'approach', 'technique'],
        'approach': ['way', 'method', 'strategy'],
        'strategy': ['plan', 'approach', 'tactic'],
        'process': ['method', 'procedure', 'way'],
        'procedure': ['process', 'method', 'way'],
        'concept': ['idea', 'notion', 'thought'],
        'principle': ['rule', 'concept', 'idea'],
    }
    
    words = text.split()
    hyper_modified = []
    
    for word in words:
        lower_word = word.lower().strip('.,;:!?')
        trailing_punct = ''.join([c for c in word if c in '.,;:!?'])
        
        # 85% replacement probability (ULTRA AGGRESSIVE)
        if lower_word in mega_vocab_map and random.random() < 0.85:
            replacement = random.choice(mega_vocab_map[lower_word])
            
            # Preserve capitalization
            if word and word[0].isupper():
                replacement = replacement.capitalize()
            
            hyper_modified.append(replacement + trailing_punct)
        else:
            hyper_modified.append(word)
    
    return ' '.join(hyper_modified)


def maximum_human_injection(text):
    """
    Inject MAXIMUM human elements - 60% contractions, casual phrases everywhere.
    """
    sentences = sent_tokenize(text)
    ultra_human = []
    
    # Super casual starters
    ultra_casual = [
        "Look, ", "Listen, ", "Simply put, ", "Basically, ",
        "The thing is, ", "Here's the deal - ", "In reality, ",
        "Honestly, ", "To be frank, ", "Let's be real - "
    ]
    
    # AGGRESSIVE contractions (60% probability)
    max_contractions = {
        ' is not': " isn't",
        ' are not': " aren't",
        ' was not': " wasn't",
        ' were not': " weren't",
        ' have not': " haven't",
        ' has not': " hasn't",
        ' had not': " hadn't",
        ' will not': " won't",
        ' would not': " wouldn't",
        ' should not': " shouldn't",
        ' could not': " couldn't",
        ' do not': " don't",
        ' does not': " doesn't",
        ' did not': " didn't",
        ' cannot': " can't",
        ' it is': " it's",
        ' that is': " that's",
        ' what is': " what's",
        ' there is': " there's",
        ' who is': " who's",
        ' they are': " they're",
        ' we are': " we're",
        ' you are': " you're",
        ' I am': " I'm",
        ' he is': " he's",
        ' she is': " she's",
    }
    
    for i, sent in enumerate(sentences):
        modified = sent
        
        # Add casual starter (50% chance on non-first sentences)
        if i > 0 and random.random() < 0.50:
            starter = random.choice(ultra_casual)
            if modified[0].isupper():
                modified = starter + modified[0].lower() + modified[1:]
        
        # AGGRESSIVE contractions (60% chance per sentence)
        if random.random() < 0.60:
            for formal, casual in max_contractions.items():
                if formal in modified:
                    modified = modified.replace(formal, casual, 1)
                    break
        
        # Add mid-sentence breaks with em dashes (30% chance)
        if ' and ' in modified and random.random() < 0.30:
            modified = modified.replace(' and ', ' — and ', 1)
        
        ultra_human.append(modified)
    
    return ' '.join(ultra_human)


def check_and_correct_grammar(text):
    """Grammar checking with LanguageTool."""
    if not GRAMMAR_CHECKER_AVAILABLE:
        return text, []
    
    try:
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        
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


def apply_nuclear_humanization(text, humanizer):
    """
    NUCLEAR option - most aggressive humanization possible.
    Every technique at maximum intensity.
    """
    # STEP 1: DESTROY all AI phrases
    text = ultra_aggressive_phrase_destruction(text)
    
    # STEP 2: Apply base transformation with MAXIMUM parameters
    transformed = humanizer.humanize_text(
        text,
        use_passive=True,
        use_synonyms=True
    )
    
    # STEP 3: COMPLETE sentence reconstruction (100% of long sentences split)
    transformed = complete_sentence_reconstruction(transformed)
    
    # STEP 4: NUCLEAR vocabulary replacement (85% replacement)
    transformed = nuclear_vocabulary_replacement(transformed)
    
    # STEP 5: MAXIMUM human element injection (60% contractions)
    transformed = maximum_human_injection(transformed)
    
    # STEP 6: Fix punctuation
    transformed = fix_punctuation_spacing(transformed)
    
    # STEP 7: Grammar check
    if GRAMMAR_CHECKER_AVAILABLE:
        transformed, corrections = check_and_correct_grammar(transformed)
    else:
        corrections = []
    
    return transformed, corrections


def main():
    """
    NUCLEAR OPTION - Most aggressive AI text humanizer possible.
    """

    download_nltk_resources()

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
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='title'>From AI to Human Written For Soumya ka dost... 😂😁</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='intro'>
        <p><b>🔥 NUCLEAR MODE - Most Aggressive Humanization:</b><br>
        • DESTROYS all AI phrases (furthermore, thus, moreover, etc. = REMOVED)<br>
        • ALWAYS splits long sentences (>20 words = automatic split)<br>
        • 85% vocabulary replacement (maximum word diversity)<br>
        • 60% contraction rate (super casual, human-like)<br>
        • Complete sentence reconstruction (word order changes)<br>
        • 50% casual starter injection (Look, Listen, Simply put, etc.)<br>
        • Target: 85-100% human scores on ALL detectors</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    if GRAMMAR_CHECKER_AVAILABLE:
        st.success("✓ Grammar checking active")
    else:
        st.info("ℹ️ Install: pip install language-tool-python")

    user_text = st.text_area("Enter your text here:", height=200)

    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    if st.button("💥 NUCLEAR HUMANIZATION"):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Applying NUCLEAR humanization (maximum aggression)..."):
                input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                # NUCLEAR PARAMETERS
                humanizer = AcademicTextHumanizer(
                    p_passive=0.20,              # 20% passive (more active = more human)
                    p_synonym_replacement=0.50,   # 50% replacement (MAXIMUM)
                    p_academic_transition=0.15    # 15% transitions (minimal formality)
                )
                
                transformed, corrections = apply_nuclear_humanization(user_text, humanizer)

                st.subheader("💥 ULTRA-HUMANIZED TEXT:")
                st.write(transformed)

                output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Input Words", input_word_count)
                with col2:
                    st.metric("Input Sentences", input_sentence_count)
                with col3:
                    st.metric("Output Words", output_word_count)
                with col4:
                    st.metric("Output Sentences", output_sentence_count)

                if GRAMMAR_CHECKER_AVAILABLE and corrections:
                    with st.expander(f"✓ {len(corrections)} grammar fixes"):
                        for i, correction in enumerate(corrections[:10], 1):
                            st.markdown(f"**{i}.** '{correction['original']}' → '{correction['correction']}'")

                with st.expander("🔥 NUCLEAR Techniques Applied"):
                    st.markdown("""
                    **💥 Step 1:** DESTROYED all AI phrases (furthermore/moreover/thus = REMOVED)  
                    **💥 Step 2:** Base transformation (20% passive, 50% synonyms, 15% transitions)  
                    **💥 Step 3:** COMPLETE sentence reconstruction (ALWAYS split >20 words)  
                    **💥 Step 4:** NUCLEAR vocab replacement (85% of words changed)  
                    **💥 Step 5:** MAXIMUM human injection (60% contractions, 50% casual starters)  
                    **💥 Step 6:** Punctuation fix  
                    **💥 Step 7:** Grammar correction
                    
                    **Expected: 85-100% human score** (most aggressive possible)
                    """)

                st.download_button(
                    label="📥 Download",
                    data=transformed,
                    file_name="ultra_humanized.txt",
                    mime="text/plain"
                )

                st.error("⚠️ **Warning:** This is the MOST AGGRESSIVE mode. Text may be very casual. Review carefully!")

    st.markdown("---")
    st.caption("Made with and assembled by joy 💫")


if __name__ == "__main__":
    main()
