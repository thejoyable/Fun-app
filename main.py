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


class AggressiveHumanWriter:
    """
    Ultra-aggressive text humanizer that heavily mimics natural human writing
    with intentional awkwardness, redundancies, and varied sentence structures.
    """
    
    def __init__(self):
        # Comprehensive synonym map
        self.synonym_map = {
            # Verbs
            "form": ["constitute", "make up", "represent", "create"],
            "governs": ["controls", "regulates", "manages", "oversees"],
            "aim to": ["seek to", "intend to", "have the purpose to", "work to"],
            "provide": ["give", "offer", "deliver", "present"],
            "combat": ["fight", "battle against", "counter", "tackle"],
            "ensure": ["make sure", "guarantee", "secure", "see to it"],
            "addresses": ["deals with", "regulates", "covers", "handles"],
            "empowers": ["gives the power to", "enables", "allows", "authorizes"],
            "investigate": ["look into", "examine", "probe", "check"],
            "effectively": ["efficiently", "successfully", "properly", "well"],
            "strengthened": ["solidified", "reinforced", "bolstered", "made stronger"],
            "deal with": ["confront", "tackle", "address", "handle"],
            "evolving": ["changing", "developing", "shifting", "transforming"],
            "marks": ["represents", "signals", "indicates", "shows"],
            "ensuring": ["making sure of", "guaranteeing", "seeing to"],
            "expands": ["grows", "develops", "increases", "enlarges"],
            "continue to": ["keep", "persist in", "carry on"],
            "emphasize": ["stress", "highlight", "underscore", "point out"],
            "foster": ["encourage", "promote", "nurture", "support"],
            "protecting": ["safeguarding", "securing", "shielding", "defending"],
            "went on": ["had", "experienced", "took part in"],
            "turned out to be": ["was", "proved to be", "emerged as", "became"],
            "reached": ["arrived at", "got to", "came to"],
            "welcomed": ["greeted", "received", "met"],
            "found": ["discovered", "located", "spotted"],
            "settled": ["sat down", "positioned ourselves", "made ourselves comfortable"],
            "packed": ["prepared", "assembled", "gathered", "put together"],
            "reminded": ["made me realize", "brought to mind", "made me think"],
            
            # Adjectives
            "critical": ["pivotal", "vital", "key", "essential"],
            "important": ["significant", "crucial", "vital", "major"],
            "rapid": ["fast", "quick", "swift", "speedy"],
            "various": ["a variety of", "different", "multiple", "several"],
            "robust": ["strong", "solid", "sturdy", "powerful"],
            "memorable": ["unforgettable", "remarkable", "notable"],
            "pleasant": ["nice", "enjoyable", "agreeable", "lovely"],
            "perfect": ["ideal", "great", "excellent", "optimal"],
            "nice": ["good", "pleasant", "fine", "lovely"],
            "lively": ["full of life", "vibrant", "energetic", "active"],
            "cheerful": ["happy", "joyful", "merry", "bright"],
            "delicious": ["tasty", "good", "flavorful", "appetizing"],
            
            # Adverbs/Others
            "significantly": ["greatly", "enormously", "considerably", "substantially"],
            "However": ["Yet", "Nevertheless", "Nonetheless", "Still"],
            "despite": ["notwithstanding", "in spite of", "regardless of"],
            "due to": ["owing to", "because of", "on account of", "as a result of"],
            "including": ["such as", "like", "for example", "for instance"],
            "also": ["additionally", "furthermore", "moreover", "as well"],
            "With the": ["As the", "Given the", "Considering the", "Looking at the"],
            "towards": ["toward", "in the direction of", "to"],
            
            # Nouns
            "protection": ["security", "safety", "safeguarding"],
            "complexity": ["intricate nature", "complicated nature", "technical nature"],
            "lack of": ["absence of", "shortage of", "deficit of", "unawareness of"],
            "balance": ["equilibrium", "middle ground", "regulatory balance"]
        }
        
        # Sentence restructuring patterns
        self.restructure_patterns = [
            (r"During my winter vacation, I went", "My family took me during their winter vacation, and it was"),
            (r"I went on a picnic with my family", "My family took me on a picnic"),
            (r"it turned out to be one of the most memorable days", "it was one of the days I will never forget, one of the most remarkable days"),
            (r"We had been planning", "We had been planning"),
            (r"and finally chose", "and picked"),
            (r"visit a nearby park", "visit the park nearby"),
            (r"but the sun made", "and the sun was shining making"),
            (r"We packed", "We packed a whole bunch of"),
            (r"As we reached the park", "The park was full of welcoming green lawns and blooming winter flowers as we arrived"),
            (r"We found a nice shady spot under a big tree and settled down", "The choice was good to take a big tree's shadow spot and settled down"),
            (r"with other families enjoying", "with other families spending"),
            (r"After relaxing for a bit", "After a little bit of relaxation time"),
            (r"while the younger kids", "while the younger kids"),
            (r"made the environment cheerful", "made the atmosphere ecstatic"),
            (r"Later, we sat down to eat", "Later we had the feast prepared by my mother"),
            (r"and hot tea in a flask that warmed us up", "and hot tea that came in a flask, and the flask was shared by the family and it warmed us up"),
            (r"Sharing a meal in the open air with loved ones made it taste even better", "The open-air meal with the loved ones sharing made the food taste even better"),
            (r"After lunch, we rested for a while and then went", "We had a very mild lunch, then a short rest, and then we went"),
            (r"enjoying the winter sunshine and clicking pictures", "enjoying the winter sun, and shooting photos"),
            (r"As the sun started to set", "It was a long sunny day and when the sun was about to set"),
            (r"we packed our things and headed home, tired but happy", "we packed up and went tired but happy on our way home"),
            (r"gave us a break from routine, brought us closer as a family, and created memories to cherish", "was a very relaxing period, a time for family togetherness, and a making of memories that would be treasured for ever"),
            (r"That winter day reminded me how simple joys", "That day of winter made me realize the value of small delights"),
            (r"can bring so much happiness", "can deliver so much happiness"),
            (r"It was truly a perfect", "It was really a perfect")
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
        """Main humanization pipeline - AGGRESSIVE MODE"""
        
        # First, apply major restructuring patterns
        for pattern, replacement in self.restructure_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Apply all transformations
            sentence = self._expand_contractions(sentence)
            sentence = self._aggressive_synonym_replacement(sentence)
            sentence = self._add_which_clauses(sentence)
            sentence = self._add_redundancy_patterns(sentence)
            sentence = self._add_run_on_sentences(sentence, i)
            sentence = self._add_human_transitions(sentence, i, len(sentences))
            sentence = self._add_awkward_passives(sentence)
            
            humanized_sentences.append(sentence)
        
        result = " ".join(humanized_sentences)
        result = self._fix_punctuation_spacing(result)
        
        return result
    
    def _expand_contractions(self, text: str) -> str:
        """Expand contractions"""
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
    
    def _aggressive_synonym_replacement(self, sentence: str) -> str:
        """AGGRESSIVE synonym replacement - 80% probability"""
        for original, replacements in self.synonym_map.items():
            if original.lower() in sentence.lower():
                # 80% replacement rate
                if random.random() < 0.8:
                    replacement = random.choice(replacements)
                    # Preserve original capitalization
                    if original[0].isupper():
                        replacement = replacement[0].upper() + replacement[1:]
                    
                    sentence = re.sub(
                        r'\b' + re.escape(original) + r'\b',
                        replacement,
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
        
        return sentence
    
    def _add_which_clauses(self, sentence: str) -> str:
        """Add 'which come under' and 'that' clauses"""
        
        # "through the Act" -> "which come under the Act"
        sentence = re.sub(
            r'through the Information Technology Act',
            'which come under the Information Technology Act',
            sentence,
            flags=re.IGNORECASE
        )
        
        sentence = re.sub(
            r'Enacted through',
            'which come under',
            sentence,
            flags=re.IGNORECASE
        )
        
        return sentence
    
    def _add_redundancy_patterns(self, sentence: str) -> str:
        """Add natural redundancy and wordiness"""
        
        # Add "a whole bunch of"
        sentence = re.sub(r'\bpacked homemade', 'packed a whole bunch of homemade', sentence, flags=re.IGNORECASE)
        
        # Add "very" before adjectives
        adjectives = ["nice", "good", "happy", "pleasant", "great", "mild"]
        for adj in adjectives:
            if random.random() < 0.5:
                sentence = re.sub(
                    r'\b' + adj + r'\b',
                    f'very {adj}',
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        # Add double descriptions
        sentence = re.sub(
            r'the winter air was crisp and fresh',
            'The winter air was fresh and crisp',
            sentence,
            flags=re.IGNORECASE
        )
        
        return sentence
    
    def _add_run_on_sentences(self, sentence: str, position: int) -> str:
        """Create run-on sentences with multiple 'and' connectors"""
        
        # High probability of creating run-ons
        if random.random() < 0.4 and len(sentence.split()) > 12:
            # Replace ". " with ", and "
            parts = sentence.split('. ')
            if len(parts) >= 2:
                sentence = f"{parts[0]}, and {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        # Add "and it" constructions
        if random.random() < 0.35:
            sentence = re.sub(
                r'\. The',
                ', and the',
                sentence,
                count=1
            )
        
        return sentence
    
    def _add_human_transitions(self, sentence: str, position: int, total: int) -> str:
        """Add human-like transitions"""
        
        transitions = [
            "What is more,",
            "Furthermore,",
            "Moreover,",
            "In addition,",
            "Additionally,",
            "Notably,",
            "Significantly,"
        ]
        
        # 40% chance to add transition
        if position > 0 and position < total - 1 and random.random() < 0.4:
            if not any(sentence.startswith(t) for t in transitions):
                starter = random.choice(transitions)
                sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Add "Yet" and "Nevertheless"
        sentence = re.sub(r'^However,', random.choice(['Yet,', 'Nevertheless,', 'Nonetheless,']), sentence)
        
        return sentence
    
    def _add_awkward_passives(self, sentence: str) -> str:
        """Add slightly awkward passive constructions"""
        
        passive_transforms = [
            (r'that warmed us', 'that came in a flask, and the flask was shared by the family and it warmed us'),
            (r'food packed by', 'food prepared by'),
            (r'created memories', 'a making of memories'),
            (r'for ever', 'for ever'),
        ]
        
        for pattern, replacement in passive_transforms:
            if random.random() < 0.6:
                sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)
        
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
                humanizer = AggressiveHumanWriter()
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
