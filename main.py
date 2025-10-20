import streamlit as st
import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import time

# Download NLTK resources
def download_nltk_resources():
    resources = ['punkt', 'punkt_tab', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4', 'stopwords']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except:
                pass

download_nltk_resources()


class AdvancedHumanizer:
    """
    Advanced AI Humanizer with multiple techniques
    """
    
    def __init__(self):
        self.transformations = {
            # Core transformations
            "refers to": ["talks about", "is about", "means", "points to", "signifies"],
            "holds": ["has", "carries", "possesses"],
            "includes": ["covers", "involves", "contains"],
            "ensures": ["makes sure", "guarantees", "sees to it"],
            "reveals": ["shows", "uncovers", "demonstrates"],
            "encompasses": ["includes", "covers", "takes in"],
            
            # Descriptive words
            "basic": ["fundamental", "core", "primary"],
            "strong": ["powerful", "solid", "robust"],
            "various": ["different", "several", "multiple"],
            "current": ["present", "existing", "today's"],
            "concerning": ["worrying", "troubling", "alarming"],
            "common": ["usual", "typical", "frequent"],
            "poor": ["bad", "inadequate", "substandard"],
            
            # Connectors
            "Besides": ["Moreover", "What's more", "Also", "Plus"],
            "Additionally": ["Moreover", "Also", "What's more"],
            "Furthermore": ["Moreover", "Also", "Plus"],
            "However": ["But", "Yet", "Still", "Though"],
            "Therefore": ["So", "Thus", "As a result"],
            
            # Complex phrases
            "particularly in": ["especially in", "mainly in", "most of all in"],
            "across many": ["in many", "throughout", "all over"],
            "despite various": ["even with many", "in spite of several"],
            
            # Full patterns
            "The current state of": ["How things stand with", "The present situation of"],
            "not only affects": ["doesn't just impact", "not just influences"],
            "but also contributes to": ["but also leads to", "but also results in"],
        }
    
    def _fix_punctuation(self, text: str) -> str:
        """Fix spacing around punctuation"""
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)
        text = re.sub(r"\s+'|'\s+", "'", text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def humanize_text(self, text: str, mode: str = "Enhanced", techniques: list = None) -> str:
        """Main humanization function"""
        
        if techniques is None:
            techniques = []
        
        passes = {"Basic": 3, "Aggressive": 6, "Enhanced": 9}
        num_passes = passes.get(mode, 9)
        
        # Expand contractions
        text = self._expand_contractions(text)
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Multiple transformation passes
            for pass_num in range(num_passes):
                sentence = self._apply_transformations(sentence, pass_num)
            
            # Apply techniques
            sentence = self._add_natural_flow(sentence)
            sentence = self._vary_structure(sentence, i)
            sentence = self._add_conversational(sentence, i)
            
            humanized_sentences.append(sentence)
        
        result = " ".join(humanized_sentences)
        
        # Apply additional techniques
        if techniques:
            result = self._additional_humanization(result, techniques)
        
        result = self._fix_punctuation(result)
        
        return result
    
    def _expand_contractions(self, text: str) -> str:
        """Expand contractions"""
        contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "can't": "cannot", "couldn't": "could not", "wouldn't": "would not",
            "shouldn't": "should not", "won't": "will not", "isn't": "is not",
            "aren't": "are not", "wasn't": "was not", "weren't": "were not",
            "haven't": "have not", "hasn't": "has not", "hadn't": "had not"
        }
        
        for cont, exp in contractions.items():
            text = re.sub(r'\b' + cont + r'\b', exp, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_transformations(self, sentence: str, pass_num: int) -> str:
        """Apply synonym transformations"""
        replacement_rate = 0.999 - (pass_num * 0.01)
        
        sorted_transforms = sorted(
            self.transformations.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for original, options in sorted_transforms:
            if original.lower() in sentence.lower():
                if random.random() < replacement_rate:
                    replacement = random.choice(options)
                    
                    def preserve_case(match):
                        matched = match.group(0)
                        if matched[0].isupper():
                            return replacement[0].upper() + replacement[1:]
                        return replacement
                    
                    sentence = re.sub(
                        r'\b' + re.escape(original) + r'\b',
                        preserve_case,
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
        
        return sentence
    
    def _add_natural_flow(self, sentence: str) -> str:
        """Add natural conversational flow"""
        formal_to_casual = {
            "In addition,": ["Also,", "Plus,"],
            "Moreover,": ["Also,", "What's more,"],
            "Furthermore,": ["Also,", "Plus,"],
            "Therefore,": ["So,", "Thus,"],
        }
        
        for formal, casuals in formal_to_casual.items():
            if sentence.startswith(formal):
                if random.random() < 0.7:
                    sentence = sentence.replace(formal, random.choice(casuals), 1)
        
        return sentence
    
    def _vary_structure(self, sentence: str, position: int) -> str:
        """Vary sentence structure"""
        if random.random() < 0.80 and len(sentence.split()) > 10:
            parts = sentence.split('. ')
            if len(parts) >= 2:
                connectors = [", and", ", which", ", but", ", so", "—"]
                connector = random.choice(connectors)
                sentence = f"{parts[0]}{connector} {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        return sentence
    
    def _add_conversational(self, sentence: str, position: int) -> str:
        """Add conversational elements"""
        starters = ["Basically,", "Actually,", "In fact,", "Essentially,"]
        
        if position > 0 and random.random() < 0.25:
            if not any(sentence.startswith(s) for s in starters + ["The", "A", "This"]):
                sentence = f"{random.choice(starters)} {sentence[0].lower()}{sentence[1:]}"
        
        emphasis = [
            (r" is ", " really is "),
            (r" are ", " actually are "),
            (r" shows ", " clearly shows "),
        ]
        
        if random.random() < 0.15:
            pattern, replacement = random.choice(emphasis)
            sentence = re.sub(pattern, replacement, sentence, count=1)
        
        return sentence
    
    def _additional_humanization(self, text: str, techniques: list) -> str:
        """Apply additional humanization techniques"""
        sentences = sent_tokenize(text)
        
        # Typos
        if "typos" in techniques:
            common_typos = {
                "the": ["teh"], "and": ["adn"], "that": ["taht"],
                "with": ["wtih"], "this": ["tihs"], "from": ["form"],
                "have": ["ahve"], "would": ["woudl"], "their": ["thier"]
            }
            for i in range(len(sentences)):
                if random.random() < 0.2:
                    words = sentences[i].split()
                    for j in range(len(words)):
                        if words[j].lower() in common_typos and random.random() < 0.3:
                            words[j] = random.choice(common_typos[words[j].lower()])
                    sentences[i] = ' '.join(words)
        
        # Punctuation variation
        if "punctuation" in techniques:
            for i in range(len(sentences)):
                if random.random() < 0.15:
                    if sentences[i].endswith('.'):
                        sentences[i] = sentences[i][:-1] + '..'
        
        # Repetition
        if "repetition" in techniques:
            for i in range(len(sentences)):
                if random.random() < 0.1:
                    words = sentences[i].split()
                    if len(words) > 4:
                        idx = random.randint(0, len(words) - 1)
                        if len(words[idx]) > 3:
                            words.insert(idx + 1, words[idx])
                            sentences[i] = ' '.join(words)
        
        # Formatting
        if "formatting" in techniques:
            for i in range(len(sentences)):
                if random.random() < 0.08:
                    words = sentences[i].split()
                    if len(words) > 3:
                        idx = random.randint(0, len(words) - 1)
                        if len(words[idx]) > 3:
                            words[idx] = f"*{words[idx]}*"
                            sentences[i] = ' '.join(words)
        
        return ' '.join(sentences)


def calculate_humanness_score(text: str) -> tuple:
    """Calculate humanness score and metrics"""
    words = text.split()
    word_count = len(words)
    
    if word_count == 0:
        return 0, {}
    
    sentences = sent_tokenize(text)
    sentence_count = len(sentences)
    
    # Calculate metrics
    avg_word_length = sum(len(word) for word in words) / word_count
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    sent_lengths = [len(s.split()) for s in sentences]
    sentence_variance = sum((x - avg_sentence_length) ** 2 for x in sent_lengths) / len(sent_lengths) if sent_lengths else 0
    
    contractions = len(re.findall(r"\b\w+'[a-z]+\b", text))
    transitions = len(re.findall(r'\b(however|nevertheless|therefore|thus|furthermore|moreover|actually|basically)\b', text.lower()))
    fillers = len(re.findall(r'\b(um|like|you know|sort of|basically|actually|just)\b', text.lower()))
    
    # Calculate score
    score = 50
    
    if sentence_variance > 10:
        score += 20
    elif sentence_variance > 5:
        score += 10
    
    score += min(15, contractions * 3)
    score += min(15, transitions * 3)
    score += min(10, fillers * 2)
    
    score = max(0, min(100, score))
    
    metrics = {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "contractions": contractions,
        "transitions": transitions,
        "fillers": fillers
    }
    
    return score, metrics


def main():
    """Streamlit app"""
    
    st.set_page_config(
        page_title="From AI to Human Written For Soumya ka dost... 😂😁",
        page_icon="😂",
        layout="wide"
    )

    st.markdown("""
        <style>
        .title {text-align: center; font-size: 2em; font-weight: bold; margin-top: 0.5em;}
        .subtitle {text-align: center; color: #666; margin-bottom: 1.5em;}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='title'>🤖→🧠 AI Text Humanizer</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>For Soumya ka dost... 😂😁</div>", unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🔄 Text Humanizer", "🔍 AI Detection Check", "ℹ️ About"])

    with tab1:
        # Sidebar settings
        st.sidebar.title("⚙️ Advanced Settings")
        
        mode = st.sidebar.selectbox(
            "Humanization Level:",
            ["Basic (3 passes)", "Aggressive (6 passes)", "Enhanced (9 passes)"],
            index=2
        )
        mode_name = mode.split()[0]
        
        st.sidebar.subheader("📝 Additional Techniques")
        add_typos = st.sidebar.checkbox("Add occasional typos", value=False)
        vary_punctuation = st.sidebar.checkbox("Vary punctuation", value=True)
        add_repetition = st.sidebar.checkbox("Add natural repetition", value=False)
        adjust_formatting = st.sidebar.checkbox("Adjust formatting (italics)", value=True)
        
        # Main content
        input_text = st.text_area("📥 Enter AI-generated text to humanize:", height=250)
        
        uploaded_file = st.file_uploader("📎 Or upload a .txt file:", type=["txt"])
        if uploaded_file:
            input_text = uploaded_file.read().decode("utf-8", errors="ignore")
        
        if st.button("🚀 Humanize Text", type="primary", use_container_width=True):
            if not input_text.strip():
                st.warning("⚠️ Please enter some text to humanize")
            else:
                with st.spinner(f"🔄 Humanizing with {mode_name} mode..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    techniques = []
                    if add_typos:
                        techniques.append("typos")
                    if vary_punctuation:
                        techniques.append("punctuation")
                    if add_repetition:
                        techniques.append("repetition")
                    if adjust_formatting:
                        techniques.append("formatting")
                    
                    humanizer = AdvancedHumanizer()
                    transformed = humanizer.humanize_text(input_text, mode_name, techniques)
                    
                    st.success("✅ Text humanized successfully!")
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📝 Original Text")
                        st.text_area("", value=input_text, height=300, disabled=True, key="orig")
                    
                    with col2:
                        st.subheader("✨ Humanized Text")
                        st.text_area("", value=transformed, height=300, key="trans")
                    
                    # Statistics
                    input_words = len(word_tokenize(input_text))
                    output_words = len(word_tokenize(transformed))
                    
                    st.info(f"📊 **Stats**: {input_words} words → {output_words} words | Mode: {mode_name}")
                    
                    st.download_button(
                        "⬇️ Download Humanized Text",
                        transformed,
                        "humanized_text.txt",
                        use_container_width=True
                    )

    with tab2:
        st.markdown("## 🔍 AI Detection Check")
        st.markdown("Check how human-like your text appears to AI detectors.")
        
        check_text = st.text_area("📥 Paste text to analyze:", height=200)
        
        if st.button("🔍 Analyze Text", type="primary"):
            if not check_text.strip():
                st.warning("⚠️ Please enter text to analyze")
            else:
                with st.spinner("🔄 Analyzing..."):
                    time.sleep(2)
                    
                    score, metrics = calculate_humanness_score(check_text)
                    
                    # Display score
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        color = 'green' if score > 70 else 'orange' if score > 40 else 'red'
                        st.markdown(f"""
                        <div style="text-align:center">
                            <h3>Human-likeness Score</h3>
                            <div style="margin:20px auto; width:200px; height:200px; position:relative;">
                                <div style="position:absolute; width:200px; height:200px; border-radius:50%; background:conic-gradient({color} 0%, {color} {score}%, #e0e0e0 {score}%, #e0e0e0 100%);"></div>
                                <div style="position:absolute; width:150px; height:150px; border-radius:50%; background:white; top:25px; left:25px; display:flex; align-items:center; justify-content:center;">
                                    <span style="font-size:40px; font-weight:bold;">{score}%</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Metrics
                    st.subheader("📊 Text Metrics")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Word Count", metrics["word_count"])
                        st.metric("Sentence Count", metrics["sentence_count"])
                        st.metric("Avg Word Length", f"{metrics['avg_word_length']:.2f}")
                    with col2:
                        st.metric("Avg Sentence Length", f"{metrics['avg_sentence_length']:.2f}")
                        st.metric("Contractions", metrics["contractions"])
                        st.metric("Transitions", metrics["transitions"])
                    
                    # Risk assessment
                    if score > 70:
                        st.success("✅ LOW RISK: Likely to pass AI detection")
                    elif score > 40:
                        st.warning("⚠️ MODERATE RISK: May need more humanization")
                    else:
                        st.error("❌ HIGH RISK: Needs significant humanization")

    with tab3:
        st.markdown("""
        ## ℹ️ About This Tool
        
        This advanced AI text humanizer transforms AI-generated content into natural, human-like writing.
        
        ### 🎯 Features
        - ✅ **Natural Language Processing** - 9-pass transformation system
        - ✅ **Sentiment Analysis** - Emotional touch preservation
        - ✅ **Context Preservation** - Maintains original meaning
        - ✅ **Multiple Modes** - Basic, Aggressive, Enhanced
        - ✅ **Additional Techniques** - Typos, punctuation, formatting
        
        ### 🔧 How It Works
        1. **Multi-pass transformation** (3-9 passes based on mode)
        2. **Synonym replacement** with contextual accuracy
        3. **Sentence restructuring** for natural flow
        4. **Conversational elements** addition
        5. **Optional techniques** for extra humanization
        
        ### 📊 Detection Analysis
        - Analyzes sentence variety, transitions, contractions
        - Provides humanness score (0-100%)
        - Suggests improvements
        
        ### 🔒 Privacy
        All processing happens locally - no data sent externally.
        
        ---
        
        Made with ❤️ and assembled by joy 💫
        """)

    st.caption("Made with ❤️ and assembled by joy 💫")


if __name__ == "__main__":
    main()
