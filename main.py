import streamlit as st
import random
import re
from typing import List, Tuple
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


class UltimateHumanWriter:
    """
    Maximum aggression humanizer with metaphors, analogies, and complex patterns
    """
    
    def __init__(self):
        # Massive synonym map with creative alternatives
        self.synonym_map = {
            # Ultra-varied verbs
            "have revolutionized": ["have brought unprecedented changes to", "have transformed dramatically", "have fundamentally altered"],
            "revolutionized": ["brought unprecedented changes to", "transformed dramatically", "altered fundamentally"],
            "is a type of": ["is a model of", "represents a form of", "constitutes a kind of"],
            "mimics": ["tries to simulate", "attempts to replicate", "seeks to emulate"],
            "using": ["by using", "through the use of", "by employing", "utilizing"],
            "process": ["understand", "analyze", "interpret", "handle"],
            "learn": ["understand and learn", "grasp and comprehend", "absorb"],
            "from large datasets": ["from diverse data the size of a mountain", "from extensive data collections", "from massive data pools"],
            "are capable of": ["are able to", "can", "have the ability to"],
            "learning": ["grasping", "understanding", "acquiring", "absorbing"],
            "making them ideal": ["which is why they are so versatile and necessary", "making them perfect", "rendering them suitable"],
            "require": ["demand", "need", "call for"],
            "high accuracy": ["the highest accuracy", "superior precision", "excellent accuracy"],
            
            # Application descriptions
            "most remarkable": ["most astonishing", "most extraordinary", "most striking"],
            "applications": ["uses", "implementations", "deployments"],
            "stands for": ["means", "represents", "is short for"],
            "uses a single": ["applies a single", "employs a single", "utilizes a single"],
            "detect": ["find", "identify", "locate", "spot"],
            "multiple objects": ["several objects", "numerous objects", "many objects"],
            "in real-time": ["with real-time speed", "instantaneously", "in real time"],
            "Unlike": ["The main difference with", "In contrast to", "Different from"],
            "traditional": ["conventional", "classical", "standard"],
            "that apply classifiers": ["that use multiple classifiers to classify", "applying classifiers"],
            "at multiple scales": ["over several resolutions", "at various scales"],
            "frames": ["treats", "approaches", "handles"],
            "as a single regression problem": ["as a single regression problem instead of using multiple classifiers"],
            "divides": ["partitions", "splits", "breaks down"],
            "into a grid": ["into grid cells", "into a grid structure"],
            "in one pass": ["in one run", "in a single pass", "in one sweep"],
            "through the network": ["through the model", "via the network"],
            "predicts": ["forecasts", "estimates", "determines"],
            "for each object": ["for each of the detections made", "for every object"],
            "This design": ["As a result", "Consequently", "This approach"],
            "allows": ["enables", "permits", "makes it possible for"],
            "to be extremely fast": ["to be lightning-fast", "to be exceptionally quick", "to be remarkably swift"],
            "efficient": ["resource-efficient", "streamlined", "optimized"],
            "making it suitable": ["no wonder it is already applied", "which makes it perfect", "making it ideal"],
            "like": ["such as", "including", "for example"],
            
            # Evolution and improvements
            "has evolved": ["has undergone various metamorphoses", "has transformed", "has developed"],
            "over the years": ["over time", "through the years", "across time"],
            "with newer versions": ["and the latest versions", "with recent iterations"],
            "offering": ["delivering", "providing", "presenting"],
            "improvements": ["enhancements", "upgrades", "advances"],
            "in speed, accuracy, and model size": ["in speed, accuracy, and size of the model"],
            "are trained on": ["are subjected to training on", "undergo training on"],
            "large datasets": ["extensive datasets", "massive datasets", "huge data collections"],
            "can detect": ["can recognize", "can identify", "are able to spot"],
            "hundreds of": ["numerous", "many", "countless"],
            "object classes": ["object categories", "classes of objects"],
            "with high precision": ["with very small error rates", "with excellent accuracy", "with superior precision"],
            
            # Limitations
            "However": ["Yet", "Nevertheless", "Nonetheless", "Still"],
            "also has": ["still suffers from some", "faces certain", "has certain"],
            "limitations": ["drawbacks", "shortcomings", "constraints"],
            "such as": ["like", "including", "for instance"],
            "difficulty detecting": ["inability to recognize", "challenges in detecting", "problems identifying"],
            "small or overlapping": ["tiny or overlapping", "small or overlapped"],
            "Despite this": ["Nevertheless", "Regardless", "Notwithstanding this"],
            "it remains": ["it continues to be", "it persists as", "it stays as"],
            "most popular": ["most favored", "most preferred", "most widely adopted"],
            "widely used": ["extensively used", "commonly employed", "broadly utilized"],
            "deep learning models": ["deep learning models", "neural network models"],
            
            # Additional complex patterns
            "especially in": ["particularly in the fields of", "most notably in"],
            "One of the": ["Among the", "One particular example of"],
            "the field of": ["the world of", "the domain of", "the realm of"],
            "capable of": ["able to", "having the capacity to"],
            "high-level features": ["very abstract characteristics that are hard to dissociate", "complex features"],
            "raw data": ["unprocessed data", "primary data"],
            "real-time applications": ["real-time scenarios", "live applications"],
            "autonomous driving": ["autopilots for cars", "self-driving vehicles"],
            "surveillance": ["monitoring", "observation systems"],
            "robotics": ["robotic systems", "robot technology"],
            "augmented reality": ["AR applications", "mixed reality"],
            "recent": ["latest", "newest", "most recent"],
            "offering improvements": ["delivering enhancements", "providing upgrades"],
            "overlapping objects": ["overlapped objects", "objects that overlap"]
        }
        
        # Complex restructuring patterns
        self.complex_patterns = [
            # Add metaphors and analogies
            (r"from large datasets", "from diverse data the size of a mountain"),
            (r"mimics the human brain", "tries to simulate human brain processing"),
            
            # Make sentences more complex
            (r"These networks are capable of learning", "The networks learn very abstract characteristics that are hard to dissociate from the raw data, which is why they are so versatile and necessary in the domains that require"),
            
            # Add embedded clauses
            (r"This design allows YOLO to be", "As a result, YOLO is"),
            (r", making it suitable for", ", no wonder it is already applied to"),
            
            # Add complex transitions
            (r"YOLO has evolved over the years", "Over time, the YOLO model has undergone various metamorphoses"),
            
            # Add unusual constructions
            (r"It divides the image into a grid and, in one pass through the network, predicts", "The picture is partitioned into grid cells, the network then predicts, in one run, the"),
            
            # Complex descriptions
            (r"Unlike traditional", "The main difference with traditional"),
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
        """ULTIMATE humanization with maximum aggression"""
        
        # First pass: Apply complex patterns
        for pattern, replacement in self.complex_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Multiple transformation passes
            sentence = self._expand_contractions(sentence)
            
            # Apply 3 rounds of synonym replacement for maximum coverage
            for _ in range(3):
                sentence = self._ultra_aggressive_synonyms(sentence)
            
            sentence = self._add_complex_clauses(sentence)
            sentence = self._add_metaphors_and_analogies(sentence)
            sentence = self._create_run_ons(sentence, i)
            sentence = self._add_varied_transitions(sentence, i, len(sentences))
            sentence = self._add_unusual_constructions(sentence)
            
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
    
    def _ultra_aggressive_synonyms(self, sentence: str) -> str:
        """ULTRA AGGRESSIVE - 90% replacement rate"""
        
        # Sort by length (longest first) to replace phrases before individual words
        sorted_synonyms = sorted(self.synonym_map.items(), key=lambda x: len(x[0]), reverse=True)
        
        for original, replacements in sorted_synonyms:
            if original.lower() in sentence.lower():
                # 90% replacement rate!
                if random.random() < 0.9:
                    replacement = random.choice(replacements)
                    
                    # Preserve capitalization
                    pattern = re.escape(original)
                    
                    def replace_preserve_case(match):
                        matched_text = match.group(0)
                        if matched_text[0].isupper():
                            return replacement[0].upper() + replacement[1:]
                        return replacement
                    
                    sentence = re.sub(
                        r'\b' + pattern + r'\b',
                        replace_preserve_case,
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
        
        return sentence
    
    def _add_complex_clauses(self, sentence: str) -> str:
        """Add complex embedded clauses"""
        
        # Add "which" clauses
        if random.random() < 0.3 and "," in sentence:
            sentence = re.sub(
                r', ([a-z]+ing)',
                r', which \1',
                sentence,
                count=1
            )
        
        # Add "that" clauses
        if random.random() < 0.3:
            sentence = re.sub(
                r' are ',
                ' that are ',
                sentence,
                count=1
            )
        
        return sentence
    
    def _add_metaphors_and_analogies(self, sentence: str) -> str:
        """Add metaphorical language"""
        
        metaphors = {
            "large datasets": ["diverse data the size of a mountain", "massive data pools", "enormous data collections"],
            "very fast": ["lightning-fast", "blazingly quick", "remarkably swift"],
            "has changed": ["has brought unprecedented changes to", "has fundamentally transformed"],
            "has improved": ["has undergone metamorphoses", "has evolved dramatically"]
        }
        
        for original, replacements in metaphors.items():
            if original in sentence.lower() and random.random() < 0.7:
                replacement = random.choice(replacements)
                sentence = re.sub(
                    re.escape(original),
                    replacement,
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return sentence
    
    def _create_run_ons(self, sentence: str, position: int) -> str:
        """Create run-on sentences with embedded clauses"""
        
        # High probability of run-ons (50%)
        if random.random() < 0.5 and len(sentence.split()) > 12:
            # Replace ". " with ", and"
            parts = sentence.split('. ')
            if len(parts) >= 2:
                connectors = [", and", ", which", ", and the", ", and this", ", consequently"]
                connector = random.choice(connectors)
                sentence = f"{parts[0]}{connector} {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        return sentence
    
    def _add_varied_transitions(self, sentence: str, position: int, total: int) -> str:
        """Add varied and unusual transitions"""
        
        transitions = [
            "What is more,",
            "Furthermore,",
            "Moreover,",
            "In addition,",
            "Additionally,",
            "Notably,",
            "Significantly,",
            "Interestingly,",
            "Remarkably,"
        ]
        
        # 45% chance
        if position > 0 and position < total - 1 and random.random() < 0.45:
            if not any(sentence.startswith(t) for t in transitions + ["The", "One", "A"]):
                starter = random.choice(transitions)
                sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Replace However
        sentence = re.sub(
            r'^However,',
            random.choice(['Yet,', 'Nevertheless,', 'Nonetheless,', 'Still,']),
            sentence
        )
        
        return sentence
    
    def _add_unusual_constructions(self, sentence: str) -> str:
        """Add slightly unusual but natural constructions"""
        
        # Add "no wonder" constructions
        sentence = re.sub(
            r'making it suitable for',
            'no wonder it is already applied to',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Add "subjected to" constructions
        sentence = re.sub(
            r'are trained on',
            'are subjected to training on',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Add "still suffers from"
        sentence = re.sub(
            r'also has limitations',
            'still suffers from some drawbacks',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Add complex negatives
        sentence = re.sub(
            r'difficulty detecting',
            'inability to recognize',
            sentence,
            flags=re.IGNORECASE
        )
        
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
                humanizer = UltimateHumanWriter()
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
