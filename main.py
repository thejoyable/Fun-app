import streamlit as st
import random
import re
from typing import List
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data
def download_nltk_resources():
    resources = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

download_nltk_resources()


class EnhancedAcademicHumanizer:
    """
    Advanced text humanizer that mimics natural human writing with intentional
    imperfections, redundancies, and natural flow variations.
    """
    
    def __init__(self):
        # Synonym replacements with natural variations
        self.synonym_map = {
            "important": ["significant", "crucial", "pivotal", "vital"],
            "form": ["constitute", "represent", "make up"],
            "critical": ["pivotal", "vital", "key"],
            "governs": ["controls", "regulates", "oversees"],
            "aim to": ["seek to", "intend to", "have the purpose to"],
            "provide": ["give", "offer", "deliver"],
            "combat": ["fight", "battle against", "counter"],
            "ensure": ["make sure", "guarantee", "secure"],
            "protection": ["security", "safety", "safeguarding"],
            "With the": ["As the", "Given the", "Considering the"],
            "rapid": ["fast", "quick", "swift"],
            "significantly": ["greatly", "enormously", "considerably"],
            "addresses": ["deals with", "regulates", "covers"],
            "various": ["a variety of", "different", "multiple"],
            "including": ["such as", "like", "for example"],
            "empowers": ["gives the power to", "enables", "authorizes"],
            "investigate": ["look into", "examine", "probe"],
            "effectively": ["efficiently", "successfully", "well"],
            "strengthened": ["solidified", "reinforced", "bolstered"],
            "deal with": ["confront", "tackle", "address"],
            "evolving": ["changing", "developing", "shifting"],
            "hold accountable": ["make responsible", "hold liable"],
            "However": ["Yet", "Nevertheless", "Nonetheless"],
            "despite": ["notwithstanding", "in spite of"],
            "due to": ["owing to", "because of", "on account of"],
            "complexity": ["intricate nature", "complicated nature"],
            "lack of": ["absence of", "shortage of", "deficit of"],
            "marks": ["represents", "signals", "indicates"],
            "towards": ["toward", "in the direction of"],
            "ensuring": ["guaranteeing", "making sure of"],
            "responsible": ["accountable", "liable"],
            "expands": ["grows", "develops", "increases"],
            "robust": ["strong", "solid", "sturdy"],
            "enhance": ["improve", "boost", "strengthen"],
            "continue to": ["keep", "persist in"],
            "emphasize": ["stress", "highlight", "underscore"],
            "balance": ["equilibrium", "middle ground"],
            "foster": ["encourage", "promote", "nurture"],
            "protecting": ["safeguarding", "securing", "shielding"],
            "went on": ["had", "experienced", "went to"],
            "turned out to be": ["was", "proved to be", "emerged as"],
            "memorable": ["unforgettable", "remarkable"],
            "pleasant": ["nice", "enjoyable", "agreeable"],
            "perfect": ["ideal", "great", "excellent"],
            "reached": ["arrived at", "got to"],
            "welcomed": ["greeted", "received"],
            "nice": ["good", "pleasant", "fine"],
            "settled": ["sat", "positioned ourselves"],
            "lively": ["full of life", "vibrant", "energetic"],
            "cheerful": ["happy", "joyful", "merry"],
            "delicious": ["tasty", "good", "flavorful"],
            "reminded": ["made me realize", "brought to mind"]
        }
        
        # Human-like awkward connectors
        self.awkward_transitions = [
            ", and it",
            ", and the",
            ", and this",
            "and",
            "and then",
            "and also"
        ]
        
        # Redundant phrase patterns
        self.redundancy_patterns = [
            ("one of the most", "one of the"),
            ("very", "extremely"),
            ("really", "truly"),
            ("a lot of", "a whole bunch of"),
            ("many", "a number of")
        ]
    
    def _fix_punctuation_spacing(self, text: str) -> str:
        """Fix spacing around punctuation marks"""
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)
        text = re.sub(r"\s+'|'\s+", "'", text)
        text = re.sub(r'\s+"', '"', text)
        text = re.sub(r'"\s+', '"', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def humanize_text(self, text: str) -> str:
        """Main humanization pipeline with natural imperfections"""
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Apply transformations
            sentence = self._expand_contractions(sentence)
            sentence = self._apply_synonym_replacement(sentence)
            sentence = self._add_awkward_constructions(sentence, i)
            sentence = self._add_redundancy(sentence)
            sentence = self._restructure_naturally(sentence, i)
            sentence = self._add_human_connectors(sentence, i, len(sentences))
            
            humanized_sentences.append(sentence)
        
        result = " ".join(humanized_sentences)
        result = self._fix_punctuation_spacing(result)
        
        return result
    
    def _expand_contractions(self, text: str) -> str:
        """Expand contractions for formal tone"""
        contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "can't": "cannot", "couldn't": "could not", "wouldn't": "would not",
            "shouldn't": "should not", "won't": "will not", "isn't": "is not",
            "aren't": "are not", "wasn't": "was not", "weren't": "were not",
            "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
            "I'm": "I am", "you're": "you are", "we're": "we are",
            "they're": "they are", "it's": "it is", "that's": "that is"
        }
        
        for contraction, expansion in contractions.items():
            text = re.sub(r'\b' + contraction + r'\b', expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_synonym_replacement(self, sentence: str) -> str:
        """Replace words with synonyms based on patterns"""
        for original, replacements in self.synonym_map.items():
            if original in sentence.lower():
                # Higher probability for replacement (60%)
                if random.random() < 0.6:
                    replacement = random.choice(replacements)
                    sentence = re.sub(
                        r'\b' + re.escape(original) + r'\b',
                        replacement,
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
        
        return sentence
    
    def _add_awkward_constructions(self, sentence: str, position: int) -> str:
        """Add slightly awkward but natural human constructions"""
        
        # Change "I went on a picnic" to "My family took me on a picnic"
        sentence = re.sub(
            r'I went on a',
            'My family took me on a',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Change "we reached the" to "as we arrived"
        sentence = re.sub(
            r'we reached the',
            'as we arrived at the',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Change "As we reached" to "The park was full of... as we arrived"
        sentence = re.sub(
            r'As we reached ([^,]+), the ([^.]+)',
            r'The \2 as we arrived at \1',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Add "which come under" pattern
        sentence = re.sub(
            r'through the Information Technology Act',
            'which come under the Information Technology Act',
            sentence,
            flags=re.IGNORECASE
        )
        
        return sentence
    
    def _add_redundancy(self, sentence: str) -> str:
        """Add natural redundancy that humans often use"""
        
        # Add "one of the... one of the..." pattern
        if "one of the most memorable" in sentence.lower():
            if random.random() < 0.5:
                sentence = re.sub(
                    r'(one of the most memorable [^,]+)',
                    r'one of the days I will never forget, \1',
                    sentence,
                    flags=re.IGNORECASE
                )
        
        # Add "very" before adjectives occasionally
        adjectives = ["nice", "good", "happy", "pleasant", "great"]
        for adj in adjectives:
            if adj in sentence.lower() and random.random() < 0.3:
                sentence = re.sub(
                    r'\b' + adj + r'\b',
                    f'very {adj}',
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return sentence
    
    def _restructure_naturally(self, sentence: str, position: int) -> str:
        """Restructure sentences with human-like patterns"""
        
        # Add run-on sentences with "and" connectors
        if random.random() < 0.25 and len(sentence.split()) > 15:
            # Replace period or comma with ", and"
            sentence = re.sub(r'\.([A-Z])', r', and \1', sentence, count=1)
        
        # Change "We found a nice spot under a tree" to "The choice was good to take a tree's shadow spot"
        sentence = re.sub(
            r'We found a nice ([^ ]+) spot under a ([^ ]+) tree',
            r'The choice was good to take a \2 tree\'s shadow spot',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Add possessive constructions
        sentence = re.sub(
            r'the park nearby',
            'the park nearby',
            sentence
        )
        
        return sentence
    
    def _add_human_connectors(self, sentence: str, position: int, total: int) -> str:
        """Add human-like connectors and transitions"""
        
        # Add "What is more," "Furthermore," etc.
        if position > 0 and random.random() < 0.25:
            starters = [
                "What is more,",
                "Furthermore,",
                "Moreover,",
                "Additionally,",
                "In addition,"
            ]
            
            if not sentence[0].isupper() or sentence.startswith("The"):
                starter = random.choice(starters)
                sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Add "and it" or "and the" patterns
        if random.random() < 0.3:
            if ", and" not in sentence and "." in sentence:
                parts = sentence.split(".")
                if len(parts) >= 2:
                    connector = random.choice(self.awkward_transitions)
                    sentence = f"{parts[0]}{connector} {parts[1].strip().lower()}"
                    if len(parts) > 2:
                        sentence += "." + ".".join(parts[2:])
        
        return sentence


def main():
    """Streamlit application main function"""
    
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

    # Custom CSS
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

    # Title
    st.markdown("<div class='title'>From AI to Human Written For Soumya ka dost... 😂😁</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='intro'>
        <p><b>This app transforms your text into a more natural academic style by:</b><br>
        • Expanding contractions and using formal vocabulary<br>
        • Adding natural sentence variations and clause structures<br>
        • Implementing subtle passive voice transformations<br>
        • Replacing words with contextual synonyms<br>
        • Creating natural flow with academic connectors</p>
        <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Text input
    user_text = st.text_area("Enter your text here:", height=200)

    # File upload
    uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # Transform button
    if st.button("Transform to Academic Style", type="primary"):
        if not user_text.strip():
            st.warning("Please enter or upload some text to transform.")
        else:
            with st.spinner("Transforming text to natural academic style..."):
                # Input statistics
                input_words = word_tokenize(user_text)
                input_sentences = sent_tokenize(user_text)
                
                # Transform
                humanizer = EnhancedAcademicHumanizer()
                transformed = humanizer.humanize_text(user_text)
                
                # Output statistics
                output_words = word_tokenize(transformed)
                output_sentences = sent_tokenize(transformed)
                
                # Display results
                st.subheader("Transformed Text:")
                st.write(transformed)
                
                # Statistics
                st.markdown(
                    f"**Input**: {len(input_words)} words, {len(input_sentences)} sentences "
                    f"| **Output**: {len(output_words)} words, {len(output_sentences)} sentences"
                )
                
                # Download button
                st.download_button(
                    label="Download Transformed Text",
                    data=transformed,
                    file_name="transformed_text.txt",
                    mime="text/plain"
                )

    st.markdown("---")
    st.caption("Made with and assembled by joy 💫")


if __name__ == "__main__":
    main()
