import numpy as np
import REtoNFA as lab1
# 以下两个包都是画图的包，第一个很鸡肋，第二个是主要的。安装可能费点功夫，但是打包成exe文件一直失败，所以实在是无能为力了
# 这是专门表示有限状态机，如果按照这个包很麻烦就注释掉它相关的代码
from transitions.extensions import GraphMachine
# 这个是只画图，这个包的安装可能不成功，实在不行可以注释掉相关的代码
from graphviz import Digraph



# 绘图的类
class Matter(object):
    pass


# DFA状态类，label属性是用来给DFA标记的，symbol是它的代表符号，set是他包含的NFA状态集合，isStart和isEnd是用来判断他们是否是开始还是接受状态
class state:
    symbol = ''
    label = 0
    set = []
    isStart = False
    isEnd = False

    # 初始化函数
    # 输入label标记（0或1），NFA状态集合，代表符号
    def __init__(self, Label, arr, char):
        self.label = Label
        self.set = arr
        self.symbol = char

    # 打印自身的函数
    # 输出代表符号，包含的NFA集合，label标签
    def print(self):
        print(self.symbol + ":", self.set)

    # 判断两个DFA是否相等
    # 输入另外一个DFA状态
    # 输出boolean值
    def equal(self, S):
        if set(self.set) == set(S.set):
            return True
        else:
            return False

    # 判断自身是否是开始或者接受状态
    # 无输入
    def judge(self):
        if start in self.set:
            self.isStart = True
        if end in self.set:
            self.isEnd = True


# 判断s集合是DFA状态集合中的哪一个状态，并且输出它的代表符号
# 输入NFA集合，全部DFA状态集合
# 输出集合s对应的DFA状态符号
def sym(s, D):
    for i in D:
        if set(s) == set(i.set):
            return i.symbol


# 由状态的符号得到对应的DFA状态
# 输入状态的符号，全部DFA状态的集合
# 输出符号c对应的DFA状态
def symToState(c, D):
    for i in D:
        if i.symbol == c:
            return i


# 判断最小化后的DFA是否是开始或接收状态
# 输入最小化后的DFA状态集合，最初的DFA状态集合
# 将最小化后的开始和接收状态标记，无输出
def judgeStartEnd(F, D):
    for i in F:
        for j in i.set:
            s = symToState(j, D)
            if s.isEnd:
                i.isEnd = True
            if s.isStart:
                i.isStart = True


# NFA状态结合的ε变迁函数
# 输入一个NFA状态集合
# 输出对应的ε闭包集合
def Epsilon(I):
    for i in I:
        for j in range(len(inp)):
            if int(inp[j][0]) == i:
                if inp[j][1] == 'ε':
                    if int(inp[j][2]) not in I:
                        I.append(int(inp[j][2]))
    return I


# 单个NFA状态的ε变迁函数
# 输入一个NFA状态
# 输出对应的ε闭包集合
def epsilon(s):
    ret = [s]
    for i in ret:
        for j in range(len(inp)):
            if int(inp[j][0]) == i:
                if inp[j][1] == 'ε':
                    if int(inp[j][2]) not in ret:
                        ret.append(int(inp[j][2]))
    return ret


# NFA集合I在x条件下的变迁函数的ε变迁结果=课本上的epsilon（move（I，x））
# 输入NFA集合I，变迁条件x
# 输出跳转后到达的集合的ε闭包集合
def move(I, x):
    ret = []
    for i in I:
        for j in range(len(inp)):
            if int(inp[j][0]) == i:
                if inp[j][1] == x:
                    if inp[j][2] not in ret:
                        ret.append(int(inp[j][2]))
    return Epsilon(ret)


# 找到最小化后的DFA状态在字符char输入下应该跳转的最小化DFA状态
# 输入最小化DFA状态a，字符char
# 输出a应该跳转的最小化DFA状态ret的代表符号
def Ftrans(a, char,tran,DFAstate,final,result,cha):
    for i in a.set:
        # a在char的输入下跳转的状态：a_t
        a_t = tran[DFAstate.index(i) + 1][cha.index(char) + 1]
        if a_t != '':
            ret = final[indexOf(a_t, result)]
            return ret.symbol
        else:
            return ''


