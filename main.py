import PySimpleGUI as sg 

def check_symbol(lst_nums):
    if len(lst_nums) == 1:
        if lst_nums[0] in ["*", "/"]:
            sg.popup_ok("Error! You have to start with a number or a opening bracket or +/-!\n", background_color = "blue1", no_titlebar = True)
            return lst_nums.pop()
    else:
        if lst_nums[-2] in ["+", "-", "*", "/"]:
            del lst_nums[-2]
            check_symbol(lst_nums)
        elif (lst_nums[-2] == "(" and lst_nums[-1] in ["*", "/"]):
            sg.popup_ok("Error! Before entering symbol (/ or *), there must be a number!\n", background_color = "blue1", no_titlebar = True)
            return lst_nums.pop()

def check_dot(lst_nums):
    if len(lst_nums) == 1:
        return lst_nums.insert(0, "0") 
    else: 
        a = lst_nums[:-1]
        a.reverse()   
        for i in a:
            if i == ".":
                sg.popup_ok("Error! Last number has a decimal separator, you can't add another!\n", background_color = "blue1", no_titlebar = True)
                return lst_nums.pop()
            elif i in ["+", "-", "*", "/", "(", ")"]:
                if not lst_nums[-2].isnumeric():
                    return lst_nums.insert(-1, "0")

def enter(lst_nums):
    #check
    if len(lst_nums) == 0:
        sg.popup_ok("Error! You have to type something in first!\n", background_color = "blue1", no_titlebar = True)
        return lst_nums
    elif lst_nums[-1] in ["+", "-", "*", "/", "("]:
        sg.popup_ok("Error! After symbols there should be a number!\n", background_color = "blue1", no_titlebar = True)
        return lst_nums
    elif lst_nums.count("(") > lst_nums.count(")"):
        sg.popup_ok("Error! You miss some closing bracket, I added them at the end.\n", background_color = "blue1", no_titlebar = True)
        while lst_nums.count("(") > lst_nums.count(")"):
            lst_nums.append(")")
        return lst_nums 
    return True

def brackets(eq):
    print(eq)
    while len(eq) != 1:
        if eq.count("(") != 0:
            start = end = 0
            print(eq)
            end = eq.index(")")
            while eq[start:end].count("(") != 0:
                start += 1
            print(eq[start:end])
            eq[start-1] = math(eq[start:end])         
            del eq[start:end+1]
            print(eq)
        else:
            eq[0] = math(eq)
            del eq[1:]
            print(eq)
    return eq[0]    

def math(eq):
    print(eq, " \n ")
    i = 0
    while len(eq) != 1:
        if eq.count("*") + eq.count("/") != 0:
            i += 1
            if eq[i] == "*":
                eq[i-1] = eq[i-1] * eq[i+1]
                del eq[i:i+2]
                i = 0
            elif eq[i] == "/":
                eq[i-1] = eq[i-1] / eq[i+1]
                del eq[i:i+2]
                i = 0
            print(eq)                    
        else:
            eq[0] = eq[0] + eq[1]
            del eq[1]
            print(eq)        
    return eq[0]

def split(lst_nums):    
    eq =[]
    val = ""
    lst_nums.append("")
    for i, x in enumerate(lst_nums):
        if x in ["+", "-"] and lst_nums[i+1].isnumeric():
            if val != "":
                eq.append(float(val))
                val = ""
            val += x 
        elif x.isnumeric() or x == ".":
            val += x
        elif x in ["-", "+"] and lst_nums[i+1] == "(":
            if val != "":
                eq.append(float(val))
                val = ""
            eq.extend([float(x + "1"), "*"])
        elif x in ["(", ")", "*", "/"]:
            if val != "":
                eq.append(float(val))
                val = ""
            if x == ")" and (lst_nums[i+1].isnumeric() or lst_nums[i+1] == "("):
                eq.extend([x, "*"])                
            elif i !=0:
                if x == "(" and lst_nums[i-1].isnumeric():
                    eq.extend(["*", x])
                else:
                    eq.append(x) 
            else:
                eq.append(x)
    if val != "":
        eq.append(float(val))
        val = ""
    return eq        

