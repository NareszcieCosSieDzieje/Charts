from __future__ import unicode_literals
import matplotlib.pyplot as plt
import matplotlib

# -*- coding: utf-8 -*-

matplotlib.rc('font', family='DejaVu Sans') #TODO:

def load_data(file_list):
    data_map = dict()
    gen_map = dict()
    for file_name in file_list:
        with open('Resources/' + file_name, 'r') as file:
            next(file)
            big_list = list()
            big_dict = dict()
            for line in file:
                all_data = line.strip('\n').split(',')
                main_data = all_data[1:]
                gens = int(all_data[0])
                for index, item in enumerate(main_data):
                    if index == 0:
                        main_data[index] = int(item)
                    else:
                        main_data[index] = float(item)
                main_data = list((main_data[0], sum(main_data[1:]) / len(main_data[1:])))
                big_dict[main_data[0]] = gens
                #secondary_data = dict(main_data[0], gens )
                big_list.extend(main_data)
                #small_list.extend(secondary_data)
            data_map[file_name] = big_list
            gen_map[file_name] = big_dict
    return data_map, gen_map



file_list = ['rsel.csv','cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']
namz = dict( zip(file_list, ['1-Evol-RS', '1-Coev-Rs', '2-Coev-Rs', '1-Coev', '2-Coev']))
#alg_names = ['2-Coev','2-Coev-RS', '1-Coev', '1-Coev-RS', '1-Evol-RS']
colors = ['blue', 'green', 'red', 'black', 'm']
markerz = ["o","v","D","s","d"]

#alg_file = dict( zip(file_list,alg_names))
alg_colors = dict( zip(file_list,colors))
alg_markers = dict( zip(file_list,markerz))


def main():
    data_map, gen_map = load_data(file_list)
  #  print(data_map)

    chart = plt.figure(figsize=(20, 20)) #TODO:
    chart, ax_lst = plt.subplots(1,2)

    ax2 = ax_lst[0].twiny()

    ax_lst[0].set_xlabel('Rozegranych gier (' + u"\u00D7" + ' 1000)')
    ax_lst[0].set_ylabel('Odsetek wygranych gier [%]')
    #ax_lst[0].set_title("Pokolenie")
    ax_lst[0].set_xlim(0, 500)
    ax_lst[0].set_ylim(60, 100)

    for keys, values in data_map.items():
        # ax_lst[0]\
        ax_lst[0].plot([val / 1000 for val in values[::2]],
                       [val * 100 for val in values[1::2]], alg_colors[keys],
                       marker=alg_markers[keys], label=namz[keys], linewidth=0.7, markersize=5, markevery=25)

    ax_lst[0].legend(loc='lower right', numpoints=2)
    ax_lst[0].grid(b=True, which='major', axis='both', color='grey', linestyle=':',
               linewidth=0.5)  # markever markersize

    ax2.set_xlabel("Pokolenie")
    ax2.set_xlim(0,200)
    epic_gamer_list = [100,200,300,400,500]
    generation_averages = list()
    ax2.set_xticks(epic_gamer_list)
    for index in epic_gamer_list:
        su=0
        for dictionary in gen_map.values():
            for k in range (index*1000 - 1000, 2000*index, 1000):
                try:
                    ge = dictionary[k]
                except KeyError:
                    pass
                else:
                    break
            else:
                ge = None
            su += ge
        su /= len(gen_map.values())
        upper_ticks = int(round(su, -1))
        generation_averages.append(upper_ticks)
    ax2.set_xticklabels(generation_averages) #usrednione pokolenia

    ax_lst[1].yaxis.tick_right()
    ax_lst[1].set_ylim(0.6, 1)

    data = list()
#    for x in ['rsel.csv','cel-rs.csv','2cel-rs.csv','cel.csv','2cel.csv']:
#        data.append(data_map[x][1::2])
    for x in ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']:
        with open('Resources/' + x, 'r') as file:
            lines = file.read().splitlines()
            last_line = lines[-1]
            last_line = last_line.strip('\n').split(',')
            last_line = last_line[2:]
            for index, item in enumerate(last_line):
                last_line[index] = float(item)
            data.append(last_line)

    boxprops = dict(linestyle='-', linewidth=1, color='blue')
    flierprops = dict(marker='+', markeredgecolor='blue', markerfacecolor='None', markersize=6, markeredgewidth=0.7)
    medianprops = dict(linestyle='-.', linewidth=2.5, color='red')
    meanpointprops = dict(marker='o', markeredgecolor='darkblue', markerfacecolor='darkblue')
    whiskerprops = dict(linestyle='--', linewidth=1.0
                        , color='blue')
    bp=ax_lst[1].boxplot(data, notch=True, vert=1, whis=1.5,
                         bootstrap=10000, showmeans=True, whiskerprops=whiskerprops, boxprops=boxprops, flierprops=flierprops, meanprops=meanpointprops, medianprops=medianprops)
    ax_lst[1].grid(b=True, which='major', axis='both', color='grey', linestyle=':',
                   linewidth=0.5)
    ax_lst[1].set_xticklabels( ['1-Evol-RS', '1-Coev-Rs', '2-Coev-Rs', '1-Coev', '2-Coev'], rotation=15, fontsize=9)
    vals = ax_lst[1].get_yticks()
    ax_lst[1].set_yticklabels(['{:.0f}'.format(x*100) for x in vals])
    #plt.tight_layout()
    plt.savefig('Resources/charts.pdf')
    plt.show()



if __name__ == "__main__":
    main()