# 判断一个DFA状态是否在一个集合里
# 输入DFA状态s，状态集合Dstate
# 输出Boolean值
def isInDstate(s, Dstate):
    for i in Dstate:
        if i.equal(s):
            return True
    return False


# 查找字符c在Partition的哪一个group里面
# 输入字符c，二维数组
# 输出字符c所在的group数组的下标，如果不存在就输出-1
def indexOf(c, P):
    for i in range(len(P)):
        if c in P[i]:
            return i
    return


# 画DFA状态转换的图
# 输入DFA状态的集合，图的名称，状态转换表
# 输出有限状态机图
def drawGraph(DFAStateSet, name, transitionTable,cha):
    f = Digraph('finite_state_machine')
    f.attr(rankdir='LR', size='8,5')

    f.attr('node', shape='doublecircle')

    # 构造最小化后的全部DFA状态集合
    states = []
    for i in DFAStateSet:
        states.append(i.symbol)
        if i.isEnd:
            f.node(i.symbol)

    f.attr('node', shape='circle')
    # 构造最小化后的transition数组，代表边
    transitions = []
    for i in range(len(DFAStateSet)):
        for j in range(len(cha)):
            sto = []
            p = transitionTable[i + 1][j + 1]
            if p != '':
                sto.append(cha[j])
                sto.append(DFAStateSet[i].symbol)

                sto.append(p)
                transitions.append(sto)

        edgesTable = []
        for edgesTableX in range(len(states) + 1):
            x = []
            for edgesTableY in range(len(states) + 1):
                x.append('')
            edgesTable.append(x)

        for index in range(len(states)):
            edgesTable[0][index + 1] = states[index]
            edgesTable[index + 1][0] = states[index]

        edgs = []
        for transition in transitions:

            shoot = edgesTable[states.index(transition[1]) + 1][states.index(transition[2]) + 1]
            if shoot == '':
                edgs.append([transition[1], transition[2], transition[0]])
                edgesTable[states.index(transition[1]) + 1][states.index(transition[2]) + 1] = shoot + transition[0]
            else:
                edgesTable[states.index(transition[1]) + 1][states.index(transition[2]) + 1] = shoot + "|" + transition[
                    0]

    for i in range(len(states)):
        for j in range(len(states)):
            p = edgesTable[i + 1][j + 1]
            if p != '':
                f.edge(states[i], states[j], label=p)
    model = Matter()

    # model是绘图类的实例化，states是状态的集合，tansitions代表边：[转换条件，起始状态，到达状态]，
    # initial本来应该是状态机的起始状态，但是因为它有双圈标红，所以把它用在接受状态

    m = GraphMachine(model=model, states=states, transitions=transitions, initial=states[-1])

    # 画出最小化的DFA
    # 有限状态机的画法，可以在指定起始条件下对输入进行跳转
    m.get_graph(name).draw(name + '.png', prog='dot')
    # 这种画法只是图，没有操作的可能，但是比前面的好看而且更正规
    f.render(name, view=True, format='jpg')


