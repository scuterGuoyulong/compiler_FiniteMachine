stateNum = 0
a = []
import numpy as np


# Thompson算法的第一步是要将正则表达式（中缀形式）转为后缀形式
def Thompson(re):
    '''用一个字典来表示运算符的优先级'''
    ops = {'*': 5, '.': 4, '|': 3}

    postfix = ""
    stack = ""

    '''将中缀表达式表达式转化为后缀表达式'''
    for a in re:
        '''()的优先级最高，首先讨论'''
        if a == "(":
            stack = stack + a

        elif a == ")":
            # print(stack)
            '''读入)以后，就将)之前直到（的所有运算符输出，再让(出栈，不输出括号的原因是后缀表达式不需要括号也能表示优先级'''
            while stack[-1] != "(":
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack[:-1]  # 删除")"

        elif a in ops:
            '''新进入栈的运算符优先级如果比栈内的运算符优先级高,直接入栈。否则就把栈内的高优先级的运算符依次出栈，加入后缀表达式中，读入的运算符则是入栈'''
            while stack and ops.get(a, 0) <= ops.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + a  # 新读入的运算符入栈

        else:
            postfix = postfix + a  # 字符直接进入后缀表达式队列

    '''#读完后，将栈内元素依次出栈'''
    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
    return postfix


# 创建NFA类,由于我们不生成图片一样的NFA，所以我们用边来指代NFA
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.states = []


# NFA的状态类
class State:
    def __init__(self, isEnd, StateNum):
        self.StateNum = StateNum  # 属性的State首字母大写与全局变量区分
        self.isEnd = isEnd  #
        self.transfunction = {}  # 通过字符能到达的状态，用字典表示，key代表转换条件字符，value代表所对应的状态
        self.epsilon = []  # 空字符转换


def createState(isEnd):
    global stateNum
    global a
    stateNum = stateNum + 1
    state = State(isEnd, stateNum)
    a.append(state)

    # print("创建%d节点"%stateNum)
    return state


# 创建两种比较基础的NFA
def add_Epsilon_for_state(come, to):
    come.epsilon.append(to)


def add_Symbol_for_States(come, to, symbol):
    come.transfunction[symbol] = to


def Epsilon_Transition():
    start = createState(False)
    end = createState(True)
    start.epsilon.append(end)  # 将空转换能达到的状态放置在同一个list中

    return start, end


def Symbol_Transition(symbol):
    start = createState(False)
    end = createState(True)
    start.transfunction[symbol] = end

    return start, end


'''创建某个字符的NFA'''


def createNFA(symbol):
    start, end = Symbol_Transition(symbol)
    nfa = NFA(start, end)
    nfa.states.append(start)
    nfa.states.append(end)
    return nfa


'''创建字符a|b的NFA:NFA(a)|NFA(b)→NFA(a|b)'''


def union(first, second):  # 这里的first和second分别代表NFA(a)和NFA(b)
    start = createState(False)  # 这个节点就是两个空跳转的起始节点
    end = createState(True)

    # 创建前两个空跳转
    add_Epsilon_for_state(start, first.start)
    add_Epsilon_for_state(start, second.start)

    # 创建后两个节点的空跳转
    add_Epsilon_for_state(first.end, end)
    first.end.isEnd = False
    add_Epsilon_for_state(second.end, end)
    first.end.isEnd = False

    for state in second.states:
        first.states.append(state)
    first.states.append(start)
    first.states.append(end)

    return NFA(start, end)


# 创建闭包的NFA
def Closure(nfa):
    start = createState(False)
    end = createState(True)

    add_Epsilon_for_state(start, end)
    add_Epsilon_for_state(start, nfa.start)

    add_Epsilon_for_state(nfa.end, end)
    add_Epsilon_for_state(nfa.end, nfa.start)

    nfa.end.isEnd = False

    nfa.states.append(start)
    nfa.states.append(end)

    return NFA(start, end)


# 创建a.b类型的NFA
def connect(first, second):
    # print("first.start%d"%first.start.StateNum)
    # print("first.end%d" % first.end.StateNum)
    # print("second.start%d" % second.start.StateNum)
    # print("second.end%d" % second.end.StateNum)
    add_Epsilon_for_state(first.end, second.start)
    first.end.isEnd = False

    for state in second.states:
        first.states.append(state)

    return NFA(first.start, second.end)


'''   最终NFA的得出
创建一个栈stack,从左往右读取后缀表达式:
    1.若读取的是某个字符a，则创建NFA(a)，入栈
    2.若读取的是某个操作符，则弹出栈中的内容，创建相关的NFA，再次入栈！
'''


def FinalNFA(postfix):
    if postfix == '':
        return Epsilon_Transition()
    stack = []
    for chr in postfix:
        if chr == ".":
            # print("读入字符%s" % chr)
            nfa1 = stack.pop()
            nfa2 = stack.pop()
            new_nfa = connect(nfa2, nfa1)
            stack.append(new_nfa)

        elif chr == "|":
            # print("读入字符%s" % chr)
            nfa1 = stack.pop()
            nfa2 = stack.pop()
            new_nfa = union(nfa1, nfa2)
            stack.append(new_nfa)

        elif chr == "*":
            # print("读入字符%s" % chr)
            nfa = stack.pop()
            new_nfa = Closure(nfa)
            stack.append(new_nfa)

        else:
            # print("读入字符%s"%chr)
            nfa = createNFA(chr)
            stack.append(nfa)

    return stack.pop()


def Output_NFA(a):
    # items代表每个状态
    result = []
    print("-------------------")
    # print("得到的NFA如下表示：")
    for items in a:
        # 输出每个节点的epsilon变迁，item代表每个当前状态能通过epsilon变迁到达的节点
        for item in items.epsilon:
            print("%d---ε--->%d" % (items.StateNum, item.StateNum))
            result.append([items.StateNum, 'ε', item.StateNum])
        # 输出每个节点的变迁：
        for item in items.transfunction:
            # 1---a--->3
            # print(type(items.transfunction))
            print("%d---%s--->%d" % (items.StateNum, item, items.transfunction[item].StateNum))
            result.append([items.StateNum, item, items.transfunction[item].StateNum])
    result = np.array(result)
    return result


def get_nfa():
    re=input("请输入正则表达式")
    # re = "(a|b)*.(a|b).(a.e)*"
    postfix = Thompson(re)  # 先转换成为后缀表达式
    # print("所求正则表达式的逆波兰式:%s"%postfix)
    tmp = FinalNFA(postfix)

    startNum = tmp.start.StateNum
    endNum = tmp.end.StateNum

    # print(len(a))
    # print(a[1].epsilon)
    # print("正则表达式的%s的NFA:"%re)
    result = Output_NFA(a)

    # 字符字典
    cha=[]
    for items in a:
        for item in items.transfunction:
            if item not in cha:
                cha.append(item)
    return startNum, endNum, result,cha

#
# if __name__=="__main__":
#     main()
