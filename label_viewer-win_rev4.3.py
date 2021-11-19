from __future__ import print_function

import xml.etree.ElementTree as ET
from tkinter import *
import tkinter.font
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime
import csv
import shutil
import textwrap
from screeninfo import get_monitors
from ctypes import windll, Structure, c_ulong, byref
# from win32api import GetSystemMetrics

class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

class frameInit():
    def __init__(self):
        self.root = Tk()
        self.new_state = 'normal'

        # full screen 설정
        # self.fullScreenState = not self.fullScreenState
        # self.root.attributes("-fullscreen", self.fullScreenState)
        # self.fullScreenState = False
        # self.root.attributes("-fullscreen", self.fullScreenState)

        for m in get_monitors():
            if m.is_primary == True:
                self.primary_w = m.width
                self.primary_h = m.height
            else:
                self.secondary_w = m.width
                self.secondary_h = m.height
            # print(m)
            # Monitor(x=0, y=0, width=1920, height=1080, width_mm=344, height_mm=194, name='\\\\.\\DISPLAY1', is_primary=True)
            # Monitor(x=1920, y=0, width=2560, height=1440, width_mm=600, height_mm=337, name='\\\\.\\DISPLAY2', is_primary=False)

        self.frame_width, self.frame_height = 1550, 850
        frame_xposi, frame_yposi = int((self.primary_w - self.frame_width) / 2), int((self.primary_h - self.frame_height - 23) / 2)
        self.root.title("Label 이미지 Viewer")
        self.root.geometry('{}x{}+{}+{}'.format(self.frame_width, self.frame_height, frame_xposi, frame_yposi))
        # self.root.geometry('1350x820+80+5')
        # self.root.state('zoomed')
        self.root.resizable(True, True) 

        font1 = tkinter.font.Font(family="Malgun Gothic", size=10, weight = "bold")
        font2 = tkinter.font.Font(family="Malgun Gothic", size=10, weight = "normal")

        self.current_path = os.getcwd()

        # top frame
        frame_top = Frame(self.root)
        frame_top.pack(side = 'top', fill = 'both', expand = True)

        # top_left path dir Open frame
        folder_path_frame = LabelFrame(frame_top, text = '작업 폴더 선택', font = font1)
        folder_path_frame.pack(side = 'top', fill = 'both', pady = 5)

        # select image folder button frame
        image_folder = Frame(folder_path_frame)
        image_folder.pack(side = 'left', anchor = 'w', fill = 'both', expand = True)

        image_folder1 = Label(image_folder, text = '이미지 폴더 선택', font = font2)
        image_folder1.pack(side = 'left', fill = 'both', padx = 5, pady = 5)

        self.image_folder2 = Entry(image_folder, width = 137, font = font2)
        self.image_folder2.pack(side = 'left', fill = 'both', padx = 5, pady = 5)

        image_folder3 = Button(image_folder, text = '열기', width = 8, command = self.image_dir, font = font2)
        image_folder3.pack(side = 'left', fill = 'both', padx = 15, pady = 5)

        self.image_folder4 = Button(image_folder, text = '시작', width = 8, command = self.pre_data_load, state = 'disabled', font = font2)
        self.image_folder4.pack(side = 'left', fill = 'both', padx = 15, pady = 5)

        # top info main frame
        info_frame_main = Frame(self.root)
        info_frame_main.pack(side = 'top', fill = 'both')

        # top info left frame
        info_frame_left = Frame(info_frame_main)
        info_frame_left.pack(side = 'left', anchor = 'w', fill = 'both', expand = True)

        # top xml meta info frame
        meta_info_frame = LabelFrame(info_frame_left, text = 'XML Meta 정보', font = font1)
        meta_info_frame.pack(side = 'top', fill = 'both', pady = 5)

        # xml meta data frame
        meta_info_sub1 = Frame(meta_info_frame)
        meta_info_sub1.pack(side = 'top', fill = 'both', padx = 5)

        self.meta_data = Label(meta_info_sub1, text = '', anchor = 'w', justify = 'left', width = 180, font = font2)
        self.meta_data.pack(side = 'left', fill = 'both')

        # top image info frame
        image_info_frame = LabelFrame(info_frame_left, text = '이미지 데이터', font = font1)
        image_info_frame.pack(side = 'top', fill = 'both', pady = 5)

        # image file name frame
        image_info_sub1 = Frame(image_info_frame)
        image_info_sub1.pack(side = 'top', fill = 'both', padx = 5)

        self.anno_label = Label(image_info_sub1, text = '', anchor = 'w', justify = 'left', width = 180, font = font2)
        self.anno_label.pack(side = 'left', fill = 'both')

        # top info right button frame
        info_frame_right = Frame(info_frame_main)
        info_frame_right.pack(side = 'right', fill = 'both')

        now = datetime.now()
        self.date = '{}{:02d}{:02d}'.format(now.year, now.month, now.day)
        # top info button frame
        self.reject_report_label = Label(info_frame_right, text = '', bg = 'yellow', font = font2)
        self.reject_report_label.pack(side = 'top', fill = 'both', padx = 5, pady = 5)

        # reject_reason_label_frame
        reject_reason_label_frame = Frame(info_frame_right)
        reject_reason_label_frame.pack(side = 'top', fill = 'both', padx = 5)

        reject_reason_label = Label(reject_reason_label_frame, text = '반려 사유 - ', font = font2)
        reject_reason_label.pack(side = 'left', fill = 'both')

        self.reject_reason_object = Label(reject_reason_label_frame, text = '', font = font2)
        self.reject_reason_object.pack(side = 'left', fill = 'both')

        self.reject_reason_text = Label(reject_reason_label_frame, text = ' > ', font = font2)
        self.reject_reason_text.pack(side = 'left', fill = 'both')

        self.reject_reason_label = Label(reject_reason_label_frame, text = '', font = font2)
        self.reject_reason_label.pack(side = 'left', fill = 'both')

        self.reject_reason = ['', '이미지 관련 XML 파일 누락', 'XML에 이미지 정보 누락', 'Bounding Box 캐릭터명 오류(오태깅)', \
            'Bounding Box 감정명 오류(오태깅)', '잘못된 Bounding Box 작업(오태깅)', '불필요한 Bounding Box 작업(과태깅)',\
            'Bounding Box 작업 안됨(미태깅)', 'Polygon 캐릭터명 오류(오태깅)', 'Polygon 감정명 오류(오태깅)', '잘못된 Polygon 작업(오태깅)',\
            '불필요한 Polygon 작업(과태깅)', 'Polygon 작업 안됨(미태깅)']
        self.reject_reason_chkbox = ttk.Combobox(info_frame_right, width = 39, height = 13, value = self.reject_reason, state = 'readonly', font = font2)
        self.reject_reason_chkbox.pack(side = 'top', fill = 'both', padx = 5, pady = 5)

        self.labels_name = 0
        # reject_button frame
        self.reject_button_frame = Frame(info_frame_right)
        self.reject_button_frame.pack(side = 'top', fill = 'both', padx = 5)

        self.reject_button = Button(self.reject_button_frame, text = '반려 / 반려취소', width = 18, command = self.anno_reject, state = 'disabled', font = font2)
        self.reject_button.pack(side = 'left', fill = 'both')

        self.reject_end_button = Button(self.reject_button_frame, text = '반려 완료', width = 18, command = self.reject_next, state = 'disabled', font = font2)
        self.reject_end_button.pack(side = 'right', fill = 'both')

        # pass_button frame
        self.pass_button_frame = Frame(info_frame_right)
        self.pass_button_frame.pack(side = 'top', fill = 'both', padx = 5, pady = 5)

        self.pass_button = Button(self.pass_button_frame, text = '통과', width = 15, command = self.anno_pass, state = 'disabled', font = font2)
        self.pass_button.pack(fill = 'both')

        self.img_reject_pass_lst = []
        self.change_reject_pass_lst = []
        self.tot_reject_pass_lst = []
        # statistics frame
        statistics_info_frame = Frame(info_frame_right)
        statistics_info_frame.pack(side = 'top', fill = 'both', padx = 5)

        self.statistics_reject = Label(statistics_info_frame, text = '반려 : {0:<10}'.format(''), anchor = 'w', justify = 'left', width = 18, font = font2)
        self.statistics_reject.pack(side = 'left', fill = 'both')

        self.statistics_pass = Label(statistics_info_frame, text = '통과 : {0:<10}'.format(''), anchor = 'w', justify = 'left', width = 18, font = font2)
        self.statistics_pass.pack(side = 'left', fill = 'both')

        # progressbar frame
        progessbar_frame = Frame(info_frame_right)
        progessbar_frame.pack(side = 'top', fill = 'both', padx = 5, pady = 5)

        self.pro_var = DoubleVar()
        self.progressbar = ttk.Progressbar(progessbar_frame, maximum =100, length = 160, variable = self.pro_var)
        self.progressbar.pack(side = 'left', padx =5)

        self.prog_rate = Label(progessbar_frame, text = '', font = font2)
        self.prog_rate.pack(side = 'right', padx = 5)

        self.grid_5_onoff = 0
        self.grid_100_onoff = 0
        # grid on/off frame
        grid_onoff_frame = Frame(info_frame_right)
        grid_onoff_frame.pack(side = 'top', fill = 'both', padx = 5)

        self.grid_left_button = Button(grid_onoff_frame, text = '5 pixel 그리드', width = 18, command = self.grid_5p_start, state = 'disabled', font = font2)
        self.grid_left_button.pack(side = 'left', fill = 'both')

        self.grid_right_button = Button(grid_onoff_frame, text = '100 pixel 그리드', width = 18, command = self.grid_100p_start, state = 'disabled', font = font2)
        self.grid_right_button.pack(side = 'right', fill = 'both')

        # top_left path dir Open frame
        image_view_frame = LabelFrame(self.root, text = '이미지 뷰어', font = font1)
        image_view_frame.pack(side = 'top', fill = 'both')

        # 검수 info window
        frame_top = Frame(image_view_frame, relief = 'solid', bd = 1)
        frame_top.pack(side = 'top', fill = 'both', expand = True)

        self.bottom_text = Label(frame_top, text = '', anchor = 'center', justify = 'left', font = font2)
        self.bottom_text.pack(side = 'left', fill = 'both', expand = True)

        # image preview frame
        frame_bottom = Frame(image_view_frame)
        frame_bottom.pack(side = 'bottom', fill = 'y', expand = True)

        self.bottom_left = Button(frame_bottom, text = '이전', width = 15, command = self.go_pre, state = 'disabled', font = font2)
        self.bottom_left.pack(side = 'left', fill = 'y', expand = True)

        photo = PhotoImage()
        self.canvas = Canvas(frame_bottom, width = 1112, height = 510, bg = 'white')
        self.canvas.create_image(556, 255, image = photo)
        self.canvas.pack(side = 'left', expand = True, fill = 'none')

        self.bottom_right = Button(frame_bottom, text = '다음', width = 15, command = self.go_next, state = 'disabled', font = font2)
        self.bottom_right.pack(side = 'right', fill = 'y', expand = True)

        self.count = 0
        self.key = ''
        self.grid_5_onoff = 0
        self.grid_100_onoff = 0
        self.canvas_centerX = 556
        self.canvas_centerY = 255
        self.x_mouse = 556
        self.y_mouse = 255
        self.percentage = 1
        self.check_state = 0
        self.current_check = ''
        self.anno_reject_cont = []
        self.content = []
        self.dragInfo = {}
        self.obj_label = ['Bounding Box', 'Polygon']

        self.canvas.bind("<MouseWheel>", self.mouse_wheel)
        self.canvas.bind("<Button-2>", self.click_c)
        self.root.bind("<KeyPress>", self.key_down)
        self.canvas.bind("<Button-1>", self.onPressToMove)
        self.canvas.bind("<ButtonRelease-1>", self.onReleaseToMove)
        self.canvas.bind("<B1-Motion>", self.onMovement)
        self.root.bind('<Configure>', self.resize_handler)

        self.root.protocol("WM_DELETE_WINDOW", self.save_exit) # 호출될 함수를 콜백으로 등록
        self.root.mainloop()

        # normal frame size = 1350 x 820, canvas size = 1112 x 510, width_no_canvas = 238, height_no_canvas = 310
        # max frame size = 1536 x 841, canvas size = (1536 - 238 = 1298) x (841 - 310 = 531)

    def queryMousePosition(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt

    def resize_handler(self, event):
        self.old_state = self.new_state # assign the old state value
        self.new_state = self.root.state() # get the new state value

        # 모니터 해상도 얻기
        # monitor_width = self.root.winfo_screenwidth()
        # monitor_height = self.root.winfo_screenheight()
        # monitor_width, monitor_height = GetSystemMetrics(0), GetSystemMetrics(1)

        mousePos = self.queryMousePosition()
        # print("This is your mouse position x: ", mousePos.x, " y:", mousePos.y)

        # MonitorFromPoint constants 
        # https://msdn.microsoft.com/en-us/library/dd145062(v=vs.85).aspx

        # MONITOR_DEFAULTTONULL    = 0
        # MONITOR_DEFAULTTOPRIMARY = 1
        # MONITOR_DEFAULTTONEAREST = 2
        # winid = windll.user32.MonitorFromPoint(mousePos, MONITOR_DEFAULTTONEAREST)

        if mousePos.x < self.primary_w:
            if self.new_state == 'zoomed':
                screen_width, screen_height = self.primary_w, self.primary_h - 23
                self.canvas_width = screen_width - 238
                self.canvas_height = screen_height - 310
                self.canvas.configure(width = self.canvas_width, height = self.canvas_height)
            elif self.new_state == 'normal' and self.old_state == 'zoomed':
                screen_width, screen_height = self.frame_width, self.frame_height - 23
                self.canvas_width = self.frame_width - 238
                self.canvas_height = self.frame_height - 310
                self.canvas.configure(width = self.canvas_width, height = self.canvas_height)
            else:
                screen_width, screen_height = self.frame_width,self.frame_height - 23
                self.canvas_width = screen_width - 238
                self.canvas_height = screen_height - 310
                self.canvas.configure(width = self.canvas_width, height = self.canvas_height)
        else:
            if self.new_state == 'zoomed':
                screen_width, screen_height = self.secondary_w, self.secondary_h - 23
                self.canvas_width = screen_width - 238
                self.canvas_height = screen_height - 310
                self.canvas.configure(width = self.canvas_width, height = self.canvas_height)
            elif self.new_state == 'normal' and self.old_state == 'zoomed':
                screen_width, screen_height = self.frame_width, self.frame_height - 23
                self.canvas_width = self.frame_width - 238
                self.canvas_height = self.frame_height - 310
                self.canvas.configure(width = self.canvas_width, height = self.canvas_height)
            else:
                screen_width, screen_height = self.frame_width,self.frame_height - 23
                self.canvas_width = screen_width - 238
                self.canvas_height = screen_height - 310
                self.canvas.configure(width = self.canvas_width, height = self.canvas_height)

    def resize(self, event):
        print("New size is: {}x{}".format(event.width, event.height))

    def key_down(self, e):
        self.key = str(e.keysym) # 모든 키 이벤트
        if self.key == 'Left':
            if self.bottom_left.cget('state') == 'normal':
                self.go_pre()
        elif self.key == 'Right':
            if self.bottom_right.cget('state') == 'normal':
                self.go_next()

    def image_dir(self):
        now = datetime.now()
        self.date = '{}{:02d}{:02d}'.format(now.year, now.month, now.day)
        self.image_direct = filedialog.askdirectory(title = '이미지 폴더 열기.', initialdir = self.current_path)
        if self.image_direct:
            self.image_folder4.configure(state = 'normal')
            self.image_folder2.configure(state = 'normal')
            self.image_folder2.delete(0, END)
            self.image_folder2.insert(0, self.image_direct)
            self.image_folder2.configure(state = 'readonly')
            self.meta_data.configure(text = '')
            self.anno_label.configure(text = '')
            self.canvas_centerX = self.canvas_width / 2
            self.canvas_centerY = self.canvas_height / 2
            photo = PhotoImage()
            self.canvas.create_image(self.canvas_centerX, self.canvas_centerY, image = photo)
            self.canvas.image_names = photo
            self.reject_report_label.configure(text = '')
            self.reject_reason_chkbox.set('')
            self.statistics_reject.configure(text = '반려 : {0:<10}'.format(''))
            self.statistics_pass.configure(text = '통과 : {0:<10}'.format(''))

            open_path = self.image_direct
            open_dir_list = os.listdir(open_path)
            open_dir_list1 = []
            self.tot_file_qy = 0
            for x in open_dir_list:
                if os.path.isdir('{}/{}'.format(open_path, x)):
                    open_dir_list1.append(x)
            if len(open_dir_list1) > 0:
                for x in open_dir_list1:
                    open_image_list = os.listdir('{}/{}'.format(open_path, x))
                    for y in open_image_list:
                        if y.strip().split('.')[-1] != 'jpg':
                            os.remove('{}\{}\{}'.format(open_path, x, y))
                    open_image_list = os.listdir('{}/{}'.format(open_path, x))
                    self.tot_file_qy += len(open_image_list)
            else:
                open_image_list = open_dir_list
                self.tot_file_qy += len(open_image_list)
            self.current_qy = 0
            self.prog_rate.configure(text = '{} / {}'.format(self.current_qy, self.tot_file_qy))

    def pre_data_load(self):
        folder_order, image_order = 0, 0
        self.reject_change, self.del_change_try = 0, 0
        self.reject_button.config(state = 'normal')
        self.pass_button.config(state = 'normal')
        try:
            if os.path.isfile('create/{}_검수결과.csv'.format(self.date)):
                response = msgbox.askyesno('예/아니오', '금일 검수결과 파일이 존재합니다.\n계속 이어서 작업하시겠습니까?\n\
이어서 작업하시려면 "예", 삭제 후 다시 작업하시려면 "아니오"를 눌러 주세요.')
                if response:
                    f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    change_line = csv.DictReader(f, fieldnames = f_field_name)
                    change_lines = []
                    for x in change_line:
                        if x['No.'] != '':
                            change_lines.append(x)
                    f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                    for y in change_lines:
                        f_writer.writerow(y)
                    f.close()
                else:
                    shutil.copyfile('create/{}_검수결과.csv'.format(self.date), 'create/{}_검수결과.bak'.format(self.date))
                    os.remove('create/{}_검수결과.csv'.format(self.date))
            self.data_load(image_order, folder_order, 0)
            self.image_folder4.configure(state = 'disabled')
            self.grid_left_button.configure(state = 'normal')
            self.grid_right_button.configure(state = 'normal')
            self.bottom_right.configure(state = 'normal')
        except:
            msgbox.showinfo('알림', 'create/{}_검수결과.csv 파일이 열려 있으면 닫고 다시 진행해 주세요.\n\
또는 이미지 폴더 위치에 xml 파일이 있는지 확인해 주세요.'.format(self.date))

    def data_load(self, image_order, folder_order, obj_order):
        self.folder_order = folder_order
        self.image_order = image_order
        self.obj_order = obj_order
        self.obj_label_order = 0
        if self.image_direct:
            self.img_folders = os.listdir(self.image_direct)
            self.img_folders1 = []
            for x in self.img_folders:
                if os.path.isdir('{}/{}'.format(self.image_direct, x)):
                    self.img_folders1.append(x)
            if len(self.img_folders) != 0:
                if len(self.img_folders1) > 0:
                    self.folder_qy = 1
                    self.parent_direct = Path(self.image_direct).parent.absolute()
                    parent_files = os.listdir(self.image_direct)
                    self.xml_files = []
                    for xx in parent_files:
                        if xx.strip().split('.')[-1] == 'xml':
                            self.xml_files.append(xx)
                    self.img_files = os.listdir('{}/{}'.format(self.image_direct, self.img_folders1[self.folder_order]))
                    for xx in self.img_files:
                        check_path = '{}/{}/{}'.format(self.image_direct, self.img_folders1[self.folder_order], xx)
                        if xx.strip().split('.')[-1] != 'jpg':
                            os.remove(check_path)
                    self.img_files = os.listdir('{}/{}'.format(self.image_direct, self.img_folders1[self.folder_order]))
                    if len(self.img_files) != 0:
                        self.get_xml_data(self.image_direct, self.img_files[self.image_order])
                        self.check_object1()
                        self.check_object = 1
                        self.check_report(self.img_files[self.image_order])
                    else:
                        msgbox.showwarning('경고', '파일이 존재하지 않습니다.')
                        self.bottom_right.configure(state = 'disabled')
                else:
                    self.folder_qy = 0
                    self.parent_direct = Path(self.image_direct).parent.absolute()
                    parent_direct_name = self.image_direct.strip().split('/')[-1]
                    # grand_parent_direct = Path(parent_direct).parent.absolute()
                    parent_files = os.listdir(self.parent_direct)
                    self.xml_files = []
                    for xx in parent_files:
                        if xx.strip().split('.')[-1] == 'xml':
                            self.xml_files.append(xx)
                    self.img_files = os.listdir(self.image_direct)
                    for xx in self.img_files:
                        check_path = '{}/{}'.format(self.image_direct, xx)
                        if xx.strip().split('.')[-1] != 'jpg':
                            os.remove(check_path)
                    self.img_files = os.listdir(self.image_direct)
                    if len(self.img_files) != 0:
                        self.get_xml_data(self.parent_direct, self.img_files[self.image_order])
                        self.check_object2()
                        self.check_object = 2
                        self.check_report(self.img_files[self.image_order])
                    else:
                        msgbox.showwarning('경고', '파일이 존재하지 않습니다.')
                        self.bottom_right.configure(state = 'disabled')
            else:
                msgbox.showwarning('경고', '폴더 또는 파일이 존재하지 않습니다.')
                self.bottom_right.configure(state = 'disabled')

    def get_xml_data(self, folder_name, img_file):
        for xx in self.xml_files:
            in_file = open('{}/{}'.format(folder_name, xx), encoding = 'utf-8')
            tree = ET.parse(in_file)
            xml_root = tree.getroot()
            image_element = []
            tot_boxes = []
            tot_polygons = []
            for x in xml_root:
                if x.tag == 'version':
                    version = xml_root.find('version').text
                elif x.tag == 'meta':
                    meta = xml_root.find('meta')
                    for y in meta:
                        if y.tag == 'task':
                            task = meta.find('task')
                            task_elements = []
                            for z in task:
                                task_element = [z.tag, task.find(z.tag).text]
                                task_elements.append(task_element)
                        elif y.tag == 'dumped':
                            dumped = meta.find('dumped').text
                elif x.tag == 'image':
                    boxes_info = []
                    polygons_info = []
                    image_element.append(x.attrib)
                    if x.find('box'):
                        for box in x.iter('box'):
                            box_attrib = box.find('attribute')
                            box_info = [box.attrib, box_attrib.attrib, box_attrib.text]
                            boxes_info.append(box_info)
                        tot_boxes.append(boxes_info)
                    else:
                        boxes_info = []
                        tot_boxes.append(boxes_info)
                    if x.find('polygon'):
                        for polygon in x.iter('polygon'):
                            polygon_attrib = polygon.find('attribute')
                            polygon_info = [polygon.attrib, polygon_attrib.attrib, polygon_attrib.text]
                            polygons_info.append(polygon_info)
                        tot_polygons.append(polygons_info)
                    else:
                        polygons_info = []
                        tot_polygons.append(polygons_info)
            tot_meta_data = ''
            self.meta_label_lst = []
            for z in task_elements:
                if z[0] != 'flipped' and '\n' not in str(z[1]):
                    tot_meta_data += '{} : {},   '.format(z[0], z[1])
                elif z[0] == 'flipped' and '\n' not in str(z[1]):
                    tot_meta_data += '{} : {},\n'.format(z[0], z[1])
                if z[0] == 'labels':
                    labels = task.find('labels')
                    labels_info = []
                    for a in labels.iter('label'):
                        for b in a:
                            if b.tag == 'name':
                                 name = a.find(b.tag).text
                            elif b.tag == 'attributes':
                                attributes = a.find(b.tag)
                                for c in attributes.iter('attribute'):
                                    label_info = '\nlabels > label > name : {}   > attributes > attribute >'.format(name)
                                    for d in c:
                                        if d.tag == 'values':
                                            values_txt = c.find(d.tag).text
                                            values_txt = values_txt.replace('\n', '/')
                                            label_info += ' {} : {},'.format(d.tag, values_txt)
                                        else:
                                            label_info += ' {} : {},  '.format(d.tag, c.find(d.tag).text)
                                    labels_info.append(label_info)
                        self.meta_label_lst.append(name)
                    for x in labels_info:
                        tot_meta_data += '{}'.format(x)
                elif z[0] == 'segments':
                    segments = task.find('segments')
                    segments_info = []
                    for a in segments.iter('segment'):
                        segment_info = '\nsegments > segment >'
                        for b in a:
                            segment_info += ' {} : {},  '.format(b.tag, a.find(b.tag).text)
                        segments_info.append(segment_info)
                    for x in segments_info:
                        tot_meta_data += '{}'.format(x)
                elif z[0] == 'owner':
                    owner = task.find('owner')
                    owner_info = '\nowner >'
                    for a in owner:
                        owner_info += ' {} : {},   '.format(a.tag, owner.find(a.tag).text)
                    tot_meta_data += owner_info
            tot_meta_data += 'dumped : {}'.format(dumped)
            
            for zzz in self.img_files:
                for xxx in image_element:
                    if zzz == xxx['name']:
                        cur_xml_file = xx
                        break
                    else:
                        cur_xml_file = ''
                if cur_xml_file == xx:
                    break
            if cur_xml_file == xx:
                break

        if cur_xml_file == xx:
            self.xml_exist = 0
            self.xml_info = 0
            for idx, xxx in enumerate(image_element):
                self.bbox_posi = []
                self.poly_posi = []
                bbox_label = []
                poly_label = []
                bbox_label_new = []
                poly_label_new = []
                bbox_anno_dict = {}
                poly_anno_dict = {}
                self.bbox_emotion = {}
                self.poly_emotion = {}
                if xxx['name'] == img_file:
                    meta_data1 = 'version : {},   {}'.format(version, tot_meta_data)
                    self.meta_data.configure(text = meta_data1)
                    tot_anno_data = '폴더명 : {},   이미지 ID : {},   파일명 : {},   width : {},   height : {},'\
                        .format(folder_name, xxx['id'], xxx['name'], xxx['width'], xxx['height'])
                    bbox_label1 = tot_boxes[idx]
                    poly_label1 = tot_polygons[idx]
                    if len(bbox_label1) != 0:
                        for aa in bbox_label1:
                            bbox_label.append(aa[0]['label'])
                            label_name = '{}-{}'.format(aa[0]['label'], bbox_label.count(aa[0]['label']))
                            bbox_label_new.append(label_name)
                            bbox_anno = '\nBounding box > label : {},   occluded : {},   z_order : {},   Attribute > name : {} > {}'\
                                        .format(label_name, aa[0]['occluded'], aa[0]['z_order'], aa[1]['name'], aa[2])
                            bbox_posi1 = [[label_name], [aa[0]['xtl'], aa[0]['ytl'], aa[0]['xbr'], aa[0]['ybr']], [aa[1]['name'], aa[2]]]
                            self.bbox_posi.append(bbox_posi1)
                            bbox_anno_dict[label_name] = bbox_anno
                            self.bbox_emotion[label_name] = aa[2]
                    if len(poly_label1) != 0:
                        for bb in poly_label1:
                            poly_label.append(bb[0]['label'])
                            label_name = '{}-{}'.format(bb[0]['label'], poly_label.count(bb[0]['label']))
                            poly_label_new.append(label_name)
                            poly_anno = '    |    Polygon > label : {},   occluded : {},   z_order : {},   Attribute > name : {} > {}'\
                                        .format(label_name, bb[0]['occluded'], bb[0]['z_order'], bb[1]['name'], bb[2])
                            poly_posi = bb[0]['points'].replace(';', ',')
                            poly_posi1 = poly_posi.strip().split(',')
                            poly_posi2 = [[label_name], poly_posi1, [bb[1]['name'], bb[2]]]
                            self.poly_posi.append(poly_posi2)
                            poly_anno_dict[label_name] = poly_anno
                            self.poly_emotion[label_name] = bb[2]
                    self.union_labels = sorted(list(set(bbox_label) | set(poly_label)))        
                    self.inter_labels = sorted(list(set(bbox_label) & set(poly_label)))
                    self.diff_b_labels = sorted(list(set(bbox_label) - set(poly_label)))
                    self.diff_p_labels = sorted(list(set(poly_label) - set(bbox_label)))
                    self.union_labels_new = sorted(list(set(bbox_label_new) | set(poly_label_new)))
                    self.inter_labels_new = sorted(list(set(bbox_label_new) & set(poly_label_new)))
                    self.diff_b_labels_new = sorted(list(set(bbox_label_new) - set(poly_label_new)))
                    self.diff_p_labels_new = sorted(list(set(poly_label_new) - set(bbox_label_new)))
                    self.labels_name_lst = self.union_labels_new
                    self.bbox_dual_label = []
                    self.poly_dual_label = []
                    if self.union_labels:
                        for cc in self.union_labels:
                            if cc in self.inter_labels:
                                if bbox_label.count(cc) == poly_label.count(cc):
                                    for i in range(bbox_label.count(cc)):
                                        label_name1 = '{}-{}'.format(cc, i + 1)
                                        tot_anno_data += bbox_anno_dict[label_name1]
                                        tot_anno_data += poly_anno_dict[label_name1]
                                    if bbox_label.count(cc) > 1:
                                        self.bbox_dual_label.append([cc, bbox_label.count(cc)])
                                        self.poly_dual_label.append([cc, poly_label.count(cc)])
                                else:
                                    if bbox_label.count(cc) > poly_label.count(cc):
                                        for i in range(bbox_label.count(cc)):
                                            label_name1 = '{}-{}'.format(cc, i + 1)
                                            tot_anno_data += bbox_anno_dict[label_name1]
                                            if poly_anno_dict[label_name1]:
                                                tot_anno_data += poly_anno_dict[label_name1]
                                            else:
                                                poly_anno1 = '    |    Polygon > <{}> Polygon 작업 안됨(미태깅)'.format(label_name1)
                                                tot_anno_data += poly_anno1
                                        if bbox_label.count(cc) > 1:
                                            self.bbox_dual_label.append([cc, bbox_label.count(cc)])
                                        if poly_label.count(cc) > 1:
                                            self.poly_dual_label.append([cc, poly_label.count(cc)])
                                    else:
                                        for i in range(poly_label.count(cc)):
                                            label_name1 = '{}-{}'.format(cc, i + 1)
                                            if bbox_anno_dict[label_name1]:
                                                tot_anno_data += bbox_anno_dict[label_name1]
                                            else:
                                                bbox_anno1 = '\nBounding box > <{}> Bounding Box 작업 안됨(미태깅)'.format(label_name1)
                                                tot_anno_data += bbox_anno1
                                            tot_anno_data += poly_anno_dict[label_name1]
                                        if bbox_label.count(cc) > 1:
                                            self.bbox_dual_label.append([cc, bbox_label.count(cc)])
                                        if poly_label.count(cc) > 1:
                                            self.poly_dual_label.append([cc, poly_label.count(cc)])
                            elif cc in self.diff_b_labels:
                                for i in range(bbox_label.count(cc)):
                                    label_name1 = '{}-{}'.format(cc, i + 1)
                                    tot_anno_data += bbox_anno_dict[label_name1]
                                    poly_anno1 = '    |    Polygon > <{}> Polygon 작업 안됨(미태깅)'.format(label_name1)
                                    tot_anno_data += poly_anno1
                                    poly_posi2 = [[label_name1]]
                                    self.poly_posi.append(poly_posi2)
                                if bbox_label.count(cc) > 1:
                                    self.bbox_dual_label.append([cc, bbox_label.count(cc)])
                            elif cc in self.diff_p_labels:
                                for i in range(poly_label.count(cc)):
                                    label_name1 = '{}-{}'.format(cc, i + 1)
                                    bbox_anno1 = '\nBounding box > <{}> Bounding Box 작업 안됨(미태깅)'.format(label_name1)
                                    tot_anno_data += bbox_anno1
                                    tot_anno_data += poly_anno_dict[label_name1]
                                    bbox_posi1 = [[label_name1]]
                                    self.bbox_posi.append(bbox_posi1)
                                if poly_label.count(cc) > 1:
                                    self.poly_dual_label.append([cc, poly_label.count(cc)])
                    else:
                        bbox_anno1 = '\nBounding box > 객체에 대한 Bounding Box 작업 안됨(미태깅)'
                        tot_anno_data += bbox_anno1
                        poly_anno1 = '    |    Polygon > 객체에 대한 Polygon 작업 안됨(미태깅)'
                        tot_anno_data += poly_anno1
                        bbox_posi1 = [['']]
                        self.bbox_posi.append(bbox_posi1)
                        poly_posi2 = [['']]
                        self.poly_posi.append(poly_posi2)
                    self.anno_label.configure(text = tot_anno_data)
                    self.xml_exist = 1
                    self.xml_info = 0
                    break
                else:
                    meta_data1 = 'version : {},   {}'.format(version, tot_meta_data)
                    self.meta_data.configure(text = meta_data1)
                    tot_anno_data = '폴더명 : {},   파일명 : {}\nXML에 이미지 정보 누락'\
                        .format(folder_name, img_file)
                    self.anno_label.configure(text = tot_anno_data)
                    self.xml_exist = 1
                    self.xml_info = 1
        else:
            meta_data1 = '이미지 관련 XML 파일 누락'
            self.meta_data.configure(text = meta_data1)
            tot_anno_data = 'XML에 이미지 정보 누락'
            self.anno_label.configure(text = tot_anno_data)
            self.xml_exist = 0

    def load_image(self, img_path):
        img_width = self.canvas_width
        img_height = self.canvas_height

        self.img_fpath = '{}/{}'.format(self.image_direct, img_path)
        image = Image.open(self.img_fpath)
        width, height = image.size[0], image.size[1]
        pre_width, pre_height = int(width * img_height / height), img_height
        self.resized_img = image.resize((pre_width, pre_height))

        img = ImageDraw.Draw(self.resized_img)
        var_font = ImageFont.truetype('font/H2HDRM.TTF', 17)
        
        if self.bbox_posi:
            for xx in self.bbox_posi:
                if len(xx) > 1:
                    resized_bbox = []
                    for j in range(len(xx[1])):
                        x = float(xx[1][j]) * img_height / height
                        resized_bbox.append(x)
                    resized_bbox_x = [resized_bbox[i] for i in range(0, len(resized_bbox), 2)]
                    resized_bbox_y = [resized_bbox[i + 1] for i in range(0, len(resized_bbox), 2)]
                    resized_bbox = tuple(resized_bbox)
                    resized_bbox_x_min, resized_bbox_x_max = min(resized_bbox_x), max(resized_bbox_x)
                    resized_bbox_y_min, resized_bbox_y_max = min(resized_bbox_y), max(resized_bbox_y)
                    bbox_txt = '{} : {} > {}'.format(xx[0][0], xx[2][0], xx[2][1])
                    bbox_txt_wrap = textwrap.wrap(bbox_txt)
                    bbox_textsize_w, bbox_textsize_h = img.textsize(bbox_txt_wrap[0], font = var_font)
                    resized_bbox_top = ((resized_bbox_x_min + resized_bbox_x_max) / 2 - bbox_textsize_w / 2, resized_bbox_y_min - 21)
                    # resized_bbox_center = ((resized_bbox_x_min + resized_bbox_x_max) / 2 - 35, (resized_bbox_y_min + resized_bbox_y_max) / 2 - 20)

                    img.rectangle(((resized_bbox[0], resized_bbox[1]), (resized_bbox[2], resized_bbox[3])), outline='green', width=2)
                    img.text((resized_bbox_top), bbox_txt, font = var_font, fill = 'green')
        else:
            pass

        if self.poly_posi:
            for yy in self.poly_posi:
                if len(yy) > 1:
                    resized_poly = []
                    for j in range(len(yy[1])):
                        x = float(yy[1][j]) * img_height / height
                        resized_poly.append(x)
                    resized_poly_x = [resized_poly[i] for i in range(0, len(resized_poly), 2)]
                    resized_poly_y = [resized_poly[i + 1] for i in range(0, len(resized_poly), 2)]
                    resized_poly = tuple(resized_poly)
                    resized_poly_x_min, resized_poly_x_max = min(resized_poly_x), max(resized_poly_x)
                    resized_poly_y_min, resized_poly_y_max = min(resized_poly_y), max(resized_poly_y)
                    poly_txt = '{} : {} > {}'.format(yy[0][0], yy[2][0], yy[2][1])
                    poly_txt_wrap = textwrap.wrap(poly_txt)
                    poly_textsize_w, poly_textsize_h = img.textsize(poly_txt_wrap[0], font = var_font)
                    resized_poly_bottom = ((resized_poly_x_min + resized_poly_x_max) / 2 - poly_textsize_w / 2, resized_poly_y_max + 5)
                    # resized_poly_center = ((resized_poly_x_min + resized_poly_x_max) / 2 - 35, (resized_poly_y_min + resized_poly_y_max) / 2 - 20)

                    img.polygon(resized_poly, fill = None, outline = 'red')
                    img.text((resized_poly_bottom), '{} : {} > {}'.format(yy[0][0], yy[2][0], yy[2][1]), font = var_font, fill = 'red')
        else:
            pass
 
        photo = ImageTk.PhotoImage(self.resized_img)
        self.canvas.create_image(self.canvas_centerX, self.canvas_centerY, image = photo)
        self.canvas.image_names = photo

    def go_pre(self):
        self.canvas_centerX = self.canvas_width / 2
        self.canvas_centerY = self.canvas_height / 2
        self.grid_5_onoff = 0
        self.grid_100_onoff = 0
        self.x_mouse = self.canvas_centerX
        self.y_mouse = self.canvas_centerY
        self.percentage = 1
        self.union_labels = []
        self.union_labels_new = []
        self.inter_labels = []
        self.inter_labels_new = []
        self.diff_b_labels = []
        self.diff_b_labels_new = []
        self.diff_p_labels = []
        self.diff_p_labels_new = []
        self.labels_name_lst = []
        self.reject_button.config(state = 'normal')
        self.pass_button.config(state = 'normal')
        self.image_order -= 1
        if self.image_order < 0:
            self.folder_order -= 1
            if self.folder_order < 0:
                self.bottom_left.configure(state = 'disabled')
                self.bottom_right.configure(state = 'normal')
                self.image_order += 1
                self.folder_order += 1
                msgbox.showwarning('경고', '이전 파일이 존재하지 않습니다.')
            else:
                self.img_files = os.listdir('{}/{}'.format(self.image_direct, self.img_folders1[self.folder_order]))
                self.image_order = len(self.img_files) - 1
                self.reject_reason_chkbox.set('')
                self.data_load(self.image_order, self.folder_order, 0)
        else:
            self.bottom_right.configure(state = 'normal')
            self.reject_reason_chkbox.set('')
            self.data_load(self.image_order, self.folder_order, 0)

    def go_next(self):
        self.canvas_centerX = self.canvas_width / 2
        self.canvas_centerY = self.canvas_height / 2
        self.grid_5_onoff = 0
        self.grid_100_onoff = 0
        self.x_mouse = self.canvas_centerX
        self.y_mouse = self.canvas_centerY
        self.percentage = 1
        self.union_labels = []
        self.union_labels_new = []
        self.inter_labels = []
        self.inter_labels_new = []
        self.diff_b_labels = []
        self.diff_b_labels_new = []
        self.diff_p_labels = []
        self.diff_p_labels_new = []
        self.labels_name_lst = []
        self.image_order += 1
        if self.image_order >= len(self.img_files):
            if self.folder_qy > 1:
                self.folder_order += 1
                if self.folder_order >= len(self.img_folders1):
                    self.bottom_left.configure(state = 'normal')
                    self.bottom_right.configure(state = 'disabled')
                    self.image_order -= 1
                    self.folder_order -= 1
                    self.check_report(self.img_files[self.image_order])
                    msgbox.showwarning('경고', '다음 파일이 존재하지 않습니다.')
                else:
                    self.image_order = 0
                    self.data_load(self.image_order, self.folder_order, 0)
            else:
                self.bottom_left.configure(state = 'normal')
                self.bottom_right.configure(state = 'disabled')
                self.image_order -= 1
                self.check_report(self.img_files[self.image_order])
                msgbox.showwarning('경고', '다음 파일이 존재하지 않습니다.')
        else:
            self.reject_reason_chkbox.set('')
            self.data_load(self.image_order, self.folder_order, 0)
            if self.image_order > 0:
                self.bottom_left.configure(state = 'normal')

    def check_object1(self):
        self.img_path = '{}/{}'.format(self.img_folders1[self.folder_order], self.img_files[self.image_order])
        if self.xml_exist == 1:
            if self.xml_info == 1:
                if self.obj_label_order <= 1:
                    self.load_image(self.img_path)
                    self.reject_reason_object.configure(text = '')
                    self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                    msgbox.showwarning('경고', 'XML에 이미지 정보 누락')
                    self.reject_reason_chkbox.set('XML에 이미지 정보 누락')
                else:
                    self.obj_label_order = 0
            else:
                if self.obj_label_order <= 1:
                    if not self.labels_name_lst:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = '')
                        self.reject_reason_label.configure(text = '')
                        msgbox.showwarning('경고', 'Bounding Box 작업 안됨(미태깅) 및 Polygon 작업 안됨(미태깅)')
                        self.reject_reason_chkbox.set('Bounding Box 작업 안됨(미태깅)')
                    elif self.labels_name_lst[self.obj_order] in self.inter_labels_new:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        if self.bbox_emotion[self.labels_name_lst[self.obj_order]] != self.poly_emotion[self.labels_name_lst[self.obj_order]]:
                            msgbox.showwarning('경고', '{} Bounding Box 감정명 오류(오태깅) 또는 Polygon 감정명 오류(오태깅)'.format(self.labels_name_lst[self.obj_order]))
                    elif self.labels_name_lst[self.obj_order] in self.diff_b_labels_new:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        if self.obj_label_order == 0:
                            self.reject_reason_chkbox.set('')
                        else:
                            msgbox.showwarning('경고', '{} Polygon 작업 안됨(미태깅)'.format(self.labels_name_lst[self.obj_order]))
                            self.reject_reason_chkbox.set('Polygon 작업 안됨(미태깅)')
                    elif self.labels_name_lst[self.obj_order] in self.diff_p_labels_new:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        if self.obj_label_order == 0:
                            msgbox.showwarning('경고', '{} Bounding Box 작업 안됨(미태깅)'.format(self.labels_name_lst[self.obj_order]))
                            self.reject_reason_chkbox.set('Bounding Box 작업 안됨(미태깅)')
                        else:
                            self.reject_reason_chkbox.set('')
                else:
                    self.obj_label_order = 0        
                warning = ''
                if len(self.bbox_dual_label) >= 1:
                    for x in self.bbox_dual_label:
                        warning += '{} 객체 Bounding Box가 {}개 존재합니다.\n'.format(x[0], x[1])
                    msgbox.showwarning('경고', warning)
                if len(self.poly_dual_label) >= 1:
                    for x in self.poly_dual_label:
                        warning += '{} 객체 Polygon이 {}개 존재합니다.\n'.format(x[0], x[1])
                    msgbox.showwarning('경고', warning)
        else:
            self.load_image(self.img_path)
            self.reject_reason_object.configure(text = '')
            self.reject_reason_label.configure(text = '')
            msgbox.showwarning('경고', '이미지 관련 XML 파일 누락')
            self.reject_reason_chkbox.set('이미지 관련 XML 파일 누락')

    def check_object2(self):
        self.img_path = '{}'.format(self.img_files[self.image_order])
        if self.xml_exist == 1:
            if self.xml_info == 1:
                if self.obj_label_order <= 1:
                    self.load_image(self.img_path)
                    self.reject_reason_object.configure(text = '')
                    self.reject_reason_label.configure(text = '')
                    msgbox.showwarning('경고', 'XML에 이미지 정보 누락')
                    self.reject_reason_chkbox.set('XML에 이미지 정보 누락')
                else:
                    self.obj_label_order = 0
            else:
                if self.obj_label_order <= 1:
                    if not self.labels_name_lst[self.obj_order]:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        msgbox.showwarning('경고', '{} Bounding Box 작업 안됨(미태깅) 및 Polygon 작업 안됨(미태깅)'.format(self.labels_name_lst[self.obj_order]))
                        self.reject_reason_chkbox.set('Bounding Box 작업 안됨(미태깅)')
                    elif self.labels_name_lst[self.obj_order] in self.inter_labels_new:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                    elif self.labels_name_lst[self.obj_order] in self.diff_b_labels_new:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        if self.obj_label_order == 0:
                            self.reject_reason_chkbox.set('')
                        else:
                            msgbox.showwarning('경고', '{} Polygon 작업 안됨(미태깅)'.format(self.labels_name_lst[self.obj_order]))
                            self.reject_reason_chkbox.set('Polygon 작업 안됨(미태깅)')
                    elif self.labels_name_lst[self.obj_order] in self.diff_p_labels_new:
                        self.load_image(self.img_path)
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        if self.obj_label_order == 0:
                            msgbox.showwarning('경고', '{} Bounding Box 작업 안됨(미태깅)'.format(self.labels_name_lst[self.obj_order]))
                            self.reject_reason_chkbox.set('Bounding Box 작업 안됨(미태깅)')
                        else:
                            self.reject_reason_chkbox.set('')
                else:
                    self.obj_label_order = 0
                warning = ''
                if len(self.bbox_dual_label) >= 1:
                    for x in self.bbox_dual_label:
                        warning += '{} 객체 Bounding Box가 {}개 존재합니다.\n'.format(x[0], x[1])
                    msgbox.showwarning('경고', warning)
                if len(self.poly_dual_label) >= 1:
                    for x in self.poly_dual_label:
                        warning += '{} 객체 Polygon이 {}개 존재합니다.\n'.format(x[0], x[1])
                    msgbox.showwarning('경고', warning)
        else:
            self.load_image(self.img_path)
            self.reject_reason_object.configure(text = '')
            self.reject_reason_label.configure(text = '')
            msgbox.showwarning('경고', '이미지 관련 XML 파일 누락')
            self.reject_reason_chkbox.set('이미지 관련 XML 파일 누락')

    def check_report(self, check_img):
        self.check_state = 0
        tot_check_report = ''
        if not os.path.isfile('create/{}_검수결과.csv'.format(self.date)):
            self.reject_report_label.configure(text = '{}/{} 검수 진행 중'.format(self.image_order + 1, self.tot_file_qy))
            self.check_state = 0
        else:
            f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'cp949')
            f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
            check_line = csv.DictReader(f, fieldnames = f_field_name)
            curr_result_lst = []
            break_point = 0
            for xx in check_line:
                if xx['이미지'] == check_img:
                    break_point = 1
                    self.check_state = 1
                    curr_result_lst.append(xx['검수 결과'])
                    check_txt = '   {} : {} {} > {},'.format(xx['객체'], xx['라벨링'], xx['검수 결과'], xx['반려 사유'])
                    tot_check_report += check_txt
                    self.reject_reason_chkbox.set('')
                elif xx['이미지'] != check_img and break_point == 1:
                    break
            if '반려' in curr_result_lst:
                self.curr_result = '반려'
            else:
                self.curr_result = '통과'
            self.reject_report_label.configure(text = '{}/{} 검수 완료 : {}'.format(self.image_order + 1, self.tot_file_qy, self.curr_result))
            if self.check_state == 0:
                self.reject_report_label.configure(text = '{}/{} 검수 진행 중'.format(self.image_order + 1, self.tot_file_qy))
                tot_check_report = ''
            f.close()
            self.bottom_text.configure(text = tot_check_report)

    def anno_reject(self):
        if self.check_state == 0:
            if self.reject_reason_chkbox.get():
                self.img_reject_pass_lst.append('반려')
                self.bottom_left.configure(state = 'disabled')
                self.bottom_right.configure(state = 'disabled')
                self.reject_end_button.configure(state = 'normal')
                if not os.path.isfile('create/{}_검수결과.csv'.format(self.date)):
                    report = {'No.' : 1, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                        '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '반려', '반려 사유' : self.reject_reason_chkbox.get()}
                    f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                    f_writer.writeheader()
                    f_writer.writerow(report)
                    f.close()
                    self.anno_reject_cont.append(self.reject_reason_chkbox.get())
                    self.content.append('  {} : {} 반려 > {}\n'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text'), self.reject_reason_chkbox.get()))
                    self.current_check = ''
                    for x in self.content:
                        self.current_check += x
                else:
                    if self.reject_reason_chkbox.get() not in self.anno_reject_cont:
                        f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
                        line_no = len(list(csv.reader(f, delimiter = ',')))
                        report = {'No.' : line_no, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                            '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '반려', '반려 사유' : self.reject_reason_chkbox.get()}
                        f = open('create/{}_검수결과.csv'.format(self.date), 'at', encoding = 'CP949', newline = '')
                        f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                        f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                        f_writer.writerow(report)
                        f.close()
                        self.anno_reject_cont.append(self.reject_reason_chkbox.get())
                        self.content.append('   {} : {} 반려 > {},'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text'), self.reject_reason_chkbox.get()))
                        self.current_check = ''
                        for x in self.content:
                            self.current_check += x
                    else:
                        response = msgbox.askyesno('예/아니오', '반려 사유가 이미 존재합니다. 기존 반려를 취소 하시겠습니까?')
                        if response:
                            f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
                            f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                            change_line = csv.DictReader(f, fieldnames = f_field_name)
                            change_lines = []
                            for x in change_line:
                                if x['이미지'] != self.img_files[self.image_order]:
                                    change_lines.append(x)
                                else:
                                    if x['객체'] != self.reject_reason_object.cget('text'):
                                        change_lines.append(x)
                                    else:
                                        if x['반려 사유'] != self.reject_reason_chkbox.get():
                                            change_lines.append(x)
                            f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
                            f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                            f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                            for y in change_lines:
                                f_writer.writerow(y)
                            f.close()
                            self.anno_reject_cont.remove(self.reject_reason_chkbox.get())
                            self.content.remove('   {} : {} 반려 > {},'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text'), self.reject_reason_chkbox.get()))
                            self.current_check = ''
                            for x in self.content:
                                self.current_check += x
                self.bottom_text.configure(text = self.current_check)
                # self.reject_reason_chkbox.set('')
            else:
                msgbox.showwarning('경고', '반려 사유를 선택하지 않았습니다.')
        else:
            if self.del_change_try == 0:
                response = msgbox.askokcancel('확인/취소', '{} 검수 결과를 삭제하고 다시 검수합니다. 계속 진행하시겠습니까?'\
                    .format(self.img_files[self.image_order]))
                if response == 1:
                    self.content = []
                    self.bottom_left.configure(state = 'disabled')
                    self.bottom_right.configure(state = 'disabled')
                    self.del_change(self.img_files[self.image_order])
                    self.add_rejt_change()
                    self.reject_change = 1
            else:
                self.add_rejt_change()

    def anno_pass(self):
        if self.check_state == 0:
            if not self.reject_reason_chkbox.get():
                self.img_reject_pass_lst.append('통과')
                if not os.path.isfile('create/{}_검수결과.csv'.format(self.date)):
                    report = {'No.' : 1, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                        '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '통과', '반려 사유' : ''}
                    f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                    f_writer.writeheader()
                    f_writer.writerow(report)
                    f.close()
                else:
                    f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
                    line_no = len(list(csv.reader(f, delimiter = ',')))
                    f.close()
                    report = {'No.' : line_no, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                        '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '통과', '반려 사유' : ''}
                    f = open('create/{}_검수결과.csv'.format(self.date), 'at', encoding = 'CP949', newline = '')
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                    f_writer.writerow(report)
                    f.close()
                    if self.current_qy == self.tot_file_qy:
                        self.reject_report_label.configure(text = '{}/{} 검수 완료'.format(self.current_qy, self.tot_file_qy))
                        self.reject_button.config(state = 'disabled')
                        self.pass_button.config(state = 'disabled')
                self.content.append('   {} : {} 통과 > ,'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text')))
                self.current_check = ''
                for x in self.content:
                    self.current_check += x
                self.bottom_text.configure(text = self.current_check)
                self.obj_label_order += 1
                if self.obj_label_order < 2:
                    if self.check_object == 1:
                        self.check_object1()
                    else:
                        self.check_object2()
                if self.obj_label_order > 1:
                    self.obj_order += 1
                    self.obj_label_order = 0
                    if self.obj_order < len(self.labels_name_lst):
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                        self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                        if self.check_object == 1:
                            self.check_object1()
                        else:
                            self.check_object2()
                        self.bottom_left.configure(state = 'disabled')
                        self.bottom_right.configure(state = 'disabled')
                    else:
                        if '반려' not in self.img_reject_pass_lst:
                            self.tot_reject_pass_lst.append('통과')
                            self.statistics_pass.configure(text = '통과 : {0:<10}'.format(self.tot_reject_pass_lst.count('통과')))
                            self.progress()
                            self.reject_reason_chkbox.set('')
                            self.reject_reason_object.configure(text = '')
                            self.reject_reason_label.configure(text = '')
                            self.bottom_left.configure(state = 'normal')
                            self.bottom_right.configure(state = 'normal')
                            self.current_check = ''
                            self.bottom_text.configure(text = self.current_check)
                            self.content = []
                            self.img_reject_pass_lst = []
                            self.go_next()
                        else:
                            self.tot_reject_pass_lst.append('반려')
                            self.statistics_reject.configure(text = '반려 : {0:<10}'.format(self.tot_reject_pass_lst.count('반려')))
                            self.progress()
                            self.reject_reason_chkbox.set('')
                            self.reject_reason_object.configure(text = '')
                            self.reject_reason_label.configure(text = '')
                            self.bottom_left.configure(state = 'normal')
                            self.bottom_right.configure(state = 'normal')
                            self.current_check = ''
                            self.bottom_text.configure(text = self.current_check)
                            self.content = []
                            self.img_reject_pass_lst = []
                            self.go_next()
                else:
                    if len(self.labels_name_lst):
                        self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                    else:
                        self.reject_reason_object.configure(text = '')
                    self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                    self.bottom_left.configure(state = 'disabled')
                    self.bottom_right.configure(state = 'disabled')
            else:
                msgbox.showwarning('경고', '반려 사유를 선택하고 통과를 누르셨습니다.')
                self.reject_reason_chkbox.set('')
        else:
            if self.del_change_try == 0:
                response = msgbox.askokcancel('확인/취소', '{} 검수 결과를 삭제하고 다시 검수합니다. 계속 진행하시겠습니까?'\
                    .format(self.img_files[self.image_order]))
                if response == 1:
                    self.content = []
                    self.bottom_left.configure(state = 'disabled')
                    self.bottom_right.configure(state = 'disabled')
                    self.del_change(self.img_files[self.image_order])
                    self.add_pass_change()
            else:
                self.add_pass_change()

    def del_change(self, image):
        self.reject_end_button.configure(state = 'normal')
        f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
        f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
        change_line = csv.DictReader(f, fieldnames = f_field_name)
        change_lines = []
        for x in change_line:
            if x['이미지'] != image:
                change_lines.append(x)
        f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
        f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
        f_writer = csv.DictWriter(f, fieldnames = f_field_name)
        for y in change_lines:
            f_writer.writerow(y)
        f.close()
        self.del_change_try = 1

    def add_rejt_change(self):
        self.change_reject_pass_lst.append('반려')
        if self.reject_reason_chkbox.get():
            self.bottom_left.configure(state = 'disabled')
            self.bottom_right.configure(state = 'disabled')
            self.reject_end_button.configure(state = 'normal')
            if not os.path.isfile('create/{}_검수결과.csv'.format(self.date)):
                report = {'No.' : 1, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                    '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '반려', '반려 사유' : self.reject_reason_chkbox.get()}
                f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
                f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                f_writer.writeheader()
                f_writer.writerow(report)
                f.close()
                self.anno_reject_cont.append(self.reject_reason_chkbox.get())
                self.content.append('  {} : {} 반려 > {}\n'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text'), self.reject_reason_chkbox.get()))
                self.current_check = ''
                for x in self.content:
                    self.current_check += x
            else:
                if self.reject_reason_chkbox.get() not in self.anno_reject_cont:
                    f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
                    line_no = len(list(csv.reader(f, delimiter = ',')))
                    report = {'No.' : line_no, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                        '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '반려', '반려 사유' : self.reject_reason_chkbox.get()}
                    f = open('create/{}_검수결과.csv'.format(self.date), 'at', encoding = 'CP949', newline = '')
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                    f_writer.writerow(report)
                    f.close()
                    self.anno_reject_cont.append(self.reject_reason_chkbox.get())
                    self.content.append('   {} : {} 반려 > {},'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text'), self.reject_reason_chkbox.get()))
                    self.current_check = ''
                    for x in self.content:
                        self.current_check += x
                else:
                    response = msgbox.askyesno('예/아니오', '반려 사유가 이미 존재합니다. 기존 반려를 취소 하시겠습니까?')
                    if response:
                        f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
                        f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                        change_line = csv.DictReader(f, fieldnames = f_field_name)
                        change_lines = []
                        for x in change_line:
                            if x['이미지'] != self.img_files[self.image_order]:
                                change_lines.append(x)
                            else:
                                if x['객체'] != self.reject_reason_object.cget('text'):
                                    change_lines.append(x)
                                else:
                                    if x['반려 사유'] != self.reject_reason_chkbox.get():
                                        change_lines.append(x)
                        f = open('create/{}_검수결과.csv'.format(self.date), 'w', encoding = 'CP949', newline = '')
                        f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                        f_writer = csv.DictWriter(f, fieldnames = f_field_name)
                        for y in change_lines:
                            f_writer.writerow(y)
                        f.close()
                        self.anno_reject_cont.remove(self.reject_reason_chkbox.get())
                        self.content.remove('   {} : {} 반려 > {},'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text'), self.reject_reason_chkbox.get()))
                        self.current_check = ''
                        for x in self.content:
                            self.current_check += x
            self.bottom_text.configure(text = self.current_check)
        else:
             msgbox.showwarning('경고', '반려 사유를 선택하지 않았습니다.')

    def add_pass_change(self):
        self.change_reject_pass_lst.append('통과')
        if not self.reject_reason_chkbox.get():
            self.reject_end_button.configure(state = 'normal')
            f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'CP949')
            line_no = len(list(csv.reader(f, delimiter = ',')))
            f.close()
            report = {'No.' : line_no, '폴더' : self.image_direct, '이미지' : self.img_files[self.image_order],\
                '객체' : self.reject_reason_object.cget('text'), '라벨링' : self.reject_reason_label.cget('text'), '검수 결과' : '통과', '반려 사유' : self.reject_reason_chkbox.get()}
            f = open('create/{}_검수결과.csv'.format(self.date), 'at', encoding = 'CP949', newline = '')
            f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
            f_writer = csv.DictWriter(f, fieldnames = f_field_name)
            f_writer.writerow(report)
            f.close()
            self.reject_reason_chkbox.set('')
        else:
            msgbox.showwarning('경고', '반려 사유를 선택하고 통과를 누르셨습니다.')
            self.reject_reason_chkbox.set('')
        self.content.append('   {} : {} 통과 > ,'.format(self.reject_reason_object.cget('text'), self.reject_reason_label.cget('text')))
        self.current_check = ''
        for x in self.content:
            self.current_check += x
        self.bottom_text.configure(text = self.current_check)
        self.obj_label_order += 1
        if self.obj_label_order < 2:
            if self.check_object == 1:
                self.check_object1()
            else:
                self.check_object2()
        if self.obj_label_order > 1:
            self.obj_order += 1
            self.obj_label_order = 0
            if self.obj_order < len(self.labels_name_lst):
                self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                self.bottom_left.configure(state = 'disabled')
                self.bottom_right.configure(state = 'disabled')
                if self.check_object == 1:
                    self.check_object1()
                else:
                    self.check_object2()
            else:
                if '반려' not in self.change_reject_pass_lst and self.curr_result == '반려':
                    self.tot_reject_pass_lst.remove('반려')
                    self.tot_reject_pass_lst.append('통과')
                    self.statistics_reject.configure(text = '반려 : {0:<10}'.format(self.tot_reject_pass_lst.count('반려')))
                    self.statistics_pass.configure(text = '통과 : {0:<10}'.format(self.tot_reject_pass_lst.count('통과')))
                elif '반려' in self.change_reject_pass_lst and self.curr_result == '통과':
                    self.tot_reject_pass_lst.remove('통과')
                    self.tot_reject_pass_lst.append('반려')
                    self.statistics_reject.configure(text = '반려 : {0:<10}'.format(self.tot_reject_pass_lst.count('반려')))
                    self.statistics_pass.configure(text = '통과 : {0:<10}'.format(self.tot_reject_pass_lst.count('통과')))
                self.reject_reason_chkbox.set('')
                self.reject_reason_object.configure(text = '')
                self.reject_reason_label.configure(text = '')
                self.go_next()
                self.del_change_try = 0
                self.bottom_left.configure(state = 'normal')
                self.bottom_right.configure(state = 'normal')
                self.check_report(self.img_files[self.image_order])
        else:
            if len(self.labels_name_lst):
                self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
            else:
                self.reject_reason_object.configure(text = '')
            self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
            self.bottom_left.configure(state = 'disabled')
            self.bottom_right.configure(state = 'disabled')

    def reject_next(self):
        self.anno_reject_cont = []
        self.reject_reason_chkbox.set('')
        if self.reject_change == 0:
            self.obj_label_order += 1
            if self.obj_label_order > 1:
                self.obj_order += 1
                self.obj_label_order = 0
                if self.obj_order < len(self.labels_name_lst):
                    self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                    self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                    self.bottom_left.configure(state = 'disabled')
                    self.bottom_right.configure(state = 'disabled')
                    if self.check_object == 1:
                        self.check_object1()
                    else:
                        self.check_object2()
                else:
                    if '반려' in self.img_reject_pass_lst:
                        self.tot_reject_pass_lst.append('반려')
                        self.statistics_reject.configure(text = '반려 : {0:<10}'.format(self.tot_reject_pass_lst.count('반려')))
                        self.progress()
                        self.reject_reason_object.configure(text = '')
                        self.reject_reason_label.configure(text = '')
                        if self.current_qy == self.tot_file_qy:
                            self.reject_report_label.configure(text = '{}/{} 검수 완료'.format(self.current_qy, self.tot_file_qy))
                            self.reject_button.config(state = 'normal')
                            self.pass_button.config(state = 'normal')
                        self.current_check = ''
                        self.content = []
                        self.img_reject_pass_lst = []
                        self.bottom_text.configure(text = self.current_check)
                        self.go_next()
                        self.bottom_left.configure(state = 'normal')
                        self.bottom_right.configure(state = 'normal')
            else:
                if self.obj_label_order < 2:
                    if self.check_object == 1:
                        self.check_object1()
                    else:
                        self.check_object2()
                if len(self.labels_name_lst):
                    self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                else:
                    self.reject_reason_object.configure(text = '')
                self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                self.bottom_left.configure(state = 'disabled')
                self.bottom_right.configure(state = 'disabled')
                self.reject_end_button.configure(state = 'disabled')
        else:
            self.obj_label_order += 1
            if self.obj_label_order > 1:
                self.obj_order += 1
                self.obj_label_order = 0
                if self.obj_order < len(self.labels_name_lst):
                    self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                    self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                    self.bottom_left.configure(state = 'disabled')
                    self.bottom_right.configure(state = 'disabled')
                    if self.check_object == 1:
                        self.check_object1()
                    else:
                        self.check_object2()
                else:
                    if '반려' in self.change_reject_pass_lst and self.curr_result == '통과':
                        self.tot_reject_pass_lst.remove('통과')
                        self.tot_reject_pass_lst.append('반려')
                        self.statistics_reject.configure(text = '반려 : {0:<10}'.format(self.tot_reject_pass_lst.count('반려')))
                        self.statistics_pass.configure(text = '통과 : {0:<10}'.format(self.tot_reject_pass_lst.count('통과')))
                    elif '반려' not in self.change_reject_pass_lst and self.curr_result == '반려':
                        self.tot_reject_pass_lst.remove('반려')
                        self.tot_reject_pass_lst.append('통과')
                        self.statistics_reject.configure(text = '반려 : {0:<10}'.format(self.tot_reject_pass_lst.count('반려')))
                        self.statistics_pass.configure(text = '통과 : {0:<10}'.format(self.tot_reject_pass_lst.count('통과')))
                    self.reject_reason_chkbox.set('')
                    self.reject_reason_object.configure(text = '')
                    self.reject_reason_label.configure(text = '')
                    self.current_check = ''
                    self.content = []
                    self.bottom_text.configure(text = self.current_check)
                    self.go_next()
                    self.del_change_try = 0
                    self.bottom_left.configure(state = 'normal')
                    self.bottom_right.configure(state = 'normal')
                    self.check_report(self.img_files[self.image_order])
            else:
                if self.obj_label_order < 2:
                    if self.check_object == 1:
                        self.check_object1()
                    else:
                        self.check_object2()
                if len(self.labels_name_lst):
                    self.reject_reason_object.configure(text = self.labels_name_lst[self.obj_order])
                else:
                    self.reject_reason_object.configure(text = '')
                self.reject_reason_label.configure(text = self.obj_label[self.obj_label_order])
                self.bottom_left.configure(state = 'disabled')
                self.bottom_right.configure(state = 'disabled')
                self.reject_end_button.configure(state = 'disabled')
            self.reject_end_button.configure(state = 'disabled')

    def save_exit(self):
        try :
            response = msgbox.askyesno('종료', '최종 검수 결과를 저장 후 종료합니다.\n프로그램 종료 후 금일 다시 계속 작업하려면 \
"아니오"를 눌러 주세요.')
            if response:
                if os.path.isfile('create/{}_검수결과.csv'.format(self.date)):
                    f_field_name = ['No.', '폴더', '이미지', '객체', '라벨링', '검수 결과', '반려 사유']
                    f = open('create/{}_검수결과.csv'.format(self.date), 'r', encoding = 'cp949')
                    cont = csv.DictReader(f, fieldnames = f_field_name)
                    image_name = ''
                    reject_pass_lsts = []
                    tot_reject_pass = []
                    final_report = []
                    reject_count, no_xml_count, no_info_count, bbox_null_err, poly_null_err = 0, 0, 0, 0, 0
                    bbox_label_err1, poly_label_err1 = {}, {}
                    bbox_label_err2, poly_label_err2 = {}, {}
                    bbox_wrong_wok, poly_wrong_wok = {}, {}
                    bbox_over_wok, poly_over_wok = {}, {}
                    bbox_no_work, poly_no_work = {}, {}
                    tot_bbox_reject_count, tot_poly_reject_count = {}, {}
                    bbox_pass_obj_lst, poly_pass_obj_lst = [], []
                    tot_bbox_pass_obj_lst, tot_poly_pass_obj_lst = [], []
                    bbox_reject_obj_lst, poly_reject_obj_lst = [], []
                    tot_bbox_reject_obj_lst, tot_poly_reject_obj_lst = [], []
                    tot_object_lst = []
                    tot_bbox_pass_obj_qy, tot_poly_pass_obj_qy = 0, 0
                    tot_bbox_reject_obj_qy, tot_poly_reject_obj_qy = 0, 0
                    for x in cont:
                        if image_name == '':
                            image_name = x['이미지']
                            reject_pass_lst = [x['객체'], x['라벨링'], x['검수 결과'], x['반려 사유']]
                            reject_pass_lsts.append(reject_pass_lst)
                            if x['라벨링'] == 'Bounding Box':
                                if x['검수 결과'] == '통과':
                                    bbox_pass_obj_lst.append(x['객체'])
                                    tot_object_lst.append(x['객체'])
                                elif x['검수 결과'] == '반려':
                                    bbox_reject_obj_lst.append(x['객체'])
                                    tot_object_lst.append(x['객체'])
                            elif x['라벨링'] == 'Polygon':
                                if x['검수 결과'] == '통과':
                                    poly_pass_obj_lst.append(x['객체'])
                                    tot_object_lst.append(x['객체'])
                                elif x['검수 결과'] == '반려':
                                    poly_reject_obj_lst.append(x['객체'])
                                    tot_object_lst.append(x['객체'])
                        else:
                            if x['이미지'] == image_name:
                                reject_pass_lst = [x['객체'], x['라벨링'], x['검수 결과'], x['반려 사유']]
                                reject_pass_lsts.append(reject_pass_lst)
                                if x['라벨링'] == 'Bounding Box':
                                    if x['검수 결과'] == '통과':
                                        bbox_pass_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                    elif x['검수 결과'] == '반려':
                                        bbox_reject_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                elif x['라벨링'] == 'Polygon':
                                    if x['검수 결과'] == '통과':
                                        poly_pass_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                    elif x['검수 결과'] == '반려':
                                        poly_reject_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                            else:
                                tot_reject_pass.append(reject_pass_lsts)
                                tot_bbox_pass_obj_lst.append(bbox_pass_obj_lst)
                                tot_bbox_reject_obj_lst.append(bbox_reject_obj_lst)
                                tot_poly_pass_obj_lst.append(poly_pass_obj_lst)
                                tot_poly_reject_obj_lst.append(poly_reject_obj_lst)
                                reject_pass_lsts = []
                                bbox_pass_obj_lst, poly_pass_obj_lst = [], []
                                bbox_reject_obj_lst, poly_reject_obj_lst = [], []
                                reject_pass_lst = [x['객체'], x['라벨링'], x['검수 결과'], x['반려 사유']]
                                reject_pass_lsts.append(reject_pass_lst)
                                if x['라벨링'] == 'Bounding Box':
                                    if x['검수 결과'] == '통과':
                                        bbox_pass_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                    elif x['검수 결과'] == '반려':
                                        bbox_reject_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                elif x['라벨링'] == 'Polygon':
                                    if x['검수 결과'] == '통과':
                                        poly_pass_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                    elif x['검수 결과'] == '반려':
                                        poly_reject_obj_lst.append(x['객체'])
                                        tot_object_lst.append(x['객체'])
                                image_name = x['이미지']
                    tot_reject_pass.append(reject_pass_lsts)
                    tot_bbox_pass_obj_lst.append(bbox_pass_obj_lst)
                    tot_bbox_reject_obj_lst.append(bbox_reject_obj_lst)
                    tot_poly_pass_obj_lst.append(poly_pass_obj_lst)
                    tot_poly_reject_obj_lst.append(poly_reject_obj_lst)
                    tot_object_lst = sorted(list(set(tot_object_lst)))
                    tot_object_lst.remove('')
                    f.close()
                    total_count = len(tot_reject_pass) - 1
                    tot_reject_obj = {}
                    for yy in tot_reject_pass:
                        reject_exist = 0
                        reject_obj = {}
                        for i in range(len(yy)):
                            if yy[i][3] == 'Bounding Box 캐릭터명 오류(오태깅)':
                                if yy[i][0] not in bbox_label_err1.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_label_err1[yy[i][0]] = 1
                                elif yy[i][0] in bbox_label_err1.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_label_err1[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    bbox_null_err += 1
                            elif yy[i][3] == 'Bounding Box 감정명 오류(오태깅)':
                                if yy[i][0] not in bbox_label_err2.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_label_err2[yy[i][0]] = 1
                                elif yy[i][0] in bbox_label_err2.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_label_err2[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    bbox_null_err += 1
                            elif yy[i][3] == '잘못된 Bounding Box 작업(오태깅)':
                                if yy[i][0] not in bbox_wrong_wok.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_wrong_wok[yy[i][0]] = 1
                                elif yy[i][0] in bbox_wrong_wok.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_wrong_wok[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    bbox_null_err += 1
                            elif yy[i][3] == '불필요한 Bounding Box 작업(과태깅)':
                                if yy[i][0] not in bbox_wrong_wok.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_over_wok[yy[i][0]] = 1
                                elif yy[i][0] in bbox_wrong_wok.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_over_wok[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    bbox_null_err += 1
                            elif yy[i][3] == 'Bounding Box 작업 안됨(미태깅)':
                                if yy[i][0] not in bbox_no_work.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_no_work[yy[i][0]] = 1
                                elif yy[i][0] in bbox_no_work.keys() and yy[i][1] == 'Bounding Box':
                                    bbox_no_work[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    bbox_null_err += 1
                            elif yy[i][3] == 'Polygon 캐릭터명 오류(오태깅)':
                                if yy[i][0] not in poly_label_err1.keys() and yy[i][1] == 'Polygon':
                                    poly_label_err1[yy[i][0]] = 1
                                elif yy[i][0] in poly_label_err1.keys() and yy[i][1] == 'Polygon':
                                    poly_label_err1[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    poly_null_err += 1
                            elif yy[i][3] == 'Polygon 감정명 오류(오태깅)':
                                if yy[i][0] not in poly_label_err2.keys() and yy[i][1] == 'Polygon':
                                    poly_label_err2[yy[i][0]] = 1
                                elif yy[i][0] in poly_label_err2.keys() and yy[i][1] == 'Polygon':
                                    poly_label_err2[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    poly_null_err += 1
                            elif yy[i][3] == '잘못된 Polygon 작업(오태깅)':
                                if yy[i][0] not in poly_wrong_wok.keys() and yy[i][1] == 'Polygon':
                                    poly_wrong_wok[yy[i][0]] = 1
                                elif yy[i][0] not in poly_wrong_wok.keys() and yy[i][1] == 'Polygon':
                                    poly_wrong_wok[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    poly_null_err += 1
                            elif yy[i][3] == '불필요한 Polygon 작업(과태깅)':
                                if yy[i][0] not in bbox_wrong_wok.keys() and yy[i][1] == 'Polygon':
                                    poly_over_wok[yy[i][0]] = 1
                                elif yy[i][0] in bbox_wrong_wok.keys() and yy[i][1] == 'Polygon':
                                    poly_over_wok[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    poly_null_err += 1
                            elif yy[i][3] == 'Polygon 작업 안됨(미태깅)':
                                if yy[i][0] not in poly_no_work.keys() and yy[i][1] == 'Polygon':
                                    poly_no_work[yy[i][0]] = 1
                                elif yy[i][0] in poly_no_work.keys() and yy[i][1] == 'Polygon':
                                    poly_no_work[yy[i][0]] += 1
                                if yy[i][0] == '':
                                    poly_null_err += 1
                            elif yy[i][3] == '이미지 관련 XML 파일 누락':
                                no_xml_count += 1
                            elif yy[i][3] == 'XML에 이미지 정보 누락':
                                no_info_count += 1

                            if yy[i][2] == '반려':
                                reject_exist = 1
                                reject_obj[yy[i][0]] = 1

                        if reject_exist == 1:
                            reject_count += 1
                        for x in reject_obj.keys():
                            if x not in tot_reject_obj:
                                tot_reject_obj[x] = reject_obj[x]
                            else:
                                tot_reject_obj[x] += reject_obj[x]
                    
                    pass_count = total_count - reject_count
                    for k in tot_object_lst:
                        if k in bbox_label_err1.keys():
                            if k not in tot_bbox_reject_count.keys():
                                tot_bbox_reject_count[k] = bbox_label_err1[k]
                            else:
                                tot_bbox_reject_count[k] += bbox_label_err1[k]
                        if k in bbox_label_err2.keys():
                            if k not in tot_bbox_reject_count.keys():
                                tot_bbox_reject_count[k] = bbox_label_err2[k]
                            else:
                                tot_bbox_reject_count[k] += bbox_label_err2[k]
                        if k in bbox_wrong_wok.keys():
                            if k not in tot_bbox_reject_count.keys():
                                tot_bbox_reject_count[k] = bbox_wrong_wok[k]
                            else:
                                tot_bbox_reject_count[k] += bbox_wrong_wok[k]
                        if k in bbox_over_wok.keys():
                            if k not in tot_bbox_reject_count.keys():
                                tot_bbox_reject_count[k] = bbox_over_wok[k]
                            else:
                                tot_bbox_reject_count[k] += bbox_over_wok[k]
                        if k in bbox_no_work.keys():
                            if k not in tot_bbox_reject_count.keys():
                                tot_bbox_reject_count[k] = bbox_no_work[k]
                            else:
                                tot_bbox_reject_count[k] += bbox_no_work[k]
                        if k in  poly_label_err1.keys():
                            if k not in tot_poly_reject_count.keys():
                                tot_poly_reject_count[k] =  poly_label_err1[k]
                            else:
                                tot_poly_reject_count[k] +=  poly_label_err1[k]
                        if k in  poly_label_err2.keys():
                            if k not in tot_poly_reject_count.keys():
                                tot_poly_reject_count[k] =  poly_label_err2[k]
                            else:
                                tot_poly_reject_count[k] +=  poly_label_err2[k]
                        if k in  poly_wrong_wok.keys():
                            if k not in tot_poly_reject_count.keys():
                                tot_poly_reject_count[k] =  poly_wrong_wok[k]
                            else:
                                tot_poly_reject_count[k] +=  poly_wrong_wok[k]
                        if k in  poly_over_wok.keys():
                            if k not in tot_poly_reject_count.keys():
                                tot_poly_reject_count[k] =  poly_over_wok[k]
                            else:
                                tot_poly_reject_count[k] +=  poly_over_wok[k]
                        if k in  poly_no_work.keys():
                            if k not in tot_poly_reject_count.keys():
                                tot_poly_reject_count[k] =  poly_no_work[k]
                            else:
                                tot_poly_reject_count[k] +=  poly_no_work[k]

                    for aa in range(len(tot_bbox_pass_obj_lst)):
                        tot_bbox_pass_obj_qy += len(list(set(tot_bbox_pass_obj_lst[aa])))
                    for bb in range(len(tot_bbox_reject_obj_lst)):
                        tot_bbox_reject_obj_qy += len(list(set(tot_bbox_reject_obj_lst[bb])))
                    for cc in range(len(tot_poly_pass_obj_lst)):
                        tot_poly_pass_obj_qy += len(list(set(tot_poly_pass_obj_lst[cc])))
                    for dd in range(len(tot_poly_reject_obj_lst)):
                        tot_poly_reject_obj_qy += len(list(set(tot_poly_reject_obj_lst[dd])))
                    tot_pass_reject_obj = int(tot_bbox_pass_obj_qy + tot_bbox_reject_obj_qy - no_xml_count/2 - no_info_count/2)
                    tot_bbox_reject_obj_qy = int(tot_bbox_reject_obj_qy - no_xml_count/2 - no_info_count/2)
                    tot_poly_reject_obj_qy = int(tot_poly_reject_obj_qy - no_xml_count/2 - no_info_count/2)
                    sum_bbox_reject_count1 = sum(tot_bbox_reject_count.values())
                    sum_poly_reject_count1 = sum(tot_poly_reject_count.values())
                    sum_reject_obj_qy = int(sum(tot_reject_obj.values()) - no_xml_count/2 - no_info_count/2)
                    tot_bbox_poly_reject_obj_qy = int(tot_bbox_reject_obj_qy + tot_poly_reject_obj_qy - sum_reject_obj_qy)
                    sum_null_error = bbox_null_err + poly_null_err
                    sum_reject_count = sum_bbox_reject_count1 + sum_poly_reject_count1 + no_xml_count + no_info_count
                    final_report.append(['', '> 전체 이미지 {} 건 중 반려 이미지 {} 건, 통과 이미지 {} 건'.\
                        format(total_count, reject_count, pass_count)])
                    final_report.append(['', '> 전체 객체 {} 건 중 반려 객체 {} 건'.\
                        format(tot_pass_reject_obj, sum_reject_obj_qy)])
                    final_report.append(['', '> 전체 반려 객체 {} 건 중 Bounding Box 반려 객체 {} 건, Polygon 반려 객체 {} 건, Bounding Box/Polygon 반려 객체 {} 건'.\
                        format(sum_reject_obj_qy, tot_bbox_reject_obj_qy, tot_poly_reject_obj_qy, tot_bbox_poly_reject_obj_qy)])
                    sub_report = '> 전체 반려 {} 건 중\n   "이미지 관련 XML 파일 누락" {} 건, "XML에 이미지 정보 누락" {} 건 외\n\
   "Bounding Box" 반려 {} 건, "Polygon" 반려 {} 건\n'.format(sum_reject_count, no_xml_count, no_info_count, sum_bbox_reject_count1, sum_poly_reject_count1)
                    if len(tot_bbox_reject_count.keys()) > 0:
                        bbox_obj_no = 0
                        for xx in tot_bbox_reject_count.keys():
                            if bbox_obj_no < 2:
                                sub_report1 = '   "{}" 관련 Bounding Box 반려 {} 건'.format(xx, tot_bbox_reject_count[xx])
                                sub_report += sub_report1
                                bbox_obj_no += 1
                            else:
                                sub_report1 = '   "{}" 관련 Bounding Box 반려 {} 건\n'.format(xx, tot_bbox_reject_count[xx])
                                sub_report += sub_report1
                                bbox_obj_no = 0
                        if bbox_null_err > 0:
                            if bbox_obj_no < 2:
                                sub_report1 = '   "" 관련 Bounding Box 반려 {} 건\n'.format(bbox_null_err)
                                sub_report += sub_report1
                            else:
                                sub_report1 = '\n   "" 관련 Bounding Box 반려 {} 건\n'.format(bbox_null_err)
                                sub_report += sub_report1
                    else:
                        sub_report1 = '   객체별 Bounding Box 반려 없음\n'
                        sub_report += sub_report1
                    sub_report += '\n'
                    poly_obj_no = 0
                    if len(tot_poly_reject_count.keys()) > 0:
                        for xx in tot_poly_reject_count.keys():
                            if poly_obj_no < 2:
                                sub_report1 = '   "{}" 관련 Polygon 반려 {} 건'.format(xx, tot_poly_reject_count[xx])
                                sub_report += sub_report1
                                poly_obj_no += 1
                            else:
                                sub_report1 = '   "{}" 관련 Polygon 반려 {} 건\n'.format(xx, tot_poly_reject_count[xx])
                                sub_report += sub_report1
                                poly_obj_no = 0
                        if poly_null_err > 0:
                            if poly_obj_no < 2:
                                sub_report1 = '   "" 관련 Polygon 반려 {} 건'.format(poly_null_err)
                                sub_report += sub_report1
                            else:
                                sub_report1 = '\n   "" 관련 Polygon 반려 {} 건'.format(poly_null_err)
                                sub_report += sub_report1
                    else:
                        sub_report1 = '   객체별 Polygon 반려 없음'
                        sub_report += sub_report1
                    final_report.append(['', sub_report])
                    sub_report = '> 전체 "Bounding Box 캐릭터명 오류(오태깅)" {} 건 중   '.format(sum(bbox_label_err1.values()))
                    if len(bbox_label_err1.keys()) > 0:
                        for xx in bbox_label_err1.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, bbox_label_err1[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "Bounding Box 감정명 오류(오태깅)" {} 건 중   '.format(sum(bbox_label_err2.values()))
                    if len(bbox_label_err2.keys()) > 0:
                        for xx in bbox_label_err2.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, bbox_label_err2[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "잘못된 Bounding Box 작업(오태깅)" {} 건 중   '.format(sum(bbox_wrong_wok.values()))
                    if len(bbox_wrong_wok.keys()) > 0:
                        for xx in bbox_wrong_wok.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, bbox_wrong_wok[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "불필요한 Bounding Box 작업(과태깅)" {} 건 중   '.format(sum(bbox_over_wok.values()))
                    if len(bbox_over_wok.keys()) > 0:
                        for xx in bbox_over_wok.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, bbox_over_wok[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "Bounding Box 작업 안됨(미태깅)" {} 건 중   '.format(sum(bbox_no_work.values()))
                    if len(bbox_no_work.keys()) > 0:
                        for xx in bbox_no_work.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, bbox_no_work[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "Polygon 캐릭터명 오류(오태깅)" {} 건 중   '.format(sum(poly_label_err1.values()))
                    if len(poly_label_err1.keys()) > 0:
                        for xx in poly_label_err1.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, poly_label_err1[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "Polygon 감정명 오류(오태깅)" {} 건 중   '.format(sum(poly_label_err2.values()))
                    if len(poly_label_err2.keys()) > 0:
                        for xx in poly_label_err2.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, poly_label_err2[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report]) 
                    sub_report = '> 전체 "잘못된 Polygon 작업(오태깅)" {} 건 중   '.format(sum(poly_wrong_wok.values()))
                    if len(poly_wrong_wok.keys()) > 0:
                        for xx in poly_wrong_wok.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, poly_wrong_wok[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "불필요한 Polygon 작업(과태깅)" {} 건 중   '.format(sum(poly_over_wok.values()))
                    if len(poly_over_wok.keys()) > 0:
                        for xx in poly_over_wok.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, poly_over_wok[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])
                    sub_report = '> 전체 "Polygon 작업 안됨(미태깅)" {} 건 중   '.format(sum(poly_no_work.values()))
                    if len(poly_no_work.keys()) > 0:
                        for xx in poly_no_work.keys():
                            sub_report1 = '"{}" 관련 반려 {} 건  '.format(xx, poly_no_work[xx])
                            sub_report += sub_report1
                        final_report.append(['', sub_report])
                    else:
                        sub_report1 = '객체별 반려 없음'
                        sub_report += sub_report1
                        final_report.append(['', sub_report])

                    f = open('create/{}_검수결과.csv'.format(self.date), 'at', encoding = 'cp949', newline = '')
                    f_writer = csv.writer(f, delimiter = ',')
                    for x in final_report:
                        f_writer.writerow(x)
                    f.close()
                    self.root.quit()
                else:
                    msgbox.showinfo('알림', 'create/{}_검수결과.csv 가 없어 저장없이 종료합니다.'.format(self.date))
                    self.root.quit()
            else:
                self.root.quit()
        except:
            msgbox.showinfo('알림', '에러가 발생하여 종료합니다.')
            self.root.quit()

    def progress(self):
        self.current_qy = len(self.tot_reject_pass_lst)

        i = (self.current_qy / self.tot_file_qy) * 100

        self.pro_var.set(i)
        self.progressbar.update()

        state = '{} / {}'.format(self.current_qy, self.tot_file_qy)
        self.prog_rate.configure(text = state)

    def mouse_wheel(self, event):
        if event.delta == -120:
            self.count -= 1
        if event.delta == 120:
            self.count += 1
        if self.count >= -9:
            self.percentage = (100 + 20 * self.count) / 100
        else:
            self.percentage = 0.1
        if self.grid_5_onoff == 1:
            self.grid_5p(self.percentage)
        elif self.grid_100_onoff == 1:
            self.grid_100p(self.percentage)
        else:
            self.grid_5p(self.percentage)

    def click_c(self, event):
        self.percentage = 1
        self.count = 0
        self.grid_5_onoff = 0
        self.grid_100_onoff = 0
        self.canvas_centerX = self.canvas_width / 2
        self.canvas_centerY = self.canvas_height / 2
        self.load_image(self.img_path)

    def grid_5p_start(self):
        if self.grid_100_onoff == 0:
            if self.grid_5_onoff == 0:
                self.grid_5_onoff = 1
            else:
                self.grid_5_onoff = 0
        else:
            self.grid_100_onoff = 0
            self.grid_5_onoff = 1
        self.grid_5p(self.percentage)

    def grid_100p_start(self):
        if self.grid_5_onoff == 0:
            if self.grid_100_onoff == 0:
                self.grid_100_onoff = 1
            else:
                self.grid_100_onoff = 0
        else:
            self.grid_5_onoff = 0
            self.grid_100_onoff = 1
        self.grid_100p(self.percentage)

    def grid_5p(self, percentage):
        diff_x, diff_y = 0, 0
        image = Image.open('{}/{}'.format(self.image_direct, self.img_path))
        width, height = image.size[0], image.size[1]

        bg_img = ImageDraw.Draw(image)
        var_font = ImageFont.truetype('font/H2HDRM.TTF', 17)
            
        if self.bbox_posi:
            for xx in self.bbox_posi:
                if len(xx) > 1:
                    resized_bbox = []
                    for j in range(len(xx[1])):
                        x = float(xx[1][j]) * width / width
                        resized_bbox.append(x)
                    resized_bbox_x = [resized_bbox[i] for i in range(0, len(resized_bbox), 2)]
                    resized_bbox_y = [resized_bbox[i + 1] for i in range(0, len(resized_bbox), 2)]
                    resized_bbox = tuple(resized_bbox)
                    resized_bbox_x_min, resized_bbox_x_max = min(resized_bbox_x), max(resized_bbox_x)
                    resized_bbox_y_min, resized_bbox_y_max = min(resized_bbox_y), max(resized_bbox_y)
                    bbox_txt = '{} : {} > {}'.format(xx[0][0], xx[2][0], xx[2][1])
                    bbox_txt_wrap = textwrap.wrap(bbox_txt)
                    bbox_textsize_w, bbox_textsize_h = bg_img.textsize(bbox_txt_wrap[0], font = var_font)
                    resized_bbox_top = ((resized_bbox_x_min + resized_bbox_x_max) / 2 - bbox_textsize_w / 2, resized_bbox_y_min - 21)
                    # resized_bbox_center = ((resized_bbox_x_min + resized_bbox_x_max) / 2 - 35, (resized_bbox_y_min + resized_bbox_y_max) / 2 - 20)

                    bg_img.rectangle(((resized_bbox[0], resized_bbox[1]), (resized_bbox[2], resized_bbox[3])), outline='green', width=2)
                    bg_img.text((resized_bbox_top), '{} : {} > {}'.format(xx[0][0], xx[2][0], xx[2][1]), font = var_font, fill = 'green')
        else:
            pass
        if self.poly_posi:
            for yy in self.poly_posi:
                if len(yy) > 1:
                    resized_poly = []
                    for j in range(len(yy[1])):
                        x = float(yy[1][j]) * width / width
                        resized_poly.append(x)
                    resized_poly_x = [resized_poly[i] for i in range(0, len(resized_poly), 2)]
                    resized_poly_y = [resized_poly[i + 1] for i in range(0, len(resized_poly), 2)]
                    resized_poly = tuple(resized_poly)
                    resized_poly_x_min, resized_poly_x_max = min(resized_poly_x), max(resized_poly_x)
                    resized_poly_y_min, resized_poly_y_max = min(resized_poly_y), max(resized_poly_y)
                    poly_txt = '{} : {} > {}'.format(yy[0][0], yy[2][0], yy[2][1])
                    poly_txt_wrap = textwrap.wrap(poly_txt)
                    poly_textsize_w, poly_textsize_h = bg_img.textsize(poly_txt_wrap[0], font = var_font)
                    resized_poly_bottom = ((resized_poly_x_min + resized_poly_x_max) / 2 - poly_textsize_w / 2, resized_poly_y_max + 5)
                    # resized_poly_center = ((resized_poly_x_min + resized_poly_x_max) / 2 - 35, (resized_poly_y_min + resized_poly_y_max) / 2 - 20)

                    bg_img.polygon(resized_poly, fill = None, outline = 'red')
                    bg_img.text((resized_poly_bottom), '{} : {} > {}'.format(yy[0][0], yy[2][0], yy[2][1]), font = var_font, fill = 'red')

        if self.grid_5_onoff == 1:
            grid_image = image.copy()

            mask_im = Image.new("L", grid_image.size, 0)
            img = ImageDraw.Draw(mask_im)
            for i in range(0, width, 5):
                img.line((i, 0, i, height), fill="silver", width=1)
            for j in range(0, height, 5):
                img.line((0, j, width, j), fill="silver", width=1)

            grid_image.paste(mask_im, (0, 0), mask_im)
            ch_width = int(width * percentage)
            ch_height = int(height * percentage)
            grid_resized_img = grid_image.resize((ch_width, ch_height))

            photo = ImageTk.PhotoImage(grid_resized_img)
            self.canvas.create_image(self.canvas_centerX, self.canvas_centerY, image = photo)
            self.canvas.image_names = photo
        else:
            ch_width = int(width * percentage)
            ch_height = int(height * percentage)
            resized_img = image.resize((ch_width, ch_height))

            photo = ImageTk.PhotoImage(resized_img)
            self.canvas.create_image(self.canvas_centerX, self.canvas_centerY, image = photo)
            self.canvas.image_names = photo

    def grid_100p(self, percentage):
        self.grid_5_onoff = 0
        diff_x, diff_y = 0, 0
        image = Image.open('{}/{}'.format(self.image_direct, self.img_path))
        width, height = image.size[0], image.size[1]

        bg_img = ImageDraw.Draw(image)
        var_font = ImageFont.truetype('font/H2HDRM.TTF', 17)
        if self.bbox_posi:
            for xx in self.bbox_posi:
                if len(xx) > 1:
                    resized_bbox = []
                    for j in range(len(xx[1])):
                        x = float(xx[1][j]) * width / width
                        resized_bbox.append(x)
                    resized_bbox_x = [resized_bbox[i] for i in range(0, len(resized_bbox), 2)]
                    resized_bbox_y = [resized_bbox[i + 1] for i in range(0, len(resized_bbox), 2)]
                    resized_bbox = tuple(resized_bbox)
                    resized_bbox_x_min, resized_bbox_x_max = min(resized_bbox_x), max(resized_bbox_x)
                    resized_bbox_y_min, resized_bbox_y_max = min(resized_bbox_y), max(resized_bbox_y)
                    bbox_txt = '{} : {} > {}'.format(xx[0][0], xx[2][0], xx[2][1])
                    bbox_txt_wrap = textwrap.wrap(bbox_txt)
                    bbox_textsize_w, bbox_textsize_h = bg_img.textsize(bbox_txt_wrap[0], font = var_font)
                    resized_bbox_top = ((resized_bbox_x_min + resized_bbox_x_max) / 2 - bbox_textsize_w / 2, resized_bbox_y_min - 21)
                    # resized_bbox_center = ((resized_bbox_x_min + resized_bbox_x_max) / 2 - 35, (resized_bbox_y_min + resized_bbox_y_max) / 2 - 20)

                    bg_img.rectangle(((resized_bbox[0], resized_bbox[1]), (resized_bbox[2], resized_bbox[3])), outline='green', width=2)
                    bg_img.text((resized_bbox_top), '{} : {} > {}'.format(xx[0][0], xx[2][0], xx[2][1]), font = var_font, fill = 'green')
        else:
            pass
        if self.poly_posi:
            for yy in self.poly_posi:
                if len(yy) > 1:
                    resized_poly = []
                    for j in range(len(yy[1])):
                        x = float(yy[1][j]) * width / width
                        resized_poly.append(x)
                    resized_poly_x = [resized_poly[i] for i in range(0, len(resized_poly), 2)]
                    resized_poly_y = [resized_poly[i + 1] for i in range(0, len(resized_poly), 2)]
                    resized_poly = tuple(resized_poly)
                    resized_poly_x_min, resized_poly_x_max = min(resized_poly_x), max(resized_poly_x)
                    resized_poly_y_min, resized_poly_y_max = min(resized_poly_y), max(resized_poly_y)
                    poly_txt = '{} : {} > {}'.format(yy[0][0], yy[2][0], yy[2][1])
                    poly_txt_wrap = textwrap.wrap(poly_txt)
                    poly_textsize_w, poly_textsize_h = bg_img.textsize(poly_txt_wrap[0], font = var_font)
                    resized_poly_bottom = ((resized_poly_x_min + resized_poly_x_max) / 2 - poly_textsize_w / 2, resized_poly_y_max + 5)
                    # resized_poly_center = ((resized_poly_x_min + resized_poly_x_max) / 2 - 35, (resized_poly_y_min + resized_poly_y_max) / 2 - 20)

                    bg_img.polygon(resized_poly, fill = None, outline = 'red')
                    bg_img.text((resized_poly_bottom), '{} : {} > {}'.format(yy[0][0], yy[2][0], yy[2][1]), font = var_font, fill = 'red')

        if self.grid_100_onoff == 1:
            grid_image = image.copy()
            mask_im = Image.new("L", grid_image.size, 0)
            img = ImageDraw.Draw(mask_im)
            for i in range(0, width, 100):
                img.line((i, 0, i, height), fill="silver", width=1)
            for j in range(0, height, 100):
                img.line((0, j, width, j), fill="silver", width=1)

            grid_image.paste(mask_im, (0, 0), mask_im)
            ch_width = int(width * percentage)
            ch_height = int(height * percentage)
            grid_resized_img = grid_image.resize((ch_width, ch_height))

            photo = ImageTk.PhotoImage(grid_resized_img)
            self.canvas.create_image(self.canvas_centerX, self.canvas_centerY, image = photo)
            self.canvas.image_names = photo
        else:
            ch_width = int(width * percentage)
            ch_height = int(height * percentage)
            resized_img = image.resize((ch_width, ch_height))

            photo = ImageTk.PhotoImage(resized_img)
            self.canvas.create_image(self.canvas_centerX, self.canvas_centerY, image = photo)
            self.canvas.image_names = photo

    def onPressToMove(self, event): #get initial location of object to be moved
        winX = event.x - self.canvas.canvasx(0)
        winY = event.y - self.canvas.canvasy(0)
        self.dragInfo["Widget"] = self.canvas.find_closest(event.x, event.y, halo = 5)[0]

        # reset the starting point for the next move
        self.dragInfo["xCoord"] = winX
        self.dragInfo["yCoord"] = winY

    def onReleaseToMove(self, event): #reset data on release
        # if self.grid_5_onoff == 1:
        #     self.grid_5p(event.x, event.y, self.percentage)
        # elif self.grid_100_onoff == 1:
        #     self.grid_100p(event.x, event.y, self.percentage)
        # else:
        #     self.grid_5p(event.x, event.y, self.percentage)
        # winX = event.x - self.canvas.canvasx(0)
        # winY = event.y - self.canvas.canvasy(0)
        # newX = winX - self.dragInfo["xCoord"]
        # newY = winY - self.dragInfo["yCoord"]
        self.dragInfo["Widget"] = None
        self.dragInfo["xCoord"] = 0
        self.dragInfo["yCoord"] = 0   

    def onMovement(self, event):
        winX = event.x - self.canvas.canvasx(0)
        winY = event.y - self.canvas.canvasy(0)
        newX = (winX - self.dragInfo["xCoord"]) / 30
        newY = (winY - self.dragInfo["yCoord"]) / 30
        self.canvas.move(self.dragInfo["Widget"], newX, newY)
        self.canvas_centerX += newX
        self.canvas_centerY += newY

    # def drag(self, event):
    #     event.widget.place(x = event.x_root, y = event.y_root, anchor = CENTER)

frameInit()