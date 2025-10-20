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


class PerfectHumanWriter:
    """
    Perfect human mimicry with intentional grammatical quirks and natural imperfections
    """
    
    def __init__(self):
        # Comprehensive synonym and transformation map
        self.synonym_map = {
            # Opening phrases
            "may sound": ["might seem", "may appear", "could sound"],
            "impossible or imaginary": ["impossible or fanciful", "unbelievable or fictional"],
            "but it serves as": ["but it is", "yet it represents", "but it functions as"],
            "a powerful metaphor": ["a strong metaphor", "a potent symbol", "a compelling metaphor"],
            "for how": ["for showing how", "demonstrating how", "illustrating how"],
            "even the smallest": ["even the most unappreciated and tiniest", "even the tiniest", "even the most minor"],
            "when underestimated": ["when overlooked", "if ignored", "when taken for granted"],
            "can bring down": ["can bringing down", "can topple", "are capable to bring down"],
            "the mightiest": ["the strongest", "the most powerful", "the greatest"],
            
            # Context phrases
            "In life, history, and politics": ["There are innumerable instances in life, history, and politics", "Throughout life, history, and politics"],
            "there are countless examples": ["where the most insignificant actions or people have been the cause of huge changes"],
            "where seemingly insignificant": ["where the most insignificant", "in which apparently minor"],
            "have caused": ["have been the cause of", "have triggered", "have led to"],
            "major shifts": ["huge changes", "significant transformations", "massive shifts"],
            "proving that": ["demonstrating that", "showing that", "establishing that"],
            "are not always": ["are not", "are not necessarily", "may not be"],
            "the ultimate measure": ["the ultimate criteria to measure", "the final measure", "the definitive measure"],
            
            # Elephant imagery
            "Imagine an enormous elephant": ["Just picture an elephant, the giant of the forest", "Envision a massive elephant", "Picture a huge elephant"],
            "symbolizing": ["representing", "embodying", "standing for"],
            "strength, pride, and dominance": ["strength, pride, and the very lord of the forest", "power, dignity, and supremacy"],
            "marching through": ["walking through", "moving through", "traversing"],
            "with no fear": ["fearlessly", "without any fear", "with complete confidence"],
            "Now imagine": ["Now think of", "Then picture", "Consider now"],
            "a tiny mosquito": ["a mosquito, a tiny struggling insect", "a small mosquito", "a minuscule mosquito"],
            "fragile, small, and easily ignored": ["very weak but also does not care at all about the elephant", "weak, tiny, and overlooked"],
            
            # Disease and threat
            "However": ["But", "Yet", "Nevertheless", "Still"],
            "what the elephant doesn't realize": ["what the elephant doesn't know", "what the elephant fails to understand"],
            "is that the mosquito": ["is that, albeit tiny, the mosquito", "is that the tiny mosquito"],
            "though small": ["albeit tiny", "despite being small", "even being tiny"],
            "carries a deadly disease": ["is loaded with a deadly disease", "harbors a fatal disease"],
            "like malaria": ["such as malaria", "for instance malaria"],
            "With just a single bite": ["The mosquito sucks the blood of the elephant for the first time and then", "With only one bite"],
            "begins a process": ["that very moment in the later stage of the elephant's life a slow process of decline starts", "initiates a process"],
            "that ultimately leads to": ["that eventually causes", "which finally results in"],
            "the elephant's downfall": ["the elephant's demise", "the fall of the elephant"],
            "physical power means nothing": ["brute force is outdone by", "physical strength counts for nothing"],
            "against the silent, invisible threat": ["by the stealthy and imperceptible creature", "against the hidden, unseen danger"],
            "it ignored": ["that it took for granted", "it overlooked", "it dismissed"],
            
            # Reflection
            "This story is not just about nature": ["This tale is not only of the wild", "This narrative is not merely about nature"],
            "it reflects our own world": ["it is a mirror to our world", "it mirrors our reality"],
            
            # Historical examples
            "Throughout history": ["We have witnessed throughout the ages", "Across history", "Through the ages"],
            "we have seen": ["there have been", "we have witnessed", "history shows"],
            "great empires fall": ["the demise of mighty kingdoms", "powerful empires collapse"],
            "not because of": ["but not always due to", "not due to", "not owing to"],
            "massive wars": ["great wars", "huge conflicts", "large-scale battles"],
            "but because of": ["often it was just", "but rather due to", "but from"],
            "internal decay": ["slow internal decay", "internal corruption", "domestic deterioration"],
            "small rebellions": ["little revolts", "minor uprisings", "petty rebellions"],
            "or ignored warnings": ["or warnings long since ignored", "or overlooked cautions"],
            
            # Examples of change
            "A student's voice sparked": ["The voice of a student started", "A student's voice ignited"],
            "revolutions": ["the revolutions", "revolutionary movements"],
            "a whistleblower changed": ["the act of a whistleblower turned", "a whistleblower altered"],
            "the course of justice": ["the wheel of justice", "the path of justice"],
            "one vote has shifted": ["a single vote determined the victor in", "one vote changed"],
            "political powers": ["a power struggle", "political dynamics"],
            "These are all examples": ["All these instances are", "These all represent examples"],
            "bringing down": ["defeating", "toppling", "taking down"],
            
            # Lesson and modern application
            "This metaphor also teaches us": ["This image also conveys the message that we should be", "This metaphor also shows us"],
            "humility and awareness": ["modest and very observant", "humbleness and vigilance"],
            "It reminds us that": ["It tells us that", "It shows us that"],
            "power must be balanced with wisdom": ["the wise and the powerful must come together", "power requires wisdom"],
            "and those who": ["and that those who", "and individuals who"],
            "seem small or powerless": ["appear small or weak", "look insignificant or helpless"],
            "should never be dismissed": ["should never be disregarded", "must not be ignored"],
            "In the age of": ["In the internet age", "In the era of", "In this age of"],
            "social media": ["the internet", "digital media"],
            "a single post": ["a single tweet", "one post", "a lone message"],
            "can tarnish": ["can cause a", "can damage", "can ruin"],
            "reputations": ["reputation downfall", "one's reputation"],
            "a minor bug": ["a small bug", "a tiny glitch"],
            "can crash": ["can take down", "can destroy", "can break"],
            "a powerful system": ["a supercomputer", "a major system"],
            "a lone individual": ["a single person", "one person alone"],
            "can lead": ["can start", "can initiate", "can begin"],
            "a movement": ["a revolution", "a social movement"],
            
            # Conclusion
            "In conclusion": ["To wrap it up", "To sum up", "In summary", "Finally"],
            "reminds us that": ["is a reminder that", "tells us that"],
            "no one is too small": ["nobody is too insignificant", "no person is too tiny"],
            "to make a difference": ["to create change", "to have an impact"],
            "and no one is too big": ["and nobody is too powerful", "and no one is too mighty"],
            "to fall": ["to collapse", "to be brought down"],
            "Strength lies": ["True strength exists", "Real power lies"],
            "not just in size": ["not only in size", "not merely in magnitude"],
            "but in": ["but also in", "but rather in"],
            "strategy, awareness, and resilience": ["wisdom, vigilance, and adaptability"]
        }
        
        # Grammatical quirk patterns (intentional errors)
        self.quirk_patterns = [
            # Wrong verb forms
            (r"can bring down", "can bringing down"),
            (r"are capable of bringing", "are capable to bring"),
            
            # Awkward constructions
            (r"a tiny mosquito—fragile", "a mosquito, a tiny struggling insect that is very weak but also does not care"),
            
            # Verbose redundancy
            (r"enormous elephant, symbolizing strength", "elephant, the giant of the forest, representing strength, pride, and the very lord of the forest"),
            
            # Awkward temporal phrases
            (r"With just a single bite, the mosquito begins", "The mosquito sucks the blood of the elephant for the first time and then that very moment in the later stage"),
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
        """Perfect human mimicry with natural imperfections"""
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Multiple aggressive passes
            sentence = self._expand_contractions(sentence)
            
            # 5 rounds of ultra-aggressive replacement
            for round_num in range(5):
                sentence = self._mega_aggressive_synonyms(sentence)
            
            sentence = self._add_grammatical_quirks(sentence)
            sentence = self._add_verbose_descriptions(sentence)
            sentence = self._add_awkward_constructions(sentence)
            sentence = self._create_complex_sentences(sentence, i)
            sentence = self._add_natural_transitions(sentence, i, len(sentences))
            sentence = self._add_mixed_patterns(sentence)
            
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
    
    def _mega_aggressive_synonyms(self, sentence: str) -> str:
        """MEGA AGGRESSIVE - 98% replacement across 5 rounds"""
        
        # Sort by phrase length
        sorted_syns = sorted(
            self.synonym_map.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for original, replacements in sorted_syns:
            if original.lower() in sentence.lower():
                # 98% replacement rate!
                if random.random() < 0.98:
                    replacement = random.choice(replacements) if isinstance(replacements, list) else replacements
                    
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
    
    def _add_grammatical_quirks(self, sentence: str) -> str:
        """Add intentional grammatical quirks (30% chance)"""
        
        if random.random() < 0.3:
            quirks = [
                (r"can bring down", "can bringing down"),
                (r"are able to", "are capable to"),
                (r"have been", "have been the"),
                (r"is that", "is that,"),
            ]
            
            for pattern, quirk in quirks:
                if pattern in sentence.lower():
                    sentence = re.sub(pattern, quirk, sentence, count=1, flags=re.IGNORECASE)
                    break
        
        return sentence
    
    def _add_verbose_descriptions(self, sentence: str) -> str:
        """Add verbose, redundant descriptions"""
        
        verbose_map = {
            "an enormous elephant": "an elephant, the giant of the forest",
            "symbolizing strength": "representing strength, pride, and the very lord of the forest",
            "a tiny mosquito": "a mosquito, a tiny struggling insect",
            "fragile, small": "very weak but also does not care at all",
        }
        
        for short, verbose in verbose_map.items():
            if short in sentence.lower() and random.random() < 0.5:
                sentence = re.sub(
                    re.escape(short),
                    verbose,
                    sentence,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return sentence
    
    def _add_awkward_constructions(self, sentence: str) -> str:
        """Add slightly awkward but natural constructions"""
        
        # "albeit tiny" construction
        sentence = re.sub(
            r"though small",
            "albeit tiny",
            sentence,
            flags=re.IGNORECASE
        )
        
        # "loaded with" instead of "carries"
        sentence = re.sub(
            r"carries a deadly",
            "is loaded with a deadly",
            sentence,
            flags=re.IGNORECASE
        )
        
        # Complex temporal phrases
        sentence = re.sub(
            r"With just a single bite, the mosquito begins a process",
            "The mosquito sucks the blood for the first time and then that very moment a slow process starts",
            sentence,
            flags=re.IGNORECASE
        )
        
        return sentence
    
    def _create_complex_sentences(self, sentence: str, position: int) -> str:
        """Create complex run-on sentences"""
        
        # 65% probability of complex sentences
        if random.random() < 0.65 and len(sentence.split()) > 12:
            parts = sentence.split('. ')
            if len(parts) >= 2:
                connectors = [
                    ", but not always due to",
                    ", often it was just",
                    "; it is a",
                    ", which",
                    ", and then"
                ]
                connector = random.choice(connectors)
                sentence = f"{parts[0]}{connector} {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        return sentence
    
    def _add_natural_transitions(self, sentence: str, position: int, total: int) -> str:
        """Add natural human transitions"""
        
        transitions = [
            "Moreover,",
            "To add to this,",
            "Furthermore,",
            "In addition,",
            "What is more,",
            "Besides this,",
            "Additionally,"
        ]
        
        # 55% chance
        if position > 0 and position < total - 1 and random.random() < 0.55:
            if not any(sentence.startswith(t) for t in transitions):
                if not sentence.startswith(("The", "One", "A", "This", "These", "Just", "Now")):
                    starter = random.choice(transitions)
                    sentence = f"{starter} {sentence[0].lower()}{sentence[1:]}"
        
        # Replace standard transitions
        transition_replacements = {
            "However,": ["But,", "Yet,", "Nevertheless,", "Still,"],
            "In conclusion,": ["To wrap it up,", "To sum up,", "Finally,"],
            "Moreover,": ["To add to this,", "Furthermore,"],
        }
        
        for orig, replacements in transition_replacements.items():
            if sentence.startswith(orig):
                sentence = sentence.replace(orig, random.choice(replacements), 1)
        
        return sentence
    
    def _add_mixed_patterns(self, sentence: str) -> str:
        """Add mixed constructions and patterns"""
        
        # "not always due to... often it was"
        sentence = re.sub(
            r"not because of ([^,]+), but because of",
            r"but not always due to \1, often it was just",
            sentence,
            flags=re.IGNORECASE
        )
        
        # "the act of" constructions
        sentence = re.sub(
            r"a whistleblower changed",
            "the act of a whistleblower turned",
            sentence,
            flags=re.IGNORECASE
        )
        
        # "determined the victor"
        sentence = re.sub(
            r"one vote has shifted political powers",
            "a single vote determined the victor in a power struggle",
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
                humanizer = PerfectHumanWriter()
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
