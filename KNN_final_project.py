import pandas as pd
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import csv
import matplotlib.pyplot as plt


class Gui:
    def __init__(self):
        self.bg_color = "azure"
        self.font_color = "navy"
        self.table_column_color = "deep pink"
        self.table_element = "purple"
        self.window = root
        self.window.minsize(600, 600)
        self.window.title("K-Nearest Neighbours")
        self.window.configure(bg=self.bg_color)
        self.k_entry = tk.IntVar()
        self.test_type = tk.IntVar()
        self.prepared = False
        self.random = False
        self.table_elements = []

        self.frame = tk.Frame(self.window, width=500, height=500, background= self.bg_color)
        self.frame.grid(column=0, row=0)

        self.age = tk.IntVar()
        self.bmi = tk.DoubleVar()
        self.children = tk.IntVar()
        self.train, self.test = prepare_data_set("insurance.csv")
        self.fresh_window()

    def fresh_window(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.window, width=600, height=600, background=self.bg_color)
        self.frame.grid(column=0, row=0)
        k_label = tk.Label(self.frame, text="K Value: ", font='Calibri 12 bold', bg=self.bg_color, fg=self.font_color)
        k_label.grid(column=0, row=0)
        entry1 = tk.Entry(self.frame, textvariable=self.k_entry, bg=self.bg_color)
        entry1.grid(column=1, row=0)

        k_label = tk.Label(self.frame, text="Test Sample ", font='Calibri 12 bold', bg=self.bg_color, fg=self.font_color)
        k_label.grid(column=0, row=1)
        random = tk.Radiobutton(self.frame, text='Random from Data Set', variable=self.test_type,
                                command=self.random_sample, value=0, bg=self.bg_color).grid(column=1, row=1,
                                                                                            sticky='w')
        ui = tk.Radiobutton(self.frame, text='User Input', variable=self.test_type, command=self.prepare_sample,
                            value=1, bg=self.bg_color).grid(column=2, row=1, sticky='e')
        self.knn_button = tk.Button(self.frame, text='Find Nearest Neighbours', command=self.find_nearest_neighbours,
                           font='Calibri 11 bold', bg="MediumPurple1", fg="MediumPurple4")
        self.knn_button.grid(column=2, row=4)
        self.retry_button = tk.Button(self.frame, text='Retry', font='Calibri 11 bold', command=self.fresh_window,
                                      bg="light blue", fg="gray")
        self.retry_button.grid(column=1, row=4, sticky="nsew")
        return

    def random_sample(self):
        self.fresh_window()
        if self.prepared:
            self.forget_preparation()
        if self.random:
            self.forget_random()

        self.knn_button.grid(column=2, row=4)
        self.retry_button.grid(column=1, row=4, sticky="nsew")

        self.test_sample = self.test.sample()
        self.random = True
        self.label1 = tk.Label(self.frame, text="Age", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.label1.grid(row=2, column=0)
        self.label2 = tk.Label(self.frame, text=str(self.test_sample['age']).split("    ")[1].split("\n")[0]
                               , font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        self.label2.grid(row=3, column=0)
        self.label3 = tk.Label(self.frame, text="Sex", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.label3.grid(row=2, column=1)
        if str(self.test_sample['sex']).split("    ")[1].split("\n")[0] == '0':
            self.label4 = tk.Label(self.frame, text="Female",
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        else:
            self.label4 = tk.Label(self.frame, text="Male",
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        self.label4.grid(row=3, column=1)
        self.label5 = tk.Label(self.frame, text="BMI", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.label5.grid(row=2, column=2)
        self.label6 = tk.Label(self.frame, text="%.2f" % float(str(self.test_sample['bmi']).split("    ")[1].split("\n")[0]),
                               font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        self.label6.grid(row=3, column=2)
        self.label7 = tk.Label(self.frame, text="Children", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.label7.grid(row=2, column=3)
        self.label8 = tk.Label(self.frame, text=str(self.test_sample['children']).split("    ")[1].split("\n")[0],
                               font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        self.label8.grid(row=3, column=3)
        self.label9 = tk.Label(self.frame, text="Smoker", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.label9.grid(row=2, column=4)
        if str(self.test_sample['smoker']).split("    ")[1].split("\n")[0] == '0':
            self.label10 = tk.Label(self.frame, text="No",
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        elif str(self.test_sample['smoker']).split("    ")[1].split("\n")[0] == '3':
            self.label10 = tk.Label(self.frame, text="Yes",
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
        self.label10.grid(row=3, column=4)

    def prepare_sample(self):
        self.fresh_window()
        if self.random:
            self.forget_random()
        self.prepared = True
        self.knn_button.grid(column=5, row=4)
        self.retry_button.grid(column=3, row=4)

        self.age1 = tk.Label(self.frame, text="Age:", font='Calibri 12', bg=self.bg_color)
        self.age1.grid(column=0, row=2)
        self.entry1 = tk.Entry(self.frame, textvariable=self.age)
        self.entry1.grid(column=1, row=2, padx=0)
        self.sex1 = tk.Label(self.frame, text="Sex:", font='Calibri 12', bg=self.bg_color)
        self.sex1.grid(column=2, row=2)
        self.sex_combobox = ttk.Combobox(self.frame, values=['Female', 'Male'])
        self.sex_combobox.grid(column=3, row=2, padx=0)
        self.bmi2 = tk.Label(self.frame, text="BMI:", font='Calibri 12', bg=self.bg_color)
        self.bmi2.grid(column=4, row=2)
        self.entry2 = tk.Entry(self.frame, textvariable=self.bmi)
        self.entry2.grid(column=5, row=2, padx=0)
        self.child3 = tk.Label(self.frame, text="Children:", font='Calibri 12', bg=self.bg_color)
        self.child3.grid(column=6, row=2)
        self.entry3 = tk.Entry(self.frame, textvariable=self.children)
        self.entry3.grid(column=7, row=2, padx=0)
        self.smoker1 = tk.Label(self.frame, text="Smoker:", font='Calibri 12', bg=self.bg_color)
        self.smoker1.grid(column=8, row=2)
        self.smoker_combobox = ttk.Combobox(self.frame, values=['Yes', 'No'])
        self.smoker_combobox.grid(column=9, row=2, padx=0)

    def forget_preparation(self):
        self.prepared = False
        self.age1.destroy()
        self.sex1.destroy()
        self.sex_combobox.destroy()
        self.entry1.destroy()
        self.bmi2.destroy()
        self.entry2.destroy()
        self.child3.destroy()
        self.entry3.destroy()
        self.smoker1.destroy()
        self.smoker_combobox.destroy()

    def forget_random(self):
        self.random = False
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label4.destroy()
        self.label5.destroy()
        self.label6.destroy()
        self.label7.destroy()
        self.label8.destroy()
        self.label9.destroy()
        self.label10.destroy()

    def find_nearest_neighbours(self):
        self.k = self.k_entry.get()
        if len(self.table_elements) > 0:
            for element in self.table_elements:
                element.destroy()
            self.table_elements = []
        if self.k == 0:
            msg.showerror(title="K Value Error", message="K value must be greater than 0.")
            return
        if self.prepared:
            print("Combobox: ", self.sex_combobox.get())
            sex = 0
            if self.sex_combobox.get() == "Female":
                sex = 0
            elif self.sex_combobox.get() == "Male":
                sex = 2
            smoker = 0
            if self.smoker_combobox.get() == "No":
                smoker = 0
            elif self.sex_combobox.get() == "Yes":
                smoker = 3
            self.test_sample = {"age": self.age.get(), "sex": sex, "bmi": self.bmi.get(),
                                "children": self.children.get(), "smoker": smoker}
            print(self.test_sample)

        k_nearest_neighbours()

    def create_knn_table(self, distances):
        self.table1 = tk.Label(self.frame, text="Age", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.table1.grid(row=6, column=0)
        self.table2 = tk.Label(self.frame, text="Sex", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.table2.grid(row=6, column=1)
        self.table3 = tk.Label(self.frame, text="BMI", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.table3.grid(row=6, column=2)
        self.table4 = tk.Label(self.frame, text="Children", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.table4.grid(row=6, column=3)
        self.table6 = tk.Label(self.frame, text="Smoker", font='Calibri 12 bold', bg=self.bg_color,
                               fg=self.table_column_color)
        self.table6.grid(row=6, column=4)
        self.table5 = tk.Label(self.frame, text="Charges", font='Calibri 12 bold', bg=self.bg_color, fg=self.table_column_color)
        self.table5.grid(row=6, column=5)
        self.table_elements = [self.table1, self.table2, self.table3, self.table4, self.table6, self.table5]
        self.last = 7
        for i in range(self.k):
            label2 = tk.Label(self.frame,
                                   text=str(self.train.loc[distances[i][0], 'age']),
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            label2.grid(row=self.last, column=0)
            self.table_elements.append(label2)
            if self.train.loc[distances[i][0], 'sex'] == 0:
                label2 = tk.Label(self.frame,
                                       text="Female",
                                       font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            else:
                label2 = tk.Label(self.frame,
                                  text="Male",
                                  font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            label2.grid(row=self.last, column=1)
            self.table_elements.append(label2)
            label2 = tk.Label(self.frame,
                                   text="%.2f" % float(self.train.loc[distances[i][0], 'bmi']),
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            label2.grid(row=self.last, column=2)
            self.table_elements.append(label2)
            label2 = tk.Label(self.frame,
                                   text=str(self.train.loc[distances[i][0], 'children']),
                              font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            label2.grid(row=self.last, column=3)
            self.table_elements.append(label2)
            if self.train.loc[distances[i][0], 'smoker'] == 0:
                label2 = tk.Label(self.frame,
                                       text="No",
                                       font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            else:
                label2 = tk.Label(self.frame,
                                  text="Yes",
                                  font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            label2.grid(row=self.last, column=4)
            self.table_elements.append(label2)
            label2 = tk.Label(self.frame,
                                   text="%.2f" % float(self.train.loc[distances[i][0], 'charges']),
                                   font='Calibri 12', bg=self.bg_color, fg=self.table_element)
            label2.grid(row=self.last, column=5)
            self.table_elements.append(label2)
            self.last += 1

    def show_expected(self, charges):
        expected = charges / self.k
        label = tk.Label(self.frame, text="Expected Charges: " + "%.2f" % expected, font='Calibri 12 bold',
                         bg=self.bg_color, fg="navy")
        label.grid(row=self.last, column=0)
        self.table_elements.append(label)

        if self.random:
            print(gui.test_sample['charges'])
            real = str(gui.test_sample['charges']).split("    ")[1].split("\n")[0]

            label = tk.Label(self.frame, text="Real Charges: " "%.2f" % float(real), font='Calibri 12 bold',
                             bg=self.bg_color, fg="maroon1")
            label.grid(row=self.last, column=1)
            self.table_elements.append(label)

            label = tk.Label(self.frame, text="Accuracy: " + "%.2f" % float(1 - abs((charges / self.k) - float(real))
                                                                            /float(real)),
                             font='Calibri 12 bold', bg=self.bg_color, fg="green2")
            label.grid(row=self.last, column=2)
            self.table_elements.append(label)


def prepare_data_set(file_name):
    insurance = pd.read_csv(file_name, delimiter=',')
    insurance = insurance[['age', 'sex', 'bmi', 'children', 'smoker', 'charges']]  # region row deleted
    mapping = {'female': 0, 'male': 2}
    insurance = insurance.replace({'sex': mapping})
    mapping = {'yes': 3, 'no': 0}
    insurance = insurance.replace({'smoker': mapping})

    train = insurance.sample(frac=0.8, random_state=200)
    test = insurance.drop(train.index)

    print("Train size: {}, Test size: {}".format(len(train), len(test)))
    return train, test


def euclidean_distance(train_sample, test_sample):
    return math.sqrt((train_sample['age'] - test_sample['age'])**2 +
                     (train_sample['sex'] - test_sample['sex'])**2 +
                     (train_sample['bmi'] - test_sample['bmi'])**2 +
                     (train_sample['children'] - test_sample['children'])**2 +
                     (train_sample['smoker'] - test_sample['smoker']) ** 2)


def k_nearest_neighbours():
    distances = []

    for i in range(len(gui.train)):
        distances.append([gui.train.index[i], euclidean_distance(gui.train.iloc[i], gui.test_sample)])

    distances = sorted(distances, key=lambda x: x[1])
    gui.create_knn_table(distances)

    charges = 0
    for i in range(gui.k):
        print(gui.train.loc[distances[i][0]], "distance: ", distances[i][1])
        charges += gui.train.loc[distances[i][0], 'charges']

    gui.show_expected(charges)
    return


def test():
    train, test = prepare_data_set("insurance.csv")

    errors = []
    ks = []

    for k in range(1, 21):
        expected = 0
        real = 0
        error = 0
        for test_sample in range(len(test)):
            distances = []
            for i in range(len(train)):
                distances.append([train.index[i], euclidean_distance(train.iloc[i], test.iloc[test_sample])])
            distances = sorted(distances, key=lambda x: x[1])
            charges = 0
            for i in range(k):
                charges += train.loc[distances[i][0], 'charges']
            expected += charges / k
            real += test.iloc[test_sample]['charges']
            error += 1 - (abs(test.iloc[test_sample]['charges'] - charges / k) / test.iloc[test_sample]['charges'])
            '''print("Expected: {}, Real: {}, Error: {}".format(charges / k, test.iloc[test_sample]['charges'],
                                                             abs(test.iloc[test_sample]['charges'] - charges / k) / test.iloc[test_sample]['charges']))'''

        expected /= len(test)
        real /= len(test)
        error /= len(test)
        print("K: {}, Expected: {}, Realities: {}, Accuracy: {}".format(k, expected, real, error))
        errors.append(error)
        ks.append(k)

        print(ks)
        print(errors)
        plt.plot(ks, errors)
        plt.grid()
        plt.xlabel('K values')
        plt.ylabel('Accuracies')
        plt.title('Experiment Results')


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui()

    root.mainloop()

    # test()
