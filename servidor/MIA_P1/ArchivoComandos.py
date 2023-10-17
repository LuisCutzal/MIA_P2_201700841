import ply.yacc as sintactico
import ply.lex as lexico
from ejecutarexecute import comandoExecute
from mkdisk import *
from rep import *
from rmdisk import *
from fdisk import *
from mount import *
from mkfs import *
from utilities import *
palabrasReservadas = {"execute":"EXECUTE",
                      "mkdisk": "MKDISK",
                      "path": "PATH",
                      "size": "SIZE",
                      "unit": "UNIT",
                      "fit": "FIT",
                      "rmdisk": "RMDISK",
                      "fdisk" : "FDISK",
                      "name" : "NAME",
                      "type" : "TYPE",
                      "delete" : "DELETE",
                      "add" : "ADD",
                      "mount" : "MOUNT",
                      "id" : "ID",
                      "mkfs" : "MKFS",
                      "pause": "PAUSE",
                      "ruta" : "RUTA",
                      "rep": "REP"}

tokens = ["IDENTIFICADOR",
          "COMILLAS",
          "STRING",
          "NUMEROS",
          "COMENTARIOS",
          "GUION",
          "IGUAL",
          "VALORDEPATH",
          "NOMBREARCHIVO"]+list(palabrasReservadas.values())


#ahora reconocemos los tokens que vamos a utilizar
t_GUION = r"-"   #como solo es un caracter se hace de esta forma
t_IGUAL = r"="   #como solo es un caracter se hace de esta forma


def t_COMILLAS(t):
    r'\"'
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_COMENTARIOS(t):
    r'\#.*' #con el punto le decimos que no importa lo que venga
    t.value = t.value[1:-1]
    return t

def t_VALORDEPATH(t): #solo es la ruta aun no esta el archivo
    r'\/[a-zA-Z0-9_ !\/]*\/'
    return t


def t_NOMBREARCHIVO(t):
    r'[a-zA-Z0-9_ !]+\.(adsj|dsk|txt|jpg)' 
    return t

def t_IDENTIFICADOR(t):
    r"([0-9])*[a-zA-Z_][a-zA-Z0-9_]*"
    #aca se deben de reconocer las palabras reservadas
    t.type = palabrasReservadas.get(t.value.lower(),"IDENTIFICADOR")
    return t

#ahora numeros 
def t_NUMEROS(t):
    r"-?\d+"
    return t

t_ignore = " \t\r"

def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print(f'Error Lexico:'+t.value[0]+' en la linea: '+str(t.lineno) +' en la columna: '+str(find_column(input, t)))
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos - line_start) + 1


#comienza lo sintactico


def p_inicio(t): 
    '''inicio : instrucciones'''
    t[0] = t[1]
    
def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion'''
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t):
    '''instrucciones : instruccion'''
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion : comandoexecute
                   | comandomkdisk
                   | comentarios
                   | comandorep
                   | comandormdisk
                   | comandofdisk
                   | comandomount
                   | comandomkfs'''
    t[0] = t[1]

def p_instruccuion_pausa(t):
    '''instruccion : PAUSE'''
    ejecutarPause()
    t[0] = ""

def p_comandoexecute(t):
    '''comandoexecute : EXECUTE GUION PATH IGUAL VALORDEPATH NOMBREARCHIVO'''
    t[0] = comandoExecute(t[5],t[6]).ejecutar()
    
def p_comandomkdisk(t):
    '''comandomkdisk : MKDISK listaparametros_mkdisk'''
    MKDISK(t[2]).ejecutar()
    t[0]= ''
    
