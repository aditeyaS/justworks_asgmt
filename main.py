# https://github.com/aditeyaS/justworks_asgmt
# Author: Aditeya Srivastava

# importing modules
import pandas as pd
import os.path

print('NOTE: Make sure the input csv and this program is in the same folder')
print('Enter the name of csv file')
input_csv_name = input()
input_csv_name = input_csv_name if input_csv_name.endswith('.csv') else input_csv_name+'.csv'

# flag for successful csv reading
is_csv_read = False

if(os.path.exists(input_csv_name)):
    try:
        # reading csv (with no header) and skipping empty lines
        input_csv = pd.read_csv(input_csv_name, skip_blank_lines=True, header=None)
        # dropping rows which have empty columns
        input_csv.dropna(inplace=True)
        # formatting the date
        input_csv[1] = pd.to_datetime(input_csv[1], format="%m/%d/%Y")
        # changing flag
        is_csv_read = True

    except pd.errors.EmptyDataError:
        print(f"{input_csv_name} is empty")

else:
    print("No such file found")

if is_csv_read:
    # creating data frame to store the result
    result_df = pd.DataFrame(columns=['CustomerID', 'MM/YYYY', 'MinBalance', 'MaxBalance', 'EndingBalance'])
    # extracting all unique customer ID's
    customer_id_list = input_csv[0].unique()

    for customer_id in customer_id_list:
        # selecting all the data for a particular customer ID
        customer_data = input_csv[input_csv[0] == customer_id]

        # adding multiple transactions on same date
        agg_function = {0: 'first', 2: 'sum'}
        customer_data = customer_data.groupby(customer_data[1], as_index=False).aggregate(agg_function)
        
        # extracting unique year
        year = customer_data[1].dt.year.unique()
        year.sort()

        for y in year:
            # selecting all data of that year
            customer_year_data = customer_data[customer_data[1].dt.year == y]

            # extracting unique months
            months = customer_year_data[1].dt.month.unique()
            months.sort()

            for m in months:
                # selecting all data of that month
                customer_month_data = customer_year_data[customer_year_data[1].dt.month == m]

                # calculating mix, max, and total
                min = 999999
                max = -999999
                total = 0
                for _, row in customer_month_data.iterrows():
                    total += row[2]
                    if total > max: max = total
                    if total < min: min = total
                
                # converting float to integer if decimal value is 0
                # eg. 3.0 will become 3
                if type(min) == float and (min).is_integer(): min = int(min)
                if type(max) == float and (max).is_integer(): max = int(max)
                if type(total) == float and (total).is_integer(): total = int(total)

                #creating the list
                month_row = [
                    customer_id,
                    f'{m}/{y}',
                    min,
                    max,
                    total,
                ]
                # adding list to the output dataframe
                result_df.loc[len(result_df)] = month_row
    
    # generating output file name
    output_file_name = "output.csv"
    if(os.path.exists(output_file_name)):
        i = 1
        while True:
            output_file_name = f'output_{i}.csv'
            i = i+1
            if (not os.path.exists(output_file_name)):
                break
    
    # writing output data frame to the file
    result_df.to_csv(output_file_name, index=False)
    print(f'Output generated: {output_file_name}')

else:
    print("Some error occcoured while reading the csv")