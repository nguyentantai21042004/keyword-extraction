#!/usr/bin/env python3
"""
Optimize spaCy+YAKE Parameters for Better Performance
"""

import json
import time
import numpy as np
from typing import Dict, List, Tuple
import asyncio

class SpacyYakeOptimizer:
    def __init__(self):
        self.test_texts = [
            "Machine learning algorithms for natural language processing applications in social media analysis require sophisticated approaches.",
            "Sustainable fashion innovation in the digital age transforms traditional retail through blockchain technology and AI-driven insights.",
            "The quantum computing paradigm shift necessitates interdisciplinary collaboration between physicists, computer scientists, and mathematicians."
        ]
        
    def create_optimized_extractor(self, config: Dict):
        """Create spaCy+YAKE extractor with optimized parameters"""
        try:
            import spacy
            import yake
            
            # Load spaCy model
            try:
                nlp = spacy.load("en_core_web_sm")
            except OSError:
                spacy.cli.download("en_core_web_sm")
                nlp = spacy.load("en_core_web_sm")
            
            # Initialize YAKE with optimized parameters
            yake_extractor = yake.KeywordExtractor(
                lan=config.get('language', 'en'),
                n=config.get('n_gram', 1),
                dedupLim=config.get('dedup_lim', 0.9),
                top=config.get('top_keywords', 20),
                features=config.get('features', None)
            )
            
            return nlp, yake_extractor
            
        except ImportError as e:
            print(f"Error: {e}")
            return None, None
    
    def extract_keywords_optimized(self, text: str, nlp, yake_extractor, config: Dict) -> Dict:
        """Extract keywords with optimized approach"""
        try:
            start_time = time.time()
            
            # Process with spaCy
            doc = nlp(text)
            
            # Extract named entities and noun chunks
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            
            # Extract keywords with YAKE
            yake_keywords = yake_extractor.extract_keywords(text)
            
            # Enhanced keyword processing
            keywords = []
            
            # Process YAKE keywords with filtering
            min_score = config.get('min_score', 0.1)
            for i, (keyword, score) in enumerate(yake_keywords):
                normalized_score = 1 - score
                if normalized_score >= min_score:
                    keywords.append({
                        'keyword': keyword,
                        'score': normalized_score,
                        'rank': i + 1,
                        'type': 'yake_keyword',
                        'relevance': normalized_score
                    })
            
            # Enhanced entity processing
            entity_weight = config.get('entity_weight', 0.8)
            for i, (entity, label) in enumerate(entities[:config.get('max_entities', 10)]):
                # Filter entities by length and relevance
                if len(entity.split()) <= config.get('max_entity_words', 3):
                    keywords.append({
                        'keyword': entity,
                        'score': entity_weight,
                        'rank': len(keywords) + 1,
                        'type': f'entity_{label.lower()}',
                        'relevance': entity_weight
                    })
            
            # Enhanced noun chunk processing
            chunk_weight = config.get('chunk_weight', 0.6)
            for i, chunk in enumerate(noun_chunks[:config.get('max_chunks', 15)]):
                # Filter chunks by relevance
                if len(chunk.split()) >= config.get('min_chunk_words', 2):
                    keywords.append({
                        'keyword': chunk,
                        'score': chunk_weight,
                        'rank': len(keywords) + 1,
                        'type': 'noun_chunk',
                        'relevance': chunk_weight
                    })
            
            # Advanced ranking and filtering
            keywords = self._advanced_ranking(keywords, config)
            
            # Calculate confidence
            confidence = self._calculate_enhanced_confidence(keywords, entities, noun_chunks, config)
            
            processing_time = time.time() - start_time
            
            return {
                'keywords': keywords[:config.get('final_keywords', 20)],
                'processing_time': processing_time,
                'confidence': confidence,
                'entities_count': len(entities),
                'noun_chunks_count': len(noun_chunks),
                'yake_keywords_count': len(yake_keywords)
            }
            
        except Exception as e:
            return {
                'keywords': [],
                'processing_time': 0,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _advanced_ranking(self, keywords: List[Dict], config: Dict) -> List[Dict]:
        """Advanced keyword ranking with multiple factors"""
        for kw in keywords:
            # Length penalty for very long keywords
            length_penalty = min(len(kw['keyword'].split()) / 5, 0.3)
            
            # Type-specific adjustments
            if kw['type'] == 'yake_keyword':
                type_bonus = 0.1
            elif 'entity' in kw['type']:
                type_bonus = 0.2
            else:
                type_bonus = 0.0
            
            # Apply adjustments
            kw['score'] = min(kw['score'] + type_bonus - length_penalty, 1.0)
        
        # Sort by adjusted score
        keywords.sort(key=lambda x: x['score'], reverse=True)
        
        # Re-rank
        for i, kw in enumerate(keywords):
            kw['rank'] = i + 1
        
        return keywords
    
    def _calculate_enhanced_confidence(self, keywords: List[Dict], entities: List, noun_chunks: List, config: Dict) -> float:
        """Enhanced confidence calculation"""
        if not keywords:
            return 0.0
        
        # Base confidence from keyword scores
        base_scores = [kw['score'] for kw in keywords]
        base_confidence = np.mean(base_scores) if base_scores else 0.5
        
        # Entity bonus
        entity_bonus = min(len(entities) / config.get('entity_bonus_divisor', 10), 0.2)
        
        # Noun chunk bonus
        chunk_bonus = min(len(noun_chunks) / config.get('chunk_bonus_divisor', 20), 0.1)
        
        # Diversity bonus (different types of keywords)
        keyword_types = set(kw['type'] for kw in keywords)
        diversity_bonus = min(len(keyword_types) / 5, 0.1)
        
        # Length penalty for very short texts
        total_text_length = sum(len(kw['keyword']) for kw in keywords)
        length_bonus = min(total_text_length / 1000, 0.1)
        
        total_confidence = base_confidence + entity_bonus + chunk_bonus + diversity_bonus + length_bonus
        
        return min(total_confidence, 1.0)
    
    def test_configuration(self, config: Dict) -> Dict:
        """Test a specific configuration"""
        print(f"\n🔍 Testing configuration: {config.get('name', 'Unknown')}")
        
        nlp, yake_extractor = self.create_optimized_extractor(config)
        if not nlp or not yake_extractor:
            return {'error': 'Failed to load models'}
        
        results = []
        total_time = 0
        total_confidence = 0
        
        for i, text in enumerate(self.test_texts):
            result = self.extract_keywords_optimized(text, nlp, yake_extractor, config)
            results.append(result)
            total_time += result.get('processing_time', 0)
            total_confidence += result.get('confidence', 0)
        
        avg_time = total_time / len(self.test_texts)
        avg_confidence = total_confidence / len(self.test_texts)
        total_keywords = sum(len(r.get('keywords', [])) for r in results)
        
        return {
            'config': config,
            'avg_processing_time': avg_time,
            'avg_confidence': avg_confidence,
            'total_keywords': total_keywords,
            'results': results
        }
    
    def optimize_parameters(self) -> Dict:
        """Test multiple configurations to find optimal parameters"""
        print("🚀 Starting spaCy+YAKE Optimization...")
        print("=" * 60)
        
        # Define different configurations to test
        configurations = [
            {
                'name': 'Default',
                'n_gram': 1,
                'dedup_lim': 0.9,
                'top_keywords': 20,
                'min_score': 0.1,
                'max_entities': 10,
                'max_chunks': 15,
                'entity_weight': 0.8,
                'chunk_weight': 0.6
            },
            {
                'name': 'High Precision',
                'n_gram': 1,
                'dedup_lim': 0.95,
                'top_keywords': 15,
                'min_score': 0.2,
                'max_entities': 8,
                'max_chunks': 10,
                'entity_weight': 0.9,
                'chunk_weight': 0.7
            },
            {
                'name': 'High Recall',
                'n_gram': 2,
                'dedup_lim': 0.8,
                'top_keywords': 30,
                'min_score': 0.05,
                'max_entities': 15,
                'max_chunks': 20,
                'entity_weight': 0.7,
                'chunk_weight': 0.5
            },
            {
                'name': 'Balanced',
                'n_gram': 1,
                'dedup_lim': 0.9,
                'top_keywords': 25,
                'min_score': 0.15,
                'max_entities': 12,
                'max_chunks': 18,
                'entity_weight': 0.8,
                'chunk_weight': 0.6
            },
            {
                'name': 'Fast Processing',
                'n_gram': 1,
                'dedup_lim': 0.85,
                'top_keywords': 15,
                'min_score': 0.25,
                'max_entities': 5,
                'max_chunks': 8,
                'entity_weight': 0.8,
                'chunk_weight': 0.6
            }
        ]
        
        # Test all configurations
        all_results = []
        for config in configurations:
            result = self.test_configuration(config)
            if 'error' not in result:
                all_results.append(result)
                print(f"✅ {config['name']}: Time={result['avg_processing_time']:.4f}s, Confidence={result['avg_confidence']:.3f}, Keywords={result['total_keywords']}")
        
        # Find best configuration
        if all_results:
            best_by_time = min(all_results, key=lambda x: x['avg_processing_time'])
            best_by_confidence = max(all_results, key=lambda x: x['avg_confidence'])
            
            print(f"\n🏆 OPTIMIZATION RESULTS:")
            print(f"   Fastest: {best_by_time['config']['name']} ({best_by_time['avg_processing_time']:.4f}s)")
            print(f"   Most Confident: {best_by_confidence['config']['name']} ({best_by_confidence['avg_confidence']:.3f})")
            
            # Save results
            optimization_results = {
                'all_configurations': all_results,
                'best_by_time': best_by_time,
                'best_by_confidence': best_by_confidence,
                'recommendations': self._generate_recommendations(all_results)
            }
            
            with open('spacy_yake_optimization_results.json', 'w') as f:
                json.dump(optimization_results, f, indent=2)
            
            print(f"💾 Results saved to 'spacy_yake_optimization_results.json'")
            
            return optimization_results
        
        return {'error': 'No valid results'}
    
    def _generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if not results:
            return recommendations
        
        # Analyze processing time
        avg_time = np.mean([r['avg_processing_time'] for r in results])
        if avg_time > 0.1:
            recommendations.append("Consider reducing 'top_keywords' or 'max_entities' for faster processing")
        
        # Analyze confidence
        avg_confidence = np.mean([r['avg_confidence'] for r in results])
        if avg_confidence < 0.7:
            recommendations.append("Consider increasing 'min_score' threshold for better quality keywords")
        
        # Analyze keyword count
        avg_keywords = np.mean([r['total_keywords'] for r in results])
        if avg_keywords < 10:
            recommendations.append("Consider lowering 'min_score' or increasing 'top_keywords' for more keywords")
        
        return recommendations

def main():
    print("🚀 SPAÇY+YAKE OPTIMIZATION TOOL")
    print("=" * 60)
    
    optimizer = SpacyYakeOptimizer()
    results = optimizer.optimize_parameters()
    
    if 'error' not in results:
        print("\n🎯 OPTIMIZATION COMPLETED!")
        print("💡 Check 'spacy_yake_optimization_results.json' for detailed results")
    else:
        print(f"\n❌ Optimization failed: {results['error']}")

if __name__ == "__main__":
    main()
