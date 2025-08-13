#!/usr/bin/env python3
"""
🧪 spaCy + YAKE Algorithm: Comprehensive Experiment Framework
Thí nghiệm chứng minh hiệu quả của thuật toán spaCy + YAKE

Author: Research Team
Purpose: Provide quantitative evidence for thesis justification
"""

import asyncio
import time
import psutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import json
import os
from datetime import datetime

# Add parent directory to path to import modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our algorithm
from multi_method_extractor import SpacyYakeExtractor, RakeExtractor, TfIdfExtractor, TextRankExtractor, KeyBertExtractor
from hybrid_ensemble import HybridEnsembleExtractor

class SpacyYakeExperiment:
    """Comprehensive experiment framework for spaCy + YAKE algorithm"""
    
    def __init__(self):
        print("🔧 Initializing Experiment Framework...")
        
        # Initialize spaCy + YAKE
        print("   📚 Loading spaCy + YAKE...")
        try:
            self.spacy_yake = SpacyYakeExtractor()
            print("   ✅ spaCy + YAKE loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to load spaCy + YAKE: {e}")
            self.spacy_yake = None
        
        # Initialize baseline methods
        print("   📚 Loading baseline methods...")
        self.baseline_methods = {}
        
        # Load RAKE
        try:
            print("   🔍 Loading RAKE...")
            self.baseline_methods['rake'] = RakeExtractor()
            print("   ✅ RAKE loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to load RAKE: {e}")
        
        # Load TF-IDF
        try:
            print("   🔍 Loading TF-IDF...")
            self.baseline_methods['tfidf'] = TfIdfExtractor()
            print("   ✅ TF-IDF loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to load TF-IDF: {e}")
        
        # Load TextRank
        try:
            print("   🔍 Loading TextRank...")
            self.baseline_methods['textrank'] = TextRankExtractor()
            print("   ✅ TextRank loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to load TextRank: {e}")
        
        # Load KeyBERT
        try:
            print("   🔍 Loading KeyBERT...")
            self.baseline_methods['keybert'] = KeyBertExtractor()
            print("   ✅ KeyBERT loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to load KeyBERT: {e}")
        
        # Load Hybrid Ensemble
        try:
            print("   🔍 Loading Hybrid Ensemble...")
            self.baseline_methods['hybrid_ensemble'] = HybridEnsembleExtractor()
            print("   ✅ Hybrid Ensemble loaded successfully")
        except Exception as e:
            print(f"   ❌ Failed to load Hybrid Ensemble: {e}")
        
        print(f"   📊 Total methods loaded: {len(self.baseline_methods) + (1 if self.spacy_yake else 0)}")
        
        # Experiment configuration
        self.experiment_config = {
            'test_cases': self._create_comprehensive_test_cases(),
            'metrics': ['processing_time', 'memory_usage', 'confidence_score', 'accuracy', 'keywords_count'],
            'iterations': 5,  # Run each test case multiple times for statistical significance
            'save_detailed_results': True
        }
        
        # Results storage
        self.experiment_results = []
        self.detailed_analysis = {}
        
        print("✅ Experiment Framework initialized successfully!")
        
    def _create_comprehensive_test_cases(self) -> List[Dict]:
        """Create comprehensive test cases covering multiple domains and scenarios"""
        
        test_cases = [
            # ===== SOCIAL MEDIA DOMAIN =====
            {
                'id': 'SM_001',
                'category': 'social_media',
                'text': "Just discovered #sustainablefashion trends! @patagonia's new eco-line is amazing 🌱 The collection features organic cotton and recycled materials. #ecofriendly #fashiontech",
                'expected_keywords': ['sustainable fashion', 'patagonia', 'eco-line', 'organic cotton', 'recycled materials', 'ecofriendly', 'fashiontech'],
                'complexity': 'high',
                'hashtags': True,
                'mentions': True,
                'emojis': True
            },
            {
                'id': 'SM_002',
                'category': 'social_media',
                'text': "Need insights on influencer marketing for beauty brands targeting Gen Z #beautytech #influencer #genz #beauty #marketing #digital",
                'expected_keywords': ['influencer marketing', 'beauty brands', 'gen z', 'beautytech', 'beauty', 'marketing', 'digital'],
                'complexity': 'medium',
                'hashtags': True,
                'mentions': False,
                'emojis': False
            },
            
            # ===== BUSINESS DOMAIN =====
            {
                'id': 'BUS_001',
                'category': 'business',
                'text': "Market analysis of renewable energy sector shows significant growth in solar and wind power technologies. Investment in clean energy reached $500 billion in 2023, with solar leading at 45% market share.",
                'expected_keywords': ['market analysis', 'renewable energy', 'solar power', 'wind power', 'investment', 'clean energy', 'market share'],
                'complexity': 'high',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            {
                'id': 'BUS_002',
                'category': 'business',
                'text': "Digital transformation strategies for traditional retail businesses in the post-pandemic era. Key focus areas: e-commerce integration, omnichannel experience, and customer data analytics.",
                'expected_keywords': ['digital transformation', 'retail businesses', 'post-pandemic era', 'e-commerce integration', 'omnichannel experience', 'customer data analytics'],
                'complexity': 'high',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            
            # ===== TECHNICAL DOMAIN =====
            {
                'id': 'TECH_001',
                'category': 'technical',
                'text': "Machine learning algorithms for natural language processing applications in social media sentiment analysis. Implementation using transformer models and attention mechanisms.",
                'expected_keywords': ['machine learning', 'natural language processing', 'sentiment analysis', 'transformer models', 'attention mechanisms'],
                'complexity': 'high',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            {
                'id': 'TECH_002',
                'category': 'technical',
                'text': "Blockchain technology implementation for secure and transparent supply chain management. Smart contracts enable automated verification and compliance tracking.",
                'expected_keywords': ['blockchain technology', 'supply chain management', 'smart contracts', 'automated verification', 'compliance tracking'],
                'complexity': 'medium',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            
            # ===== SHORT TEXT DOMAIN =====
            {
                'id': 'SHORT_001',
                'category': 'short_text',
                'text': "AI startup funding trends 2024",
                'expected_keywords': ['ai startup', 'funding trends'],
                'complexity': 'low',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            {
                'id': 'SHORT_002',
                'category': 'short_text',
                'text': "Sustainable fashion innovation",
                'expected_keywords': ['sustainable fashion', 'innovation'],
                'complexity': 'low',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            
            # ===== CHALLENGING CASES =====
            {
                'id': 'CHALLENGE_001',
                'category': 'challenging',
                'text': "The quantum computing paradigm shift necessitates interdisciplinary collaboration between physicists, computer scientists, and mathematicians to develop novel algorithms for optimization problems.",
                'expected_keywords': ['quantum computing', 'paradigm shift', 'interdisciplinary collaboration', 'physicists', 'computer scientists', 'mathematicians', 'novel algorithms', 'optimization problems'],
                'complexity': 'very_high',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            },
            {
                'id': 'CHALLENGE_002',
                'category': 'challenging',
                'text': "Neuroscience-inspired artificial intelligence approaches leverage computational neuroscience principles to develop brain-like learning systems with enhanced cognitive capabilities.",
                'expected_keywords': ['neuroscience-inspired', 'artificial intelligence', 'computational neuroscience', 'brain-like learning systems', 'cognitive capabilities'],
                'complexity': 'very_high',
                'hashtags': False,
                'mentions': False,
                'emojis': False
            }
        ]
        
        return test_cases
    
    async def run_comprehensive_experiment(self) -> Dict:
        """Run the complete experiment with all test cases and methods"""
        
        print("🚀 Starting spaCy + YAKE Comprehensive Experiment")
        print("=" * 70)
        print(f"📊 Test Cases: {len(self.experiment_config['test_cases'])}")
        print(f"🔄 Iterations: {self.experiment_config['iterations']}")
        print(f"📈 Metrics: {', '.join(self.experiment_config['metrics'])}")
        print(f"🔬 Methods to Test: spaCy + YAKE + {len(self.baseline_methods)} baselines")
        print("=" * 70)
        
        # Check if methods are available
        if not self.spacy_yake:
            print("❌ spaCy + YAKE not available. Cannot run experiment.")
            return {}
        
        if not self.baseline_methods:
            print("⚠️  No baseline methods available. Only testing spaCy + YAKE.")
        
        start_time = time.time()
        
        # Run experiments for each test case
        for i, test_case in enumerate(self.experiment_config['test_cases']):
            print(f"\n🧪 Test Case {i+1}/{len(self.experiment_config['test_cases'])}: {test_case['id']}")
            print(f"   Category: {test_case['category']} | Complexity: {test_case['complexity']}")
            print(f"   Text: {test_case['text'][:80]}...")
            
            # Run multiple iterations for statistical significance
            case_results = []
            for iteration in range(self.experiment_config['iterations']):
                print(f"   🔄 Iteration {iteration+1}/{self.experiment_config['iterations']}")
                
                # Test spaCy + YAKE
                print(f"      🔍 Testing spaCy + YAKE...")
                spacy_yake_result = await self._run_single_test(
                    self.spacy_yake, test_case, 'spacy_yake'
                )
                
                # Test baseline methods
                baseline_results = {}
                for method_name, method in self.baseline_methods.items():
                    print(f"      🔍 Testing {method_name}...")
                    baseline_results[method_name] = await self._run_single_test(
                        method, test_case, method_name
                    )
                
                # Store iteration results
                case_results.append({
                    'iteration': iteration + 1,
                    'spacy_yake': spacy_yake_result,
                    'baselines': baseline_results
                })
            
            # Analyze case results
            case_analysis = self._analyze_case_results(test_case, case_results)
            self.detailed_analysis[test_case['id']] = case_analysis
            
            # Store in main results
            self.experiment_results.append({
                'test_case': test_case,
                'results': case_results,
                'analysis': case_analysis
            })
        
        # Generate comprehensive analysis
        total_time = time.time() - start_time
        print(f"\n⏱️  Total Experiment Time: {total_time:.2f} seconds")
        
        comprehensive_analysis = self._generate_comprehensive_analysis()
        
        # Save results
        if self.experiment_config['save_detailed_results']:
            self._save_experiment_results(comprehensive_analysis)
        
        return comprehensive_analysis
    
    async def _run_single_test(self, method, test_case: Dict, method_name: str) -> Dict:
        """Run a single test with performance measurement"""
        
        if method is None:
            return {
                'method': method_name,
                'success': False,
                'processing_time': 0,
                'memory_usage': 0,
                'confidence_score': 0.0,
                'keywords_count': 0,
                'accuracy': 0.0,
                'extracted_keywords': [],
                'error': 'Method not available'
            }
        
        # Measure system resources before
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        start_time = time.time()
        
        try:
            # Run extraction
            result = await method.extract(test_case['text'])
            
            # Measure system resources after
            end_time = time.time()
            end_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Calculate accuracy
            accuracy = self._calculate_accuracy(result.keywords, test_case['expected_keywords'])
            
            return {
                'method': method_name,
                'success': True,
                'processing_time': end_time - start_time,
                'memory_usage': end_memory - start_memory,
                'confidence_score': result.confidence_score,
                'keywords_count': len(result.keywords),
                'accuracy': accuracy,
                'extracted_keywords': [kw['keyword'] for kw in result.keywords[:10]],
                'metadata': result.metadata
            }
            
        except Exception as e:
            end_time = time.time()
            return {
                'method': method_name,
                'success': False,
                'processing_time': end_time - start_time,
                'memory_usage': 0,
                'confidence_score': 0.0,
                'keywords_count': 0,
                'accuracy': 0.0,
                'extracted_keywords': [],
                'error': str(e)
            }
    
    def _calculate_accuracy(self, extracted_keywords: List[Dict], expected_keywords: List[str]) -> float:
        """Calculate F1 score accuracy"""
        if not expected_keywords:
            return 1.0 if not extracted_keywords else 0.0
        
        extracted_set = set([kw['keyword'].lower() for kw in extracted_keywords])
        expected_set = set([kw.lower() for kw in expected_keywords])
        
        if not expected_set:
            return 1.0 if not extracted_set else 0.0
        
        intersection = extracted_set.intersection(expected_set)
        precision = len(intersection) / len(extracted_set) if extracted_set else 0
        recall = len(intersection) / len(expected_set)
        
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    def _analyze_case_results(self, test_case: Dict, case_results: List[Dict]) -> Dict:
        """Analyze results for a specific test case"""
        
        # Aggregate spaCy + YAKE results
        spacy_yake_results = [r['spacy_yake'] for r in case_results if r['spacy_yake']['success']]
        
        # Aggregate baseline results
        baseline_aggregates = {}
        for method_name in self.baseline_methods.keys():
            method_results = [r['baselines'][method_name] for r in case_results if r['baselines'][method_name]['success']]
            if method_results:
                baseline_aggregates[method_name] = {
                    'processing_time': np.mean([r['processing_time'] for r in method_results]),
                    'memory_usage': np.mean([r['memory_usage'] for r in method_results]),
                    'confidence_score': np.mean([r['confidence_score'] for r in method_results]),
                    'accuracy': np.mean([r['accuracy'] for r in method_results]),
                    'keywords_count': np.mean([r['keywords_count'] for r in method_results]),
                    'success_rate': len(method_results) / len(case_results)
                }
        
        # Calculate spaCy + YAKE statistics
        if spacy_yake_results:
            spacy_yake_stats = {
                'processing_time': {
                    'mean': np.mean([r['processing_time'] for r in spacy_yake_results]),
                    'std': np.std([r['processing_time'] for r in spacy_yake_results]),
                    'min': np.min([r['processing_time'] for r in spacy_yake_results]),
                    'max': np.max([r['processing_time'] for r in spacy_yake_results])
                },
                'memory_usage': {
                    'mean': np.mean([r['memory_usage'] for r in spacy_yake_results]),
                    'std': np.std([r['memory_usage'] for r in spacy_yake_results]),
                    'min': np.min([r['memory_usage'] for r in spacy_yake_results]),
                    'max': np.max([r['memory_usage'] for r in spacy_yake_results])
                },
                'confidence_score': {
                    'mean': np.mean([r['confidence_score'] for r in spacy_yake_results]),
                    'std': np.std([r['confidence_score'] for r in spacy_yake_results])
                },
                'accuracy': {
                    'mean': np.mean([r['accuracy'] for r in spacy_yake_results]),
                    'std': np.std([r['accuracy'] for r in spacy_yake_results])
                },
                'keywords_count': {
                    'mean': np.mean([r['keywords_count'] for r in spacy_yake_results]),
                    'std': np.std([r['keywords_count'] for r in spacy_yake_results])
                },
                'success_rate': len(spacy_yake_results) / len(case_results)
            }
        else:
            spacy_yake_stats = None
        
        return {
            'test_case_info': test_case,
            'spacy_yake_stats': spacy_yake_stats,
            'baseline_stats': baseline_aggregates,
            'performance_comparison': self._compare_performance(spacy_yake_stats, baseline_aggregates),
            'statistical_significance': self._calculate_statistical_significance(case_results)
        }
    
    def _compare_performance(self, spacy_yake_stats: Dict, baseline_stats: Dict) -> Dict:
        """Compare spaCy + YAKE performance against baselines"""
        
        if not spacy_yake_stats:
            return {}
        
        comparison = {}
        
        for metric in ['processing_time', 'memory_usage', 'confidence_score', 'accuracy', 'keywords_count']:
            if metric in spacy_yake_stats and 'mean' in spacy_yake_stats[metric]:
                spacy_yake_value = spacy_yake_stats[metric]['mean']
                
                metric_comparison = {}
                for baseline_method, baseline_data in baseline_stats.items():
                    if metric in baseline_data:
                        baseline_value = baseline_data[metric]
                        
                        # Calculate improvement percentage
                        if metric in ['processing_time', 'memory_usage']:
                            # Lower is better
                            improvement = ((baseline_value - spacy_yake_value) / baseline_value) * 100
                            metric_comparison[baseline_method] = {
                                'baseline_value': baseline_value,
                                'spacy_yake_value': spacy_yake_value,
                                'improvement_percent': improvement,
                                'better_than_baseline': spacy_yake_value < baseline_value
                            }
                        else:
                            # Higher is better
                            improvement = ((spacy_yake_value - baseline_value) / baseline_value) * 100
                            metric_comparison[baseline_method] = {
                                'baseline_value': baseline_value,
                                'spacy_yake_value': spacy_yake_value,
                                'improvement_percent': improvement,
                                'better_than_baseline': spacy_yake_value > baseline_value
                            }
                
                comparison[metric] = metric_comparison
        
        return comparison
    
    def _calculate_statistical_significance(self, case_results: List[Dict]) -> Dict:
        """Calculate statistical significance of results"""
        
        # This is a simplified version - in real research, you'd use proper statistical tests
        spacy_yake_accuracies = [r['spacy_yake']['accuracy'] for r in case_results if r['spacy_yake']['success']]
        
        if len(spacy_yake_accuracies) < 2:
            return {'statistical_significance': 'insufficient_data'}
        
        # Calculate confidence interval (simplified)
        mean_accuracy = np.mean(spacy_yake_accuracies)
        std_accuracy = np.std(spacy_yake_accuracies)
        confidence_interval = 1.96 * (std_accuracy / np.sqrt(len(spacy_yake_accuracies)))
        
        return {
            'mean_accuracy': mean_accuracy,
            'std_accuracy': std_accuracy,
            'confidence_interval_95': confidence_interval,
            'confidence_range': (mean_accuracy - confidence_interval, mean_accuracy + confidence_interval),
            'sample_size': len(spacy_yake_accuracies)
        }
    
    def _generate_comprehensive_analysis(self) -> Dict:
        """Generate comprehensive analysis of all experiment results"""
        
        # Aggregate results across all test cases
        all_spacy_yake_results = []
        all_baseline_results = {method: [] for method in self.baseline_methods.keys()}
        
        for result in self.experiment_results:
            if result['analysis']['spacy_yake_stats']:
                all_spacy_yake_results.append(result['analysis']['spacy_yake_stats'])
            
            for method_name, method_stats in result['analysis']['baseline_stats'].items():
                all_baseline_results[method_name].append(method_stats)
        
        # Calculate overall statistics
        overall_analysis = {
            'experiment_summary': {
                'total_test_cases': len(self.experiment_results),
                'total_iterations': len(self.experiment_results) * self.experiment_config['iterations'],
                'spacy_yake_success_rate': len(all_spacy_yake_results) / len(self.experiment_results),
                'baseline_methods_tested': list(self.baseline_methods.keys()),
                'experiment_timestamp': datetime.now().isoformat()
            },
            'spacy_yake_overall_performance': self._calculate_overall_stats(all_spacy_yake_results),
            'baseline_overall_performance': {
                method: self._calculate_overall_stats(results) 
                for method, results in all_baseline_results.items() 
                if results
            },
            'performance_ranking': self._rank_methods_performance(all_spacy_yake_results, all_baseline_results),
            'domain_specific_analysis': self._analyze_domain_performance(),
            'statistical_insights': self._generate_statistical_insights()
        }
        
        return overall_analysis
    
    def _calculate_overall_stats(self, results: List[Dict]) -> Dict:
        """Calculate overall statistics for a method"""
        
        if not results:
            return {}
        
        metrics = ['processing_time', 'memory_usage', 'confidence_score', 'accuracy', 'keywords_count']
        overall_stats = {}
        
        for metric in metrics:
            values = []
            for r in results:
                if metric in r:
                    if isinstance(r[metric], dict) and 'mean' in r[metric]:
                        # spaCy+YAKE format: {'mean': value, 'std': value, ...}
                        values.append(r[metric]['mean'])
                    elif isinstance(r[metric], (int, float)):
                        # Baseline format: {'processing_time': value, ...}
                        values.append(r[metric])
            
            if values:
                overall_stats[metric] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                    'median': np.median(values)
                }
        
        return overall_stats
    
    def _rank_methods_performance(self, spacy_yake_results: List, baseline_results: Dict) -> Dict:
        """Rank methods by overall performance"""
        
        # Calculate composite scores for each method
        method_scores = {}
        
        # spaCy + YAKE score
        if spacy_yake_results:
            spacy_yake_score = self._calculate_composite_score(spacy_yake_results)
            method_scores['spacy_yake'] = spacy_yake_score
        
        # Baseline method scores
        for method_name, results in baseline_results.items():
            if results:
                baseline_score = self._calculate_composite_score(results)
                method_scores[method_name] = baseline_score
        
        # Sort by score (higher is better)
        ranked_methods = sorted(method_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'ranking': ranked_methods,
            'best_method': ranked_methods[0][0] if ranked_methods else None,
            'best_score': ranked_methods[0][1] if ranked_methods else None,
            'score_details': method_scores
        }
    
    def _calculate_composite_score(self, results: List[Dict]) -> float:
        """Calculate composite performance score"""
        
        if not results:
            return 0.0
        
        # Normalize metrics to 0-1 scale and weight them
        weights = {
            'accuracy': 0.35,      # Most important
            'confidence_score': 0.25,
            'keywords_count': 0.20,
            'processing_time': 0.15,  # Lower is better
            'memory_usage': 0.05      # Lower is better
        }
        
        composite_score = 0.0
        
        for metric, weight in weights.items():
            if metric in results[0]:
                values = []
                for r in results:
                    if metric in r:
                        if isinstance(r[metric], dict) and 'mean' in r[metric]:
                            # spaCy+YAKE format: {'mean': value, 'std': value, ...}
                            values.append(r[metric]['mean'])
                        elif isinstance(r[metric], (int, float)):
                            # Baseline format: {'accuracy': value, ...}
                            values.append(r[metric])
                
                if values:
                    if metric in ['processing_time', 'memory_usage']:
                        # Lower is better - invert and normalize
                        normalized_value = 1.0 - min(np.mean(values) / 10.0, 1.0)  # Cap at 10s/100MB
                    else:
                        # Higher is better - normalize to 0-1
                        normalized_value = min(np.mean(values), 1.0)
                    
                    composite_score += normalized_value * weight
        
        return composite_score
    
    def _analyze_domain_performance(self) -> Dict:
        """Analyze performance across different domains"""
        
        domain_analysis = {}
        
        for result in self.experiment_results:
            domain = result['test_case']['category']
            if domain not in domain_analysis:
                domain_analysis[domain] = []
            
            if result['analysis']['spacy_yake_stats']:
                domain_analysis[domain].append(result['analysis']['spacy_yake_stats'])
        
        # Calculate domain-specific statistics
        domain_stats = {}
        for domain, results in domain_analysis.items():
            if results:
                domain_stats[domain] = {
                    'test_cases_count': len(results),
                    'avg_accuracy': np.mean([r['accuracy']['mean'] for r in results]),
                    'avg_confidence': np.mean([r['confidence_score']['mean'] for r in results]),
                    'avg_processing_time': np.mean([r['processing_time']['mean'] for r in results])
                }
        
        return domain_stats
    
    def _generate_statistical_insights(self) -> Dict:
        """Generate statistical insights and recommendations"""
        
        insights = {
            'performance_trends': {},
            'reliability_metrics': {},
            'optimization_recommendations': []
        }
        
        # Analyze performance trends
        if self.experiment_results:
            accuracies = []
            processing_times = []
            complexities = []
            
            for result in self.experiment_results:
                if result['analysis']['spacy_yake_stats']:
                    accuracies.append(result['analysis']['spacy_yake_stats']['accuracy']['mean'])
                    processing_times.append(result['analysis']['spacy_yake_stats']['processing_time']['mean'])
                    complexities.append(result['test_case']['complexity'])
            
            if accuracies:
                insights['performance_trends'] = {
                    'accuracy_correlation_with_complexity': self._calculate_complexity_correlation(accuracies, complexities),
                    'processing_time_vs_accuracy': np.corrcoef(processing_times, accuracies)[0, 1] if len(processing_times) > 1 else 0,
                    'overall_accuracy_consistency': np.std(accuracies) if accuracies else 0
                }
        
        # Generate recommendations
        if self.experiment_results:
            avg_accuracy = np.mean([r['analysis']['spacy_yake_stats']['accuracy']['mean'] 
                                  for r in self.experiment_results 
                                  if r['analysis']['spacy_yake_stats']])
            
            if avg_accuracy < 0.7:
                insights['optimization_recommendations'].append(
                    "Consider tuning YAKE parameters for better accuracy"
                )
            
            avg_processing_time = np.mean([r['analysis']['spacy_yake_stats']['processing_time']['mean'] 
                                         for r in self.experiment_results 
                                         if r['analysis']['spacy_yake_stats']])
            
            if avg_processing_time > 1.0:
                insights['optimization_recommendations'].append(
                    "Consider using smaller spaCy model for faster processing"
                )
        
        return insights
    
    def _calculate_complexity_correlation(self, accuracies: List[float], complexities: List[str]) -> float:
        """Calculate correlation between accuracy and complexity"""
        
        # Convert complexity to numeric values
        complexity_map = {'low': 1, 'medium': 2, 'high': 3, 'very_high': 4}
        numeric_complexities = [complexity_map.get(c, 2) for c in complexities]
        
        if len(accuracies) > 1 and len(numeric_complexities) > 1:
            return np.corrcoef(accuracies, numeric_complexities)[0, 1]
        return 0.0
    
    def _convert_numpy_types(self, obj):
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        return obj

    def _save_experiment_results(self, comprehensive_analysis: Dict):
        """Save experiment results to files"""
        
        # Create results directory
        os.makedirs('experiment_results', exist_ok=True)
        
        # Convert numpy types to native Python types
        detailed_analysis_clean = self._convert_numpy_types(self.detailed_analysis)
        comprehensive_analysis_clean = self._convert_numpy_types(comprehensive_analysis)
        
        # Save detailed results
        with open('experiment_results/detailed_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(detailed_analysis_clean, f, indent=2, ensure_ascii=False)
        
        # Save comprehensive analysis
        with open('experiment_results/comprehensive_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(comprehensive_analysis_clean, f, indent=2, ensure_ascii=False)
        
        # Save summary report
        self._generate_summary_report(comprehensive_analysis)
        
        print(f"\n💾 Results saved to 'experiment_results/' directory")
    
    def _generate_summary_report(self, comprehensive_analysis: Dict):
        """Generate human-readable summary report"""
        
        report_path = 'experiment_results/experiment_summary_report.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("🧪 SPAÇY + YAKE ALGORITHM EXPERIMENT SUMMARY REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            # Experiment Summary
            f.write("EXPERIMENT SUMMARY:\n")
            f.write("-" * 20 + "\n")
            summary = comprehensive_analysis['experiment_summary']
            f.write(f"Total Test Cases: {summary['total_test_cases']}\n")
            f.write(f"Total Iterations: {summary['total_iterations']}\n")
            f.write(f"spaCy + YAKE Success Rate: {summary['spacy_yake_success_rate']*100:.1f}%\n")
            f.write(f"Baseline Methods Tested: {', '.join(summary['baseline_methods_tested'])}\n")
            f.write(f"Experiment Timestamp: {summary['experiment_timestamp']}\n\n")
            
            # Performance Ranking
            f.write("PERFORMANCE RANKING:\n")
            f.write("-" * 20 + "\n")
            ranking = comprehensive_analysis['performance_ranking']
            f.write(f"Best Method: {ranking['best_method']}\n")
            f.write(f"Best Score: {ranking['best_score']:.3f}\n\n")
            
            f.write("Method Rankings:\n")
            for i, (method, score) in enumerate(ranking['ranking']):
                f.write(f"{i+1}. {method}: {score:.3f}\n")
            f.write("\n")
            
            # spaCy + YAKE Performance
            f.write("SPAÇY + YAKE OVERALL PERFORMANCE:\n")
            f.write("-" * 30 + "\n")
            spacy_yake_perf = comprehensive_analysis['spacy_yake_overall_performance']
            for metric, stats in spacy_yake_perf.items():
                f.write(f"{metric.replace('_', ' ').title()}:\n")
                f.write(f"  Mean: {stats['mean']:.4f}\n")
                f.write(f"  Std: {stats['std']:.4f}\n")
                f.write(f"  Range: {stats['min']:.4f} - {stats['max']:.4f}\n")
                f.write(f"  Median: {stats['median']:.4f}\n\n")
            
            # Baseline Methods Performance
            if comprehensive_analysis['baseline_overall_performance']:
                f.write("BASELINE METHODS PERFORMANCE:\n")
                f.write("-" * 30 + "\n")
                for method_name, method_stats in comprehensive_analysis['baseline_overall_performance'].items():
                    f.write(f"{method_name.upper()}:\n")
                    for metric, stats in method_stats.items():
                        f.write(f"  {metric.replace('_', ' ').title()}:\n")
                        f.write(f"    Mean: {stats['mean']:.4f}\n")
                        f.write(f"    Std: {stats['std']:.4f}\n")
                        f.write(f"    Range: {stats['min']:.4f} - {stats['max']:.4f}\n")
                        f.write(f"    Median: {stats['median']:.4f}\n")
                    f.write("\n")
            
            # Domain Analysis
            f.write("DOMAIN-SPECIFIC PERFORMANCE:\n")
            f.write("-" * 30 + "\n")
            domain_stats = comprehensive_analysis['domain_specific_analysis']
            for domain, stats in domain_stats.items():
                f.write(f"{domain.replace('_', ' ').title()}:\n")
                f.write(f"  Test Cases: {stats['test_cases_count']}\n")
                f.write(f"  Avg Accuracy: {stats['avg_accuracy']:.3f}\n")
                f.write(f"  Avg Confidence: {stats['avg_confidence']:.3f}\n")
                f.write(f"  Avg Processing Time: {stats['avg_processing_time']:.3f}s\n\n")
            
            # Statistical Insights
            f.write("STATISTICAL INSIGHTS:\n")
            f.write("-" * 20 + "\n")
            insights = comprehensive_analysis['statistical_insights']
            if 'performance_trends' in insights:
                trends = insights['performance_trends']
                f.write(f"Accuracy-Complexity Correlation: {trends.get('accuracy_correlation_with_complexity', 0):.3f}\n")
                f.write(f"Processing Time-Accuracy Correlation: {trends.get('processing_time_vs_accuracy', 0):.3f}\n")
                f.write(f"Overall Accuracy Consistency (Std): {trends.get('overall_accuracy_consistency', 0):.3f}\n\n")
            
            if 'optimization_recommendations' in insights:
                f.write("OPTIMIZATION RECOMMENDATIONS:\n")
                f.write("-" * 25 + "\n")
                for rec in insights['optimization_recommendations']:
                    f.write(f"• {rec}\n")
                f.write("\n")
            
            f.write("=" * 60 + "\n")
            f.write("Report generated automatically by spaCy + YAKE Experiment Framework\n")
            f.write("For detailed analysis, check the JSON files in this directory.\n")

async def main():
    """Main experiment execution"""
    
    print("🧪 spaCy + YAKE Algorithm: Comprehensive Experiment")
    print("=" * 60)
    
    # Initialize experiment
    experiment = SpacyYakeExperiment()
    
    # Run experiment
    try:
        results = await experiment.run_comprehensive_experiment()
        
        if not results:
            print("\n❌ Experiment failed to produce results")
            return
        
        print("\n🎉 Experiment completed successfully!")
        print("\n📊 Key Results:")
        
        # Show performance ranking
        ranking = results['performance_ranking']
        print(f"🏆 Best Method: {ranking['best_method']}")
        print(f"📈 Best Score: {ranking['best_score']:.3f}")
        
        # Show spaCy + YAKE performance
        spacy_yake_perf = results['spacy_yake_overall_performance']
        if 'accuracy' in spacy_yake_perf:
            print(f"🎯 spaCy + YAKE Average Accuracy: {spacy_yake_perf['accuracy']['mean']:.3f}")
        if 'processing_time' in spacy_yake_perf:
            print(f"⏱️  spaCy + YAKE Average Processing Time: {spacy_yake_perf['processing_time']['mean']:.3f}s")
        
        # Show baseline methods tested
        summary = results['experiment_summary']
        print(f"🔬 Baseline Methods Tested: {', '.join(summary['baseline_methods_tested'])}")
        
        print(f"\n💾 Detailed results saved to 'experiment_results/' directory")
        print("📖 Check 'experiment_summary_report.txt' for human-readable summary")
        
    except Exception as e:
        print(f"\n❌ Experiment failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
