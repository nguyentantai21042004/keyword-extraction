"""
Text processing utilities
"""

import re
from typing import List

def preprocess_text(text: str) -> str:
    """Basic text preprocessing"""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep Vietnamese diacritics
    text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text)
    
    return text

def detect_language(text: str) -> str:
    """Simple language detection based on character patterns"""
    
    # Count Vietnamese characters
    vietnamese_chars = sum(1 for char in text if char in 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ')
    
    # Count English characters
    english_chars = sum(1 for char in text if char.isascii() and char.isalpha())
    
    if vietnamese_chars > 0:
        return "vi"
    elif english_chars > len(text) * 0.7:
        return "en"
    else:
        return "mixed"

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    
    hashtags = re.findall(r'#\w+', text)
    return [tag[1:] for tag in hashtags]  # Remove # symbol

def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text"""
    
    mentions = re.findall(r'@\w+', text)
    return [mention[1:] for mention in mentions]  # Remove @ symbol

def clean_social_media_text(text: str) -> str:
    """Clean social media text for better processing"""
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove emojis (basic)
    text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text
