
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("unpaid_work.csv")

print("DATASET OVERVIEW")
print("----------------")
print(df.head())

print("\nDataset Information")
df.info()

print("\nStatistical Summary")
print(df.describe())

print("\nNumber of Countries:")
print(df["Country Name"].nunique())

print("\nGender Categories:")
print(df["Disaggregation"].unique())

print("\nRecords per Gender:")
print(df["Disaggregation"].value_counts())

comparison = df.pivot_table(
    index=["Country Name", "Year"],
    columns="Disaggregation",
    values="Value"
).dropna()

average = comparison[["female", "male"]].mean()

print("\nAverage Unpaid Work by Gender:")
print(average)

country_avg = comparison.groupby("Country Name")[["female", "male"]].mean()

country_avg["Gender Gap"] = country_avg["female"] - country_avg["male"]

print("\nTop 10 Countries with Highest Gender Gap:")
print(country_avg.sort_values("Gender Gap", ascending=False).head(10))


# CHART 1: Gender-wise comparison

plt.figure(figsize=(8, 5))

bars = plt.bar(
    ["Female", "Male"],
    average.values,
    color=["#E69A45", "#4A90C2"]
)

plt.title("Average Unpaid Domestic and Care Work by Gender")
plt.xlabel("Gender")
plt.ylabel("Time Spent (% of 24-hour day)")

plt.bar_label(bars, fmt="%.2f%%", padding=4)

plt.tight_layout()
plt.savefig("chart1_gender_comparison.png", dpi=300)
plt.show()


# CHART 2: Country-wise comparison

country_plot = country_avg[["female", "male"]].sort_values(
    "female", ascending=False
)

ax = country_plot.plot(
    kind="bar",
    figsize=(14, 6),
    color=["#E69A45", "#4A90C2"],
    width=0.8
)

ax.set_title("Country-wise Unpaid Domestic and Care Work by Gender")
ax.set_xlabel("Country")
ax.set_ylabel("Average Time Spent (% of 24-hour day)")
ax.legend(["Female", "Male"], title="Gender")
ax.tick_params(axis="x", rotation=60)

plt.tight_layout()
plt.savefig("chart2_country_comparison.png", dpi=300)
plt.show()


# CHART 3: Histogram

plt.figure(figsize=(9, 5))

plt.hist(
    df["Value"],
    bins=10,
    color="#8E7CC3",
    edgecolor="black"
)

plt.title("Distribution of Unpaid Domestic and Care Work")
plt.xlabel("Time Spent (% of 24-hour day)")
plt.ylabel("Number of Records")

plt.tight_layout()
plt.savefig("chart3_distribution.png", dpi=300)
plt.show()


# CHART 4: Gender gap by country

top_countries = country_avg.sort_values(
    "Gender Gap", ascending=False
).head(10)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    top_countries.index,
    top_countries["Gender Gap"],
    color="#6A9C89"
)

plt.title("Top 10 Countries with Highest Gender Gap")
plt.xlabel("Country")
plt.ylabel("Difference in Time Spent (percentage points)")
plt.xticks(rotation=45, ha="right")

plt.bar_label(bars, fmt="%.2f", padding=3)

plt.tight_layout()
plt.savefig("chart4_gender_gap.png", dpi=300)
plt.show()

print("\nAll four charts saved successfully!")
