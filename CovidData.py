import csv

"""Creates an list of rolling 7 day averages for plotting

    Args:
        filename: name of csv file you would like to read

    Returns:
         A list of covid case numbers."""


def get_avg_daily_cases(file_name):
    avg = []
    count = 0
    my_sum = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        is_first = 1
        for row in csv_reader:
            if is_first:
                is_first ^= 1
            else:
                count += 1
                if not row[1].isnumeric():
                    break
                my_sum += int(row[1])
                if count == 7:
                    avg.append(my_sum / 7)
                    count = 0
                    my_sum = 0

    with open("UScovidAVG.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["cases"])
        for num in avg:
            writer.writerow([int(num)])


get_avg_daily_cases("us.csv")
