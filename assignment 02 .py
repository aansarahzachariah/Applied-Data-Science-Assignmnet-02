import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read and clean World Bank data
def read_world_bank_data(filename):
    
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(filename, index_col=['Country Name', 'Indicator Name'])

    # Drop unnecessary columns and rows
    df = df.drop(columns=['Country Code', 'Indicator Code'])

    # Convert data types
    df = df.apply(pd.to_numeric, errors='coerce')

    # Fill NaN values
    df = df.fillna(method='ffill', axis=0).fillna(method='bfill', axis=0)

    df = df.reset_index()
   
    
    # extract the years as columns
    df_years = df.filter(regex='^\\d{4}$')
    
    print("years as columns",df_years)
   
    # extract the countries as columns
    df_countries = df.drop(df_years.columns, axis=1)
    
    print("Contries as columns",df_countries)
    
    return df



# Load World Bank data and clean it
filename = 'Assignment file.csv'
df = read_world_bank_data(filename)

# Select indicators to analyze
co2_emissions = 'CO2 emissions (metric tons per capita)'
renewable_energy = 'Renewable energy consumption (% of total final energy consumption)'
forest_area = 'Forest area (% of land area)'
Population_growth ='Population growth (annual %)'
energy_consumption = 'Electric power consumption (kWh per capita)'
# Calculate summary statistics for selected indicators
co2_stats = df[df['Indicator Name'] == co2_emissions]
re_stats = df[df['Indicator Name'] == renewable_energy]
forest_stats = df[df['Indicator Name'] == forest_area]
population_stats= df[df['Indicator Name'] == Population_growth]
energy_stats = df[df['Indicator Name'] == energy_consumption ]

# Print summary statistics
print('CO2 emissions statistics:')
print(co2_stats.describe())
print('\nRenewable energy consumption statistics:')
print(re_stats.describe())
print('\nForest area statistics:')
print(forest_stats.describe())

# # Plot time-series graphs for selected countries and regions
countries = ['China', 'United States', 'India', 'Brazil']

for country in countries:
    co2_stats_temp = df[df['Country Name'] == country]
    co_stats_temp = co2_stats_temp.describe()
    co2_stats_temp.plot(label=country,legend=False)  
    plt.title('CO2 emissions over time for selected countries')
    plt.xlabel('Year')
    plt.ylabel('CO2 emissions (metric tons per capita)')
    plt.show()

# Calculate correlations between selected indicators and additional population growth and energy consumption
combined_df = pd.concat([co2_stats.describe(), re_stats.describe(), forest_stats.describe()])
combine_df = pd.concat([population_stats.describe(), energy_stats.describe()])
# compute the correlation matrix using the corr() method
correlation_matrix = combined_df.corr()
correlation_matrix2 = combine_df.corr()

# Print correlation matrix
print('Correlation matrix:')
print(correlation_matrix)
print('Correlation between population growth and energy stats')
print(correlation_matrix2)
# # Plot scatter plots of selected indicators
plt.scatter(re_stats.describe(), co2_stats.describe())
plt.title('Renewable energy consumption vs CO2 emissions')
plt.xlabel('Renewable energy consumption (% of total final energy consumption)')
plt.ylabel('CO2 emissions (metric tons per capita)')
plt.show()

plt.scatter(re_stats.describe(), forest_stats.describe())
plt.title('Renewable energy consumption vs forest area')
plt.xlabel('Renewable energy consumption (% of total final energy consumption)')
plt.ylabel('Forest area (% of land area)')
plt.show()

# visualize the correlation matrix for each indicator for each country using a heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
