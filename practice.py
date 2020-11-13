from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert

import time
import pandas
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox

agent_url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(r'D:\pythonTest\v1\Scripts\chromedriver.exe',options=chrome_options)
driver.get(agent_url)
myagent = driver.find_element_by_id('detected_value').text
myagent = myagent.replace('Headless', '')
print(myagent)
driver.quit()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--lang=ko-kr')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user-agent=' + myagent)


driver = webdriver.Chrome(r'D:\pythonTest\v1\Scripts\chromedriver.exe',options=chrome_options)
#driver = webdriver.Chrome()

class_df = pandas.DataFrame(columns=("name", "teacher"))
choose_df = None
select_df = pandas.DataFrame(columns=("name", "url", "time"))
selCount = 0
action = ActionChains(driver)
checklogin = False
videotype = ""



def user_login():
    global driver
    driver.get("https://portal.du.ac.kr/login.jsp")

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "label_pw_input")))
    except:
        driver.quit()

    root = Tk()
    root.title("로그인")
    root.geometry("300x160+500+300") 
    frame1 = Frame(root)
    frame2 = Frame(root)
    frame1.pack(pady = 10)
    frame2.pack(pady = 5)
    
    idlabel = Label(frame1, text="학번")
    idlabel.pack(side='left')
    identry = Entry(frame1, width=20)
    identry.pack(padx=3, pady =5)

    pwlabel = Label(frame2, text="비번")
    pwlabel.pack(side='left')
    pwentry = Entry(frame2, width=20)
    pwentry.pack(padx=3, pady=5)

    
    def buttoncmd():
        id = driver.find_element_by_class_name("label_id_input").find_element_by_name("user_id")
        pw = driver.find_element_by_class_name("label_pw_input").find_element_by_name("user_password")
        login = driver.find_element_by_xpath('//*[@id="loginFrm"]/ul[2]/li/a')
        time.sleep(0.2)

        id.send_keys(identry.get())
        pw.send_keys(pwentry.get())
        identry.delete(0, END)
        pwentry.delete(0, END)

        login.click()
        time.sleep(0.3)
        check_Login()
        
    
    def check_Login():
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "portlet-body")))
            global checklogin
            checklogin = True
            root.destroy()
            root.quit()
            
            elearn = driver.find_element_by_xpath('//*[@id="quicklink_0000000021"]/img')
            elearn.click()
            class_list()
        except:
            msgbox.showinfo("알림", "아이디, 비밀번호를 확인해주세요")
            driver.switch_to_alert().accept()
           
    button = Button(root, width=8, height=3, text="로그인", command=buttoncmd)
    button.pack()

    root.mainloop()

root2 = None
frame2 = None
frame3 = None

