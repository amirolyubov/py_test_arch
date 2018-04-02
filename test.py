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
                                        ).grid(row=1, column=2, padx=10)

        self.lab_ser_2 = ttk.Label(self.master,text='глаз правый').grid(row=4, column=1)
        self.right_e = IntVar()
        self.angle_box2 = ttk.Entry(self.master, textvariable=self.right_e, width=3)
        self.angle_box2.grid(row=5, column=1)
        self.loop_r_e = ttk.Checkbutton(self.master,
                                        ).grid(row=4, column=2, padx=10)

        self.lab_ser_3 = ttk.Label(self.master, text='плечо правое').grid(row=8, column=1)
        self.right_sholder = IntVar()
        self.angle_box3 = ttk.Entry(self.master,
                                    textvariable=self.right_sholder, width=3)
        self.angle_box3.grid(row=9, column=1)
        self.loop_r_s = ttk.Checkbutton(self.master,
                                        ).grid(row=8, column=2, padx=10)

        self.lab_ser_4 = ttk.Label(self.master, text='рука правая').grid(row=1, column=3, )
        self.right_hand = IntVar()
        self.angle_box4 = ttk.Entry(self.master, textvariable=self.right_hand, width=3)
        self.angle_box4.grid(row=2, column=3)
        self.loop_r_h = ttk.Checkbutton(self.master,
                                        ).grid(row=1, column=4, padx=10)

        self.lab_ser_5 = ttk.Label(self.master, text='рука левая').grid(row=4, column=3)
        self.left_hand = IntVar()
        self.angle_box5 = ttk.Entry(self.master, textvariable=self.left_hand, width=3)
        self.angle_box5.grid(row=5, column=3)
        self.loop_r_l = ttk.Checkbutton(self.master,
                                        ).grid(row=4, column=4, padx=10)

        self.lab_ser_6 = ttk.Label(self.master, text='нога левая').grid(row=8, column=3)
        self.left_leg = IntVar()
        self.angle_box6 = ttk.Entry(self.master, textvariable=self.left_leg, width=3)
        self.angle_box6.grid(row=9, column=3)
        self.loop_l_l = ttk.Checkbutton(self.master,
                                        ).grid(row=8, column=4, padx=10)

        self.lab_ser_7 = ttk.Label(self.master, text='нога правая ').grid(row=1, column=6)
        self.right_leg = IntVar()
        self.angle_box7 = ttk.Entry(self.master, textvariable=self.right_leg, width=3)
        self.angle_box7.grid(row=2, column=6)

        self.loop_r_l = ttk.Checkbutton(self.master,
                                        ).grid(row=1, column=7, padx=10)

        self.lab_ser_8 = ttk.Label(self.master, text='reserved_1 ').grid(row=4, column=6)
        self.reserved_1 = IntVar()
        self.angle_box8 = ttk.Entry(self.master, textvariable=self.reserved_1, width=3)
        self.angle_box8.grid(row=5, column=6)
        self.loop_res = ttk.Checkbutton(self.master,
                                        ).grid(row=4, column=7, padx=10)

        self.lab_ser_9 = ttk.Label(self.master, text='reserved_2 ').grid(row=8, column=6)
        self.reserved_2 = IntVar()
        self.angle_box9 = ttk.Entry(self.master, textvariable=self.reserved_2, width=3)
        self.angle_box9.grid(row=9, column=6)
        self.loop_res2 = ttk.Checkbutton(self.master,
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
                            command=self.write_keys_to_sql
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

        self.model = {
            'current_time': 0,
            'scenario_stack': {
                0: [20, 20, 20, 20, 20, 20, 20, 20, 20, 20],

            }
        }



    def update_slider(self,val):
        # take value from slider and check
        self.model['current_time'] = round(float(val))
        self.check_servos(self.model['current_time'])


    def check_servos(self,sec):
        # cheking and equalize
        if sec in self.model['scenario_stack']:
            self.update_view(self.model['scenario_stack'][sec])

    def update_view(self,sec):
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
            arr = self.get_prev_from_dict(self.model['scenario_stack'], self.model['current_time'])
            arr[servo_id] = value
            self.model['scenario_stack'][self.model['current_time']] = arr


    def check_Model(self):
        if self.model['current_time'] == self.model['scenario_stack']:
            print(self.model['scenario_stack'])





    def adden_key_to_model(self):
        #obtain values from windows
        self.model['scenario_stack'][round(self.time_scale.get())]=[
            self.left_eye.get(), self.right_e.get(),
            self.right_sholder.get(),self.right_hand.get(),
            self.left_hand.get(),self.left_leg.get(),
            self.right_leg.get(),self.reserved_1.get(),
            self.reserved_2.get(),round(self.speed_slider.get())
        ]
        print(self.model['scenario_stack'])

    def write_keys_to_sql(self):
            for key, value in self.model['scenario_stack'].items():

                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute("""
                    insert into `servo_i` values (%d) 
                    """ % (value[self.LEFT_EYE]))
                    cursor.execute("""
                     insert into `servo_` values (%d) 
                    """ % ((value[self.RIGHT_EYE])))
                    cursor.execute("""
                    insert into `servo_3` values (%d) 
                    """ % (value[self.RIGHT_SHOLDER]))
                    cursor.execute("""
                    insert into `servo_4` values (%d) 
                    """ % (value[self.RIGHT_HAND]))
                    cursor.execute("""
                    insert into `servo_5` values (%d) 
                    """ % (value[self.LEFT_HAND]))
                    cursor.execute("""
                    insert into `servo_6` values (%d) 
                    """ % (value[self.LEFT_LEG]))
                    cursor.execute("""
                    insert into `servo_7` values (%d) 
                    """ % (value[self.RIGHT_LEG]))
                    cursor.execute("""
                    insert into `servo_8` values (%d) 
                    """ % (value[self.RESERVED_1]))
                    cursor.execute("""
                    insert into `servo_9` values (%d) 
                    """ % (value[self.RESERVED_2]))
                    cursor.execute("""
                    insert into `time` values (%s) 
                    """ % (key))
                    cursor.execute("""
                    insert into `speed` values (%s) 
                    """ % (value[9]))


            conn.commit()

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