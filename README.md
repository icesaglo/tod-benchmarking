# Global Benchmarking of Transit-Oriented Developments

This repository contains the spatial data and Python algorithms used for the final year project: **Global Benchmarking of Transit-Oriented Developments: A Data-Driven Framework for Sustainable Urban Investment** at Imperial College London.

## Project Overview
This study develops a quantitative framework to measure the performance and market resilience of Transit-Oriented Developments (TOD) across London, Hong Kong, and Singapore. By analysing the topological centrality of public transport networks and integrating it with local commercial data, the algorithms isolate the specific transport corridors that successfully convert physical connectivity into sustained economic demand.

## Repository Structure

### Data Files
* `raw_benchmarking_data.xlsx`: The complete citywide spatial and economic dataset.
* **London:** `london_station_nodes.csv` and `london_network_links.csv` detailing the topological connections of the London Underground.
* **Hong Kong:** `hk_mtr_data.csv` containing the spatial and network data for the MTR network.
* **Singapore:** `sg_mrt_data.zip` containing the compressed spatial data for the MRT network.

### Analytical Scripts
* `london_centrality.py`: Calculates network centrality metrics for the London Underground.
* `hk_centrality.py`: Calculates network centrality metrics for the Hong Kong MTR.
* `sg_centrality.py`: Calculates network centrality metrics for the Singapore MRT.
* `benchmarking_analysis.py`: The final algorithm that integrates the centrality scores with economic indicators to generate the benchmarking scorecard.

## Requirements
To execute these scripts, ensure Python 3.x is installed along with the following libraries:
* pandas
* networkx
* openpyxl

## Usage
1. **Data Preparation:** Extract the contents of `sg_mrt_data.zip` into the main repository folder.
2. **Topological Analysis:** Execute the centrality scripts for each respective city (`london_centrality.py`, `hk_centrality.py`, `sg_centrality.py`) to generate the required network metrics.
3. **Benchmarking:** Finally, run `benchmarking_analysis.py` to process the combined dataset and produce the final benchmarking scorecard outputs.

## Author
**Isaac Lo**
Department of Civil and Environmental Engineering
Imperial College London

## Acknowledgements
Generative AI tools were used to refine and polish the computational code structure in this repository.
