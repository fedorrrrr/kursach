from llvmlite import ir
import sys


type = None


class Number():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        if type == ir.IntType(32):
            i = ir.Constant(ir.IntType(32), int(self.value))
        else:
            i = ir.Constant(ir.FloatType(), float(self.value))
        return i


class BinaryOp():
    def __init__(self, builder, module, left, right):
        global type
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


builder_new = None
flag = False

def new_b(b):
    if flag == True:
        b = builder_new
    return b


class Sum(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        if type == ir.IntType(32):
            i = self.builder.add(self.left.eval(), self.right.eval())
        else:
            i = self.builder.fadd(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        if type == ir.IntType(32):
            i = self.builder.sub(self.left.eval(), self.right.eval())
        else:
            i = self.builder.fsub(self.left.eval(), self.right.eval())
        return i


class Mul(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        if type == ir.IntType(32):
            i = self.builder.mul(self.left.eval(), self.right.eval())
        else:
            i = self.builder.fmul(self.left.eval(), self.right.eval())
        return i


class Div(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        if type == ir.IntType(32):
            i = self.builder.sdiv(self.left.eval(), self.right.eval())
        else:
            i = self.builder.fdiv(self.left.eval(), self.right.eval())
        return i


class Equal(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.icmp_signed('==', self.left.eval(), self.right.eval())
        return i


class More(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.icmp_signed('>', self.left.eval(), self.right.eval())
        return i


class Less(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.icmp_signed('<', self.left.eval(), self.right.eval())
        return i

class Not_equal(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.icmp_signed('!=', self.left.eval(), self.right.eval())
        return i


class And_(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.and_(self.left.eval(), self.right.eval())
        return i


class Or_(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.or_(self.left.eval(), self.right.eval())
        return i


class Not_():
    def __init__(self, builder, module, left):
        self.builder = builder
        self.module = module
        self.left = left

    def eval(self):
        self.builder = new_b(self.builder)
        i = self.builder.not_(self.left.eval())
        return i

class If_(BinaryOp):
    def eval(self):
        self.builder = new_b(self.builder)
        with self.builder.if_then(self.left.eval()):
            i = self.right.eval()
        return i


class If_else():
    def __init__(self, builder, module, boolean, left, right):
        self.builder = builder
        self.module = module
        self.boolean = boolean
        self.left = left
        self.right = right

    def eval(self):
        self.builder = new_b(self.builder)
        with self.builder.if_else(self.boolean.eval()) as (then, otherwise):
            with then:
                i = self.left.eval()
            with otherwise:
                y = self.right.eval()
        return i


class Eval_(BinaryOp):
    def eval(self):
        i = self.left.eval()
        y = self.right.eval()
        return i


values = [None]
variable = [None] * 100
n = 0
value_num = [None] * 100
count = [1] * 100

class Id_save():
    def __init__(self, builder, module, type_, left, right):
        self.builder = builder
        self.module = module
        self.type_ = type_
        self.left = left
        self.right = right

    def eval(self):
        global variable
        global n
        global values
        global value_num
        global count
        i = None
        superval = self.left.value
        values.append(superval)
        for x in range(0, len(values) - 1):
            if values[x] == self.left.value:
                count[x] += 1
                value_num[x] = values[x] + str(count[x])
                superval = value_num[x]
                break
        global type
        if self.type_.value == "integer":
            type = ir.IntType(32)
        elif self.type_.value == "float":
            type = ir.FloatType()
        variable[n] = ir.GlobalVariable(self.module, type, superval)
        variable[n].linkage = 'internal'
        self.builder = new_b(self.builder)
        i = self.builder.store(self.right.eval(), variable[n])
        n += 1
        if i == None:
            sys.stderr.write("Error storing variable: %s\n" % self.left.value)
            sys.exit(1)
        return i

def num(x):
    for i in x:
        if i.isdigit():
            return True
    return False

class Id_load():
    def __init__(self, builder, module, left):
        self.builder = builder
        self.module = module
        self.left = left

    def eval(self):
        global variable
        global n
        global value_num
        global count
        i = None
        check = self.left.value
        if num(self.left.value):
            check = self.left.value[:-1]
        if num(check):
            check = check[:-1]
        for x in range(0, len(value_num) - 1):
            if value_num[x] == check + str(count[x]):
                check = check + str(count[x])
                break
        for x in range(0, n):
            if ("@\"" + check + "\"" in str(variable[x])):
                self.builder = new_b(self.builder)
                i = self.builder.load(variable[x])
        if i == None:
            sys.stderr.write("Error loading variable: %s\n" % self.left.value)
            sys.exit(1)
        return i


func_num = 0


class Print():
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self):
        value = self.value.eval()
        voidvariable_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global func_num
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr" + str(func_num))
        func_num += 1
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        self.builder = new_b(self.builder)
        fmt_arg = self.builder.bitcast(global_fmt, voidvariable_ty)
        self.builder.call(self.printf, [fmt_arg, value])


func_new = None
func_return = 0	


class Func_():
    def __init__(self, builder, module, func_name, param, stm):
        self.builder = builder
        self.module = module
        self.func_name = func_name
        self.param = param
        self.stm = stm

    def eval(self):
        global func_new
        global builder_new
        global variable
        global n
        global flag
        global func_return
        i = None
        func_new = ir.Function(self.module, ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)]), name="function")
        builder_new = ir.IRBuilder(func_new.append_basic_block(name="entry"))
        a1, a2 = func_new.args
        variable[n] = ir.GlobalVariable(self.module, ir.IntType(32), self.param[0].value)
        variable[n].linkage = 'internal'
        builder_new.store(a1, variable[n])
        n += 1
        variable[n] = ir.GlobalVariable(self.module, ir.IntType(32), self.param[1].value)
        variable[n].linkage = 'internal'
        builder_new.store(a2, variable[n])
        n += 1
        flag = True
        y = self.stm.eval()
        flag = False
        func_return = self.func_name.value
        for x in range(0, n):
            if ("@\"" + self.func_name.value + "\"" in str(variable[x])):
                i = builder_new.load(variable[x])
        ii = builder_new.ret(i)
        if ii == None:
            sys.stderr.write("Error returning in function")
            sys.exit(1)
        return ii


class Call_():
    def __init__(self, builder, module, func_name, param):
        self.builder = builder
        self.module = module
        self.func_name = func_name
        self.param = param

    def eval(self):
        global func_new
        self.builder = new_b(self.builder)
        for x in range(0, n):
            if ("@\"" + self.param[0].value + "\"" in str(variable[x])):
                a1 = self.builder.load(variable[x])
        for x in range(0, n):
            if ("@\"" + self.param[1].value + "\"" in str(variable[x])):
                a2 = self.builder.load(variable[x])
        i = self.builder.call(func_new, [a1, a2])
        return i
