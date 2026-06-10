import matplotlib
# Use the non-interactive Agg backend to generate a fixed file output directly
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# Exact scenario index values converted to decimal format
scenarios = ['Baseline Weighting', 'Scenario A:\nSustainability Priority', 'Scenario B:\nROI Priority']
london_scores = [0.4556, 0.4605, 0.4487]
hong_kong_scores = [0.5838, 0.6391, 0.5284]
singapore_scores = [0.5593, 0.6407, 0.4876]

x = np.arange(len(scenarios))
width = 0.24  # Maintained structural width for clear separation

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)

# Colour configuration using requested palette with alpha transparency
# London: Imperial Blue | Hong Kong: Vivid Red | Singapore: Balanced Green
rects1 = ax.bar(x - width, london_scores, width, label='London', color='#002147', alpha=0.85)     
rects2 = ax.bar(x, hong_kong_scores, width, label='Hong Kong', color='#DC241F', alpha=0.85)    
rects3 = ax.bar(x + width, singapore_scores, width, label='Singapore', color='#00A15C', alpha=0.85) 

# Visual layout adjustments using UK terminology
ax.set_ylabel('Consolidated Performance Score', fontsize=16, fontweight='bold', labelpad=12)
ax.set_title('Sensitivity Analysis Matrix: Scenario-Based Performance Comparison', fontsize=18, pad=22, fontweight='bold')
ax.set_xticks(x)

# Enlarged horizontal axis text assets for poster legibility (16pt)
ax.set_xticklabels(scenarios, fontsize=16, fontweight='bold')

# Cleaned up y-axis bounds to minimise dead space and amplify visible differences
ax.set_ylim(0.0, 0.75)
ax.tick_params(axis='y', labelsize=14)

# Removed boundary lines and vertical gridlines to eliminate visual clutter
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Faint grey horizontal gridlines only
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#b0b0b0')

# Enlarged legend elements for long-distance legibility (16pt)
ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none', fontsize=16)

# Direct data labels function placing exact numerical scores on top of each bar
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6),  # Elevated slightly for clarity
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

add_labels(rects1)
add_labels(rects2)
add_labels(rects3)

plt.tight_layout()

# Save the permanent fixed static figure asset directly to your project directory
plt.savefig('tod_scenarios_combined.png', bbox_inches='tight')
plt.close(fig)
print("Fixed figure successfully saved with swapped transparent colours as 'tod_scenarios_combined.png'")