sg.theme("PythonPlus")
bs = (5, 1)
col1 = [
    [sg.Button("C", k = "-CLEAR-", size = bs), sg. Button("\u232b", k = "-BACKSP-", size = bs), sg.Button("=", k = "-ENTER-", size = bs, button_color = "green4"), sg.Button("/", size = bs)],
    [sg.Button(7, size = bs), sg.Button(8, size = bs), sg.Button(9, size = bs), sg.Button("*", size = bs)],
    [sg.Button(4, size = bs), sg.Button(5, size = bs), sg.Button(6, size = bs), sg.Button("-", size = bs)],
    [sg.Button(1, size = bs), sg.Button(2, size = bs), sg.Button(3, size = bs), sg.Button("+", size = bs)],
    [sg.Button(0, size = bs, bind_return_key = True), sg.Button("(..", size = bs), sg.Button("..)", size = bs),sg.Button(".", size = bs)]
]
col2 = [
    [sg.Multiline(default_text = "No calculation yet.", disabled = True, k = "-HISTORY-", size = (30, 0), expand_y = True)]
]
layout = [
    [sg.Frame("", [[sg.Text(key = "-OUTPUT-", justification = "right", size = (57,1))]])],
    [sg.Column(col1), sg.Column(col2, expand_y = True)]
]
window = sg.Window("Calculator", layout, icon = bytes("iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAJFJREFUSEvtlcEOgCAMQ8uXqX+uX4bxMA9bSOmAeNGbGevrimYFi5+yWB8ecALYBqGPxmEaHlAHxYNuC5CNzgy+/Z8DeiMzo/IEPyD8ByFD8bOV70DUhwzwDeo7jUgVlCdgETEDdILlAOaQ1ekETIDVKYBF5OvTLzkNUJ378819MGNlXgD21socdR76s6ux28gNu/s4GTBlxTsAAAAASUVORK5CYII=", "utf-8"), return_keyboard_events = True)
cur_num = []
history = ""

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break 
    if event in ["-CLEAR-", "Escape:27", "Escape:889192475", "c", chr(27), chr(99)]:
        cur_num.clear()
        out_str = ""
        window["-OUTPUT-"].update(out_str)    
    if event in ["-BACKSP-", "BackSpace:8", "BackSpace:855638143", chr(8)]:
        if cur_num != []:
            del cur_num[-1]
            out_str = "".join(cur_num)
            window["-OUTPUT-"].update(out_str)
    if event in ["-ENTER-", "Return:603979789", chr(13), chr(61), "="]:
        if enter(cur_num) == True:
            result = round(brackets(split(cur_num)), 5)
            history = "= " + str(result) +"\n\n" + history
            history = out_str + "\n" + history
            out_str = "= " + str(result)
            window["-OUTPUT-"].update(out_str)
            window["-HISTORY-"].update(history.rstrip())
            cur_num.clear()                         
        else:
            out_str = "".join(cur_num)
            window["-OUTPUT-"].update(out_str)    
    if event in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        cur_num.append(event)  
        out_str = "".join(cur_num)
        window["-OUTPUT-"].update(out_str)
    if event in ["+", "-", "*", "/"]:
        cur_num.append(event)
        check_symbol(cur_num)
        out_str = "".join(cur_num)
        window["-OUTPUT-"].update(out_str)
    if event in [".", ","]:
        event = "."
        cur_num.append(event)
        check_dot(cur_num)
        out_str = "".join(cur_num)
        window["-OUTPUT-"].update(out_str)
    if event in ["(..", "("]:
        cur_num.append("(")
        out_str = "".join(cur_num)
        window["-OUTPUT-"].update(out_str)
    if event in ["..)", ")"]:
        cur_num.append(")")
        count = 0
        if len(cur_num) == 1:
            cur_num[0] = "("
        elif cur_num[-2] in [".", "+", "-", "*", "/", "("]:
            sg.popup_ok("Error! Number missing!\n", background_color = "blue1", no_titlebar = True)
            del cur_num[-1]
        else:    
            for i in cur_num:
                if i == "(":
                    count += 1
                elif i == ")":
                    count -= 1
                if count < 0:
                    sg.popup_ok("Error! Opening bracket missing!\n", background_color = "blue1", no_titlebar = True)
                    del cur_num[-1]
        out_str = "".join(cur_num)
        window["-OUTPUT-"].update(out_str)        

window.close()