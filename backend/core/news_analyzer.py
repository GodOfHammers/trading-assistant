# backend/core/news_analyzer.py

import numpy as np
from typing import Dict, List
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging
from datetime import datetime, timedelta

class NewsAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')
        except Exception as e:
            logging.error(f"NLTK download error: {str(e)}")
        
        self.stop_words = set(stopwords.words('english'))
        self.important_keywords = {
            'positive': [
                'growth', 'profit', 'increase', 'expansion', 'partnership',
                'innovation', 'launch', 'success', 'record', 'breakthrough'
            ],
            'negative': [
                'loss', 'decline', 'bankruptcy', 'lawsuit', 'investigation',
                'scandal', 'downgrade', 'layoff', 'recall', 'violation'
            ]
        }
    
    async def analyze(self, news_data: List[Dict]) -> Dict:
        """Analyze news articles for sentiment and impact."""
        try:
            if not news_data:
                return self._generate_neutral_analysis()
            
            # Process each article
            article_scores = []
            for article in news_data:
                score = await self._analyze_article(article)
                article_scores.append(score)
            
            # Combine scores with time decay
            combined_score = self._combine_scores(article_scores)
            
            # Generate final analysis
            return {
                'score': combined_score['sentiment'],
                'impact': combined_score['impact'],
                'confidence': combined_score['confidence'],
                'summary': self._generate_summary(article_scores),
                'key_topics': self._extract_key_topics(news_data)
            }
            
        except Exception as e:
            logging.error(f"News analysis error: {str(e)}")
            return self._generate_neutral_analysis()
    
    async def _analyze_article(self, article: Dict) -> Dict:
        """Analyze individual article."""
        try:
            text = f"{article['title']} {article['description']}"
            
            # Basic sentiment analysis
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            
            # Keyword analysis
            keywords = self._extract_keywords(text)
            keyword_impact = self._analyze_keywords(keywords)
            
            # Calculate impact and confidence
            impact = self._calculate_impact(
                sentiment,
                keyword_impact,
                article.get('source_reliability', 0.5)
            )
            
            confidence = self._calculate_confidence(
                len(text),
                article.get('source_reliability', 0.5),
                len(keywords)
            )
            
            return {
                'sentiment': sentiment,
                'impact': impact,
                'confidence': confidence,
                'keywords': keywords,
                'timestamp': article.get('published_at', datetime.now())
            }
            
        except Exception as e:
            logging.error(f"Article analysis error: {str(e)}")
            return {
                'sentiment': 0,
                'impact': 0,
                'confidence': 0,
                'keywords': [],
                'timestamp': datetime.now()
            }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        try:
            # Tokenize and remove stop words
            tokens = word_tokenize(text.lower())
            tokens = [t for t in tokens if t not in self.stop_words]
            
            # Part of speech tagging
            tagged = nltk.pos_tag(tokens)
            
            # Extract relevant parts of speech
            keywords = [
                word for word, pos in tagged
                if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBG', 'JJ']
            ]
            
            return keywords
            
        except Exception as e:
            logging.error(f"Keyword extraction error: {str(e)}")
            return []
    
    def _analyze_keywords(self, keywords: List[str]) -> float:
        """Analyze keywords for sentiment impact."""
        try:
            positive_count = sum(
                1 for k in keywords
                if k in self.important_keywords['positive']
            )
            negative_count = sum(
                1 for k in keywords
                if k in self.important_keywords['negative']
            )
            
            if not keywords:
                return 0
                
            return (positive_count - negative_count) / len(keywords)
            
        except Exception as e:
            logging.error(f"Keyword analysis error: {str(e)}")
            return 0
    
    def _calculate_impact(
        self,
        sentiment: float,
        keyword_impact: float,
        source_reliability: float
    ) -> float:
        """Calculate news impact score."""
        try:
            # Combine factors with weights
            impact = (
                sentiment * 0.4 +
                keyword_impact * 0.4 +
                source_reliability * 0.2
            )
            
            return np.clip(impact, -1, 1)
            
        except Exception as e:
            logging.error(f"Impact calculation error: {str(e)}")
            return 0
    
    def _calculate_confidence(
        self,
        text_length: int,
        source_reliability: float,
        keyword_count: int
    ) -> float:
        """Calculate confidence in the analysis."""
        try:
            # Factors affecting confidence
            length_score = min(text_length / 1000, 1)  # Normalize to 1000 chars
            keyword_score = min(keyword_count / 20, 1)  # Normalize to 20 keywords
            
            confidence = (
                length_score * 0.3 +
                source_reliability * 0.5 +
                keyword_score * 0.2
            )
            
            return np.clip(confidence, 0, 1)
            
        except Exception as e:
            logging.error(f"Confidence calculation error: {str(e)}")
            return 0.5
    
    def _combine_scores(self, article_scores: List[Dict]) -> Dict:
        """Combine multiple article scores with time decay."""
        try:
            if not article_scores:
                return {'sentiment': 0, 'impact': 0, 'confidence': 0}
            
            # Sort by timestamp
            sorted_scores = sorted(
                article_scores,
                key=lambda x: x['timestamp'],
                reverse=True
            )
            
            # Calculate time decay weights
            now = datetime.now()
            weights = []
            sentiments = []
            impacts = []
            confidences = []
            
            for score in sorted_scores:
                time_diff = (now - score['timestamp']).total_seconds() / 3600
                weight = 1 / (1 + time_diff/24)  # 24-hour half-life
                
                weights.append(weight)
                sentiments.append(score['sentiment'])
                impacts.append(score['impact'])
                confidences.append(score['confidence'])
            
            # Normalize weights
            weights = np.array(weights) / sum(weights)
            
            # Calculate weighted averages
            return {
                'sentiment': np.average(sentiments, weights=weights),
                'impact': np.average(impacts, weights=weights),
                'confidence': np.average(confidences, weights=weights)
            }
            
        except Exception as e:
            logging.error(f"Score combination error: {str(e)}")
            return {'sentiment': 0, 'impact': 0, 'confidence': 0}
    
    def _generate_summary(self, article_scores: List[Dict]) -> str:
        """Generate summary of news analysis."""
        try:
            if not article_scores:
                return "No recent news available."
            
            combined = self._combine_scores(article_scores)
            
            sentiment_str = (
                "positive" if combined['sentiment'] > 0.2
                else "negative" if combined['sentiment'] < -0.2
                else "neutral"
            )
            
            impact_str = (
                "high" if combined['impact'] > 0.6
                else "moderate" if combined['impact'] > 0.3
                else "low"
            )
            
            return f"Recent news sentiment is {sentiment_str} with {impact_str} impact."
            
        except Exception as e:
            logging.error(f"Summary generation error: {str(e)}")
            return "Unable to generate news summary."
    
    def _extract_key_topics(self, news_data: List[Dict]) -> List[str]:
        """Extract key topics from news articles."""
        try:
            all_keywords = []
            for article in news_data:
                text = f"{article['title']} {article['description']}"
                keywords = self._extract_keywords(text)
                all_keywords.extend(keywords)
            
            # Count keyword frequencies
            keyword_freq = pd.Series(all_keywords).value_counts()
            
            # Return top 5 topics
            return keyword_freq.head(5).index.tolist()
            
        except Exception as e:
            logging.error(f"Topic extraction error: {str(e)}")
            return []
    
    def _generate_neutral_analysis(self) -> Dict:
        """Generate neutral analysis when no news is available."""
        return {
            'score': 0,
            'impact': 0,
            'confidence': 0,
            'summary': "No recent news available for analysis.",
            'key_topics': []
        }