# 对于每一个P里的group，对于同一个输入，判断这个group里的两个状态跳转的group是否相同，不同则分，否则不做处理
# 输入状态最小化的第一步的结果：接收状态集合和非接收状态集合
# 输出不能再划分的groups
def split(P,tran,cha,DstateBefore,DFAstate):  # 我们先假设是[A,B,C,D],[E]
    if P == DstateBefore:
        # 第一次分解，划分接受和非接收状态集合
        S = []
        F = []
        Par = []
        for i in DstateBefore:
            if i.isEnd:
                F.append(i.symbol)
            else:
                S.append(i.symbol)
        if S:
            Par.append(S)
        if F:
            Par.append(F)
        print(Par)
        return split(Par,tran,cha,DstateBefore,DFAstate)
    output = []
    # i代表的是一个group如：[A,B,C,D]
    for i in P:
        # 对大于一个元素的group进行分解
        # 分两种情况：
        # 第一种：遍历一边之后发现不需要分割，一个group内的元素对所有的输入都遍历一边之后不需要分割就加它自己进入output
        # 第二种：发现需要分割，那就让它分割成两个数组sub1和sub2，需要对这两个数组再进行partition的操作
        sub1 = []
        for c in cha:
            # 如果形如[E]，则不需要做分解
            if len(i) == 1:
                output.append(i)
                break
            sub1 = []
            sub2 = []
            for k in range(len(i)):
                sub1.append(i[k])
                # i[0]指i里的第一个字符,如A
                # trk是group的第一个元素在转换表内c输入下的变迁状态
                trk = tran[DFAstate.index(i[k]) + 1][cha.index(c) + 1]
                for j in range(1, len(i)):
                    # 判断状态s和t对于同一个输入c到达的group是否相同，前提是先找到s，t的变迁状态
                    # 输入：字符c，i：当前group
                    # 输出：在转换表内查找它对于输入c的变迁目标
                    trj = tran[DFAstate.index(i[j]) + 1][cha.index(c) + 1]
                    # 对group：每一个元素与第一个元素比较它们的变迁目标是否在同一个group里面
                    # 如果是就都丢进sub1，如果不是就丢进sub2
                    if indexOf(trj, P) == indexOf(trk, P):
                        if i[j] not in sub1:
                            sub1.append(i[j])
                    else:
                        if i[j] not in sub2:
                            sub2.append(i[j])
                # 如果sub2非空，则说明有分解
                if sub2:
                    # 假设第一次分解后变成[[A,B,C],[D]],第二次再对第一个group分解
                    # 第二次变成[A,B],[C],[D],但是不可能用递归，因为如果切分了更小的子集后
                    # 并不能保证其他的group不会在这个切分后的group上对应的跳转不会改变
                    # 有可能一个其它未被切分的group里不同的元素在相同的输入下跳转到这个切分后的不同group中
                    SplitRes = []
                    if sub1 not in output:
                        SplitRes.append(sub1)
                    if sub2 not in output:
                        SplitRes.append(sub2)
                    output = output + SplitRes
                    break
            else:
                continue
            break
        # 对所有的输入和组内的元素都遍历一边之后，如果没有切分那就把这个group加回去
        if sub1 not in output and sub1 != []:
            output.append(sub1)

    # 采取递归的方法，也可以说是循环。如果经过上面的步骤后groups的数量有变化，也就是有被切分的group，那就继续切分。
    # 如果group的数量相同，则表明无法再切分了。结束循环并且输出结果
    if len(P) == len(output):
        return P
    else:
        P = output
        print(P)
        return split(P,tran,cha,DstateBefore,DFAstate)


# 构建最初的DFA的状态集合
# 输入开始NFA状态
# 输出最初的DFA状态集合
def constructDFAset(startNFA,cha):
    j = 0
    Dstates = []
    s = state(0, epsilon(startNFA), 'A')
    s.judge()  # 判断它们的开始或者接收状态
    Dstates.append(s)
    for i in Dstates:
        while i.label == 0:
            i.label = 1

            for c in cha:
                if move(i.set, c):
                    j = j + 1
                    U = state(0, move(i.set, c), chr(ord('A') + j))
                    if not isInDstate(U, Dstates):
                        Dstates.append(U)
                        U.judge()
    return Dstates


# 构建最小化DFA的状态集合
# 输入未最小化的DFA状态集合，Partition后的groups
# 输出最小化后的DFA状态集合
def constructFinalDFA(DFAStateSet, result):
    final = []
    for i in result:
        fi = state(0, i, i[0])
        final.append(fi)
    # 判断final里的元素的isEnd和isStart
    judgeStartEnd(final, DFAStateSet)
    return final


