import pyglet
from pyglet.gl import GL_LINE_STRIP
import numpy as np
from collections import deque

class TreeNode:
    """Simple binary tree node for demonstration."""
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

class PygletVisualizer:
    def __init__(self, width=800, height=600, title="Audio Visualizer"):
        self.width = width
        self.height = height
        self.title = title

        self.alpha = 0.3  # Smoothing factor for magnitudes
        self.smoothed_magnitudes = None
        self.rolling_max = 1.0  # Start with a default max

        self.window = pyglet.window.Window(width, height, title)
        self.batch = pyglet.graphics.Batch()
        self.lines = []

        # Data Structures Integration -------------------------
        # List to store recent average values
        self.recent_avg_values = []

        # Queue (using deque) to store recent normalized values
        self.normalized_history = deque(maxlen=10)

        # Hash table (dict) for frequency thresholds
        self.freq_ranges = {
            "low": (0, 300),
            "mid": (300, 2000),
            "high": (2000, None)
        }

        # Tree structure
        self.freq_tree = TreeNode("All Frequencies")
        self.freq_tree.left = TreeNode("Low")
        self.freq_tree.right = TreeNode("Mid-High")
        self.freq_tree.right.left = TreeNode("Mid")
        self.freq_tree.right.right = TreeNode("High")

        # Graph structure
        self.freq_graph = {
            "Low": ["Mid"],
            "Mid": ["High"],
            "High": []
        }

        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()

    def traverse_tree(self, node):
        # Inorder traversal to utilize the tree
        if node is None:
            return []
        return self.traverse_tree(node.left) + [node.name] + self.traverse_tree(node.right)

    def update_lines(self, freq_bins, magnitudes):
        # Exponential smoothing of magnitudes
        if self.smoothed_magnitudes is None:
            self.smoothed_magnitudes = magnitudes.copy()
        else:
            self.smoothed_magnitudes = self.alpha * magnitudes + (1 - self.alpha) * self.smoothed_magnitudes

        low_range = self.freq_ranges["low"]   # (0, 300)
        mid_range = self.freq_ranges["mid"]   # (300, 2000)
        high_range = self.freq_ranges["high"] # (2000, None)

        low_freq_mask = (freq_bins < low_range[1])
        mid_freq_mask = (freq_bins >= mid_range[0]) & (freq_bins <= mid_range[1])
        high_freq_mask = (freq_bins > high_range[0])

        weights = np.zeros_like(self.smoothed_magnitudes)
        weights[low_freq_mask] = 1.0
        weights[mid_freq_mask] = 0.2
        weights[high_freq_mask] = 1.0

        weighted_magnitudes = self.smoothed_magnitudes * weights

        current_max = np.max(weighted_magnitudes)
        self.rolling_max = 0.1 * current_max + 0.9 * self.rolling_max
        if self.rolling_max < 1e-6:
            self.rolling_max = 1e-6

        avg_val = np.mean(weighted_magnitudes) if np.sum(weights) > 0 else 0.0
        normalized_val = avg_val / self.rolling_max if self.rolling_max > 0 else 0.0

        # Store avg_val in the list
        self.recent_avg_values.append(avg_val)
        if len(self.recent_avg_values) > 50:
            self.recent_avg_values.pop(0)

        # Store normalized_val in the queue
        self.normalized_history.append(normalized_val)

        # Traverse the tree to ensure it's being utilized
        _ = self.traverse_tree(self.freq_tree)

        # Color fixed to green
        chosen_color = (0.0, 1.0, 0.0)

        line_offset = normalized_val * (self.height * 0.5)
        center_y = self.height / 2

        if current_max < 1e-3:
            line_offset = 0

        x_values = np.linspace(0, self.width, 200)
        vertices = []
        for x in x_values:
            y = center_y + line_offset
            vertices.extend([x, y])

        self.batch = pyglet.graphics.Batch()
        self.lines.clear()

        if len(vertices) > 2:
            self.lines.append(
                self.batch.add(
                    len(vertices)//2, GL_LINE_STRIP, None,
                    ("v2f", vertices),
                    ("c3f", chosen_color * (len(vertices)//2))
                )
            )

    def run(self, update_callback):
        def update(dt):
            freq_bins, magnitudes = update_callback()
            self.update_lines(freq_bins, magnitudes)

        pyglet.clock.schedule_interval(update, 1 / 60.0)
        pyglet.app.run()
