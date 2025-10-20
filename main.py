import streamlit as st
import random
import re
from typing import List, Tuple, Dict
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
    Maximum aggression humanizer with all natural human patterns
    """
    
    def __init__(self):
        # Ultra-comprehensive synonym map
        self.synonym_map = {
            # Primary expressions
            "refers to": ["is the term used to signify", "denotes", "represents", "signifies"],
            "among nations": ["not only among states but also among", "between countries and"],
            "encompasses": ["covers", "includes", "spans", "comprises"],
            "a wide range of": ["a wide variety of", "a broad spectrum of", "numerous"],
            "including": ["such as", "like", "for example", "including but not limited to"],
            
            # Temporal expressions
            "In today's": ["In the present day,", "In the current era,", "In modern times,"],
            "interconnected world": ["interconnected world", "globally connected environment"],
            "can have": ["can produce", "can create", "can generate", "may have"],
            "far-reaching effects": ["consequences in different parts of the world", "widespread impacts"],
            "making": ["thus,", "therefore,", "consequently,"],
            "more significant than ever": ["more important than ever", "more crucial than before"],
            
            # Historical context
            "is largely shaped by": ["has been largely influenced by", "has been molded by", "is primarily formed by"],
            "historical events": ["historical occurrences", "past events", "historical developments"],
            "like": ["such as", "including", "for instance"],
            "the rise of": ["the establishment of", "the formation of", "the creation of"],
            "such as": ["like", "including", "for example"],
            
            # Power dynamics
            "shifted towards": ["moved towards", "transitioned to", "evolved into"],
            "led by": ["headed by", "dominated by", "controlled by"],
            "However": ["Yet", "Nevertheless", "Nonetheless", "Still"],
            "with the collapse": ["the disintegration", "the fall", "the breakdown"],
            "emerged": ["arose", "appeared", "came into being"],
            "with the United States as": ["with the United States as", "marking the United States as"],
            "the dominant": ["the most powerful", "the leading", "the preeminent"],
            "Today": ["Currently", "At present", "In the current situation"],
            "is increasingly": ["is becoming more and more", "is growing more", "is progressively becoming"],
            "multipolar": ["multipolar", "polycentric"],
            "playing influential roles": ["being prominent", "playing significant roles", "exerting influence"],
            "on the global stage": ["on the world stage", "in global affairs", "in international politics"],
            
            # Contemporary issues
            "Key issues": ["Main concerns", "Primary matters", "Central topics"],
            "today include": ["currently are", "at present encompass"],
            "the balance of power": ["Balancing power", "Power equilibrium", "The power balance"],
            "Conflicts in regions": ["The situation in", "Tensions in areas", "Disputes in regions"],
            "such as": ["like", "including", "for example"],
            "highlight": ["signify", "demonstrate", "illustrate", "point to"],
            "the ongoing challenges": ["the difficulty", "the continuous struggles", "the persistent problems"],
            "achieving": ["attaining", "reaching", "obtaining"],
            "At the same time": ["Nevertheless", "Simultaneously", "Concurrently"],
            "cooperation through": ["leaders managing to meet at", "collaboration via"],
            "summits like": ["meetings such as", "conferences including"],
            "agreements like": ["accords such as", "treaties like"],
            "show efforts toward": ["can be seen as pointing toward", "demonstrate attempts at", "indicate moves toward"],
            "solving common problems": ["tackle global issues", "address shared challenges", "resolve mutual concerns"],
            
            # Non-state actors
            "is also influenced by": ["is also impacted by", "is additionally affected by"],
            "non-state actors": ["non-state entities", "non-governmental actors"],
            "multinational corporations": ["transnational companies", "global corporations", "international firms"],
            "NGOs": ["non-governmental organizations (NGOs)", "civil society organizations"],
            "which play a role": ["These entities have a hand", "that contribute to", "which participate"],
            "in shaping": ["in molding", "in forming", "in influencing"],
            "opinions and policies": ["public perception and government policy", "viewpoints and regulations"],
            "Moreover": ["To add to this", "Furthermore", "In addition", "Additionally"],
            "globalization and digital communication": ["globalization and digital technology", "global connectivity and technology"],
            "have made": ["have rendered", "have caused", "have transformed"],
            "political developments": ["countries and people", "political events", "policy changes"],
            "more visible and impactful": ["more interconnected than ever", "more transparent and influential"],
            "worldwide": ["globally", "across the world", "internationally"],
            
            # Conclusion patterns
            "In conclusion": ["To conclude", "In summary", "Ultimately"],
            "is a dynamic and complex field": ["represents a multifaceted domain", "is an intricate and evolving area"],
            "that affects": ["that impacts", "that influences", "with effects on"],
            "every individual": ["all people", "each person", "everyone"],
            "Understanding it": ["Comprehending this field", "Grasping these dynamics"],
            "is essential for": ["is crucial to", "is vital for", "is necessary for"],
            "promoting": ["fostering", "advancing", "encouraging"],
            "in a rapidly changing": ["in an evolving", "in a dynamic", "in a constantly shifting"],
            "global environment": ["international landscape", "world context"]
        }
        
        # Complex transformation patterns
        self.transformation_rules = [
            # Passive constructions
            (r"refers to the study", "is the term used to signify the study"),
            (r"among nations, international", "not only among states but also among international"),
            
            # Complex clauses
            (r"the actions of one country can have far-reaching effects, making", 
             "the actions of one country can produce consequences in different parts of the world; thus,"),
            
            # Awkward but natural constructions
            (r"with the collapse of the Soviet Union in 1991, a unipolar moment emerged",
             "the disintegration of the Soviet Union in 1991 marked the beginning of a unipolar moment"),
             
            # Add "not only... but also"
            (r"among nations", "not only among nations but also among"),
            
            # Change "show" to passive
            (r"show efforts toward solving", "can be seen as pointing toward a common will to tackle"),
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
        """ULTIMATE humanization with maximum natural patterns"""
        
        # Apply transformation rules first
        for pattern, replacement in self.transformation_rules:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Multiple passes for maximum coverage
            sentence = self._expand_contractions(sentence)
            
            # 4 rounds of aggressive synonym replacement
            for round_num in range(4):
                sentence = self._ultra_aggressive_synonyms(sentence, round_num)
            
            sentence = self._add_complex_constructions(sentence)
            sentence = self._add_formal_language(sentence)
            sentence = self._create_subordinate_clauses(sentence, i)
            sentence = self._add_passive_voice(sentence)
            sentence = self._add_human_transitions(sentence, i, len(sentences))
            
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
    
    def _ultra_aggressive_synonyms(self, sentence: str, round_num: int) -> str:
        """ULTRA AGGRESSIVE - 95% replacement rate across 4 rounds"""
        
        # Sort by phrase length (longest first)
        sorted_synonyms = sorted(
            self.synonym_map.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for original, replacements in sorted_synonyms:
            # Skip if already replaced in earlier round
            if original.lower() in sentence.lower():
                # 95% replacement probability
                if random.random() < 0.95:
                    replacement = random.choice(replacements)
                    
                    # Preserve capitalization
                    def replace_with_case(match):
                        matched = match.group(0)
                        if matched[0].isupper():
                            return replacement[0].upper() + replacement[1:]
                        return replacement
                    
                    sentence = re.sub(
                        r'\b' + re.escape(original) + r'\b',
                        replace_with_case,
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
        
        return sentence
    
    def _add_complex_constructions(self, sentence: str) -> str:
        """Add 'not only... but also' and other complex patterns"""
        
        # Add "not only... but also"
        sentence = re.sub(
            r'among nations, international',
            'not only among states but also among international',
            sentence,
            flags=re.IGNORECASE
        )
        
        # Add "including but not limited to"
        if "including" in sentence.lower() and random.random() < 0.4:
            sentence = re.sub(
                r'\bincluding\b',
                'including but not limited to',
                sentence,
                count=1,
                flags=re.IGNORECASE
            )
        
        return sentence
    
    def _add_formal_language(self, sentence: str) -> str:
        """Add formal, academic-style language"""
        
        formal_patterns = {
            "is": ["represents", "constitutes", "denotes"],
            "refers to": ["is the term used to signify", "denotes"],
            "have made": ["have rendered", "have caused"],
            "play a role": ["have a hand", "contribute to"],
            "show": ["can be seen as", "demonstrate", "indicate"]
        }
        
        for original, replacements in formal_patterns.items():
            if original in sentence.lower() and random.random() < 0.6:
                replacement = random.choice(replacements)
                sentence = re.sub(
                    r'\b' + re.escape(original) + r'\b',
                    replacement,
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return sentence
    
    def _create_subordinate_clauses(self, sentence: str, position: int) -> str:
        """Create complex subordinate clauses and run-ons"""
        
        # High probability of complex sentences (60%)
        if random.random() < 0.6 and len(sentence.split()) > 12:
            # Replace periods with semicolons or commas + thus/therefore
            parts = sentence.split('. ')
            if len(parts) >= 2:
                connectors = [
                    "; thus,",
                    "; therefore,",
                    ", and thus",
                    ", which",
                    ", and this"
                ]
                connector = random.choice(connectors)
                sentence = f"{parts[0]}{connector} {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        return sentence
    
    def _add_passive_voice(self, sentence: str) -> str:
        """Add passive voice constructions"""
        
        passive_transforms = [
            (r"is largely shaped by", "has been largely influenced by"),
            (r"shifted towards", "moved towards"),
            (r"led by", "headed by"),
            (r"emerged", "marked the beginning of"),
            (r"show efforts", "can be seen as pointing"),
            (r"play a role", "have a hand"),
            (r"which play", "These entities have")
        ]
        
        for pattern, replacement in passive_transforms:
            if random.random() < 0.7:
                sentence = re.sub(
                    pattern,
                    replacement,
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return sentence
    
    def _add_human_transitions(self, sentence: str, position: int, total: int) -> str:
        """Add varied human-like transitions"""
        
        transitions = [
            "Moreover,",
            "To add to this,",
            "Furthermore,",
            "In addition,",
            "Additionally,",
            "Notably,",
            "Significantly,",
            "Besides this,",
            "What is more,"
        ]
        
        # 50% chance to add transition
        if position > 0 and position < total - 1 and random.random() < 0.5:
            has_transition = any(sentence.startswith(t) for t in transitions)
            if not has_transition and not sentence.startswith(("The", "One", "A", "Key", "Main")):
                starter = random.choice(transitions)
                sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Replace standard transitions
        replacements = {
            "However,": ["Yet,", "Nevertheless,", "Nonetheless,", "Still,"],
            "Moreover,": ["To add to this,", "Furthermore,", "In addition,"],
            "At the same time,": ["Nevertheless,", "Simultaneously,"]
        }
        
        for original, options in replacements.items():
            if sentence.startswith(original):
                sentence = sentence.replace(original, random.choice(options), 1)
        
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
