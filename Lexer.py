import Methods


class Lexer:
    def __init__(self, code):
        self.code = code
        self.variables = {}
        self.IsInFunction = False
        self.HasLocalVariables = False
        self.FunctionName = ''
        self.tokens = {}
        self.LocalVariables = {}
        self.Classes = {
            'Method': Methods.Methods
        }
        for index, line in enumerate(self.code):
            if line == "" or (line[0] == "-" and line[1] == "-"):  # eliminates dead space and comments
                pass
            elif line[-1] == ";":  # built-in method
                line = list(line[:-2])
                method = ''
                parameters = ''
                while True:
                    if line[0] == "(":
                        line.pop(0)
                        for letter in line:
                            parameters += letter
                        break
                    else:
                        method += line[0]
                        line.pop(0)
                if self.IsInFunction:
                    self.tokens[self.FunctionName].append({"Type": "Method", "Object": method.split()[0], "Parameters": parameters, "Index": index})
                else:
                    Methods.Methods(method, self.checkEquation(parameters.split(), None), index)
            elif "=" in line and line[-1] != ":":  # Variables
                line = str(line).split()
                Key = line[0]
                line.pop(0)
                line.pop(0)
                if self.IsInFunction:
                    if not self.HasLocalVariables:
                        self.LocalVariables.update({self.FunctionName: {}})
                        self.HasLocalVariables = True
                    self.LocalVariables[self.FunctionName].update({Key: self.checkEquation(line, None)})
                else:
                    self.variables.update({Key: self.checkEquation(line, None)})
            elif "function" in line:  # Function
                self.IsInFunction = True
                self.FunctionName = str(line).split()[1]
                self.tokens.update({self.FunctionName: []})
            elif line == "end":  # End Of Function
                self.IsInFunction = False
                self.FunctionName = ''
                self.HasLocalVariables = False
            elif line[0] == "@" and line[1:] in self.tokens:  # Function Called
                func = line[1:]
                for Token in self.tokens[func]:
                    try:
                        self.Classes[Token['Type']](Token['Object'], self.checkEquation(Token['Parameters'].split(), self.LocalVariables[func]), Token['Index'])
                    except KeyError:
                        self.Classes[Token['Type']](Token['Object'], self.checkEquation(Token['Parameters'].split(), None), Token['Index'])
            elif line[0] == "i" and line[1] == "f" and line[-1] == ":":
                line = line[2:]
                line = str(line).split()
                conditions = []
                condition = ''
                for item in line:
                    if item == 'and' or item == ":":
                        print(item)
                        conditions.append(condition)
                        condition = ''
                    else:
                        condition += item
                print(conditions)
                print(condition)

    def checkEquation(self, line, Local):
        IsEquation = False
        Line = ''
        for item in line:
            if "+" == item or "*" == item or "/" == item or "-" == item:
                Line += f"{item} "
                IsEquation = True
            elif Local is not None and item in Local:
                Line += f"{Local[item]} "
            else:
                Line += f"{self.checkVar(item)} "
        if IsEquation:
            Line = eval(Line)
        return Line

    def checkVar(self, param):  # Only Used By checkEquation
        for key in self.variables.keys():
            if key == param:
                return self.variables[key]
        return param
