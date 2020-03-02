import pandas as pd

ox = pd.read_csv("LaqnData_OxfordRd.csv")
ox = pd.DataFrame(ox)

print("Dataypes: \n{} ".format(ox.dtypes), '\n')

print("Columns containing NaN values: \n{}".format(ox.isnull().sum()), '\n')

# print(np.mean(ox['Value']))

ox_species = ox.groupby('Species').size().reset_index(
    name='Occurences')  # show all species and how many time each occur
print("The different species in Oxford: \n {} ".format(ox_species), '\n')
print(ox['Units'].unique())  # show any whitespace or mispelling
ox['Units'] = ox['Units'].apply(
    {'ug m -3 as NO 2': 'ug m-3 as NO2', 'ug m-3': 'ug m-3', 'ug m-3 as NO2': 'ug m-3 as NO2', 'ug/m3': 'ug/m3',
     'ug m-3 as NO 2': 'ug m-3 as NO2'}.get)  # correcting the units
ox = ox.dropna()  # this man might not care about NaN values but only measured values. (Assumption)
# I understand this will skew the data beacuse i am dropping ~40000 data

ox['Units'] = ox['Units'].str.strip()
print(ox['Units'].unique())  # show corrected units
ox_value = ox.groupby('Value').size().reset_index(name='Occurences')  # group values from smallest to largest
print('\n', ox_value.head(20))
print("\nTotal values = {}".format(len(ox['Value'])))  # how many rows in value column


def neg():  # count number of negative values
    neg_num = []
    for i in ox['Value']:
        if i < 0:
            neg_num.append(i)

    print("Total negative values = {}".format(len(neg_num)))


neg()
# removing negative values
ox = ox[ox['Value'] >= 0]  # only consider values >= 0
print("Total values minus the negative values = {}".format(len(ox['Value'])),
      '\n')  # number of rows in value column minus -ive values

# print(ox['ReadingDateTime'].head(10))  # sample of datetime data


# filtering time data: only data pertaining to his time spent outside in the morning & evening (roughly)
ox = ox[ox['ReadingDateTime'].str.contains('08:00|08:15|08:30|08:45|09:00|17:00|17:15|17:30|17:45|18:00|18:15')]


# ox_eve = ox[ox['ReadingDateTime'].str.contains('17:00|17:15|17:30|17:45|18:00|18:15')]
# print(ox_eve['ReadingDateTime'].head(30)) #sample of new df
# ox_total = ox_mrn.append([ox_eve])

# calculating mean values for each species (values are for the time joe is outside 08:00 -9:00, and 17:00-18:00)
def species_mean():
    ox['SpeciesMeanValue'] = ox.Species.map(ox.groupby(['Species']).Value.mean())  # new mean column
    ox['Site'] = ox['Site'].replace('WM6', "Oxford")


species_mean()


mean_ox = ox['Value'].groupby(ox['Species'])
print(mean_ox)


def morning_csv():  # creating new csv for cleaned data
    # ox_time = ox_mrn.app([ox_eve])
    ox.to_csv('oxford_cleaned.csv', sep=',', encoding='utf-8')


morning_csv()
# print(ox['ReadingDateTime'].head(10))  # show values are to same number of significant figures

# Provisional ratified data
print('\n', ox.groupby('Provisional or Ratified').size())
