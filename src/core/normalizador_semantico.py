import difflib
from src.config import SEMANTIC_SIMILARITY_THRESHOLD

class SemanticNormalizer:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.canonical_terms = []
        self.update_canonical_terms()

    def update_canonical_terms(self):
        self.canonical_terms = self.db_manager.fetch_unique_classifications()
        print(f"DEBUG: Termos para correção de digitação atualizados: {self.canonical_terms}")

    def normalize(self, term):
        if not term or not self.canonical_terms:
            return term.strip().capitalize() if term else ""

        term_lower = term.lower().strip()

        for canonical in self.canonical_terms:
            if canonical.lower() == term_lower:
                return canonical

        matches = difflib.get_close_matches(
            term_lower,
            [t.lower() for t in self.canonical_terms],
            n=1,
            cutoff=SEMANTIC_SIMILARITY_THRESHOLD
        )

        if matches:
            for canonical in self.canonical_terms:
                if canonical.lower() == matches[0]:
                    print(f"Debug Corretor -> Input: '{term}', corrigido para: '{canonical}'")
                    return canonical
        
        return term.strip().capitalize()