def class_list():
    global driver
    global class_df
    global action

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])

    #어도비 flash 허용하기
    # driver.get("chrome://settings/content/flash")
    # time.sleep(3)
    # driver.get_screenshot_as_file("Scrennoption1.png")

    # action.move_by_offset(500, 200)
    # action.click()
    # action.perform()
    # action.reset_actions()
    # driver.get_screenshot_as_file("Scrennoption2.png")

    # time.sleep(1) 
    # driver.back()
    # time.sleep(2)
    def getlist():
        lists = driver.find_elements_by_class_name("course_label_re_02")

        for idx, mylist in enumerate(lists):
            name = mylist.find_element_by_tag_name("h3")
            teacher = mylist.find_element_by_class_name("prof")  

            class_df.loc[idx] = [name, teacher]
    
    getlist()

    WebDriverWait(driver, 1.5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal.notice_popup.ui-draggable")))

    popup = driver.find_elements_by_class_name('modal.notice_popup.ui-draggable')
    count = len(popup)

    for i in range(0, 5):
        try:
            #driver.execute_script("document.getElementsByClassName('modal')[{}].style.display='none';".format(i))
            popup[count-1].find_element_by_class_name('close_notice').click()
            count -= 1
        except:
            pass
    time.sleep(0.5)
    global root2
    global frame2
    global frame3

    root2 = Tk()
    
    frame1 = LabelFrame(root2, text='과목', labelanchor='n', relief='solid', bd=1)
    frame1.pack(fill='both',side='left')
    frame2 = LabelFrame(root2, text='강좌', labelanchor='n', relief='solid', bd=1)
    # frame2.pack(fill='y')
    frame3 = LabelFrame(root2, text="선택된 강좌", labelanchor='n', relief='solid', bd=1)
    frame3.pack(side='right', fill='y')

    #frame3.pack()
    
    def btn_cmd0():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[0]['name'].click()
        choose_class()
    def btn_cmd1():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[1]['name'].click()
        choose_class()
    def btn_cmd2():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[2]['name'].click()
        choose_class()
    def btn_cmd3():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[3]['name'].click()
        choose_class()
    def btn_cmd4():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[4]['name'].click()
        choose_class()
    def btn_cmd5():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[5]['name'].click()
        choose_class()
    def btn_cmd6():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[6]['name'].click()
        choose_class()
    def btn_cmd7():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[7]['name'].click()
        choose_class()
    def btn_cmd8():
        driver.switch_to.window(driver.window_handles[1])
        driver.get('http://lms.du.ac.kr/')
        getlist()
        class_df.loc[8]['name'].click() 
        choose_class()
    

    
    root2.title("동서울대학교 포털시스템")
    try:
        btn0 = Button(frame1, text=class_df.loc[0]['name'].text, width=50, height=3, command=btn_cmd0)
        btn1 = Button(frame1, text=class_df.loc[1]['name'].text, width=50, height=3, command=btn_cmd1)
        btn2 = Button(frame1, text=class_df.loc[2]['name'].text, width=50, height=3, command=btn_cmd2)
        btn3 = Button(frame1, text=class_df.loc[3]['name'].text, width=50, height=3, command=btn_cmd3)
        btn4 = Button(frame1, text=class_df.loc[4]['name'].text, width=50, height=3, command=btn_cmd4)
        btn5 = Button(frame1, text=class_df.loc[5]['name'].text, width=50, height=3, command=btn_cmd5)
        btn6 = Button(frame1, text=class_df.loc[6]['name'].text, width=50, height=3, command=btn_cmd6)
        btn7 = Button(frame1, text=class_df.loc[7]['name'].text, width=50, height=3, command=btn_cmd7)
        btn8 = Button(frame1, text=class_df.loc[8]['name'].text, width=50, height=3, command=btn_cmd8)
        
        btn0.pack(padx=3,pady=3)
        btn1.pack(padx=3,pady=3)
        btn2.pack(padx=3,pady=3)
        btn3.pack(padx=3,pady=3)
        btn4.pack(padx=3,pady=3)
        btn5.pack(padx=3,pady=3)
        btn6.pack(padx=3,pady=3)
        btn7.pack(padx=3,pady=3)
        btn8.pack(padx=3,pady=3)
    except:
        pass

    root2.mainloop()
    

onceCount = 0
calculateTime = 0
timelabel = None
btnCount = 0


def choose_class():
    global driver
    global choose_df
    global select_df
    global selCount
    global videotype
    global root2
    global frame2
    global frame3

    
    choose_df = pandas.DataFrame(columns=("name", "term", "time", "link", "realtime"))
    count = 0
    #time.sleep(1.5)
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "activityinstance")))


    if driver.find_elements_by_class_name('activity.vod.modtype_vod') == []:
        weeks = driver.find_elements_by_class_name('weeks.ubsweeks')
        sections = weeks[2].find_elements_by_class_name('activity.econtents.modtype_econtents')
        videotype = "youtube"
    else:
        weeks = driver.find_elements_by_class_name('weeks.ubsweeks')
        sections = weeks[2].find_elements_by_class_name('activity.vod.modtype_vod')
        videotype = "lms"

    
    for section in sections:
        try:            
            if section.find_element_by_class_name('availabilityinfo') is not None:              
                continue
        except: 
            pass

        try:           
            name = section.find_element_by_class_name('instancename').text
            term = section.find_element_by_class_name('text-ubstrap').text
            videotime = section.find_element_by_class_name('text-info').text
            link = section.find_element_by_tag_name('a').get_attribute('href')

            name = name.replace('이러닝콘텐츠', '')
            name = name.replace('동영상', '').strip()
            term = term.strip()
            videotime = videotime.replace(',', '')
            videotime = videotime.replace(' ', '')
            
            realtime = videotime.replace(":", '')
            
            h = IntVar()
            m = IntVar()

            if int(realtime) >= 10000:
                h = int(int(realtime) / 10000)
                m = int(int(realtime) - (h * 10000))
                m = int(int(m) / 100)
            else:
                h = 0
                m = int(int(realtime) / 100)
            
            realtime = h * 60 + m

            link = link.replace('view', 'viewer')
            
            choose_df.loc[count] = [name, term, videotime, link, str(realtime)]
  
            print(choose_df.loc[count]['name'])
            print(choose_df.loc[count]['term'])
            print(choose_df.loc[count]['time'])
            print(choose_df.loc[count]['link'])
            print(choose_df.loc[count]['realtime'])
            count += 1
        except:
            pass

    def button0():
        global selCount
        name = choose_df.loc[0]['name']
        url = choose_df.loc[0]['link']
        time = choose_df.loc[0]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button1():
        global selCount
        name = choose_df.loc[1]['name']
        url = choose_df.loc[1]['link']
        time = choose_df.loc[1]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button2():
        global selCount
        name = choose_df.loc[2]['name']
        url = choose_df.loc[2]['link']
        time = choose_df.loc[2]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button3():
        global selCount
        name = choose_df.loc[3]['name']
        url = choose_df.loc[3]['link']
        time = choose_df.loc[3]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button4():
        global selCount
        name = choose_df.loc[4]['name']
        url = choose_df.loc[4]['link']
        time = choose_df.loc[4]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button5():
        global selCount
        name = choose_df.loc[5]['name']
        url = choose_df.loc[5]['link']
        time = choose_df.loc[5]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button6():
        global selCount
        name = choose_df.loc[6]['name']
        url = choose_df.loc[6]['link']
        time = choose_df.loc[6]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button7():
        global selCount
        name = choose_df.loc[7]['name']
        url = choose_df.loc[7]['link']
        time = choose_df.loc[7]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button8():
        global selCount
        name = choose_df.loc[8]['name']
        url = choose_df.loc[8]['link']
        time = choose_df.loc[8]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button9():
        global selCount
        name = choose_df.loc[9]['name']
        url = choose_df.loc[9]['link']
        time = choose_df.loc[9]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button10():
        global selCount
        name = choose_df.loc[10]['name']
        url = choose_df.loc[10]['link']
        time = choose_df.loc[10]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button11():
        global selCount
        name = choose_df.loc[11]['name']
        url = choose_df.loc[11]['link']
        time = choose_df.loc[11]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button12():
        global selCount
        name = choose_df.loc[12]['name']
        url = choose_df.loc[12]['link']
        time = choose_df.loc[12]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button13():
        global selCount
        name = choose_df.loc[13]['name']
        url = choose_df.loc[13]['link']
        time = choose_df.loc[13]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button14():
        global selCount
        name = choose_df.loc[14]['name']
        url = choose_df.loc[14]['link']
        time = choose_df.loc[14]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button15():
        global selCount
        name = choose_df.loc[15]['name']
        url = choose_df.loc[15]['link']
        time = choose_df.loc[15]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button16():
        global selCount
        name = choose_df.loc[16]['name']
        url = choose_df.loc[16]['link']
        time = choose_df.loc[16]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button17():
        global selCount
        name = choose_df.loc[17]['name']
        url = choose_df.loc[17]['link']
        time = choose_df.loc[17]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button18():
        global selCount
        name = choose_df.loc[18]['name']
        url = choose_df.loc[18]['link']
        time = choose_df.loc[18]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button19():
        global selCount
        name = choose_df.loc[19]['name']
        url = choose_df.loc[19]['link']
        time = choose_df.loc[19]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    def button20():
        global selCount
        name = choose_df.loc[20]['name']
        url = choose_df.loc[20]['link']
        time = choose_df.loc[20]['realtime']
        select_df.loc[selCount] = [name, url, time]
        show_select(selCount)
        selCount += 1
    

    def calTime():
        global select_df
        global calculateTime
        calculateTime = 0
        for i in range(0, 8):
            try:
                a = select_df.loc[i]['time']
                calculateTime += int(a)
            except:
                break
        h = 0
        m = 0
        if calculateTime > 60:
            h = int(calculateTime / 60)
            m = calculateTime - (h * 60)
        else:
            h = 0
            m = calculateTime
        

        return h, m

    def clear():
        global onceCount
        global select_df
        global selCount
        global frame3
        global timelabel
        global calculateTime
        frame3.destroy()
        frame3 = LabelFrame(root2, text="선택된 강좌", labelanchor='n', relief='solid', bd=1)
        frame3.pack(side='right', fill='y')
        
        select_df = pandas.DataFrame(columns=("name", "url", "time"))
        onceCount = 0
        selCount = 0
        calculateTime = 0

        if onceCount == 0:
            bottomframe = Frame(frame3)
            bottomframe.pack(side='bottom')
            if calTime()[0] == 0:
                timelabel = Label(bottomframe, text="예상시간은 {}분 입니다".format(calTime()[1]))
            else:
                timelabel = Label(bottomframe, text="예상시간은 {}시간 {}분 입니다".format(calTime()[0], calTime()[1]))
            
            resetbtn = Button(bottomframe, text="초기화", width=25, height=2, command=clear)
            startbtn = Button(bottomframe, text="강좌 시작", width=25, height=2, command=videostart)
            timelabel.pack()
            resetbtn.pack(side='left')
            startbtn.pack(side='right')
            onceCount += 1
        
    def videostart():
        global select_df
        global driver
        global flashurl
             
        for i in range(0, 8):
            try:                         
                url = select_df.loc[i]['url']
                driver.switch_to.window(driver.window_handles[1])
                flashurl = "chrome://settings/content/siteDetails?site=https://" + url
                driver.execute_script('window.open(' + '"' +url + '"' + ');')
                control_video()
                time.sleep(1)
            except:
                break
       
        msgbox.showinfo("알림", "영상시청이 완료되었습니다.")
       

                    
    def show_select(index):
        global onceCount
        global timelabel
        selbtn = Button(frame3, text=select_df.loc[index]['name'], width=50, height=3)
        selbtn.pack()
        
        if timelabel is not None:
            if calTime()[0] == 0:
                timelabel.config(text="예상시간은 {}분 입니다".format(calTime()[1]))
            else:
                timelabel.config(text="예상시간은 {}시간 {}분 입니다".format(calTime()[0], calTime()[1]))

        if onceCount == 0:
            bottomframe = Frame(frame3)
            bottomframe.pack(side='bottom')
            if calTime()[0] == 0:
                timelabel = Label(bottomframe, text="예상시간은 {}분 입니다".format(calTime()[1]))
            else:
                timelabel = Label(bottomframe, text="예상시간은 {}시간 {}분 입니다".format(calTime()[0], calTime()[1]))

            resetbtn = Button(bottomframe, text="초기화", width=25, height=2, command=clear)
            startbtn = Button(bottomframe, text="강좌 시작", width=25, height=2, command=videostart)
            timelabel.pack()
            resetbtn.pack(side='left')
            startbtn.pack(side='right')
            onceCount += 1
        
 
    frame2.destroy()
    frame2 = LabelFrame(root2, text='강좌', labelanchor='n', relief='solid', bd=1)
    #frame2 = Frame(root2)
    frame2.pack(side='left', fill='y')
    

    # 스크롤바 추가하기
    mycanvas = Canvas(frame2)
    mycanvas.pack(side='left', fill='both', expand=1)
    scrollbar = ttk.Scrollbar(frame2, orient='vertical', command=mycanvas.yview)
    scrollbar.pack(side='right', fill='y')

    mycanvas.configure(yscrollcommand=scrollbar.set)
    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion = mycanvas.bbox('all')))
    second_frame = Frame(mycanvas)

    mycanvas.create_window((0,0), window=second_frame)
     
    try:              
        btn0 = Button(second_frame, text=choose_df.loc[0]['name'] + "\n" + choose_df.loc[0]['term'] +
        "\t" + choose_df.loc[0]['time'] , width=50, height=3, command=button0)
        btn0.pack(padx=3,pady=3)
        btn1 = Button(second_frame, text=choose_df.loc[1]['name'] + "\n" + choose_df.loc[1]['term'] + 
        "\t" + choose_df.loc[1]['time'] , width=50, height=3, command=button1)
        btn1.pack(padx=3,pady=3)
        btn2 = Button(second_frame, text=choose_df.loc[2]['name'] + "\n" + choose_df.loc[2]['term'] +
        "\t" + choose_df.loc[2]['time'] , width=50, height=3, command=button2)
        btn2.pack(padx=3,pady=3)
        btn3 = Button(second_frame, text=choose_df.loc[3]['name'] + "\n" + choose_df.loc[3]['term'] + 
        "\t" + choose_df.loc[3]['time'] , width=50, height=3, command=button3)
        btn3.pack(padx=3,pady=3)
        btn4 = Button(second_frame, text=choose_df.loc[4]['name'] + "\n" + choose_df.loc[4]['term'] +
        "\t" + choose_df.loc[4]['time'] , width=50, height=3, command=button4)
        btn4.pack(padx=3,pady=3)
        btn5 = Button(second_frame, text=choose_df.loc[5]['name'] + "\n" + choose_df.loc[5]['term'] + 
        "\t" + choose_df.loc[5]['time'] , width=50, height=3, command=button5)
        btn5.pack(padx=3,pady=3)
        btn6 = Button(second_frame, text=choose_df.loc[6]['name'] + "\n" + choose_df.loc[6]['term'] + 
        "\t" + choose_df.loc[6]['time'] , width=50, height=3, command=button6)
        btn6.pack(padx=3,pady=3)
        btn7 = Button(second_frame, text=choose_df.loc[7]['name'] + "\n" + choose_df.loc[7]['term'] + 
        "\t" + choose_df.loc[7]['time'] , width=50, height=3, command=button7)
        btn7.pack(padx=3,pady=3)
        btn8 = Button(second_frame, text=choose_df.loc[8]['name'] + "\n" + choose_df.loc[8]['term'] + 
        "\t" + choose_df.loc[8]['time'] , width=50, height=3, command=button8)
        btn8.pack(padx=3,pady=3)
        btn9 = Button(second_frame, text=choose_df.loc[9]['name'] + "\n" + choose_df.loc[9]['term'] + 
        "\t" + choose_df.loc[9]['time'] , width=50, height=3, command=button9)
        btn9.pack(padx=3,pady=3)
        btn10 = Button(second_frame, text=choose_df.loc[10]['name'] + "\n" + choose_df.loc[10]['term'] + 
        "\t" + choose_df.loc[10]['time'] , width=50, height=3, command=button10)
        btn10.pack(padx=3,pady=3)
        btn11 = Button(second_frame, text=choose_df.loc[11]['name'] + "\n" + choose_df.loc[11]['term'] + 
        "\t" + choose_df.loc[11]['time'] , width=50, height=3, command=button11)
        btn11.pack(padx=3,pady=3)
        btn12 = Button(second_frame, text=choose_df.loc[12]['name'] + "\n" + choose_df.loc[12]['term'] + 
        "\t" + choose_df.loc[12]['time'] , width=50, height=3, command=button12)
        btn12.pack(padx=3,pady=3)
        btn13 = Button(second_frame, text=choose_df.loc[13]['name'] + "\n" + choose_df.loc[13]['term'] + 
        "\t" + choose_df.loc[13]['time'] , width=50, height=3, command=button13)
        btn13.pack(padx=3,pady=3)
        btn14 = Button(second_frame, text=choose_df.loc[14]['name'] + "\n" + choose_df.loc[14]['term'] + 
        "\t" + choose_df.loc[14]['time'] , width=50, height=3, command=button14)
        btn14.pack(padx=3,pady=3)
        btn15 = Button(second_frame, text=choose_df.loc[15]['name'] + "\n" + choose_df.loc[15]['term'] + 
        "\t" + choose_df.loc[15]['time'] , width=50, height=3, command=button15)
        btn15.pack(padx=3,pady=3)
        btn16 = Button(second_frame, text=choose_df.loc[16]['name'] + "\n" + choose_df.loc[16]['term'] + 
        "\t" + choose_df.loc[16]['time'] , width=50, height=3, command=button16)
        btn16.pack(padx=3,pady=3)
        btn17 = Button(second_frame, text=choose_df.loc[17]['name'] + "\n" + choose_df.loc[17]['term'] + 
        "\t" + choose_df.loc[17]['time'] , width=50, height=3, command=button17)
        btn17.pack(padx=3,pady=3)
        btn18 = Button(second_frame, text=choose_df.loc[18]['name'] + "\n" + choose_df.loc[18]['term'] + 
        "\t" + choose_df.loc[18]['time'] , width=50, height=3, command=button18)
        btn18.pack(padx=3,pady=3)
        btn19 = Button(second_frame, text=choose_df.loc[19]['name'] + "\n" + choose_df.loc[19]['term'] + 
        "\t" + choose_df.loc[19]['time'] , width=50, height=3, command=button19)
        btn19.pack(padx=3,pady=3)
        btn20 = Button(second_frame, text=choose_df.loc[20]['name'] + "\n" + choose_df.loc[20]['term'] + 
        "\t" + choose_df.loc[20]['time'] , width=50, height=3, command=button20)
        btn20.pack(padx=3,pady=3)

    except:
        pass



