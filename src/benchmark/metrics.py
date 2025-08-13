"""
Accuracy metrics calculation for keyword extraction
"""

def calculate_accuracy_metrics(extracted_keywords: list, expected_keywords: list) -> dict:
    """Calculate comprehensive accuracy metrics"""
    
    if not expected_keywords:
        return {
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'exact_match': 0.0,
            'partial_match': 0.0
        }
    
    extracted_texts = [kw['keyword'].lower() if isinstance(kw, dict) else kw.lower() for kw in extracted_keywords]
    expected_lower = [kw.lower() for kw in expected_keywords]
    
    # Exact matches
    exact_matches = sum(1 for kw in extracted_texts if kw in expected_lower)
    
    # Partial matches (substring)
    partial_matches = 0
    for expected in expected_lower:
        for extracted in extracted_texts:
            if expected in extracted or extracted in expected:
                partial_matches += 1
                break
    
    # Calculate metrics
    precision_exact = exact_matches / len(extracted_texts) if extracted_texts else 0.0
    recall_exact = exact_matches / len(expected_keywords)
    
    precision_partial = partial_matches / len(extracted_texts) if extracted_texts else 0.0
    recall_partial = partial_matches / len(expected_keywords)
    
    # F1 scores
    f1_exact = 2 * (precision_exact * recall_exact) / (precision_exact + recall_exact) if (precision_exact + recall_exact) > 0 else 0.0
    f1_partial = 2 * (precision_partial * recall_partial) / (precision_partial + recall_partial) if (precision_partial + recall_partial) > 0 else 0.0
    
    return {
        'precision_exact': precision_exact,
        'recall_exact': recall_exact,
        'f1_exact': f1_exact,
        'precision_partial': precision_partial,
        'recall_partial': recall_partial,
        'f1_partial': f1_partial,
        'exact_matches': exact_matches,
        'partial_matches': partial_matches,
        'total_extracted': len(extracted_texts),
        'total_expected': len(expected_keywords)
    }
