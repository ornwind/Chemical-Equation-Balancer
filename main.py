import math

import sympy
from sympy.abc import *
import string


class Ce:
    def __init__(self,line=""):
        self.line=line
        self.uppercase_letters = string.ascii_uppercase
        self.lowercase_letters = string.ascii_lowercase
        self.parameters=[eval(i) for i in self.lowercase_letters]
        self.numbers=string.digits
        # self.numbers="₀₁₂₃₄₅₆₇₈₉"
        if self.line:
            self.reactant,self.product=self.count(self.line)
    def replace_num(self,obj):
        return obj.replace("0","₀").replace("1","₁").replace("2","₂").replace("4","₄").replace("3","₃").replace("5","₅").replace("6","₆").replace("7","₇").replace("8","₈").replace("9","₉")
    def count(self,line):
        reactant, product = list(line.split("→"))
        reactant_matters = self.count_matter(reactant)
        product_matters = self.count_matter(product)
        reactant_atom=[]
        product_atom=[]
        for i in reactant_matters:
            elements,num=self.count_atom(i,list(self.count_element(i)))
            reactant_atom.append([elements,num,i])
        for i in product_matters:
            elements,num=self.count_atom(i,list(self.count_element(i)))
            product_atom.append([elements,num,i])
        # print(reactant_atom,product_atom)
        return reactant_atom,product_atom
    def count_matter(self,line):
        matters = list(line.split("+"))
        return matters

    def count_element(self,matter):
        elements=set()
        # print(matter)
        i = 0
        while i < len(matter):
            # print(matter[i] in self.uppercase_letters)
            try:
                if matter[i] in self.uppercase_letters and matter[i + 1] in self.uppercase_letters:
                    elements.add(matter[i])
                if matter[i] in self.uppercase_letters and matter[i + 1] in self.numbers:
                    elements.add(matter[i])

            except:
                if i + 1 >= len(matter) and matter[i] in self.uppercase_letters:
                    elements.add(matter[i])
            if matter[i] in self.lowercase_letters:
                elements.add(matter[i - 1:i + 1])
            if matter[i] == "(":
                end_index = list(matter[i:]).index(")")
                group = matter[i + 1:i + end_index]
                elements = elements | self.count_element(group)
                i += len(group)
            i += 1
        return elements
    def count_atom(self,matter,elements):
        # print(elements)
        num=[0 for i in elements]
        i = 0
        while i < len(matter):
            try:
                if matter[i] in self.uppercase_letters and matter[i + 1] in self.uppercase_letters:
                    num[elements.index(matter[i])]+=1
                if matter[i] in self.uppercase_letters and matter[i + 1] in self.numbers:
                    if i+2<len(matter):
                        try:
                            if matter[i+2] in self.numbers:
                                num[elements.index(matter[i])] += int(matter[i + 1:i+3])
                            else:
                                num[elements.index(matter[i])] += int(matter[i + 1])
                        except:
                            num[elements.index(matter[i])] += int(matter[i + 1])
                    else:
                        num[elements.index(matter[i])]+=int(matter[i+1])
                if matter[i] in self.lowercase_letters and matter[i + 1] in self.numbers:
                    if i+2<len(matter):
                        try:
                            if matter[i+2] in self.numbers:
                                num[elements.index(matter[i - 1:i + 1])] += int(matter[i + 1:i+3])
                            else:
                                num[elements.index(matter[i - 1:i + 1])] += int(matter[i + 1])
                        except:
                            num[elements.index(matter[i - 1:i + 1])] += int(matter[i + 1])
                    else:
                        num[elements.index(matter[i - 1:i + 1])] += int(matter[i+1])
                elif matter[i] in self.lowercase_letters:
                    num[elements.index(matter[i - 1:i + 1])] += 1
            except:
                if i + 1 >= len(matter) and matter[i] in self.uppercase_letters:
                    num[elements.index(matter[i])]+=1
                if i + 1 >= len(matter) and matter[i] in self.lowercase_letters:
                    num[elements.index(matter[i-1:])] += 1
            if matter[i] == "(":
                end_index = list(matter[i:]).index(")")
                group = matter[i + 1:i + end_index]
                number=1

                if matter[i+end_index+1] in self.numbers:
                    number=int(matter[i+end_index+1])
                _,num_=self.count_atom(group,elements)
                for j in range(len(elements)):
                    num[j]+=number*num_[j]
                i += len(group)
            i += 1
        # print(elements,num,sep=",")
        return elements,num
    def min_multiple(self,a,b):
        # print(a,b)
        max_divisor=math.gcd(a,b)
        return a*b//max_divisor
    def solve(self,reactant="",product=""):
        if not reactant+product:
            reactant=self.reactant
            product=self.product
        elements=[]
        # print(reactant+product)
        for i in reactant+product:
            # print(i)
            elements.extend(i[0])
        elements=list(set(elements))
        rfx=[0 for i in elements]
        pfx=rfx.copy()
        print(elements)
        for i in range(len(elements)):
            for j in range(len(reactant)):
                if elements[i] in reactant[j][0]:
                    rfx[i]+=reactant[j][1][reactant[j][0].index(elements[i])]*self.parameters[j]

        for i in range(len(elements)):
            for j in range(len(product)):
                if elements[i] in product[j][0]:
                    pfx[i]+=product[j][1][product[j][0].index(elements[i])]*self.parameters[len(reactant)+j]
        print(rfx,pfx)
        fxs=[]
        for i in range(len(elements)):
            eq=sympy.Eq(rfx[i],pfx[i])
            fxs.append(eq)
        print(fxs)
        # print(self.parameters[:len(reactant)+len(product)-1])
        Flag=False
        k=0
        while not Flag:
            print(k)
            t=self.parameters[:len(reactant)+len(product)].copy()
            t.pop(k)
            print(t)
            ans=sympy.solve(fxs,t)
            try:
                print(ans)
                min_coefficient=1
                parameter=[]
                for i in range(len(list(ans.keys()))):
                    if "/" in str(ans[self.parameters[i]]):
                        t=list(str(ans[self.parameters[i]]).split("/"))[-1]
                        # print(t)
                        if " " in t:
                            t=t[:t.index(" ")]
                        min_coefficient=self.min_multiple(min_coefficient,int(t))
                # print(min_coefficient)
                for i in range(len(list(ans.keys()))):
                    parameter.append(ans[self.parameters[i]] / self.parameters[len(list(ans.keys()))]*min_coefficient)
                parameter.append(min_coefficient)
                Flag=True
                break
            except Exception as e:
                print(e)
                k+=1
            if k>=len(self.parameters[:len(reactant)+len(product)]):
                print("无法配平")
                exit(-1)
        # print(parameter)
        answer=""
        for i in range(len(reactant)):
            if parameter[i]!=1:
                answer+="\033[33m{0}\033[0m".format(str(parameter[i]))
            answer+="\033[35m{}\033[0m".format(self.replace_num(str(reactant[i][2])))
            answer+="\033[34m+"
        answer=answer[:-1]+"\033[34m====\033[0m"
        for i in range(len(product)):
            if parameter[len(reactant)+i]!=1:
                answer+="\033[33m{0}\033[0m".format(str(parameter[len(reactant)+i]))
            answer+="\033[35m{}\033[0m".format(self.replace_num(str(product[i][2])))
            answer+="\033[34m+"
        # print(answer)
        return parameter,answer[:-1]


if __name__=="__main__":
    c=Ce(input("输入需要配平的化学方程式："))
    _,answer=c.solve()
    print(answer)
    # c=Ce()
    # print(c.count_element("O2"))