lms_sound = 0
youtube_sound = 0

def control_video():
    global driver
    global videotype
    global action
    global lms_sound
    global youtube_sound
    
 

    time.sleep(3)
    driver.switch_to.window(driver.window_handles[2])
    

    time.sleep(1.5)

    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.window(driver.window_handles[2])

    time.sleep(1.5)    

    try:
        time.sleep(1)
        start = driver.find_element_by_id('vod_player').click()
        print("영상시작버튼클릭")
        
        time.sleep(0.5)

        if lms_sound == 0:
            try:
                sound = driver.find_element_by_class_name('jw-icon.jw-icon-tooltip.jw-icon-volume.jw-button-color.jw-reset').click()
            except:
                pass
            lms_sound += 1
        
        

        fulltime = driver.find_elements_by_class_name('jw-text.jw-reset.jw-text-duration')
        playtime = 0

        try:
            if fulltime[0].text == "":
                playtime = int(fulltime[1].text.replace(':', ""))
            else:
                playtime = int(fulltime[0].text.replace(":", ""))
            
        except:
            playtime = int(fulltime.text.replace(':', ""))
            
        
        

        if playtime >= 10000:
            h = int(playtime / 10000)
            m = int(playtime - (h * 10000))
            m = int(m / 100)
        else:
            h = 0
            m = int(playtime / 100)

        playtime = h * 3600 + m * 60 + 120
        
        time.sleep(playtime)
        

        driver.find_element_by_class_name('vod_close').click()  
        

        time.sleep(1)

        driver.switch_to_alert().accept()
        print("나가기")
               

    except:
        time.sleep(1)
        start = driver.find_element_by_class_name('econtents_viewer')
        start.click()
        time.sleep(1.5)
        
        frame = driver.find_element_by_tag_name('iframe')
        driver.switch_to_frame(frame)

        if youtube_sound == 0:
            sound = driver.find_element_by_class_name('ytp-mute-button.ytp-button')
            sound.click()
            youtube_sound += 1

        fulltime = driver.find_element_by_class_name('ytp-time-duration')

        playtime = int(fulltime.text.replace(":", ""))
        if playtime >= 10000:
            h = int(playtime / 10000)
            m = int(playtime - (h * 10000))
            m = int(m / 100)
        else:
            h = 0
            m = int(playtime / 100)

        playtime = h * 3600 + m * 60 + 120
        
        time.sleep(playtime)

        driver.switch_to_default_content()
        driver.find_element_by_id('econtents_close_button').click()
        time.sleep(1)

        driver.switch_to_alert().accept()

    # if videotype == "lms":
    #     start = driver.find_element_by_id('vod_player')
    #     start.click()
    #     time.sleep(1.5)
                                                    
    #     sound = driver.find_element_by_class_name('jw-icon.jw-icon-tooltip.jw-icon-volume.jw-button-color.jw-reset')
    #     sound.click()

    #     fulltime = driver.find_elements_by_class_name('jw-text.jw-reset.jw-text-duration')
    #     playtime = 0
    #     if fulltime[0].text == "":
    #         playtime = int(fulltime[1].text.replace(':', ""))
    #     else:
    #         playtime = int(fulltime[0].text.replace(":", ""))

    #     print(playtime)

    #     playtime = 3
    #     time.sleep(playtime)

    #     driver.find_element_by_class_name('vod_close').click()
    #     time.sleep(1)

    #     driver.switch_to_alert().accept()
    
    # elif videotype == "youtube":
    #     start = driver.find_element_by_class_name('econtents_viewer')
    #     start.click()
    #     time.sleep(1.5)
        
    #     frame = driver.find_element_by_tag_name('iframe')
    #     driver.switch_to_frame(frame)

    #     sound = driver.find_element_by_class_name('ytp-mute-button.ytp-button')
    #     sound.click()
    #     fulltime = driver.find_element_by_class_name('ytp-time-duration')

    #     #playtime = int(fulltime.text.replace(":", ""))

    #     driver.switch_to_default_content()
    #     driver.find_element_by_id('econtents_close_button').click()

    #     time.sleep(1.5)
    #     driver.switch_to_alert().accept()
        


if __name__ == '__main__':
    user_login()
    

    
    
    




    





     
    

