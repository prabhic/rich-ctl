"""
Tests for Telugu text shaping.
"""

import unittest
from rich_ctl.shape import shape_text
from rich_ctl.measure import px_to_cells


class TestTeluguShaping(unittest.TestCase):
    """Test cases for Telugu text shaping."""
    
    def test_telugu_shaping(self):
        """Test that Telugu text is shaped correctly."""
        # Telugu sample text
        text = "తెలుగు"  # "Telugu" in Telugu
        
        # Shape the text with the Telugu script
        clusters = shape_text(text, script="telu")
        
        # Verify the results
        self.assertIsNotNone(clusters)
        self.assertGreater(len(clusters), 0)
        
        # Check that each cluster has a positive advance
        for cluster in clusters:
            self.assertGreater(cluster.advance_px, 0)
        
        # Print debug information
        print(f"\nTelugu text: {text}")
        for i, cluster in enumerate(clusters):
            print(f"Cluster {i+1}: '{cluster.text}' - {cluster.advance_px}px")
    
    def test_telugu_width_calculation(self):
        """Test width calculation for Telugu text."""
        # Telugu sample text
        text = "తెలుగు"  # "Telugu" in Telugu
        
        # Shape the text
        clusters = shape_text(text, script="telu")
        
        # Calculate cell widths
        total_width_px = sum(cluster.advance_px for cluster in clusters)
        total_width_cells = px_to_cells(total_width_px)
        
        # Verify the width is reasonable
        self.assertGreater(total_width_cells, 0)
        self.assertLessEqual(total_width_cells, len(text) * 2)  # Shouldn't be more than double the character count
        
        # Print debug information
        print(f"\nTelugu text: {text}")
        print(f"Total width: {total_width_px}px = {total_width_cells} cells")
        
        # Individual cluster widths
        for i, cluster in enumerate(clusters):
            cell_width = px_to_cells(cluster.advance_px)
            print(f"Cluster {i+1}: '{cluster.text}' - {cluster.advance_px}px = {cell_width} cells")


if __name__ == "__main__":
    unittest.main()
