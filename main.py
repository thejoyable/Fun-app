import streamlit as st
import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict

def download_nltk_resources():
    resources = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4', 'stopwords']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

download_nltk_resources()


class HumanizeAIPro:
    """
    Professional AI Humanizer using proven humanizeai.io techniques:
    - Natural Language Processing (NLP)
    - Sentiment Analysis
    - Personalization
    - Feedback Loops
    - Context Preservation
    """
    
    def __init__(self):
        # Comprehensive transformation database
        self.transformations = {
            # Action verbs - make more conversational
            "refers to": ["talks about", "is about", "means", "relates to", "points to"],
            "holds": ["has", "carries", "possesses", "bears"],
            "includes": ["covers", "involves", "contains", "encompasses"],
            "ensures": ["makes sure", "guarantees", "sees to it that"],
            "reveals": ["shows", "uncovers", "demonstrates", "brings to light"],
            "indicates": ["shows", "points out", "suggests", "hints at"],
            "demonstrates": ["shows", "proves", "illustrates", "displays"],
            "encompasses": ["includes", "covers", "involves", "takes in"],
            "comprises": ["includes", "consists of", "is made up of"],
            
            # Descriptive adjectives - natural variations
            "basic": ["fundamental", "core", "primary", "main"],
            "strong": ["powerful", "solid", "robust", "firm"],
            "various": ["different", "several", "numerous", "multiple"],
            "current": ["present", "existing", "ongoing", "today's"],
            "concerning": ["worrying", "troubling", "alarming", "disturbing"],
            "common": ["usual", "typical", "frequent", "regular"],
            "poor": ["bad", "inadequate", "substandard", "unsatisfactory"],
            "inconsistent": ["irregular", "erratic", "unpredictable", "variable"],
            
            # Connector phrases - natural flow
            "Besides": ["Moreover", "What's more", "On top of that", "Additionally", "Also"],
            "Additionally": ["Moreover", "Furthermore", "On top of this", "What's more", "Also"],
            "Furthermore": ["Moreover", "Besides", "What's more", "In addition", "Also"],
            "However": ["But", "Yet", "Still", "Though", "That said"],
            "Therefore": ["So", "Thus", "Hence", "As a result", "Because of this"],
            
            # Complex phrases - simplify and vary
            "particularly in": ["especially in", "mainly in", "specifically in", "most of all in"],
            "across many": ["in many", "throughout", "in numerous", "all over"],
            "often poor": ["usually bad", "frequently inadequate", "commonly substandard"],
            "despite various": ["even with many", "in spite of several", "regardless of various"],
            "remains inconsistent": ["stays irregular", "continues to vary", "is still unpredictable"],
            
            # Prepositional phrases
            "toward society": ["to society", "towards the community", "for society"],
            "of public property": ["of community property", "of shared resources"],
            "in India": ["within India", "across India", "in this country"],
            "among many citizens": ["for many people", "with numerous citizens", "for a lot of people"],
            
            # Full sentence patterns
            "The current state of": ["How things stand with", "The present situation of", "The way things are with"],
            "a concerning gap between": ["a worrying divide between", "a troubling gap between", "an alarming disconnect between"],
            "not only affects": ["doesn't just impact", "not just influences", "doesn't only affect"],
            "but also contributes to": ["but also leads to", "but additionally causes", "but also results in"],
        }
        
        # Sentence starters for variety
        self.sentence_starters = [
            "Basically,", "Essentially,", "In fact,", "Actually,", "To be honest,",
            "Realistically,", "Truthfully,", "Interestingly,", "Notably,"
        ]
        
        # Casual connectors
        self.casual_connectors = [
            "and", "but", "so", "yet", "plus", "also"
        ]
    
    def _fix_punctuation(self, text: str) -> str:
        """Fix spacing around punctuation"""
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)
        text = re.sub(r"\s+'|'\s+", "'", text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def humanize_text(self, text: str, mode: str = "Enhanced") -> str:
        """
        Main humanization with multiple passes
        Modes: Basic (3 passes), Aggressive (6 passes), Enhanced (9 passes)
        """
        
        passes = {"Basic": 3, "Aggressive": 6, "Enhanced": 9}
        num_passes = passes.get(mode, 9)
        
        # Expand contractions first
        text = self._expand_contractions(text)
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Multiple transformation passes
            for pass_num in range(num_passes):
                sentence = self._apply_transformations(sentence, pass_num)
            
            # Apply humanization techniques
            sentence = self._add_natural_flow(sentence)
            sentence = self._vary_sentence_structure(sentence, i)
            sentence = self._add_conversational_elements(sentence, i)
            sentence = self._personalize_content(sentence)
            
            humanized_sentences.append(sentence)
        
        result = " ".join(humanized_sentences)
        
        # Final polish
        result = self._add_emotional_touch(result)
        result = self._fix_punctuation(result)
        
        return result
    
    def _expand_contractions(self, text: str) -> str:
        """Expand contractions for formal tone"""
        contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "can't": "cannot", "couldn't": "could not", "wouldn't": "would not",
            "shouldn't": "should not", "won't": "will not", "isn't": "is not",
            "aren't": "are not", "wasn't": "was not", "weren't": "were not",
            "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
            "it's": "it is", "that's": "that is", "there's": "there is"
        }
        
        for cont, exp in contractions.items():
            text = re.sub(r'\b' + cont + r'\b', exp, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_transformations(self, sentence: str, pass_num: int) -> str:
        """
        Apply transformations with decreasing pickiness
        Pass 0: 99.9% replacement
        Pass 8: 95% replacement
        """
        
        replacement_rate = 0.999 - (pass_num * 0.01)
        
        # Sort by phrase length (longest first)
        sorted_transforms = sorted(
            self.transformations.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for original, options in sorted_transforms:
            if original.lower() in sentence.lower():
                if random.random() < replacement_rate:
                    replacement = random.choice(options)
                    
                    # Preserve capitalization
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
        """Add natural, conversational flow"""
        
        # Replace formal connectors with casual ones
        formal_to_casual = {
            "In addition,": ["Also,", "Plus,", "And,"],
            "Moreover,": ["Also,", "Plus,", "What's more,"],
            "Furthermore,": ["Also,", "Plus,", "On top of that,"],
            "Therefore,": ["So,", "Thus,", "Because of this,"],
            "Consequently,": ["So,", "As a result,", "Because of this,"],
        }
        
        for formal, casuals in formal_to_casual.items():
            if sentence.startswith(formal):
                if random.random() < 0.7:
                    sentence = sentence.replace(formal, random.choice(casuals), 1)
        
        return sentence
    
    def _vary_sentence_structure(self, sentence: str, position: int) -> str:
        """Vary sentence structure for naturalness"""
        
        # 80% chance to create complex sentences
        if random.random() < 0.80 and len(sentence.split()) > 10:
            # Split and reconnect with natural connectors
            parts = sentence.split('. ')
            if len(parts) >= 2:
                connectors = [
                    ", and", ", which", ", but", ", so", 
                    "—", "; thus,", ", meaning"
                ]
                connector = random.choice(connectors)
                sentence = f"{parts[0]}{connector} {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        return sentence
    
    def _add_conversational_elements(self, sentence: str, position: int) -> str:
        """Add conversational elements"""
        
        # 25% chance to add sentence starter
        if position > 0 and random.random() < 0.25:
            if not any(sentence.startswith(s) for s in self.sentence_starters + ["The", "A", "This", "It"]):
                starter = random.choice(self.sentence_starters)
                sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Add emphasis words occasionally
        emphasis_words = [
            (r" is ", " really is "),
            (r" are ", " really are "),
            (r" has ", " actually has "),
            (r" shows ", " clearly shows "),
        ]
        
        if random.random() < 0.15:
            pattern, replacement = random.choice(emphasis_words)
            sentence = re.sub(pattern, replacement, sentence, count=1)
        
        return sentence
    
    def _personalize_content(self, sentence: str) -> str:
        """Personalize content for relatability"""
        
        # Make passive constructions more active
        passive_to_active = [
            (r"is included", "includes"),
            (r"are included", "include"),
            (r"is ensured", "ensures"),
            (r"is revealed", "reveals"),
        ]
        
        for passive, active in passive_to_active:
            if random.random() < 0.4:
                sentence = re.sub(passive, active, sentence, count=1, flags=re.IGNORECASE)
        
        # Add human perspective
        if "citizens" in sentence.lower() and random.random() < 0.3:
            sentence = sentence.replace("citizens", "people", 1)
        
        return sentence
    
    def _add_emotional_touch(self, text: str) -> str:
        """Add emotional resonance (sentiment analysis simulation)"""
        
        # Strengthen negative sentiments naturally
        sentiment_enhancers = {
            "concerning": "quite concerning",
            "worrying": "really worrying",
            "poor": "pretty poor",
            "weak": "rather weak",
        }
        
        for original, enhanced in sentiment_enhancers.items():
            if original in text.lower() and random.random() < 0.3:
                text = re.sub(
                    r'\b' + original + r'\b',
                    enhanced,
                    text,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return text


def main():
    """Streamlit application"""
    
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

    st.markdown("<div class='title'>From AI to Human Written For Soumya ka dost... 😂😁</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Using HumanizeAI.io Professional Techniques</div>", unsafe_allow_html=True)

    # Mode selection
    mode = st.selectbox(
        "Select Humanization Mode:",
        ["Basic (3 passes)", "Aggressive (6 passes)", "Enhanced (9 passes)"],
        index=2
    )
    
    mode_name = mode.split()[0]

    user_text = st.text_area("Enter your AI-generated text:", height=250)
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    
    if uploaded_file:
        user_text = uploaded_file.read().decode("utf-8", errors="ignore")

    col1, col2 = st.columns([3, 1])
    
    with col1:
        transform_button = st.button("🚀 Humanize Text", type="primary", use_container_width=True)
    
    with col2:
        st.write("")  # Spacing

    if transform_button:
        if not user_text.strip():
            st.warning("⚠️ Please enter some text to humanize")
        else:
            with st.spinner(f"🔄 Humanizing text using {mode_name} mode..."):
                humanizer = HumanizeAIPro()
                transformed = humanizer.humanize_text(user_text, mode_name)
                
                st.success("✅ Text humanized successfully!")
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📝 Original Text")
                    st.text_area("", value=user_text, height=300, disabled=True, key="original")
                
                with col2:
                    st.subheader("✨ Humanized Text")
                    st.text_area("", value=transformed, height=300, key="transformed")
                
                # Statistics
                input_words = len(word_tokenize(user_text))
                output_words = len(word_tokenize(transformed))
                
                st.info(f"📊 **Statistics**: {input_words} words → {output_words} words | Mode: {mode_name}")
                
                # Download button
                st.download_button(
                    label="⬇️ Download Humanized Text",
                    data=transformed,
                    file_name="humanized_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    st.markdown("---")
    st.markdown("### 🎯 Features")
    st.markdown("""
    - ✅ **Natural Language Processing (NLP)** - Converts AI text to human-like flow
    - ✅ **Sentiment Analysis** - Adds emotional touch to content
    - ✅ **Personalization** - Makes content relatable and engaging
    - ✅ **Context Preservation** - Maintains original meaning
    - ✅ **Multiple Modes** - Basic, Aggressive, and Enhanced options
    """)
    
    st.caption("Made with ❤️ and assembled by joy 💫")


if __name__ == "__main__":
    main()
