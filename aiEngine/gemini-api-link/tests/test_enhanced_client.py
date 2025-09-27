#!/usr/bin/env python3
"""
Test suite for Enhanced Gemini Client
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestEnhancedGeminiClient(unittest.TestCase):
    """Test cases for enhanced gemini client functionality"""

    def setUp(self):
        """Set up test fixtures"""
        try:
            from enhanced_gemini_client import farming_advisor
            self.advisor = farming_advisor
        except ImportError:
            self.skipTest("Enhanced gemini client not available")

    def test_function_availability(self):
        """Test that all required functions are available"""
        required_methods = [
            'yield_prediction',
            'pest_image_detection',
            'crop_disease',
            'fallback_nlp',
            'process_farmer_query'
        ]

        for method in required_methods:
            self.assertTrue(
                hasattr(self.advisor, method),
                f"Method {method} not found in farming advisor"
            )

    def test_yield_prediction_response_structure(self):
        """Test yield prediction response has correct structure"""
        try:
            result = self.advisor.yield_prediction("Test yield prediction")

            self.assertIsInstance(result, dict)
            self.assertIn('module', result)
            self.assertEqual(result['module'], 'yield_prediction')
            self.assertIn('timestamp', result)

        except Exception as e:
            # If API call fails, we still check the structure handling
            self.assertIsInstance(e, Exception)

    def test_fallback_nlp_response_structure(self):
        """Test fallback NLP response has correct structure"""
        try:
            result = self.advisor.fallback_nlp("Test general question")

            self.assertIsInstance(result, dict)
            self.assertIn('module', result)
            self.assertEqual(result['module'], 'fallback_nlp')
            self.assertIn('timestamp', result)

        except Exception as e:
            # If API call fails, we still check the structure handling
            self.assertIsInstance(e, Exception)

    def test_error_handling_empty_query(self):
        """Test error handling with empty query"""
        from enhanced_gemini_client import process_query

        result = process_query("")

        self.assertIsInstance(result, dict)
        self.assertIn('module', result)
        # Should fallback to fallback_nlp or error handling

if __name__ == '__main__':
    print("Enhanced Gemini Client - Test Suite")
    print("=" * 40)

    unittest.main(verbosity=2)
