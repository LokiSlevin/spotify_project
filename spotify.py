

# Libraries

import pandas as pd
import scipy.stats as st
from scipy.stats import normaltest
import numpy as np
import matplotlib.pyplot as plt

# reading original dataset

spotify = pd.read_excel('/users/olhapopova/Downloads/spotify_genre_final.xlsx')

# let's take a look what genres we have

genres = spotify['Genre'].unique()

# i want to sort original dataset
# i will extract all info only about genres rock and pop
# and will create data frames for each genre i am interested in

rock = spotify[spotify.Genre == 'rock']
pop = spotify[spotify.Genre == 'pop']

# next step - i have duration of songs in milliseconds
# i will convert duration of songs into minutes and add it as a column to genre dataframes

rock['duration_min'] = round(rock['duration_ms'] / 60000, 2)
pop['duration_min'] = round(pop['duration_ms'] / 60000, 2)

# I want to take a look to the average duration of the songs of my rock and pop samples

avg_rock = rock['duration_min'].mean()
print('the average duration of the rock song is: ', round(avg_rock, 2))

avg_pop = pop['duration_min'].mean()
print('the average duration of the pop song is: ', round(avg_pop, 2))

# Hypothesis testing

# I have a hypothesis, that the average duration of rock songs is longer, 
# than the average duration of pop songs. 
# Let's test it.

# h0: avg duration rock < avg duration pop
# h1: avg duration rock > avg duration pop

duration_rock = rock['duration_min']
duration_pop = pop['duration_min']

ttest = st.ttest_ind(duration_rock, duration_pop, equal_var = False)
a = 1 - 0.95
p_value = ttest[1]

a > p_value

# So i can reject the h0 so avg duration of rock songs is not smaller than
# avg duration of pop songs. 
# But also I would like to see the confidence interval 

# Confidance intervals of my rock and pop samples

# create 90% confidence interval for rock and pop samples
rock90 = st.norm.interval(alpha = 0.9, 
                 loc = np.mean(rock['duration_min']), 
                 scale = st.sem(rock['duration_min']))

pop90 = st.norm.interval(alpha = 0.9, 
                 loc = np.mean(pop['duration_min']), 
                 scale = st.sem(pop['duration_min']))

print('90% confidence that the avg duration of rock song: ', 
      round(rock90[0], 2), ',', round(rock90[1], 2))
print('90% confidence that the avg duration of rock song: ',
      round(pop90[0], 2), ',', round(pop90[1], 2))

# create 95% confidence interval for rock and pop samples
rock95 = st.norm.interval(alpha = 0.95, 
                 loc = np.mean(rock['duration_min']), 
                 scale = st.sem(rock['duration_min']))

pop95 = st.norm.interval(alpha = 0.95, 
                 loc = np.mean(pop['duration_min']), 
                 scale = st.sem(pop['duration_min']))

print('95% confidence that the avg duration of rock song: ',
      round(rock95[0], 2), ',', round(rock95[1], 2))
print('95% confidence that the avg duration of rock song: ', 
      round(pop95[0], 2), ',', round(pop95[1], 2))

# create 99% confidence interval for rock and pop samples
rock99 = st.norm.interval(alpha = 0.99, 
                 loc = np.mean(rock['duration_min']), 
                 scale = st.sem(rock['duration_min']))

pop99 = st.norm.interval(alpha = 0.99, 
                 loc = np.mean(pop['duration_min']), 
                 scale = st.sem(pop['duration_min']))

print('99% confidence that the avg duration of rock song: ', 
      round(rock99[0], 2), ',', round(rock99[1], 2))
print('99% confidence that the avg duration of rock song: ',
      round(pop99[0], 2), ',', round(pop99[1], 2))

# Let's take a look on distribution of duration songs oboth genres we are interested in

f, (a1, a2) = plt.subplots(nrows = 1, ncols = 2)
a1.hist(rock['duration_min'], color = '#afd6ad')
a2.hist(pop['duration_min'], color = '#ffd099')
a1.set_title('duration of rock')
a1.set_xlabel('mins')
a1.set_ylabel('songs in sample')
a2.set_title('duration of pop')
a2.set_xlabel('mins')
plt.show()

