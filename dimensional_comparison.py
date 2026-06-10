import matplotlib
# Use the non-interactive Agg backend to generate a fixed file output directly
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# Empirical dimensional breakdown data matrix
dimensions = ['Transport', 'Spatial', 'Economic', 'Social & Sustainability']
london_scores = [0.5440, 0.2370, 0.4729, 0.5060]
hk_scores = [0.7191, 0.6045, 0.3467, 0.7149]
singapore_scores = [0.6626, 0.5232, 0.3140, 0.8569]

x = np.arange(len(dimensions))
width = 0.24  # Maintained structural width for clear column clustering

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)

# Colour configuration using requested palette with alpha transparency
# London: Imperial Blue | Hong Kong: Vivid Red | Singapore: Balanced Green
rects1 = ax.bar(x - width, london_scores, width, label='London', color='#002147', alpha=0.85)     
rects2 = ax.bar(x, hk_scores, width, label='Hong Kong', color='#DC241F', alpha=0.85)    
rects3 = ax.bar(x + width, singapore_scores, width, label='Singapore', color='#00A15C', alpha=0.85) 

# Visual layout adjustments using UK terminology
ax.set_ylabel('Dimensional Index Score', fontsize=16, fontweight='bold', labelpad=12)
ax.set_title('Dimensional Performance Comparison Matrix', fontsize=18, pad=22, fontweight='bold')
ax.set_xticks(x)

# Enlarged horizontal axis text assets for poster and slide legibility (16pt)
ax.set_xticklabels(dimensions, fontsize=16, fontweight='bold')

# Normalised y-axis limits to represent the full theoretical scale up to 1.0
ax.set_ylim(0.0, 1.0)
ax.tick_params(axis='y', labelsize=14)

# Removed boundary lines to eliminate visual clutter
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Faint grey horizontal gridlines only for quantitative references
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#b0b0b0')

# Enlarged legend elements for maximum legibility (16pt)
ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none', fontsize=16)

# Direct data labels function placing exact numerical scores on top of each bar
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6),  # Elevated slightly for clarity
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

add_labels(rects1)
add_labels(rects2)
add_labels(rects3)

plt.tight_layout()

# Save the permanent fixed static figure asset directly to your project directory
plt.savefig('tod_dimensional_comparison.png', bbox_inches='tight')
plt.close(fig)
print("Dimensional chart successfully saved with white background as 'tod_dimensional_comparison.png'")