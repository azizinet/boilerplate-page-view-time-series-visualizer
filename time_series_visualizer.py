import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as nppip
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter
from calendar import month_name, month_abbr
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date', parse_dates = True)
# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(1,1, figsize = (30,10))
    df.plot(ax = ax, fontsize = 20, legend = False, lw = 3)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize = 25)
    ax.set_xlabel("Date", fontsize = 20)
    ax.set_ylabel("Page Views", fontsize = 20)
    plt.xticks(rotation = 0)
    fmt = DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(fmt)
    fig.tight_layout(pad = 4)


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().groupby(pd.Grouper(freq = "M", axis = 0)).sum()
    df_bar = pd.pivot_table(data = df_bar, index = df_bar.index.year, columns = df_bar.index.month, values = 'value')
    df_bar.columns = month_name[1:]

    # Draw bar plot
    fig, ax = plt.subplots(1,1, figsize = (20,10))
    df_bar.plot.bar(ax = ax, fontsize = 15)
    ax.set_xlabel("Years", fontsize = 20)
    ax.set_ylabel("Average Page Views", fontsize = 20)
    plt.legend(loc = 2, fontsize = 15)
    ax.ticklabel_format(style = 'plain', axis = 'y')
    fig.tight_layout(pad = 4)
    

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2, figsize = (30,10))
    sns.boxplot(data = df_box, x = 'year', hue = 'year', y = 'value', legend = False, palette = "Set1", ax = ax[0])
    sns.boxplot(data = df_box, x = 'month', hue = 'month', y = 'value', order = month_abbr[1:], legend = False, ax = ax[1])
    sns.set_theme(font_scale = 2, style = 'white')
    ax[0].set_xlabel("Year", fontsize = 20)
    ax[0].set_title("Year-wise Box Plot (Trend)", fontsize = 20)
    ax[0].set_ylabel("Page Views", fontsize = 20)
    ax[1].set_xlabel("Month", fontsize = 20)
    ax[1].set_title("Month-wise Box Plot (Seasonality)", fontsize = 20)
    ax[1].set_ylabel("Page Views", fontsize = 20)
    fig.tight_layout(pad = 4)


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig