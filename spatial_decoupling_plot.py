import matplotlib
# Use the non-interactive Agg backend to generate a fixed file output directly
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# Empirical index coordinates from the updated dimensional evaluation matrix
cities = ['London', 'Hong Kong', 'Singapore']
spatial_fabric = [0.2370, 0.6045, 0.5232]
economic_maturity = [18.6078, 14.1515, 3.5329]

# Colour configuration matching institutional branding
# London: Imperial Blue | Hong Kong: Vivid Red | Singapore: Balanced Green
colours = ['#002147', '#DC241F', '#00A15C']

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)

# Plot each urban typology as an enlarged distinct data node
for i, city in enumerate(cities):
    ax.scatter(spatial_fabric[i], economic_maturity[i], 
               color=colours[i], alpha=0.85, s=350, 
               label=city, edgecolors='#333333', linewidths=1.5, zorder=3)
    
    # Direct text annotations detailing precise coordinates next to each node
    ax.annotate(f"{city}\n(Spatial: {spatial_fabric[i]:.4f}\nEconomic Maturity Index: {economic_maturity[i]:.4f})",
                xy=(spatial_fabric[i], economic_maturity[i]),
                xytext=(15, 0),  # Offset rightward to prevent overlap
                textcoords="offset points",
                ha='left', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#e2e8f0', alpha=0.9))

# Visual layout adjustments using UK terminology
ax.set_xlabel('Spatial', fontsize=16, fontweight='bold', labelpad=12)
ax.set_ylabel('Economic Maturity Index', fontsize=16, fontweight='bold', labelpad=12)
ax.set_title('Decoupling of Density and Value: Spatial vs Economic Maturity', fontsize=18, pad=22, fontweight='bold')

# Normalised operational bounds to isolate the quadrant workspace clearly
ax.set_xlim(0.0, 0.80)
ax.set_ylim(0.0, 22.0)
ax.tick_params(axis='both', labelsize=14)

# Removed boundary lines to eliminate unnecessary visual clutter
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Complete gridline array to allow easy coordinate tracking by examiners
ax.grid(axis='both', linestyle='--', alpha=0.5, color='#b0b0b0', zorder=1)

# Enlarged legend elements for maximum legibility
ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none', fontsize=16)

plt.tight_layout()

# Save the permanent static figure asset directly to your project repository
plt.savefig('tod_spatial_economic_decoupling.png', bbox_inches='tight')
plt.close(fig)
print("Spatial scatter plot successfully saved with corrected absolute values as 'tod_spatial_economic_decoupling.png'")