# I can't easily say what kind of distribution it is, 
# but i want to belive, that my sample follows a normal distribution
# So i want to test it

# i alredy calculate mean and saved it in variables avg_rock and avg_pop
# but also need a standard deviation of my samples

# normality test for rock sample
stat_rock, p_rock = normaltest(rock['duration_min'])
print('Rock sample: ', 'Statistics=%.3f, p=%.3f' % (stat_rock, p_rock))

# interpret
alpha = 0.05
if p_rock > alpha:
	print('Rock sample looks Normal')
else:
	print('Rock sample does not look Normal')
 
# normality test for pop sample
stat_pop, p_pop = normaltest(pop['duration_min'])
print('Pop sample: ', 'Statistics=%.3f, p=%.3f' % (stat_pop, p_pop))

# interpret
if p_pop > alpha:
	print('Pop sample looks Normal')
else:
	print('Pop sample does not look Normal')
    
# So my hypothesis was rejected and duration of songs is not a normal distribution
# If it is not normal - i want to see the skewness

rock_skew = st.skew(rock['duration_min'])
pop_skew = st.skew(pop['duration_min'])

if -0.5 > rock_skew and rock_skew < 0.5:
  print('rock data are fairly symmetrical') 
elif -1 > rock_skew and rock_skew < -0.5:
  print('rock data are moderately skewed')
elif 0.5 > rock_skew and rock_skew < 1:
  print('rock data are moderately skewed')
else:  
  print('rock data are highly skewed')

if rock_skew > 0:
  print('rock data has skewed to the left')
else:
   print('rock data skewed to the right')

if -0.5 > pop_skew and pop_skew < 0.5:
  print('pop data are fairly symmetrical') 
elif -1 > pop_skew and pop_skew < -0.5:
  print('pop data are moderately skewed')
elif 0.5 > pop_skew and pop_skew < 1:
  print('pop data are moderately skewed')
else:  
  print('pop data are highly skewed')

if pop_skew > 0:
  print('pop data has skewed to the left')
else:
   print('pop data skewed to the right')
   
# Let's take a look how popular the genres are

avg_p_rock = rock['popularity'].mean()
avg_p_pop = pop['popularity'].mean()

print('average popularity of rock music is: ', round(avg_p_rock, 2))
print('average popularity of pop music is: ', round(avg_p_pop, 2))

# Hypothesis testing

# I have a hypothesis, that the pop music is more popular than rock 
# Let's test it.

# h0: avg popularity pop < avg popularity rock
# h1: avg popularity pop > avg popularity rock

rock_popularity = rock['popularity']
pop_popularity = pop['popularity']

ttest = st.ttest_ind(pop_popularity, rock_popularity, equal_var = False)
a = 1 - 0.95
p_value = ttest[1]

a > p_value

# So i can reject the h0 
# But let's take a look if the duration of song have any relationship with popularity 

spotify['duration_min'] = round(spotify['duration_ms'] / 60000, 2)

corr_poptomin = spotify[['duration_min', 'popularity']].corr()
corr_poptomin

# Our correlation all over the sample, no matter of genre, 
# gave us a hint, that it is true - as longer the song is, as less popular it is
# but correlation -0.12 still is too small to say, that the duration of the song
# realy afects the popularity

# That's why i want to take a look on correlation all over the charachteristics
# and see if anything else afects popularity

spotify.corr()

# actually, there is no strong correlation between any of characteristic and popularity
# so we will accept the fact, that duration of the song can be a reason, but not the only

# also correlation all over the dataset gave us an idea about some other relationships:
# explicit and speechiness
# energy and loudness
# energy and acousticness (negative)

# but non of them a significant enough (less than 0.8)

# I would like to calculate popularity of every genre and see what is the most popular

spotify.groupby(['Genre'])['popularity'].mean().sort_values(ascending = False)