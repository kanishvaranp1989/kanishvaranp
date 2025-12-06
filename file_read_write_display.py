import csv


def display_records():
    #read extracted file for given sku/product id
    column_values = []
    with open('to_constructor_save.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:            
            format_str=f"column header:{'column_header'}']"
            column_values.append(format_str) # is a column header
            print(format_str)
    return column_values
            

def search_in_csv_file(inputfilename,search_str,i):
    print(f"{inputfilename}, {search_str}")
    if not inputfilename or not search_str:
        print("filename and search string to be provided!!")
        return False
    data1=open(inputfilename)
    csv_reader=csv.reader(data1)
    data_lines=list(csv_reader)    
    full_names=[]
    for data in data_lines:
        if search_str in data:
            full_names.append(data)

    #write records to file to_save.csv
    file_to_output=open("to_save.csv",mode='a',newline='')
    csv_writer=csv.writer(file_to_output,delimiter=",")
    if i==0:#taking first row column
        csv_writer.writerow(data_lines[0])
    csv_writer.writerows(full_names)
    file_to_output.close()
    return full_names

#list of strings
search_str=['name','age']
for i in search_str:
    search_in_csv_file("filename.csv",search_str[i],i)
print("Searched string written in to_save.csv")
display_records()