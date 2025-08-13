# 🎓 Multi-Method Keyword Extraction Research Framework

**Comprehensive Comparative Analysis Framework for Đồ Án**

This research framework implements and benchmarks multiple keyword extraction methods to provide evidence-based optimization decisions for your thesis project.

## 🏗️ Architecture Overview

The framework consists of 6 extraction methods:

1. **spaCy + YAKE** - Primary hybrid method combining NLP and statistical extraction
2. **RAKE + NLTK** - Fast baseline method for comparison
3. **TextRank** - Graph-based method for semantic analysis
4. **TF-IDF** - Statistical baseline method
5. **KeyBERT** - High-accuracy semantic method
6. **Hybrid Ensemble** - Intelligent combination of multiple methods

## 📁 Project Structure

```
smap-keyword-extraction/
├── multi_method_extractor.py    # Core extraction methods
├── hybrid_ensemble.py           # Ensemble method implementation
├── benchmark_framework.py       # Benchmarking and testing framework
├── visualization.py             # Charts and graphs generation
├── optimization_analyzer.py     # Optimization analysis and justification
├── main.py                     # Main orchestrator and entry point
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Some methods require additional setup:
- **spaCy**: Will automatically download `en_core_web_sm` model
- **KeyBERT**: Will download `all-MiniLM-L6-v2` model on first use

### 2. Run the Research Framework

```bash
python main.py
```

The framework will:
- Run all 6 methods on test cases
- Generate performance metrics
- Create visualizations
- Perform optimization analysis
- Save comprehensive reports

### 3. View Results

After execution, you'll find:
- `research_benchmark_results.csv` - Raw benchmark data
- `research_performance_report.txt` - Performance analysis
- `research_optimization_report.txt` - Optimization justification
- Various PNG visualization files

## 🔬 Research Methodology

### Benchmark Process

1. **Test Case Setup**: Predefined test cases across different categories
   - Social media content
   - Business documents
   - Technical text
   - Short text

2. **Performance Metrics**:
   - Processing time (seconds)
   - Memory usage (MB)
   - Confidence score (0-1)
   - Keywords count
   - Accuracy (F1 score when ground truth available)
   - Success rate

3. **Multi-Method Execution**: All methods run concurrently on each test case

### Optimization Analysis

The framework uses weighted criteria to determine the optimal method:

- **Processing Time** (25%): Lower is better
- **Memory Usage** (15%): Lower is better
- **Confidence Score** (25%): Higher is better
- **Accuracy** (25%): Higher is better
- **Success Rate** (10%): Higher is better

## 📊 Output Files

### 1. Benchmark Results (`research_benchmark_results.csv`)
Contains raw performance data for each method on each test case.

### 2. Performance Report (`research_performance_report.txt`)
Statistical analysis including:
- Overall performance by method
- Category-specific performance
- Social media performance
- Summary statistics

### 3. Optimization Report (`research_optimization_report.txt`)
Justification for method selection including:
- Optimal method identification
- Detailed comparison table
- Performance insights
- Optimization suggestions
- Use case recommendations

### 4. Visualizations
- `method_performance_comparison.png` - Performance comparison charts
- `accuracy_analysis.png` - Accuracy analysis
- `method_comparison_heatmap.png` - Performance heatmap
- `social_media_analysis.png` - Social media specific analysis
- `summary_statistics.png` - Summary table
- `optimization_radar_chart.png` - Radar chart comparison
- `weighted_scores_comparison.png` - Weighted score comparison

## 🎯 Customization

### Adding Custom Test Cases

Modify the `create_custom_test_cases()` function in `main.py`:

```python
def create_custom_test_cases():
    custom_cases = [
        {
            'text': "Your custom text here",
            'expected_keywords': ['keyword1', 'keyword2'],
            'category': 'custom_category'
        }
    ]
    return custom_cases
```

### Modifying Method Weights

Adjust weights in `optimization_analyzer.py`:

```python
weights = {
    'processing_time': 0.30,    # Increase importance
    'memory_usage': 0.10,       # Decrease importance
    'confidence_score': 0.25,
    'accuracy': 0.25,
    'success_rate': 0.10
}
```

### Adding New Extraction Methods

1. Create a new class inheriting from `BaseExtractor`
2. Implement the `extract()` method
3. Add it to the `ExtractionBenchmark` class
4. Update the `ExtractionMethod` enum

## 🔍 Understanding Results

### Key Metrics Explained

- **Processing Time**: Actual execution time in seconds
- **Memory Usage**: Additional memory consumed during extraction
- **Confidence Score**: Method's confidence in extracted keywords (0-1)
- **Accuracy**: F1 score when comparing with expected keywords
- **Success Rate**: Percentage of successful extractions

### Interpreting Visualizations

- **Box Plots**: Show distribution of performance metrics
- **Heatmap**: Normalized comparison across all metrics
- **Radar Chart**: Multi-dimensional performance comparison
- **Bar Charts**: Direct metric comparisons

## 📚 Thesis Integration

### What to Include in Your Report

1. **Methodology Section**:
   - "Implemented 6 different keyword extraction methods"
   - "Conducted comprehensive benchmarking on X test cases"
   - "Used weighted optimization criteria for method selection"

2. **Results Section**:
   - Include generated visualizations
   - Reference performance metrics from reports
   - Use optimization justification for method selection

3. **Discussion Section**:
   - Explain why your chosen method is optimal
   - Reference the quantitative evidence
   - Discuss trade-offs between methods

### Sample Thesis Text

> "The research framework evaluated 6 keyword extraction methods across multiple text categories. 
> Quantitative analysis using weighted criteria (processing time: 25%, confidence: 25%, accuracy: 25%, 
> memory: 15%, success rate: 10%) identified [METHOD] as optimal with a score of X.XX. 
> This method provides the best balance of performance, accuracy, and resource efficiency for 
> real-time social media analysis."

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Model Download Issues**: Check internet connection for spaCy/KeyBERT models
3. **Memory Issues**: Some methods (KeyBERT) require significant RAM
4. **Timeout Errors**: Increase timeout values for slow methods

### Performance Tips

- Run on a machine with sufficient RAM (8GB+ recommended)
- Close other applications during benchmarking
- Use SSD storage for faster model loading
- Consider running overnight for large datasets

## 📈 Extending the Framework

### Future Enhancements

1. **Additional Methods**: BERT-based, transformer models
2. **Language Support**: Multi-language extraction
3. **Real-time Analysis**: Streaming text processing
4. **Custom Metrics**: Domain-specific evaluation criteria
5. **Web Interface**: GUI for easier interaction

### Contributing

Feel free to extend the framework by:
- Adding new extraction methods
- Improving visualization quality
- Enhancing optimization algorithms
- Adding more test case categories

## 📞 Support

For questions or issues:
1. Check the generated error logs
2. Verify all dependencies are installed
3. Ensure sufficient system resources
4. Review the console output for specific error messages

---

**Happy Researching! 🎓✨**

This framework provides the quantitative evidence you need to justify your method selection in your thesis. The comprehensive benchmarking and optimization analysis will demonstrate your systematic approach to solving the keyword extraction problem.
