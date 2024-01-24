import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('presents.csv')

# Process the 'reviews' column values
df['reviews'] = df['reviews'].replace(to_replace=r'^(\d+)k$', value=r'\1', regex=True)  # Replace 'k' with 1000
df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')  # Convert to numeric, NaN for non-convertible values

# Convert 'price' column to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to numeric, NaN for non-convertible values

# Drop rows with NaN values
df = df.dropna(subset=['reviews'])

# Calculate average reviews
average_reviews = df['reviews'].mean()

# Extract information for the product with the highest price
max_price_product = df.loc[df['price'].idxmax()]

# Extract information for the best product based on price and ratings
best_product = df.loc[(df['price'] / df['reviews']).idxmax()]

# Shorten product names to one-third of their original length
max_price_product_title_shortened = max_price_product['title'][:int(len(max_price_product['title']) / 3)]
best_product_title_shortened = best_product['title'][:int(len(best_product['title']) / 3)]

# Create the plot
fig, ax1 = plt.subplots()

# First y-axis (left)
color = 'tab:red'
ax1.set_xlabel('Categories')
ax1.set_ylabel('Price', color=color)
bars1 = ax1.bar(['Average Reviews', 'Max Price Product', 'Best Product'], [average_reviews, max_price_product['price'], best_product['price']], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Display values for the high-priced product
for bar in bars1:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', color=color, fontweight='bold')

# Second y-axis (right)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Reviews', color=color)
bars2 = ax2.bar(['Average Reviews'], [average_reviews], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Display values for reviews
for bar in bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', color=color, fontweight='bold')

# Add product names to the x-axis
ax1.set_xticks(['Average Reviews', 'Max Price Product', 'Best Product'])
ax1.set_xticklabels(['Average Reviews', f'Max Price Product{max_price_product_title_shortened}', f'Best Product\n{best_product_title_shortened}'])

# Adjust for more space
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

plt.title('Product Information')
plt.savefig('output.png')
plt.show()

# Print the results
print(f'Average Reviews: {average_reviews}')
print(f'Max Price Product: Name - {max_price_product_title_shortened}, Price - {max_price_product["price"]}, Rating - {max_price_product["reviews"]}')
print(f'Best Product: Name - {best_product_title_shortened}, Price - {best_product["price"]}, Rating - {best_product["reviews"]}')
