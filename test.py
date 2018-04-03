from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import threading
import sqlite3
from subprocess import call, PIPE, Popen
import shutil
from sketchbooks.SW.run_servo import compiling
from db_input import *
from tkinter.messagebox import showinfo


class SERVO_MAN:
    def __init__(self, master):
        self.master = master
        self.master.geometry('800x400')
        self.frame = tk.Frame(self.master)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.master.title('серво менеджер')

        ##########angles from window######################
        self.left_eye = 0
        self.right_e = 0
        self.right_sholder = 0
        self.right_hand = 0
        self.left_hand = 0
        self.left_leg = 0
        self.right_leg = 0
        self.reserved_1 = 0
        self.reserved_2 = 0

        #################VALUES FOR TIMER##################################
        self.timer = False
        self.default_seconds = 0
        self.timer_seconds = self.default_seconds
        self.sql_time = []
        self.sql_servo_1 = 0
        self.sql_servo_2 = 0
        self.sql_servo_3 = 0
        self.sql_servo_4 = 0
        self.sql_servo_5 = 0
        self.sql_servo_6 = 0
        self.sql_servo_7 = 0
        self.sql_servo_8 = 0
        self.sql_servo_9 = 0
        self.sql_speed = 0
        self.time = 0
        #########values for changer default databases#########
        self.current_name_db = ''
        self.path = '/home/qbc/PycharmProjects/ard/scenario/2.db'
        ######## additional loop variables ##################

        self.loop_sec_entry1 = 0
        self.loop_sec_entry2 = 0
        self.loop_sec_entry3 = 0
        self.loop_sec_entry4 = 0
        self.loop_sec_entry5 = 0
        self.loop_sec_entry6 = 0
        self.loop_sec_entry7 = 0
        self.loop_sec_entry8 = 0
        self.loop_sec_entry9 = 0

        self.loop_int_entry1 = 0
        self.loop_int_entry2 = 0
        self.loop_int_entry3 = 0
        self.loop_int_entry4 = 0
        self.loop_int_entry5 = 0
        self.loop_int_entry6 = 0
        self.loop_int_entry7 = 0
        self.loop_int_entry8 = 0
        self.loop_int_entry9 = 0

        self.loop_speed1=0
        self.loop_speed2=0
        self.loop_speed3=0
        self.loop_speed4=0
        self.loop_speed5=0
        self.loop_speed6=0
        self.loop_speed7=0
        self.loop_speed8=0
        self.loop_speed9=0

        self.primary_time = 0
        self.final_time = 0
        self.interval =1
        self.count=0
        ############# constants for dictionaries###############
        self.LEFT_EYE = 0
        self.RIGHT_EYE = 1
        self.RIGHT_SHOLDER = 2
        self.RIGHT_HAND = 3
        self.LEFT_HAND = 4
        self.LEFT_LEG = 5
        self.RIGHT_LEG = 6
        self.RESERVED_1 = 7
        self.RESERVED_2 = 8




        self.lab_ser_1 = ttk.Label(self.master,
                                   text='глаз левый ').grid(row=1, column=1)
        self.left_eye = IntVar()
        self.angle_box1 = ttk.Entry(self.master,
                                    width=3,
                                    textvariable=self.left_eye)
        self.angle_box1.grid(row=2, column=1)
        self.loop_l_e = ttk.Checkbutton(self.master,
                                        command=self.check_loop
                                        ).grid(row=1, column=2, padx=10)

        self.lab_ser_2 = ttk.Label(self.master,text='глаз правый').grid(row=4, column=1)
        self.right_e = IntVar()
        self.angle_box2 = ttk.Entry(self.master, textvariable=self.right_e, width=3)
        self.angle_box2.grid(row=5, column=1)
        self.loop_r_e = ttk.Checkbutton(self.master,
                                        command=self.check_loop2).grid(row=4, column=2, padx=10)

        self.lab_ser_3 = ttk.Label(self.master, text='плечо правое').grid(row=8, column=1)
        self.right_sholder = IntVar()
        self.angle_box3 = ttk.Entry(self.master,
                                    textvariable=self.right_sholder, width=3)
        self.angle_box3.grid(row=9, column=1)
        self.loop_r_s = ttk.Checkbutton(self.master,command=self.check_loop3
                                        ).grid(row=8, column=2, padx=10)

        self.lab_ser_4 = ttk.Label(self.master, text='рука правая').grid(row=1, column=3, )
        self.right_hand = IntVar()
        self.angle_box4 = ttk.Entry(self.master, textvariable=self.right_hand, width=3)
        self.angle_box4.grid(row=2, column=3)
        self.loop_r_h = ttk.Checkbutton(self.master,command=self.check_loop4
                                        ).grid(row=1, column=4, padx=10)

        self.lab_ser_5 = ttk.Label(self.master, text='рука левая').grid(row=4, column=3)
        self.left_hand = IntVar()
        self.angle_box5 = ttk.Entry(self.master, textvariable=self.left_hand, width=3)
        self.angle_box5.grid(row=5, column=3)
        self.loop_r_l = ttk.Checkbutton(self.master,command=self.check_loop5
                                        ).grid(row=4, column=4, padx=10)

        self.lab_ser_6 = ttk.Label(self.master, text='нога левая').grid(row=8, column=3)
        self.left_leg = IntVar()
        self.angle_box6 = ttk.Entry(self.master, textvariable=self.left_leg, width=3)
        self.angle_box6.grid(row=9, column=3)
        self.loop_l_l = ttk.Checkbutton(self.master,command=self.check_loop6
                                        ).grid(row=8, column=4, padx=10)

        self.lab_ser_7 = ttk.Label(self.master, text='нога правая ').grid(row=1, column=6)
        self.right_leg = IntVar()
        self.angle_box7 = ttk.Entry(self.master, textvariable=self.right_leg, width=3)
        self.angle_box7.grid(row=2, column=6)

        self.loop_r_l = ttk.Checkbutton(self.master,command=self.check_loop7
                                        ).grid(row=1, column=7, padx=10)

        self.lab_ser_8 = ttk.Label(self.master, text='reserved_1 ').grid(row=4, column=6)
        self.reserved_1 = IntVar()
        self.angle_box8 = ttk.Entry(self.master, textvariable=self.reserved_1, width=3)
        self.angle_box8.grid(row=5, column=6)
        self.loop_res = ttk.Checkbutton(self.master,command=self.check_loop8
                                        ).grid(row=4, column=7, padx=10)

        self.lab_ser_9 = ttk.Label(self.master, text='reserved_2 ').grid(row=8, column=6)
        self.reserved_2 = IntVar()
        self.angle_box9 = ttk.Entry(self.master, textvariable=self.reserved_2, width=3)
        self.angle_box9.grid(row=9, column=6)
        self.loop_res2 = ttk.Checkbutton(self.master,command=self.check_loop9
                                        ).grid(row=8, column=7, padx=10)

        self.play_butt = ttk.Button(self.master,
                                    text='проиграть',
                                    ).grid(row=12, column=3)
        self.button = ttk.Button(self.master,
                                 text='записать позиции',
                                 command = self.adden_key_to_model)
        self.button.grid(row=10, column=3)
        self.button_save = ttk.Button(self.master,
                            text='сохранить сценарий ',
                            command=self.write_changes_to_sql
                            ).grid(row=11, column=3)
        self.new = ttk.Button(
            self.master,
            text="новый сценарий",
            command=self.new_data
           ).grid(row=1, column=8)
        self.window_curr = ttk.Button(self.master,
                                      text="выбрать сценарий",
                                      command =self.choose_db).grid(row=1, column=9)

        self.window_db = Listbox(self.master, width=28, height=10)
        self.window_db.grid(row=2, column=8,rowspan=8,columnspan=10)
        self.request_butt = ttk.Button(self.master,
                                       text='выбрать текущий',
                                       command= self.current_db).grid(row=10, column=8)
        self.label_time = ttk.Label(self.master)
        self.label_time.grid(row=11, column=3)

        self.time_scale = ttk.Scale(self.master,
                                    orient='horizontal',
                                    length=400,
                                    from_=0, to=180,
                                    command = self.update_slider
                                    )
        self.time_scale.grid(row=19, column=0, columnspan=8)
        # digit near "время"
        self.time_label = ttk.Label(self.master, text="время").grid(row=17, column=1)

        self.time_digit = ttk.Label(self.master)
        self.time_digit.grid(row=16, column=0,rowspan=1,columnspan=7)

        self.speed_label = ttk.Label(self.master, text="cкорость").grid(row=22, column=1)

        self.speed_digit = ttk.Label(self.master)
        self.speed_digit.grid(row=22, column=1,columnspan=6)

        self.speed_slider = ttk.Scale(self.master,
                                      orient="horizontal",
                                      length=100,
                                      from_=0, to=100,
                                      )
        self.speed_slider.grid(row=23, column=0,columnspan=3)

        self.model = {}

    def update_slider(self,val):
      pass

    def check_servos(self,sec):
        # cheking and equalize
        if sec in self.model['scenario_stack']:
            self.update_view(self.model['scenario_stack'][sec])

    def update_view(self,sec):
        #for return old values from model
        self.model = {

                round(self.time_scale.get()): [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_hand.get(), self.left_hand.get(),
                    self.left_leg.get(), self.right_leg.get(),
                    self.reserved_1.get(), self.reserved_2.get(),
                    self.speed_slider.get()
                ]

        }
        print(self.model)

    def setServosFromGUI(self,sec):
        #for return old values from model
        self.model = {
            'current_time': sec,
            'scenario_stack': {
                round(self.time_scale.get()): [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_hand.get(), self.left_hand.get(),
                    self.left_leg.get(), self.right_leg.get(),
                    self.reserved_1.get(), self.reserved_2.get(),
                    self.speed_slider.get()
                ]
            }
        }
        print(self.model)



    def get_prev_from_dict(self,dic, elem):
        return dic[elem] if elem in dic else self.get_prev_from_dict(dic, elem - 1)



    def update_servo_controller(self, servo_id, value):
        if self.model['current_time'] in self.model['scenario_stack']:
            self.model['scenario_stack'][self.model['current_time']][servo_id] = value
        else:
            previous = self.get_prev_from_dict(self.model['scenario_stack'], self.model['current_time'])
            previous[servo_id] = value
            self.model['scenario_stack'][self.model['current_time']] = previous


    def check_Model(self):
        if self.model['current_time'] == self.model['scenario_stack']:
            print(self.model['scenario_stack'])





    def adden_key_to_model(self):
        #obtain values from windows
        self.model[round(self.time_scale.get()*1000)]=[
            self.left_eye.get(), self.right_e.get(),
            self.right_sholder.get(),self.right_hand.get(),
            self.left_hand.get(),self.left_leg.get(),
            self.right_leg.get(),self.reserved_1.get(),
            self.reserved_2.get(),round(self.speed_slider.get())
        ]
        print(self.model)



    def write_to_h(self):

        # take all from data base
        conn = sqlite3.connect(self.path)  # here will be avalibale data bases
        cursor = conn.cursor()
        # time
        cursor.execute("SELECT * FROM `time` order by  `time_pos` ")
        sql_time = cursor.fetchall()
        # servo_1
        cursor.execute("SELECT * FROM `servo_0`  ")
        sql_servo_1 = cursor.fetchall()
        # servo_2
        cursor.execute("SELECT * FROM `servo_1`  ")
        sql_servo_2 = cursor.fetchall()
        # servo_3
        cursor.execute("SELECT * FROM `servo_2` ")
        sql_servo_3 = cursor.fetchall()
        # servo_4
        cursor.execute("SELECT * FROM `servo_3`  ")
        sql_servo_4 = cursor.fetchall()
        # servo_5
        cursor.execute("SELECT * FROM `servo_4`  ")
        sql_servo_5 = cursor.fetchall()
        # servo_6
        cursor.execute("SELECT * FROM `servo_5`  ")
        sql_servo_6 = cursor.fetchall()
        # servo_7
        cursor.execute("SELECT * FROM `servo_6`  ")
        sql_servo_7 = cursor.fetchall()
        # servo_8
        cursor.execute("SELECT * FROM `servo_7`  ")
        sql_servo_8 = cursor.fetchall()
        # servo_9
        cursor.execute("SELECT * FROM `servo_8`  ")
        sql_servo_9 = cursor.fetchall()
        cursor.execute("SELECT * FROM `speed` order by  `speed_pos` ")
        sql_speed = cursor.fetchall()
        # servo_1
        with open('template.h', 'w') as file:
            file.writelines('int time_play=1;\n')
            file.writelines('int speed_row[] = {')
            file.writelines(str(sql_speed))
            file.writelines('};\n')
            file.writelines('int LEyeArray[][] = {')
            file.writelines(str(sql_servo_1))
            file.writelines('};\n')
            file.writelines('int REyeArray[] = {')
            file.writelines(str(sql_servo_2))
            file.writelines('};\n')
            file.writelines('int LArmArray[] = {')
            file.writelines(str(sql_servo_3))
            file.writelines('};\n')
            file.writelines('int RArmArray[] = {')
            file.writelines(str(sql_servo_4))
            file.writelines('};\n')
            file.writelines('int LhandArray[] = {')
            file.writelines(str(sql_servo_5))
            file.writelines('};\n')
            file.writelines('int RhandArray[] = {')
            file.writelines(str(sql_servo_6))
            file.writelines('};\n')
            file.writelines('int LLegArray[] = {')
            file.writelines(str(sql_servo_7))
            file.writelines('};\n')
            file.writelines('int RLegArray[] = {')
            file.writelines(str(sql_servo_8))
            file.writelines('};\n')
            file.writelines('int AssArray[] = {')
            file.writelines(str(sql_servo_9))
            file.writelines('};\n')
            file.writelines('unsigned long KeyArray[] = {')
            file.writelines(str(sql_time))
            file.writelines('};\n')
        self.clear_strings()

    def clear_strings(self):
        # clean by rubish
        f = open('template.h', 'r')
        o = open('VAL.h', 'w')
        while 1:
            line = f.readline()
            if not line: break
            line = line.replace('(', '')
            line = line.replace(')', '')
            line = line.replace(',,', ',')
            line = line.replace("''", '0')
            line = line.replace('[][]', '[]')
            line = line.replace('{[]}', '{}')
            line = line.replace('{[', '{')
            line = line.replace(']}', '}')
            line = line.replace(')]};', '')
            o.write(line)
        o.close()
        call('rm template.h', shell=True)
        shutil.move("/home/qbc/PycharmProjects/ard/VAL.h",
                    "/usr/share/arduino/hardware/arduino/cores/arduino/VAL.h")

    def check_loop(self):

        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл1')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.left_eye = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.left_eye, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry1 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry1, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed1 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed1, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow,text = 'засечь время',command= lambda: self.count_clicks(self.loop_to)).grid(row=5,column=1)

    def check_loop2(self):

        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл2')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.right_e = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.right_e, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry2 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry2, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed2 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed2, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время', command=lambda: self.count_clicks(self.loop_to2)).grid(
            row=5, column=1)

    def check_loop3(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл3')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.right_sholder = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.right_sholder, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry3 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry3, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed3 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed3, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время',
                               command=lambda: self.count_clicks(self.loop_to3)).grid(
            row=5, column=1)

    def check_loop4(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл4')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.right_hand = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.right_hand, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry4 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry4, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed4 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed4, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)
        temp_time = ttk.Button(newonfWindow, text='засечь время',
                               command=lambda: self.count_clicks(self.loop_to4)).grid(row=5, column=1)

    def check_loop5(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл5')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.left_hand = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.left_hand, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry5 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry5, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed5 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed5, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время',
                           command=lambda: self.count_clicks(self.loop_to5)).grid(row=5, column=1)

    def check_loop6(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл6')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.left_leg = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.left_leg, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry6 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry6, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed6 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed6, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время',
                           command=lambda: self.count_clicks(self.loop_to6)).grid(row=5, column=1)

    def check_loop7(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл7')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.right_leg = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.right_leg, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry7 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry7, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed7 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed7, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время',
                               command=lambda: self.count_clicks(self.loop_to7)).grid(row=5, column=1)

    def check_loop8(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл8')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.reserved_1 = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.reserved_1, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry8 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry8, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed8 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed8, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время',
                               command=lambda: self.count_clicks(self.loop_to8)).grid(row=5, column=1)
    def check_loop9(self):
        newonfWindow = tk.Toplevel(self.master)
        newonfWindow.geometry('200x130')
        newonfWindow.title('цикл9')
        first_label = ttk.Label(newonfWindow, text='первый', borderwidth=3).grid(row=1, column=1)
        self.reserved_2 = IntVar()
        loop_le1 = ttk.Entry(newonfWindow, textvariable=self.reserved_2, width=4)
        loop_le1.grid(row=1, column=2)
        self.loop_sec_entry9 = IntVar()
        second_label = ttk.Label(newonfWindow, text='второй', borderwidth=3).grid(row=2, column=1)
        loop_le2 = ttk.Entry(newonfWindow, textvariable=self.loop_sec_entry9, width=4)
        loop_le2.grid(row=2, column=2)

        self.loop_int_entry = IntVar()
        interval_label = ttk.Label(newonfWindow, text='интервал', borderwidth=3).grid(row=3, column=1)
        loop_le_int = ttk.Entry(newonfWindow, textvariable=self.loop_int_entry, width=4)
        loop_le_int.grid(row=3, column=2)

        self.loop_speed9 = IntVar()
        loop_speed = ttk.Entry(newonfWindow, textvariable=self.loop_speed9, width=4)
        loop_speed.grid(row=4, column=2)
        speed_label = ttk.Label(newonfWindow, text='cкорость', borderwidth=3).grid(row=4, column=1)

        cancell_but = ttk.Button(newonfWindow, text='отмена', command=lambda: newonfWindow.destroy())
        cancell_but.grid(row=5, column=2)

        temp_time = ttk.Button(newonfWindow, text='засечь время',
                               command=lambda: self.count_clicks(self.loop_to9)).grid(row=5, column=1)







    def loop_to(self):
        # call to each calling func to
        print('loop')
        range_index = 0
        primary_time =self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry1.get() * 1000)):
            primary_time+=int(self.loop_int_entry1.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                self.left_eye.get(), self.right_e.get(),
                self.right_sholder.get(),self.right_hand.get(),
                self.left_hand.get(),self.left_leg.get(),
                self.right_leg.get(),self.reserved_1.get(),
                self.reserved_2.get(),round(self.loop_speed1.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                self.loop_sec_entry1.get(), self.right_e.get(),
                self.right_sholder.get(), self.right_hand.get(),
                self.left_hand.get(), self.left_leg.get(),
                self.right_leg.get(), self.reserved_1.get(),
                self.reserved_2.get(), round(self.loop_speed1.get())]
            range_index += 1
            print(self.model)

    def loop_to2(self):
        # call to each calling func to
        print('loop2')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry2.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed2.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.loop_sec_entry2.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed2.get())]
            range_index += 1
            print(self.model)

    def loop_to3(self):
        # call to each calling func to
        print('loop3')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry3.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed2.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.loop_sec_entry3.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed4.get())]
            range_index += 1
            print(self.model)

    def loop_to4(self):
        # call to each calling func to
        print('loop4')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed4.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.right_e.get(),
                    self.right_sholder.get(), self.loop_sec_entry4.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed4.get())]
            range_index += 1
            print(self.model)

    def loop_to5(self):
        # call to each calling func to
        print('loop5')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed5.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.loop_sec_entry5.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed5.get())]
            range_index += 1
            print(self.model)

    def loop_to6(self):
        # call to each calling func to
        print('loop6')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed6.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.loop_sec_entry6.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed6.get())]
            range_index += 1
            print(self.model)
    def loop_to7(self):
        # call to each calling func to
        print('loop7')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed7.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.loop_sec_entry2.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.loop_sec_entry7.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed7.get())]
            range_index += 1
            print(self.model)

    def loop_to8(self):
        # call to each calling func to
        print('loop2')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry2.get() * 1000)):
            primary_time += int(self.loop_int_entry2.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed2.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.loop_sec_entry2.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.loop_sec_entry8.get(),
                    self.reserved_2.get(), round(self.loop_speed2.get())]
            range_index += 1
            print(self.model)

    def loop_to9(self):
        # call to each calling func to
        print('loop2')
        range_index = 0
        primary_time = self.primary_time
        final_time = self.final_time
        for i in range(int(primary_time),
                       int(self.final_time),
                       int(self.loop_int_entry.get() * 1000)):
            primary_time += int(self.loop_int_entry.get() * 1000)
            if range_index % 2 != 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(), self.right_e.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.reserved_2.get(), round(self.loop_speed9.get())]
            if range_index % 2 == 0:
                self.model['{}'.format(primary_time)] = [
                    self.left_eye.get(),self.loop_sec_entry2.get(),
                    self.right_sholder.get(), self.right_hand.get(),
                    self.left_hand.get(), self.left_leg.get(),
                    self.right_leg.get(), self.reserved_1.get(),
                    self.loop_sec_entry9.get(), round(self.loop_speed9.get())]
            range_index += 1
            print(self.model)

    def count_clicks(self, calling_loop):
        self.count += 1
        # TODO ALL REFACTOR BELLOW
        if self.count == 1:
            self.primary_time = round(self.time_scale.get() * 1000)
            messagebox.showinfo("значение", "записано первое значение")
        if self.count == 2:
            self.count = 0
            messagebox.showinfo("значение", "записано второе значение ")
            self.final_time = round(self.time_scale.get() * 1000)
            calling_loop()  # space for another loops



    def write_changes_to_sql(self):
        conn = sqlite3.connect(self.path)  # here will be avalibale data bases
        cursor = conn.cursor()
        for key,values in self.model.items():
            cursor.execute(""" insert into`servo_0`values( % d)""" % (values[self.LEFT_EYE]))
            cursor.execute(""" insert into`servo_1`values( % d)""" % (values[self.RIGHT_EYE]))
            cursor.execute(""" insert into`servo_2`values( % d)""" % (values[self.RIGHT_SHOLDER]))
            cursor.execute(""" insert into`servo_3`values( % d)""" % (values[self.RIGHT_HAND]))
            cursor.execute(""" insert into`servo_4`values( % d)""" % (values[self.LEFT_HAND]))
            cursor.execute(""" insert into`servo_5`values( % d)""" % (values[self.LEFT_LEG]))
            cursor.execute(""" insert into`servo_6`values( % d)""" % (values[self.RIGHT_LEG]))
            cursor.execute(""" insert into`servo_7`values( % d)""" % (values[self.RESERVED_1]))
            cursor.execute(""" insert into`servo_8`values( % d)""" % (values[self.RESERVED_2]))
            cursor.execute(""" insert into`time`values( % s)""" % (key))
            cursor.execute(""" insert into`speed`values( % d)""" % (values[-1]))
        conn.commit()
        self.write_to_h()



    def choose_db(self):
        fname = askopenfilename(filetypes=(("scenario", "*.db"),
                                           ("All files", "*.*")),
                                initialdir='~/PycharmProjects/ard/')
        print(fname[-8:-1])
        self.current_name_db = fname
        self.window_db.insert(END, fname[-25:-1] + '\n')

    def current_db(self):
        self.path = self.current_name_db

    def new_data(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = new_base(self.newWindow)


def main():
    root = tk.Tk()
    root.title("SERVO_M")

    app = SERVO_MAN(root)
    root.mainloop()


if __name__ == '__main__':
    main()