# 构建最初的DFA状态转换表
# 输入DFA状态集合，字典表
# 输出最初的DFA状态符号转换表
def DFATransitionTabel(Dstates, chaDirctionary):
    j = 0
    TransitionTable = []
    for TransitionTableX in range(len(Dstates) + 1):
        x = []
        for TransitionTableY in range(len(chaDirctionary) + 1):
            x.append('')
        TransitionTable.append(x)
    TransitionTable[0][0] = "State"
    for i in chaDirctionary:
        TransitionTable[0][chaDirctionary.index(i) + 1] = i
    for i in Dstates:
        TransitionTable[Dstates.index(i) + 1][0] = i.symbol
        for character in chaDirctionary:
            if move(i.set, character):
                newU = state(0, move(i.set, character), chr(ord('A') + j))
                if isInDstate(newU, Dstates):
                    TransitionTable[Dstates.index(i) + 1][chaDirctionary.index(character) + 1] = sym(
                        move(i.set, character), Dstates)
    TransitionTable = np.array(TransitionTable)
    return TransitionTable


# 构建最小化的DFA状态转换表
# 输入最小化后的DFA状态集合，字典表
# 输出最小化后的DFA状态符号转换表
def finalDFATransitionTable(finalStateSet, chaDirctionary,tran,DFAstate,final,result):
    finalTransition = []
    for finalTransitionX in range(len(finalStateSet) + 1):
        x = []
        for finalTransitionY in range(len(chaDirctionary) + 1):
            x.append('')
        finalTransition.append(x)
    finalTransition[0][0] = "State"
    for i in range(len(chaDirctionary)):
        finalTransition[0][i + 1] = chaDirctionary[i]

    for i in range(len(finalStateSet)):
        finalTransition[i + 1][0] = finalStateSet[i].symbol
        for j in range(len(chaDirctionary)):
            finalTransition[i + 1][j + 1] = Ftrans(finalStateSet[i], chaDirctionary[j],tran,DFAstate,final,result,chaDirctionary)
    finalTransition = np.array(finalTransition)
    return finalTransition


# 画NFA状态转换图
# 输入NFA边，接收状态
def drawNFA(nfa, endNum):
    f = Digraph('finite_state_machine')
    f.attr(rankdir='LR', size='8,5')

    f.attr('node', shape='doublecircle')

    f.node(str(endNum))
    f.attr('node', shape='circle')
    for i in nfa:
        f.edge(i[0], i[2], label=i[1])
    f.render('NFA', view=True, format='jpg')

# 程序开始执行的位置，接收NFA的边的信息和开始状态，接收状态，cha是字典表，可扩充，当然会降低效率
start, end, inp, cha = lab1.get_nfa()

def main():

    # 构造最开始的DFA状态集合
    DstateBefore = constructDFAset(start,cha)
    # 构建最开始的DFA状态转换表
    tran = DFATransitionTabel(DstateBefore, cha)
    print("NFA转化为DFA后的转换表：")
    print(tran)
    print("DFA包含的NFA集合：")
    for i in DstateBefore:
        i.print()

    # 把DFA的状态集合转化为字符集合，在最小化DFA状态的时候会用的
    DFAstate = []
    for i in DstateBefore:
        DFAstate.append(i.symbol)
    # 输出分割的过程
    print("等价状态集合划分的过程：")

    # 开始分割最小化DFA状态
    result = split(DstateBefore,tran,cha,DstateBefore,DFAstate)
    # 构造最小化后的DFA状态的全部集合
    final = constructFinalDFA(DstateBefore, result)
    print("最小化后的DFA包含的子集：")
    for i in final:
        i.print()
    # 最小化后的状态转换表
    finalTran = finalDFATransitionTable(final, cha,tran,DFAstate,final,result)
    # 输出最后的转换表
    print("最小化后的转换表：")
    print(finalTran)
    # 画NFA
    drawNFA(inp, end)
    # 画出一开始DFA状态转换的图和最小化后的图
    # 输入状态集合，图片标题，转换表
    # 输出jpg和png图片，jpg图片是比较接近课本的转换表的，png不太一样但是png对应的是真正的有限状态机
    # 注：红色只能有一个圈，只能标出一个接收状态，这在最小化后的DFA图是无歧义的，但是在最小化前有歧义
    drawGraph(DstateBefore, "DFA", tran,cha)
    drawGraph(final, "finalDFA", finalTran,cha)

if __name__=="__main__":
    main()