import Methods


class Lexer:
    def __init__(self, code):
        self.code = code

        # Booleans
        self.IsInFunction = False
        self.HasLocalVariables = False
        self.HasParameters = False

        # Name
        self.FunctionName = ''

        # Dictionaries
        self.variables = {}
        self.tokens = {}
        self.Parameters = {}
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
                    Methods.Methods(method, self.Check(parameters.split(), None, None) if parameters != '' else None, index)
            elif "=" in line and line[-1] != ":":  # Variables
                line = str(line).split()
                Key = line[0]
                line.pop(0)
                line.pop(0)
                if self.IsInFunction:
                    if not self.HasLocalVariables:
                        self.LocalVariables.update({self.FunctionName: {}})
                        self.HasLocalVariables = True
                    self.LocalVariables[self.FunctionName].update({Key: self.Check(line, None, None)})
                else:
                    self.variables.update({Key: self.Check(line, None, None)})
            elif "function" in line:  # Function
                self.IsInFunction = True
                line = str(line).split()
                self.FunctionName = line[1]
                params = self.RetrieveParams(line[-1])
                if params is None:
                    pass
                else:
                    self.Parameters.update({self.FunctionName: params})
                self.tokens.update({self.FunctionName: []})
            elif line == "end":  # End Of Function
                self.IsInFunction = False
                self.FunctionName = ''
                self.HasLocalVariables = False
            elif line[0] == "@":  # Function Called
                line = line[1:]
                line = line.split()
                func = line[0]
                if func in self.tokens:
                    params = self.RetrieveParams(line[1]) if len(line) >= 2 else None
                    for Token in self.tokens[func]:
                        Locals = self.LocalVariables[func] if func in self.LocalVariables else None
                        Parameters = self.Parameters[func] if func in self.Parameters else None
                        self.Classes[Token['Type']](Token['Object'], self.Check(Token["Parameters"].split(), Locals, Parameters, params) if Token['Parameters'] != '' else None, Token['Index'])
            elif line[0] == "i" and line[1] == "f" and line[-1] == ":":  # IN WORKS
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
                # print(conditions)
                # print(condition)

    def RetrieveParams(self, Params):
        Params = Params.replace('(', '').replace(')', '')
        param = ''
        params = []
        for item in Params:
            if item == ',':
                params.append(param)
                param = ''
            else:
                param += item
        params.append(param)
        if '' in params:
            return None
        return params

    def Check(self, line, local, DeclaredParameters, GivenParameters=None):
        GivenParameters = None if GivenParameters is None else self.SetParams(DeclaredParameters, GivenParameters)
        IsEquation = False
        Line = ''
        for item in line:
            if "+" == item or "*" == item or "/" == item or "-" == item:
                Line += f"{item} "
                IsEquation = True
            elif local is not None and item in local:
                Line += f"{local[item]} "
            elif GivenParameters is not None and item in GivenParameters.keys():
                Line += f"{GivenParameters[item]} "
            else:
                Line += f"{self.checkVar(item)} "
        if IsEquation:
            Line = eval(Line)
        return Line

    def SetParams(self, Declared, Given):
        Params = {}
        for i in range(len(Given)):
            Params.update({Declared[i]: self.checkVar(Given[i])})
        return Params

    def checkVar(self, param):  # Check if word is global variable
        for key in self.variables.keys():
            if key == param:
                return self.variables[key]
        return param
