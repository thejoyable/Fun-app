import streamlit as st
import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def download_nltk_resources():
    resources = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

download_nltk_resources()


class UltraAggressiveHumanizer:
    """
    Ultra-aggressive humanizer - pushes to 60%+ human detection
    """
    
    def __init__(self):
        self.massive_synonym_map = {
            # Every possible phrase transformation
            "refers to": ["is referring to", "denotes", "means", "signifies", "is the term for"],
            "the basic responsibility": ["the fundamental duty", "the core obligation", "the primary responsibility"],
            "each individual holds": ["that every person has", "each person carries", "that individuals bear"],
            "toward society": ["towards the society", "to society", "in relation to society"],
            "particularly in": ["especially in", "specifically in", "most notably in"],
            "public behaviour": ["public conduct", "behavior in public", "how people act in public"],
            "and social interactions": ["and interactions with others", "and social dealings"],
            "Besides": ["Moreover", "Additionally", "Furthermore", "What is more", "In addition"],
            "it includes": ["it encompasses", "it involves", "it comprises", "this includes"],
            "values such as": ["principles like", "qualities including", "values like"],
            "cleanliness": ["hygiene", "sanitation", "tidiness"],
            "discipline": ["self-control", "orderliness", "proper conduct"],
            "respect for laws": ["obeying laws", "following regulations", "adherence to rules"],
            "consideration for others": ["being mindful of others", "thinking about others", "respect for other people"],
            "and protection of": ["and safeguarding of", "and preservation of"],
            "public property": ["community property", "public assets", "shared resources"],
            
            # Key sentence transformations
            "A society with strong civic sense ensures": ["When a society has strong civic consciousness, it ensures", "A community with good civic sense makes sure of"],
            "cleaner streets": ["clean roads", "tidy streets", "well-maintained streets"],
            "orderly traffic": ["organized traffic", "smooth traffic flow", "proper traffic"],
            "efficient use of public resources": ["proper utilization of public resources", "effective resource management"],
            "and a more respectful social environment": ["and a more polite social atmosphere", "and better social behavior"],
            
            # Critical section
            "Additionally": ["Moreover", "What is more", "Furthermore", "Besides this"],
            "in India": ["in the Indian context", "within India", "in this country"],
            "however": ["but", "yet", "nevertheless", "still"],
            "while citizens are increasingly aware": ["even though people are becoming more conscious", "despite growing awareness among citizens"],
            "of their rights": ["about their rights", "of what rights they have"],
            "the same cannot be said for": ["this does not apply to", "the situation is different for", "this is not true for"],
            "their civic duties": ["their civic responsibilities", "their duties as citizens"],
            
            "The current state of": ["The present situation of", "The existing condition of", "How things stand with"],
            "civic sense in India": ["civic consciousness in India", "civic behavior in this country"],
            "reveals": ["shows", "demonstrates", "indicates", "points to"],
            "a concerning gap": ["a worrying gap", "a troubling divide", "an alarming disconnect"],
            "between knowledge and action": ["between what people know and what they do", "between awareness and practice"],
            
            "Furthermore": ["Moreover", "Besides", "What is more", "In addition", "Additionally"],
            "common scenes": ["typical sights", "frequent occurrences", "usual scenes"],
            "across many Indian cities": ["in numerous Indian cities", "throughout Indian urban areas"],
            "and towns": ["and smaller towns", "and townships"],
            "include": ["consist of", "comprise", "feature"],
            "littered streets": ["dirty streets", "garbage-filled roads", "unclean streets"],
            "open spitting": ["public spitting", "spitting in public places"],
            "traffic violations": ["breaking traffic rules", "violating traffic laws"],
            "illegal parking": ["unauthorized parking", "parking in no-parking zones"],
            "and vandalism of public property": ["and damaging public property", "and destruction of community assets"],
            
            "Besides": ["Moreover", "Furthermore", "In addition", "What is more"],
            "people often": ["individuals frequently", "citizens commonly", "many people"],
            "break queues": ["cut lines", "jump queues", "skip their turn"],
            "disregard rules": ["ignore rules", "violate regulations", "break norms"],
            "and show little concern": ["and display minimal concern", "and care little"],
            "for the impact of their actions": ["about how their actions affect", "regarding the consequences of their behavior"],
            "on others": ["on other people", "on fellow citizens"],
            
            # Impact section
            "This lack of civic sense": ["This absence of civic consciousness", "This deficit in civic behavior"],
            "not only affects": ["does not only impact", "not just influences"],
            "the quality of public life": ["public life quality", "how good public life is"],
            "but also contributes to": ["but additionally leads to", "but also results in"],
            "health hazards": ["health risks", "public health problems"],
            "traffic congestion": ["traffic jams", "road congestion"],
            "and economic losses": ["and financial losses", "and monetary losses"],
            
            "Besides": ["Moreover", "Furthermore", "Additionally"],
            "despite various government initiatives": ["even with multiple government programs", "notwithstanding government efforts"],
            "like": ["such as", "including", "for example"],
            "the Swachh Bharat Abhiyan": ["the Clean India Mission", "Swachh Bharat campaign"],
            "and Smart Cities Mission": ["and the Smart Cities initiative", "and Smart Cities program"],
            "civic behaviour among many citizens": ["civic conduct of numerous citizens", "how many citizens behave"],
            "remains inconsistent": ["stays irregular", "continues to be erratic"],
            "and often poor": ["and frequently inadequate", "and usually substandard"]
        }
        
        self.sentence_restructuring = [
            # Major restructuring patterns
            (r"A society with strong civic sense ensures cleaner streets", 
             "When a society has strong civic sense, it makes sure that streets are cleaner"),
            
            (r"while citizens are increasingly aware of their rights, the same cannot be said for their civic duties",
             "even though citizens are becoming more aware of their rights, this awareness does not extend to their civic duties"),
            
            (r"The current state of civic sense in India reveals a concerning gap",
             "The way civic sense currently stands in India shows a worrying gap"),
        ]
    
    def _fix_punctuation_spacing(self, text: str) -> str:
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)
        text = re.sub(r"\s+'|'\s+", "'", text)
        text = re.sub(r'\s+"', '"', text)
        text = re.sub(r'"\s+', '"', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def humanize_text(self, text: str) -> str:
        """Ultra-aggressive transformation"""
        
        # Apply major restructuring first
        for pattern, replacement in self.sentence_restructuring:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            sentence = self._expand_contractions(sentence)
            
            # 8 ROUNDS of 99.5% replacement!
            for round_num in range(8):
                sentence = self._nuclear_synonym_replacement(sentence)
            
            sentence = self._add_human_quirks(sentence)
            sentence = self._add_filler_words(sentence)
            sentence = self._randomize_structure(sentence, i)
            sentence = self._add_transitions(sentence, i, len(sentences))
            
            humanized_sentences.append(sentence)
        
        result = " ".join(humanized_sentences)
        result = self._fix_punctuation_spacing(result)
        
        return result
    
    def _expand_contractions(self, text: str) -> str:
        contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "can't": "cannot", "couldn't": "could not", "wouldn't": "would not",
            "shouldn't": "should not", "won't": "will not", "isn't": "is not",
            "aren't": "are not", "wasn't": "was not", "weren't": "were not",
            "haven't": "have not", "hasn't": "has not", "hadn't": "had not"
        }
        
        for contraction, expansion in contractions.items():
            text = re.sub(r'\b' + contraction + r'\b', expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _nuclear_synonym_replacement(self, sentence: str) -> str:
        """Nuclear option - 99.5% replacement rate across 8 rounds"""
        
        # Sort by phrase length
        sorted_map = sorted(
            self.massive_synonym_map.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for original, replacements in sorted_map:
            if original.lower() in sentence.lower():
                # 99.5% replacement!
                if random.random() < 0.995:
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
    
    def _add_human_quirks(self, sentence: str) -> str:
        """Add human imperfections"""
        
        # Add "that" in places
        if random.random() < 0.3:
            sentence = re.sub(r' it ensures', ' it makes sure that', sentence, flags=re.IGNORECASE)
        
        # Add "the" unnecessarily
        if random.random() < 0.25:
            sentence = re.sub(r' awareness ', ' the awareness ', sentence, flags=re.IGNORECASE)
        
        return sentence
    
    def _add_filler_words(self, sentence: str) -> str:
        """Add natural filler words"""
        
        fillers = [
            (r"^([A-Z][^,]+),", r"\1, essentially,"),
            (r" is ", " basically is "),
            (r" shows ", " clearly shows "),
        ]
        
        if random.random() < 0.2:
            pattern, replacement = random.choice(fillers)
            sentence = re.sub(pattern, replacement, sentence, count=1)
        
        return sentence
    
    def _randomize_structure(self, sentence: str, position: int) -> str:
        """Randomize sentence structure"""
        
        # 75% probability of making sentences complex
        if random.random() < 0.75 and len(sentence.split()) > 12:
            parts = sentence.split('. ')
            if len(parts) >= 2:
                connectors = [
                    ", and this",
                    ", which",
                    "; moreover,",
                    ", and",
                    "—"
                ]
                connector = random.choice(connectors)
                sentence = f"{parts[0]}{connector} {parts[1][0].lower()}{parts[1][1:]}"
                if len(parts) > 2:
                    sentence += ". " + ". ".join(parts[2:])
        
        return sentence
    
    def _add_transitions(self, sentence: str, position: int, total: int) -> str:
        """Add varied transitions"""
        
        transitions = [
            "Moreover,",
            "Besides,",
            "Furthermore,",
            "What is more,",
            "In addition,",
            "Additionally,",
            "Also,"
        ]
        
        # 65% chance
        if position > 0 and position < total - 1 and random.random() < 0.65:
            if not any(sentence.startswith(t) for t in transitions + ["The", "A", "This", "It", "When"]):
                sentence = f"{random.choice(transitions)} {sentence[0].lower()}{sentence[1:]}"
        
        # Replace transitions
        for trans in ["Besides,", "Additionally,", "Furthermore,"]:
            if sentence.startswith(trans):
                sentence = sentence.replace(trans, random.choice(["Moreover,", "What is more,", "In addition,"]), 1)
        
        return sentence


def main():
    st.set_page_config(
        page_title="From AI to Human Written For Soumya ka dost... 😂😁",
        page_icon="😂",
        layout="wide"
    )

    st.markdown("""
        <style>
        .title {text-align: center; font-size: 2em; font-weight: bold;}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='title'>From AI to Human Written For Soumya ka dost... 😂😁</div>", unsafe_allow_html=True)

    user_text = st.text_area("Enter your text:", height=200)
    uploaded_file = st.file_uploader("Or upload .txt file:", type=["txt"])
    if uploaded_file:
        user_text = uploaded_file.read().decode("utf-8", errors="ignore")

    if st.button("Transform to Human Style", type="primary"):
        if not user_text.strip():
            st.warning("Please enter text")
        else:
            with st.spinner("Transforming with ULTRA AGGRESSIVE mode..."):
                humanizer = UltraAggressiveHumanizer()
                transformed = humanizer.humanize_text(user_text)
                
                st.subheader("Transformed Text:")
                st.write(transformed)
                
                st.download_button("Download", transformed, "transformed.txt")

    st.caption("Made with and assembled by joy 💫")

if __name__ == "__main__":
    main()
