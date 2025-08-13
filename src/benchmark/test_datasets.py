"""
Test dataset creation for benchmarking
"""

def create_research_test_dataset():
    """Create comprehensive test dataset for research"""
    
    # Enhanced test cases with Vietnamese support
    enhanced_test_cases = [
        # English Social Media
        {
            'text': "Just discovered #sustainablefashion trends! @patagonia's new eco-line is amazing 🌱 The collection features organic cotton and recycled materials. #ecofriendly #fashiontech",
            'expected_keywords': ['sustainable fashion', 'patagonia', 'eco-line', 'organic cotton', 'recycled materials', 'ecofriendly', 'fashiontech'],
            'category': 'social_media',
            'language': 'en',
            'complexity': 'high'
        },
        {
            'text': "Need insights on influencer marketing for beauty brands targeting Gen Z #beautytech #influencer #genz #beauty #marketing #digital",
            'expected_keywords': ['influencer marketing', 'beauty brands', 'gen z', 'beautytech', 'beauty', 'marketing', 'digital'],
            'category': 'social_media',
            'language': 'en',
            'complexity': 'medium'
        },
        
        # Vietnamese Social Media
        {
            'text': "Xu hướng thời trang bền vững tại Việt Nam! 🌱 Các thương hiệu đang sử dụng vật liệu tái chế và công nghệ xanh #thoitrangbenvung #ecofriendly #vietnam",
            'expected_keywords': ['xu hướng thời trang', 'bền vững', 'việt nam', 'thương hiệu', 'vật liệu tái chế', 'công nghệ xanh', 'thoitrangbenvung', 'ecofriendly'],
            'category': 'social_media',
            'language': 'vi',
            'complexity': 'high'
        },
        {
            'text': "Marketing influencer cho ngành beauty tại Việt Nam #beautytech #influencer #beauty #marketing #digital #vietnam",
            'expected_keywords': ['marketing influencer', 'ngành beauty', 'việt nam', 'beautytech', 'beauty', 'marketing', 'digital'],
            'category': 'social_media',
            'language': 'vi',
            'complexity': 'medium'
        },
        
        # English Business
        {
            'text': "Market analysis of renewable energy sector shows significant growth in solar and wind power technologies. Investment in clean energy reached $500 billion in 2023, with solar leading at 45% market share.",
            'expected_keywords': ['market analysis', 'renewable energy', 'solar power', 'wind power', 'investment', 'clean energy', 'market share'],
            'category': 'business',
            'language': 'en',
            'complexity': 'high'
        },
        
        # Vietnamese Business
        {
            'text': "Phân tích thị trường năng lượng tái tạo tại Việt Nam cho thấy tăng trưởng mạnh mẽ trong công nghệ năng lượng mặt trời và gió. Đầu tư vào năng lượng sạch đạt 500 tỷ đồng năm 2023.",
            'expected_keywords': ['phân tích thị trường', 'năng lượng tái tạo', 'việt nam', 'công nghệ năng lượng', 'mặt trời', 'gió', 'đầu tư', 'năng lượng sạch'],
            'category': 'business',
            'language': 'vi',
            'complexity': 'high'
        },
        
        # English Technical
        {
            'text': "Machine learning algorithms for natural language processing applications in social media sentiment analysis. Implementation using transformer models and attention mechanisms.",
            'expected_keywords': ['machine learning', 'algorithms', 'natural language processing', 'social media', 'sentiment analysis', 'transformer models', 'attention mechanisms'],
            'category': 'technical',
            'language': 'en',
            'complexity': 'high'
        },
        
        # Vietnamese Technical
        {
            'text': "Thuật toán machine learning cho ứng dụng xử lý ngôn ngữ tự nhiên trong phân tích cảm xúc mạng xã hội. Triển khai sử dụng transformer models và attention mechanisms.",
            'expected_keywords': ['thuật toán machine learning', 'ứng dụng xử lý ngôn ngữ tự nhiên', 'phân tích cảm xúc', 'mạng xã hội', 'transformer models', 'attention mechanisms'],
            'category': 'technical',
            'language': 'vi',
            'complexity': 'high'
        },
        
        # Short Text Examples
        {
            'text': "AI startup funding trends 2024",
            'expected_keywords': ['ai startup', 'funding trends', '2024'],
            'category': 'short_text',
            'language': 'en',
            'complexity': 'low'
        },
        {
            'text': "Xu hướng đầu tư startup AI 2024",
            'expected_keywords': ['xu hướng đầu tư', 'startup ai', '2024'],
            'category': 'short_text',
            'language': 'vi',
            'complexity': 'low'
        },
        
        # Challenging Cases
        {
            'text': "The quantum computing paradigm shift necessitates interdisciplinary collaboration between physicists, computer scientists, and mathematicians to develop novel algorithms for optimization problems.",
            'expected_keywords': ['quantum computing', 'paradigm shift', 'interdisciplinary collaboration', 'physicists', 'computer scientists', 'mathematicians', 'novel algorithms', 'optimization problems'],
            'category': 'challenging',
            'language': 'en',
            'complexity': 'very_high'
        },
        {
            'text': "Sự thay đổi mô hình trong điện toán lượng tử đòi hỏi sự hợp tác liên ngành giữa các nhà vật lý, khoa học máy tính và toán học để phát triển các thuật toán mới cho bài toán tối ưu hóa.",
            'expected_keywords': ['thay đổi mô hình', 'điện toán lượng tử', 'hợp tác liên ngành', 'nhà vật lý', 'khoa học máy tính', 'toán học', 'thuật toán mới', 'bài toán tối ưu hóa'],
            'category': 'challenging',
            'language': 'vi',
            'complexity': 'very_high'
        }
    ]
    
    return enhanced_test_cases