def p_listaparametros_mkdisk(t):
    '''listaparametros_mkdisk : listaparametros_mkdisk parametromkdisk
                              | parametromkdisk'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
                         

def p_parametromkdisk(t):
    '''parametromkdisk : GUION parametropath
                       | GUION parametrosize
                       | GUION parametrounit
                       | GUION parametrofit'''
    t[0] = t[2]

def p_parametropath(t):
    '''parametropath : PATH IGUAL valorespath'''
    t[0] = t[3]

def p_valorespath(t):
    '''valorespath : VALORDEPATH NOMBREARCHIVO 
                   | COMILLAS VALORDEPATH NOMBREARCHIVO COMILLAS'''
    if len(t) == 3:
        t[0] = {"rutaArchivo" : t[1],
                "nombrearchivo": t[2]}
    else:
        t[0] = {"rutaArchivo" : t[2],
                "nombrearchivo": t[3]}

def p_parametrosize(t):
    '''parametrosize : SIZE IGUAL NUMEROS'''
    t[0] = {"valorsize" : t[3]}
    
def p_parametrounit(t):
    '''parametrounit : UNIT IGUAL IDENTIFICADOR'''
    t[0] = {"valorunit" : t[3]}
    
def p_parametrofit(t):
    '''parametrofit : FIT IGUAL IDENTIFICADOR'''
    t[0] = {"valorfit" : t[3]}

def p_comentarios(t):
    '''comentarios : COMENTARIOS'''
    print("#"+t[1])
    t[0] = ""

def p_rep(t):
    '''comandorep : REP listaparametros_rep'''
    REP(t[2]).ejecutarRep(listaMount)
    t[0]= ""
    
def p_listaparametros_rep(t):
    '''listaparametros_rep : listaparametros_rep parametrorep
                           | parametrorep'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
        
def p_parametrorep(t):
    '''parametrorep : GUION parametroname
                    | GUION parametropath
                    | GUION parametroid
                    | GUION parametroruta'''
    t[0] = t[2]

def p_parametroruta(t):
    '''parametroruta : RUTA IGUAL VALORDEPATH NOMBREARCHIVO'''
    t[0] = {"ruta" : t[3],
            "nombre": t[4]}

    
def p_comandormdisk(t):
    '''comandormdisk : RMDISK GUION parametropath'''
    RMDISK().ejecutarRMDISK(t[3])
    t[0]=""
    

def p_comandofdisk(t):
    '''comandofdisk : FDISK listaparametros_fdisk'''
    FDISK(t[2]).ejecutarFDISK()
    t[0]=""

def p_listaparametros_fdisk(t):
    '''listaparametros_fdisk : listaparametros_fdisk parametrofdisk
                             | parametrofdisk'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_parametrofdisk(t):
    '''parametrofdisk : GUION parametrosize
                      | GUION parametropath
                      | GUION parametroname
                      | GUION parametrounit
                      | GUION parametrotype
                      | GUION parametrofit
                      | GUION parametrodelete
                      | GUION parametroadd'''
    t[0] = t[2]
    
def p_parametroname(t):
    '''parametroname : NAME IGUAL STRING
                     | NAME IGUAL IDENTIFICADOR'''
    t[0] = {"valorname" : t[3]}

def p_parametrotype(t):
    '''parametrotype : TYPE IGUAL IDENTIFICADOR'''
    t[0] = {"valortype" : t[3]}


def p_parametrodelete(t):
    '''parametrodelete : DELETE IGUAL IDENTIFICADOR'''
    t[0] = {"valordelete" : t[3]}
    
def p_parametroadd(t):
    '''parametroadd : ADD IGUAL NUMEROS'''
    t[0] = {"valoradd" : t[3]}
    
def p_comandomount(t):
    '''comandomount : MOUNT listaparametros_mount'''
    MOUNT(t[2]).ejecutarMOUNT(listaMount)
    t[0]=""

def p_listaparametros_mount(t):
    '''listaparametros_mount : listaparametros_mount parametromount
                             | parametromount'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_parametromount(t):
    '''parametromount : GUION parametropath
                       | GUION parametroname'''
    t[0] = t[2]


def p_parametroid(t):
    '''parametroid : ID IGUAL IDENTIFICADOR'''
    t[0] = {"valorid" : t[3]}

def p_comandomkfs(t):
    '''comandomkfs : MKFS listaparametros_mkfs'''
    MKFS(t[2]).ejecutarMKFS()
    t[0]=""

def p_listaparametros_mkfs(t):
    '''listaparametros_mkfs : listaparametros_mkfs parametromkfs
                            | parametromkfs'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_parametromkfs(t):
    '''parametromkfs : GUION parametroid
                     | GUION parametrotype'''
    t[0] = t[2]

def iniciarAnalisis(comando):
    global input
    global listaMount
    input = comando
    listaMount = []
    lex = lexico.lex()
    parser = sintactico.yacc()
    salIDENTIFICADORa = parser.parse(comando)
    if salIDENTIFICADORa == None:
        return ""
    elif salIDENTIFICADORa == []:
        return ""
    else: return salIDENTIFICADORa[0]

