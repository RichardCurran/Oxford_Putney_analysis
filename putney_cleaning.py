import pandas as pd

ptny = pd.read_csv("LaqnData_Putney_d.csv")
ptny = pd.DataFrame(ptny)
print(ptny.info())
print(ptny['Site'].unique())  # show what needs to be cleaned in Site column

print("Dataypes: \n{} ".format(ptny.dtypes), '\n')

print("Columns containing NaN values: \n{}".format(ptny.isnull().sum()), '\n')

ptny_species = ptny.groupby('Species').size().reset_index(name='Occurences')
print(ptny_species)  # show number of occurences of each species in dataset as well as errors

ptny['Species'] = ptny['Species'].apply(
    {'CO': 'CO', 'Co': 'CO', 'co': 'CO', 'no': 'NO',
     'NO2': 'NO2', 'NOX': 'NOX', 'NO': 'NO', 'PM10': 'PM10'}.get)
ptny_species = ptny.groupby('Species').size().reset_index(
    name='Occurences')  # check again to see if errors are fixed and correct number of rows still present
ptny['Species'] = ptny['Species'].str.strip()
print(ptny_species)

ptny['Units'] = ptny['Units'].str.strip()

# Units data that must be cleaned

print(ptny.groupby('Units').size().reset_index(name='Occurences'))  # show all the different units
ptny['Units'] = ptny['Units'].str.strip()  # whitespace stripped from units to make cleaning easier
ptny = ptny.dropna()  # understood that dropping null values skew the data
ptny_units = ptny.groupby('Units').size().reset_index(name='Occurences')
print(ptny_units)  # show all units after nulls are dropped. NaN units are now gone as well as mg m-3

# print(ptny['ReadingDateTime'].unique())   #sample of code to show the uniqe values in each column
# useful for spotting some errors

ptny_value = ptny.groupby('Value').size().reset_index(name='Occurences')  # group values from smallest to largest
print('\n', ptny_value.head(20))  # show first 20 of grouped values; finding out if there are negative values
print("\nTotal values = {}".format(len(ptny['Value'])))


def neg():  # count number of negative values
    neg_num = []
    for i in ptny['Value']:
        if i < 0:
            neg_num.append(i)

    print("Total negative values = {}".format(len(neg_num)))


neg()

ptny = ptny[ptny['Value'] >= 0]  # only consider values >= 0. Changing these data to positive would skew the data.
# removing them might also skew the data but since this dataset deals with air quality
# it's better to just filter the negative values out and only use positive values
print("Total values minus the negative values = {}".format(len(ptny['Value'])),
      '\n')  # number of rows in value column minus -ive values

# filtering time data: only data pertaining to his time spent outside in the morning & evening (roughly)
ptny = ptny[
    ptny['ReadingDateTime'].str.contains('08:00|08:15|08:30|08:45|09:00|17:00|17:15|17:30|17:45|18:00|18:15')]


# calculating mean values for each species (values are for the time joe is outside 08:00-9:00, and 17:00-18:00)
def species_mean():
    ptny['SpeciesMeanValue'] = ptny.Species.map(ptny.groupby(['Species']).Value.mean())  # new mean column
    ptny['Site'] = ptny['Site'].replace("WA9", "Putney")  # renaming site to putney for analysis


species_mean()


def morning_csv():  # creating new csv for cleaned data

    ptny.to_csv('putney_cleaned.csv', sep=',', encoding='utf-8')


morning_csv()
# print(ptny['Value'].head(10))  # show values are to same number of significant figures (not as detailed as Oxford
# dataset)
print(ptny.describe())

# Provisional ratified data
print('\n', ptny.groupby('Provisional or Ratified').size())
