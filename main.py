import streamlit as st
import random
import re
from typing import List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet

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
    Advanced text humanizer that mimics natural academic writing patterns
    by implementing subtle variations, clause restructuring, and natural flow.
    """
    
    def __init__(self):
        # Academic connectors for natural flow
        self.sentence_starters = [
            "Furthermore,", "Moreover,", "In addition,", "Additionally,",
            "What is more,", "Notably,", "Significantly,", "Importantly,"
        ]
        
        self.mid_sentence_transitions = [
            "which", "that", "where", "as", "while", "though", "although",
            "yet", "however", "nevertheless", "nonetheless"
        ]
        
        # Passive voice helper phrases
        self.passive_phrases = [
            ("made", "was made"),
            ("created", "was created"),
            ("established", "was established"),
            ("developed", "was developed"),
            ("introduced", "was introduced"),
            ("presented", "was presented"),
            ("designed", "was designed")
        ]
        
        # Synonym replacements for natural academic tone
        self.synonym_map = {
            "very": ["extremely", "highly", "particularly", "remarkably", "notably"],
            "important": ["significant", "crucial", "pivotal", "essential", "vital"],
            "big": ["substantial", "considerable", "major", "significant"],
            "good": ["beneficial", "advantageous", "favorable", "positive"],
            "bad": ["detrimental", "adverse", "unfavorable", "negative"],
            "show": ["demonstrate", "illustrate", "reveal", "indicate", "display"],
            "use": ["utilize", "employ", "implement", "apply"],
            "get": ["obtain", "acquire", "secure", "attain"],
            "help": ["assist", "facilitate", "aid", "support"],
            "make": ["create", "establish", "form", "constitute"],
            "give": ["provide", "offer", "present", "deliver"],
            "start": ["commence", "initiate", "begin", "launch"],
            "end": ["conclude", "terminate", "finalize", "complete"],
            "think": ["consider", "believe", "regard", "perceive"],
            "many": ["numerous", "various", "multiple", "several"],
            "also": ["additionally", "furthermore", "moreover", "likewise"],
            "because": ["owing to", "due to", "as a result of", "on account of"],
            "but": ["however", "nevertheless", "yet", "nonetheless"],
            "so": ["therefore", "consequently", "thus", "hence"],
            "went": ["proceeded", "traveled", "ventured"],
            "turned out": ["proved to be", "emerged as"],
            "packed": ["prepared", "assembled", "gathered"],
            "perfect": ["ideal", "optimal", "excellent"],
            "enjoyed": ["experienced", "appreciated", "relished"]
        }
    
    def humanize_text(self, text: str) -> str:
        """Main humanization pipeline"""
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Apply multiple transformation layers
            sentence = self._expand_contractions(sentence)
            sentence = self._add_clause_variations(sentence, i)
            sentence = self._apply_synonym_replacement(sentence)
            sentence = self._restructure_sentence(sentence, i)
            sentence = self._add_natural_connectors(sentence, i, len(sentences))
            
            humanized_sentences.append(sentence)
        
        return " ".join(humanized_sentences)
    
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
    
    def _add_clause_variations(self, sentence: str, position: int) -> str:
        """Add subordinate clauses and variations"""
        # Randomly add relative clauses
        if random.random() < 0.25 and len(sentence.split()) > 10:
            words = sentence.split()
            insert_pos = random.randint(len(words)//2, len(words)-2)
            
            relative_clauses = [
                "which",
                "that",
                "where"
            ]
            
            if words[insert_pos].endswith(','):
                words[insert_pos] = words[insert_pos] + " " + random.choice(relative_clauses)
            
            sentence = " ".join(words)
        
        return sentence
    
    def _apply_synonym_replacement(self, sentence: str) -> str:
        """Replace common words with academic synonyms"""
        words = word_tokenize(sentence)
        result = []
        
        for word in words:
            lower_word = word.lower()
            
            # Replace with synonym if available and probability check
            if lower_word in self.synonym_map and random.random() < 0.4:
                synonym = random.choice(self.synonym_map[lower_word])
                
                # Preserve capitalization
                if word[0].isupper():
                    synonym = synonym.capitalize()
                
                result.append(synonym)
            else:
                result.append(word)
        
        return " ".join(result)
    
    def _restructure_sentence(self, sentence: str, position: int) -> str:
        """Restructure sentences for natural variation"""
        # Occasionally convert to passive voice
        if random.random() < 0.2:
            for active, passive in self.passive_phrases:
                if active in sentence.lower():
                    sentence = re.sub(
                        r'\b' + active + r'\b',
                        passive,
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
                    break
        
        # Add prepositional phrase variations
        if random.random() < 0.25:
            prep_phrases = [
                ("in order to", "to"),
                ("for the purpose of", "to"),
                ("with regard to", "regarding"),
                ("in relation to", "concerning")
            ]
            
            for verbose, concise in prep_phrases:
                if random.choice([True, False]):
                    sentence = sentence.replace(concise, verbose)
        
        return sentence
    
    def _add_natural_connectors(self, sentence: str, position: int, total: int) -> str:
        """Add natural connectors and transitions"""
        # Add sentence starters occasionally
        if position > 0 and position < total - 1 and random.random() < 0.3:
            if not any(sentence.startswith(starter) for starter in self.sentence_starters):
                starter = random.choice(self.sentence_starters)
                sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Add mid-sentence transitions
        if random.random() < 0.2 and ',' in sentence:
            parts = sentence.split(',', 1)
            if len(parts) == 2 and random.random() < 0.5:
                transition = random.choice(self.mid_sentence_transitions)
                sentence = f"{parts[0]}, {transition} {parts[1].strip()}"
        
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
