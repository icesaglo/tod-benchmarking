import pandas as pd
import numpy as np
import re
import warnings

warnings.filterwarnings("ignore")

# 1. Load data
df = pd.read_excel('raw_benchmarking_data.xlsx', sheet_name='Data')

df = df.dropna(subset=["London", "HK", "SG"], how="all")

df["Data"] = df["Data"].mask(df["Data"].duplicated(), df["Data"] + " (Duplicate)")
df.set_index("Data", inplace=True)

cities = ["London", "HK", "SG"]


def clean_num(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    if val_str == "IDEAL":
        return np.nan
    cleaned = re.sub(r"[^\d.]", "", val_str)
    return float(cleaned) if cleaned else np.nan


df_cities = df[cities].applymap(clean_num)

# 2. Calculate Framework Metrics
df_bench = df_cities.copy()

opex = df_bench.loc["METRO Operating Expense"]
total_rev = df_bench.loc["METRO Revenue (Farebox)"] + df_bench.loc["METRO Revenue (Non-Farebox)"]
df_bench.loc["Operating Ratio (OR)"] = opex / total_rev
df_bench.loc["Network Density"] = df_bench.loc["Total mileage of rail lines"] / df_bench.loc["Total City Land Area"]
df_bench.loc["Interchange Ratio"] = (
    df_bench.loc["Total Number of interchange stations"] / df_bench.loc["Total Number of stations"]
)

land_uses = ["Residential", "Commercial", "Industrial", "Public & Institutional", "Transport & Infrastructure"]
lu_data = df_bench.loc[land_uses]
lu_proportions = lu_data.div(lu_data.sum(axis=0), axis=1)
k = len(land_uses)
entropy = -(lu_proportions * np.log(lu_proportions.replace(0, np.nan))).sum(axis=0) / np.log(k)
df_bench.loc["Land-use Diversity Index (H)"] = entropy.fillna(0)

I_norm = df_bench.loc["Intersection Density"] / 100.0
P_temp = np.clip(abs(df_bench.loc["Median temperature"] - 21) / 15.0, 0, 1)
P_hum = np.clip(abs(df_bench.loc["Median Humidity"] - 50) / 40.0, 0, 1)
P_grad = np.clip(df_bench.loc["Mean gradient"] / 10.0, 0, 1)
rain_per_day = df_bench.loc["Median rainfall per year"] / df_bench.loc["Number of rainy days per year"]
P_rain = np.clip(rain_per_day / 10.0, 0, 1)
penalty_sum = (0.40 * P_grad) + (0.25 * P_temp) + (0.20 * P_hum) + (0.15 * P_rain)
df_bench.loc["Walkability Index (WI)"] = I_norm * (1 - penalty_sum)

df_bench.loc["Market Resilience Index"] = (
    df_bench.loc["Commercial Real Estate Absorption Rate"] / df_bench.loc["Commercial vacancy rates"]
)
df_bench.loc["Employment Density"] = (
    df_bench.loc["Total City Employment (million)"] / df_bench.loc["Total City Land Area"]
)
df_bench.loc["Population Density"] = (
    df_bench.loc["Total City Population (million)"] / df_bench.loc["Total City Land Area"]
)
tertiary = df_bench.loc["Tertiary Industry Share"]
non_tertiary = df_bench.loc["Primary Industry Share"] + df_bench.loc["Secondary Industry Share"]
df_bench.loc["Economic Maturity Index"] = tertiary / non_tertiary
df_bench.loc["Financial Spread"] = df_bench.loc["Average Internal Rate of Return (IRR)"] - df_bench.loc["WACC"]

df_bench.loc["Transport Affordability Index"] = (
    df_bench.loc["Monthly Transit Pass Cost (Population-weighted average)"]
    / df_bench.loc["Median Monthly Household Income"]
)
df_bench.loc["Housing Affordability Index"] = (
    df_bench.loc["Median Monthly Rent"] / df_bench.loc["Median Monthly Household Income"]
)

# 3. Taxonomy and bounds
dimensions = {
    "Transport": [
        "METRO Mode Share",
        "Operating Ratio (OR)",
        "Avg Peak service headway",
        "Avg Off-peak service headway",
        "Network Density",
        "Interchange Ratio",
        "Network Centrality",
        "Service Reliability",
    ],
    "Spatial": [
        "Plot Ratio (Floor Space Index)",
        "Land-use Diversity Index (H)",
        "Walkability Index (WI)",
        "Vertical Connectivity Index",
    ],
    "Economic": [
        "LVC Property Price Premium",
        "Market Resilience Index",
        "Financial Spread",
        "Employment Density",
        "Population Density",
        "Economic Maturity Index",
    ],
    "Social": [
        "Transport Affordability Index",
        "Housing Affordability Index",
        "Step-free metro station access",
        "Car Ownership per Household",
        "Transport Carbon Intensity",
        "Affordable Housing Share",
    ],
}

directions = {
    "METRO Mode Share": 1,
    "Operating Ratio (OR)": 0,
    "Avg Peak service headway": 0,
    "Avg Off-peak service headway": 0,
    "Network Density": 1,
    "Interchange Ratio": 1,
    "Network Centrality": 0,
    "Service Reliability": 1,
    "Plot Ratio (Floor Space Index)": 1,
    "Land-use Diversity Index (H)": 1,
    "Walkability Index (WI)": 1,
    "Vertical Connectivity Index": 1,
    "LVC Property Price Premium": 1,
    "Market Resilience Index": 1,
    "Financial Spread": 1,
    "Employment Density": 1,
    "Population Density": 1,
    "Economic Maturity Index": 1,
    "Transport Affordability Index": 0,
    "Housing Affordability Index": 0,
    "Step-free metro station access": 1,
    "Car Ownership per Household": 0,
    "Transport Carbon Intensity": 0,
    "Affordable Housing Share": 1,
}

global_bounds = {
    "METRO Mode Share": (0, 100),
    "Operating Ratio (OR)": (0, 2),
    "Avg Peak service headway": (0, 10),
    "Avg Off-peak service headway": (0, 20),
    "Network Density": (0, 1.0),
    "Interchange Ratio": (0, 0.5),
    "Network Centrality": (0, 0.05),
    "Service Reliability": (0, 100),
    "Plot Ratio (Floor Space Index)": (0, 15),
    "Land-use Diversity Index (H)": (0, 1),
    "Walkability Index (WI)": (0, 2),
    "Vertical Connectivity Index": (1, 5),
    "LVC Property Price Premium": (0, 50),
    "Market Resilience Index": (0, 50),
    "Financial Spread": (-5, 20),
    "Employment Density": (0, 0.05),
    "Population Density": (0, 0.05),
    "Economic Maturity Index": (0, 30),
    "Transport Affordability Index": (0, 0.5),
    "Housing Affordability Index": (0, 1.0),
    "Step-free metro station access": (0, 100),
    "Car Ownership per Household": (0, 2),
    "Transport Carbon Intensity": (0, 100),
    "Affordable Housing Share": (0, 100),
}

scenarios = {
    "Baseline": {"Transport": 0.35, "Spatial": 0.20, "Economic": 0.30, "Social": 0.15},
    "Scenario A (Carbon Priority)": {"Transport": 0.35, "Spatial": 0.20, "Economic": 0.15, "Social": 0.30},
    "Scenario B (ROI Priority)": {"Transport": 0.30, "Spatial": 0.20, "Economic": 0.45, "Social": 0.05},
}


# 5. Execute Analysis 

def run_scoring_pipeline(use_abs_bounds, scoring_name):
    print("\n" + "=" * 70)
    print(f" {scoring_name}")
    print("=" * 70 + "\n")

    df_norm = pd.DataFrame(index=directions.keys(), columns=cities)
    for m in directions.keys():
        vals = df_bench.loc[m].values

        if use_abs_bounds:
            v_min, v_max = global_bounds[m]
        else:
            v_min, v_max = np.min(vals), np.max(vals)
            if v_max == v_min:
                v_min, v_max = 0, v_max * 2 if v_max > 0 else 1

        if directions[m] == 1:
            norm_vals = (vals - v_min) / (v_max - v_min)
        else:
            norm_vals = (v_max - vals) / (v_max - v_min)

        df_norm.loc[m] = np.clip(norm_vals, 0, 1) if use_abs_bounds else norm_vals

    df_norm = df_norm.fillna(0)

    dynamic_weights = {}
    print("Calculated Level 2 Weights (Pearson Correlation):")
    for dim, metrics in dimensions.items():
        print(f"\n{dim} Dimension:")
        dim_data = df_norm.loc[metrics].T.astype(float)
        baseline_composite = dim_data.mean(axis=1)
        dim_weights_raw = {}
        for m in metrics:
            corr = dim_data[m].corr(baseline_composite, method="pearson")
            if pd.isna(corr) or corr < 0:
                corr = 0.001
            dim_weights_raw[m] = corr

        total_corr = sum(dim_weights_raw.values())
        for m in metrics:
            final_weight = dim_weights_raw[m] / total_corr
            dynamic_weights[m] = final_weight
            print(f"  {m}: {final_weight:.4f}")

    print("\n" + "=" * 50 + "\n")

    dimension_scores = pd.DataFrame(index=dimensions.keys(), columns=cities)
    for dim, metrics in dimensions.items():
        for city in cities:
            score = sum(df_norm.loc[m, city] * dynamic_weights[m] for m in metrics)
            dimension_scores.loc[dim, city] = score

    dimension_scores = dimension_scores.astype(float)
    print("Level 2 Dimension Sub-Scores (Out of 1.0):")
    print(dimension_scores.to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n" + "=" * 50)

    for scenario_name, weights in scenarios.items():
        print(f"\n--- {scenario_name} ---")
        final_scores = {}
        for city in cities:
            total = sum(dimension_scores.loc[dim, city] * weights[dim] for dim in dimensions.keys())
            final_scores[city] = total

        for city, score in final_scores.items():
            print(f"  {city}: {score:.4f}")


if __name__ == "__main__":
    print("Transit Oriented Development Benchmarking Analysis (dual scoring)")
    print("=" * 70)
    run_scoring_pipeline(use_abs_bounds=False, scoring_name="METHOD 1: RELATIVE SCORING (Min/Max Bounds)")
    run_scoring_pipeline(use_abs_bounds=True, scoring_name="METHOD 2: STANDARD SCORING (Global Bounds)")