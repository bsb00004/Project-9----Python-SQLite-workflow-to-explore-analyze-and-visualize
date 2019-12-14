#!/usr/bin/env python
# coding: utf-8

# Project 9 -- Python SQLite workflow to explore, analyze, and visualize

# ### Introduction 
# In this project, we'll work with data from the CIA World Factbook, 
# a compendium of statistics about all of the countries on Earth. 
# The Factbook contains demographic information like:

# - __population__ - The population as of 2015.
# - __population_growth__ - The annual population growth rate, as a percentage.
# - __area__ - The total land and water area.

# importing SQLite & pandas
import sqlite3
import pandas as pd

# connecting the database to SQLite
conn = sqlite3.connect("factbook.db")
q1 = "SELECT * FROM sqlite_master WHERE type='table';"
# Ceated an instance 
cursor = conn.cursor()
# execute and fecth the database
cursor.execute(q1).fetchall()

# But we are uisng pandas and matplotlib to display results neatly and visualize them 
# because they let us focus on practicing thinking and working in SQL.

# reading into the pandas dataframe and 
# to return information on the tables in the database.
pd.read_sql_query(q1, conn)

#Ruing a query that returns the first 5 rows of the facts table in the database.
q2 = "select * from facts limit 5"
#  to return information on the tables in the database.
pd.read_sql_query(q2, conn)

# ### Summary Statistics
# Let's start by calculating some summary statistics and look for any outlier countries.

# Writing a single query that returns the:

# - Minimum population
# - Maximum population
# - Minimum population growth
# - Maximum population growth

# a single query minimum population 
q3 = '''
select min(population) min_pop, max(population) max_pop, 
min(population_growth) min_pop_grwth, max(population_growth) max_pop_grwth 
from facts
'''
pd.read_sql_query(q3, conn)

# ### Outliers
# Let's zoom in on just these countries.

# - Writing a query that returns the countrie(s) with a population of 7256490011.
q4 = '''
select *
from facts
where population == (select max(population) from facts);
'''
pd.read_sql_query(q4, conn)


# - Write a query that returns the countrie(s) with a population of 0.
q5 = '''
select *
from facts
where population == (select min(population) from facts);
'''
pd.read_sql_query(q5, conn)

# ### Histograms
# Let's move on to generating histograms for the rest of the countries in the table, ignoring these 2 rows. 
# We want to write a query that returns all of the values in the columns we want to visualize.

# Using just the non-outlier rows, generate a 2 by 2 grid of histograms for the following columns: 
# - population
# - population_growth
# - birth_rate
# - death_rate

q6 = '''
select population, population_growth, birth_rate, death_rate
from facts
where population != (select max(population) from facts)
and population != (select min(population) from facts);
'''
pd.read_sql_query(q6, conn)

import matplotlib.pyplot as plt
import seaborn as sns
# using for juypter notebook
get_ipython().magic('matplotlib inline')

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

# generating histograms
pd.read_sql_query(q6, conn).hist(ax=ax)


### Which countries have the highest population density?
q7 = "select name, cast(population as float)/cast(area as float) density from facts order by density desc limit 20"
pd.read_sql_query(q7, conn)


### histogram of population densities
fig1 = plt.figure(figsize=(10,5))
ax1 = fig1.add_subplot(111)
ax1.set_ylabel('name')
ax1.set_xlabel('density')
pd.read_sql_query(q7, conn).hist(ax=ax1)
