import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import variation

# must run oxford_cleaning & putney_cleaning first before analysis can be carried out

ox_a = pd.read_csv("oxford_cleaned.csv")
ox_a = pd.DataFrame(data=ox_a)
ptny_a = pd.read_csv("putney_cleaned.csv")
ptny_a = pd.DataFrame(data=ptny_a)

print("Descriptive stats for cleaned Values Oxford: \n{}".format(ox_a['Value'].describe()), '\n',
      "Descriptive stats for cleaned Values Putney: \n{}".format(ptny_a['Value'].describe()))

# variance of each value from the mean
print(variation(ox_a['Value']))
print(variation(ptny_a['Value']))

# crating new dataframes
ox = pd.DataFrame(data=ox_a, columns=['Site', 'Species', 'SpeciesMeanValue'])
ptny = pd.DataFrame(data=ptny_a, columns=['Site', 'Species', 'SpeciesMeanValue'])

# dropping all duplicate values because the mean for each species has been computed
ox1 = ox.drop_duplicates(['Species'])
ptny1 = ptny.drop_duplicates(['Species'])
print(ox1)


def morning_csv():  # creating new csv for new dataframes
    # ox_time = ox_mrn.app([ox_eve])
    ox1.to_csv('oxford_mean.csv', sep=',', encoding='utf-8')
    ptny1.to_csv('ptny_mean.csv', sep=',', encoding='utf-8')


morning_csv()

plot_results = pd.concat([ox1, ptny1])
sns.factorplot(x="Site", y="SpeciesMeanValue", hue="Species", kind="bar", data=plot_results)
plt.title('Oxford vs Putney')
plt.xlabel('Site')
plt.show()
plt.savefig('ox_v_ptny.png')

print(ox1)
