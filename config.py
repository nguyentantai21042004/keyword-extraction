"""
Configuration file for the Multi-Method Keyword Extraction Research Framework
"""

# Research Framework Configuration
RESEARCH_CONFIG = {
    # Test case configuration
    'test_cases': {
        'max_text_length': 1000,
        'min_text_length': 10,
        'categories': ['social_media', 'business', 'technical', 'short_text', 'custom']
    },
    
    # Benchmark configuration
    'benchmark': {
        'timeout_seconds': 30,
        'max_keywords_per_method': 20,
        'save_intermediate_results': True
    },
    
    # Performance measurement
    'performance': {
        'measure_memory': True,
        'measure_processing_time': True,
        'memory_unit': 'MB',  # MB or KB
        'time_unit': 'seconds'
    }
}

# Method-specific configurations
METHOD_CONFIGS = {
    'spacy_yake': {
        'spacy_model': 'en_core_web_sm',
        'yake_language': 'en',
        'yake_max_keywords': 20,
        'yake_dedup_lim': 0.9,
        'yake_window_size': 1
    },
    
    'rake_nltk': {
        'min_phrase_length': 2,
        'max_phrase_length': 4,
        'min_frequency': 1
    },
    
    'textrank': {
        'window_size': 4,
        'candidate_pos': ['NOUN', 'PROPN'],
        'word_min_len': 2
    },
    
    'tf_idf': {
        'ngram_range': (1, 2),
        'max_features': 50,
        'use_stop_words': True
    },
    
    'keybert': {
        'model_name': 'all-MiniLM-L6-v2',
        'keyphrase_ngram_range': (1, 2),
        'top_k': 20,
        'diversity': 0.5
    },
    
    'hybrid_ensemble': {
        'method_weights': {
            'spacy_yake': 0.4,
            'rake': 0.2,
            'tfidf': 0.2,
            'keybert': 0.2
        },
        'consensus_threshold': 0.5,
        'timeout_per_method': 10.0
    }
}

# Optimization criteria weights
OPTIMIZATION_WEIGHTS = {
    'default': {
        'processing_time': 0.25,    # Lower is better
        'memory_usage': 0.15,       # Lower is better
        'confidence_score': 0.25,   # Higher is better
        'accuracy': 0.25,           # Higher is better
        'success_rate': 0.10        # Higher is better
    },
    
    'speed_focused': {
        'processing_time': 0.40,
        'memory_usage': 0.20,
        'confidence_score': 0.20,
        'accuracy': 0.15,
        'success_rate': 0.05
    },
    
    'accuracy_focused': {
        'processing_time': 0.15,
        'memory_usage': 0.10,
        'confidence_score': 0.30,
        'accuracy': 0.35,
        'success_rate': 0.10
    },
    
    'balanced': {
        'processing_time': 0.20,
        'memory_usage': 0.20,
        'confidence_score': 0.20,
        'accuracy': 0.25,
        'success_rate': 0.15
    }
}

# Visualization configuration
VISUALIZATION_CONFIG = {
    'style': 'seaborn-v0_8',
    'color_palette': 'husl',
    'figure_size': {
        'performance_comparison': (15, 12),
        'accuracy_analysis': (15, 6),
        'heatmap': (10, 8),
        'social_media_analysis': (15, 10),
        'summary_statistics': (12, 8),
        'radar_chart': (10, 8),
        'weighted_scores': (12, 6)
    },
    'dpi': 300,
    'save_format': 'png'
}

# Output configuration
OUTPUT_CONFIG = {
    'save_results': True,
    'output_directory': './research_results',
    'file_prefixes': {
        'benchmark_results': 'research_benchmark_results',
        'performance_report': 'research_performance_report',
        'optimization_report': 'research_optimization_report'
    },
    'file_extensions': {
        'data': 'csv',
        'reports': 'txt',
        'visualizations': 'png'
    }
}

# Test dataset configuration
TEST_DATASET_CONFIG = {
    'social_media': {
        'sample_texts': [
            "Just discovered #sustainablefashion trends! @patagonia's new eco-line is amazing 🌱",
            "Need insights on influencer marketing for beauty brands targeting Gen Z #beautytech #influencer",
            "AI-powered social media analytics platform #tech #startup #innovation"
        ],
        'expected_keywords': [
            ['sustainable fashion', 'patagonia', 'eco-line', 'trends'],
            ['influencer marketing', 'beauty brands', 'gen z', 'beautytech'],
            ['ai-powered', 'social media analytics', 'platform', 'tech', 'startup']
        ]
    },
    
    'business': {
        'sample_texts': [
            "Market analysis of renewable energy sector shows significant growth in solar and wind power technologies",
            "Digital transformation strategies for traditional retail businesses in the post-pandemic era",
            "Supply chain optimization using machine learning and predictive analytics"
        ],
        'expected_keywords': [
            ['market analysis', 'renewable energy', 'solar power', 'wind power'],
            ['digital transformation', 'retail businesses', 'post-pandemic era'],
            ['supply chain optimization', 'machine learning', 'predictive analytics']
        ]
    },
    
    'technical': {
        'sample_texts': [
            "Machine learning algorithms for natural language processing applications in social media sentiment analysis",
            "Blockchain technology implementation for secure and transparent supply chain management",
            "Cloud-native microservices architecture for scalable web applications"
        ],
        'expected_keywords': [
            ['machine learning', 'natural language processing', 'sentiment analysis'],
            ['blockchain technology', 'supply chain management', 'secure'],
            ['cloud-native', 'microservices architecture', 'scalable web applications']
        ]
    },
    
    'short_text': {
        'sample_texts': [
            "AI startup funding trends 2024",
            "Sustainable fashion innovation",
            "Digital marketing strategies"
        ],
        'expected_keywords': [
            ['ai startup', 'funding trends'],
            ['sustainable fashion', 'innovation'],
            ['digital marketing', 'strategies']
        ]
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_to_file': True,
    'log_file': 'research_framework.log'
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'processing_time': {
        'excellent': 0.1,    # seconds
        'good': 0.5,
        'acceptable': 1.0,
        'poor': 2.0
    },
    'memory_usage': {
        'excellent': 10,     # MB
        'good': 50,
        'acceptable': 100,
        'poor': 200
    },
    'confidence_score': {
        'excellent': 0.9,    # 0-1 scale
        'good': 0.7,
        'acceptable': 0.5,
        'poor': 0.3
    },
    'accuracy': {
        'excellent': 0.9,    # F1 score
        'good': 0.7,
        'acceptable': 0.5,
        'poor': 0.3
    }
}
