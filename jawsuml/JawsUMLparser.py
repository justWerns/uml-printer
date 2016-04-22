# -----------------------------------------------------------------------------
# JawsUMLparser.py    A translator that accepts a textual notation describing
#               various UML (Unified Modeling Language) diagram types
#               and emits a Java serializable Container object, stored
#               in a data file, that holds the annotated parse tree
#               for back-end processing by Java. Planned back ends include
#               flattening out whitespace for non-sighted readers, pumping
#               in whitespace indentation for sighted readers, and generated
#               graphical diagrams using GraphViz or other.
# -----------------------------------------------------------------------------

import sys
import copy
import re
# import logging
DEBUG = 10      # From logging.DEBUG, not available in Jython
import pprint

if sys.version_info[0] >= 3:
    raw_input = input

# Tokens

reserved = {        # Map the reserved lexeme to its TOKEN name.
    'classDiagram'      :   'CLASSDIAGRAM',
    'package'           :   'PACKAGE',
    'interface'         :   'INTERFACE',
    'class'             :   'CLASS',
    'abstract'          :   'ABSTRACT',
    'active'            :   'ACTIVE',
    'static'            :   'STATIC',
    'implements'        :   'IMPLEMENTS',
    'extends'           :   'EXTENDS',
    'uses'              :   'USES',
    'usedby'            :   'USEDBY',
    'useboth'           :   'USEBOTH',
    'usehuh'            :   'USEQ',
    'composedof'        :   'COMPOSEDOF',
    'sequenceDiagram'   :   'SEQUENCEDIAGRAM',
    'object'            :   'OBJECT',
    'calls'             :   'CALLS',
    'returns'           :   'RETURNS',
    'sends'             :   'SENDS',
    'to'                :   'TO',
    'constructs'        :   'CONSTRUCTS',
    'destructs'         :   'DESTRUCTS',
    'objectDiagram'     :   'OBJECTDIAGRAM',
    'deploymentDiagram' :   'DEPLOYMENTDIAGRAM',
    'node'              :   'NODE',
    'artifact'          :   'ARTIFACT',
    'link'              :   'LINK',
#    'statemachineDiagram' : 'STATEMACHINEDIAGRAM',
#    'state'             :   'STATE',
#    'final'             :   'FINAL',
#    'start'             :   'START',
#    'goto'              :   'GOTO',
#    'when'              :   'WHEN',
    'string_constant1'  :   'STRING_CONSTANT1',
    'int_constant'      :   'INT_CONSTANT'
}

tokens = (
    'ID', 'COMMA', 'EQ', 'LBRACE', 'RBRACE', 'SEMIC', 'ATSIGN',
    'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'STAR', 'COLON',
    'PLUS', 'MINUS', 'TILDE', 'HASHSIGN', 'LT', 'GT', 'DOT', 'QUES'
#    'SQUOTE', 'AMPERSAND', 'VBAR', 'SLASH'
) + tuple(reserved.values())    # append TOKENS for reserved words

def t_newline(t):
    r'\n+'
    global __global_line_number__
    t.lexer.lineno += t.value.count("\n")
    # print "DEBUG ADDING LINES", t.value.count("\n"), "TO", t.lexer.lineno
    # DEBUG __global_line_number__ = t.lexer.lineno
    __global_line_number__ += t.value.count("\n")

def t_STRING_CONSTANT1(t):
    '\\"[^"]*\\"'
    rawvalue = str(t.value)
    # t.value = rawvalue[1:-1]
    t.value = rawvalue
    return t

# def t_FLOAT_CONSTANT(t):
    # r'(-)?((\d*\.\d+)|(\d+\.\d*))'
    # t.value = str(float(t.value))
    # return t

def t_INT_CONSTANT(t):
    r'(-)?\d+'
    t.value = str(int(t.value))
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_.]*'
    if (reserved.has_key(t.value)):
        t.type = reserved[t.value]
    else:
        t.type = 'ID'
    return t
                                    # Operator TYPE requirements follow.
                                    # Numeric allows mix of int and float.
t_LBRACE =               "{"
t_RBRACE =               "}"
t_LPAREN =               "\\("
t_RPAREN =               "\\)"
t_LBRACK =               "\\["
t_RBRACK =               "]"
t_SEMIC =                ";"
# t_SQUOTE =               "'"
# t_AMPERSAND =            '&'
# t_VBAR =                 '\\|'
t_ATSIGN =               "@"
t_COMMA =                ","
t_EQ =                   "="
# t_SLASH =                "/"
t_STAR  =                "\\*"
t_COLON  =               ":"
t_PLUS  =                "\\+"
t_MINUS  =               "\\-"
t_TILDE  =               "\\~"
t_HASHSIGN  =            "\\#"
t_LT  =                  "<"
t_GT  =                  ">"
t_DOT  =                 "\\."
t_QUES  =                "\\?"

# Token patterns. Those that overlap with t_ID
# are handled above, and do not appear in this group.
t_ignore =    ' \t'

__global_line_number__ = 1
# If __global_error__ is not yet set, then upon finding an error, 
# set it to one of the following and also set __global_error_string__.
# There errors are built-in Python error types.
#
# SyntaxError           on lexical or syntax error
# TypeError             on type mismatch or missing / extra argument
# NameError             symbol not in scope or redefined at same scope
# ValueError            linker raises this on invalid program memory entry
__global_error__ = None
__global_error_string__ = None

def t_error(t):
    global __global_error__
    global __global_error_string__
    print "Illegal character '%s'" % t.value[0], "near line",   \
        __global_line_number__
    t.lexer.skip(1)
    if __global_error__ == None:
        __global_error_string__ =   \
            ("ERROR: Illegal character '%s'" % t.value[0]) + " near line "\
            + str( __global_line_number__)
        __global_error__ = SyntaxError
    
# Build the lexer
import ply.lex as lex
lex.lex()

# User this error reporing function for syntax and semantic errors.
def terror(ex, st, isprint=True, isthrow=False): # exception type and string
    global __global_error__
    global __global_error_string__
    if (isprint):
        print st
    if __global_error__ == None:
        __global_error_string__ = st
        __global_error__ = ex
    if isthrow:
        raise ex, st

# Invokes terror with a forced throw
def horror(ex, st, isprint=True):
    terror(ex, st, isprint=isprint, isthrow=True)


# Parsing rules

precedence = (
    )

# We are building lists instead of tuples to make deletion of empty
# lists, empty strings, and None values easier after parsing.
def p_goal(p):
    '''goal :   comment diagram comment'''
    # Any diagram is opening comments, the actual diagram, and closing comments.
    if (p[1]):
        if (p[3]):
            p[0] = ["diagram:", p[1], p[2], p[3]]   # ADDY diagram: 4/20
        else:
            p[0] = ["diagram:", p[1], p[2]]
    else:
        p[0] = ["diagram:", p[2]]

def p_diagram(p):
    '''diagram : classdgm
               | seqdgm
               | deploydgm
               | objdgm'''
    p[0] = p[1]

def p_classdgm(p):      # ADDY class-sequence: 4/20
    '''classdgm : CLASSDIAGRAM ID LBRACE comment class_seq RBRACE'''
    if p[5]:
        cs = ["class-sequence:"]+p[5]       # ADDY
    else:
        cs = p[5]
    p[0] = [p[1]+":", p[2], p[3], p[4], cs, p[6]]

def p_class_seq(p):
    '''class_seq : class_seq classIface_decl
                 | class_seq package_decl
                 | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_package_decl(p):
    '''package_decl : PACKAGE ID LBRACE comment class_seq RBRACE comment'''
    if p[5]:
        pcc = ["package-contents:"] + p[5]
    else:
        pcc = p[5]
    p[0] = [p[1]+":", p[2], p[3], p[4], pcc, p[6], p[7]]

def p_classIface_decl(p):
    '''classIface_decl : visibility abstractStaticQualifiers maybeActive classORinterface genericid generalization LBRACE comment class_contents RBRACE associations comment'''
    if (p[4] == "interface"):
        if (p[2] or p[3]):
            terror(NameError, "ERROR, keyword " + str(p[2]) + " " + str(p[3])
                + " does not apply for an interface: " + p[5])
        for g in p[6]:
            if g == 'implements':
                terror(NameError, "ERROR, keyword implements"
                    + " does not apply to an interface: " + p[5])
                break
    if p[9]:
        cc = ["class-contents:"]+p[9]   # ADDY
    else:
        cc = p[9]
    if p[11]:
        asl = ["association-list:"] + p[11] # ADDY
    else:
        asl = p[11]
    p[0] = [p[4]+":",p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],
        cc,p[10],asl,p[12]]

def p_classORinterface(p):
    '''classORinterface : CLASS
                        | INTERFACE'''
    p[0] = p[1]

def p_class_contents(p):
    '''class_contents : class_contents classIface_decl
                      | class_contents attribute_decl
                      | class_contents method_decl
                      | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_attribute_decl(p):
    '''attribute_decl : visibility abstractStaticQualifiers ID optionaltype optionalmultiplicity optionalvalue SEMIC comment'''
    p[0] = ['attribute:', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]

def p_optionalvalue(p):
    '''optionalvalue : EQ valuecon
                        | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1] + p[2]

def p_method_decl(p):
    '''method_decl : visibility abstractStaticQualifiers ID LPAREN optionalparams RPAREN optionaltype SEMIC comment'''
    if p[5]:
        pll = ["param-list:"] + p[5]
    else:
        pll = p[5]
    p[0] = ['method:', p[1], p[2], p[3], p[4], pll, p[6], p[7], p[8], p[9]]

def p_optionalparams(p):
    '''optionalparams : ID optionaltype
                    | optionalparams COMMA ID optionaltype
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    elif p[2] == ',':
        p[0] = p[1] + [[p[3], p[4]]]
    else:
        p[0] = [[p[1], p[2]]]

def p_optionaltype(p):
    '''optionaltype : COLON optionalarray genericid
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = ["type:", p[2], p[3]]

def p_optionalarray(p):
    '''optionalarray : LBRACK RBRACK
                     | LBRACK INT_CONSTANT RBRACK
                     | epsilon'''
    if p[1] == None:
        p[0] = []
    elif p[2] == ']':
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3]]

# Multiplicity is a string
def p_optionalmultiplicity(p):
    '''optionalmultiplicity : LBRACK numberthingy tailmultiplicity RBRACK
                            | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1] + p[2] + p[3] + p[4]

def p_tailmultiplicity(p):
    '''tailmultiplicity : DOT DOT numberthingy
                            | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = ".." + p[3]

def p_numberthingy(p):
    '''numberthingy : INT_CONSTANT
                    | STAR'''
    p[0] = p[1]

def p_visibility(p):
    '''visibility : PLUS
        | MINUS
        | TILDE
        | HASHSIGN
        | epsilon'''
    p[0] = p[1]

def p_abstractStaticQualifiers(p):
    '''abstractStaticQualifiers : ABSTRACT maybeStatic
                    | STATIC maybeAbstract
                    | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = (p[1], p[2])

def p_maybeStatic(p):
    '''maybeStatic : STATIC
                    | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1]

def p_maybeAbstract(p):
    '''maybeAbstract : ABSTRACT
                    | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1]

def p_maybeActive(p):
    '''maybeActive : ACTIVE
                    | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1]

# Return a list of base classes and a list of base interfaces.
def p_generalization(p):
    '''generalization : implementation optextension
                      | extension optimplementation
                      | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + p[2]

def p_optextension(p):
    '''optextension : extension
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1]

def p_optimplementation(p):
    '''optimplementation : implementation
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1]

def p_implementation(p):
    '''implementation : IMPLEMENTS genericid idrestlist'''
    p[0] = [p[1], p[2]] + p[3]

def p_extension(p):
    '''extension : EXTENDS genericid idrestlist'''
    p[0] = [p[1], p[2]] + p[3]

# generic rules return concatenated strings
def p_genericid(p):
    '''genericid : ID generic'''
    p[0] = p[1] + p[2].strip()

def p_generic(p):
    '''generic : LT genericid idrest GT
                    | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1] + p[2] + p[3].strip() + p[4]

def p_idrest(p):
    '''idrest : idrest COMMA genericid
                    | epsilon'''
    if p[1] == None:
        p[0] = ""
    elif p[1]:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[2] + p[3]

def p_idrestlist(p):
    '''idrestlist : idrestlist COMMA genericid
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    elif p[1]:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[3]]

def p_associations(p):
    '''associations : association associationlist SEMIC
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2] + [p[3]]

def p_association(p):
    '''association : role optionalmultiplicity usekeyword optionalmultiplicity role genericid'''
    p[0] = [p[3]+":", p[1], p[2], p[4], p[5], p[6]]

def p_usekeyword(p):
    '''usekeyword : USES
                    | USEDBY
                    | USEBOTH
                    | USEQ
                    | COMPOSEDOF'''
    p[0] = p[1]

def p_role(p):
    '''role : stringcon
        | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = p[1]

def p_associationlist(p):
    '''associationlist : associationlist COMMA association
                        | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[3]]

# tokenizeComments has put @ integer=index-into-comments-list @
def p_comment(p):
    '''comment : ATSIGN INT_CONSTANT ATSIGN
                | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1], p[2], p[3]]
        # print "REDUCING COMMENT: ", str(p[0])

def p_stringcon(p):
    '''stringcon : STRING_CONSTANT1'''
    p[0] = p[1]

def p_valuecon(p):
    '''valuecon : stringcon 
                | ID'''
    p[0] = p[1]

def p_epsilon(p):
    'epsilon :'
    p[0] = None

def p_seqdgm(p):
    '''seqdgm : SEQUENCEDIAGRAM ID LBRACE comment seq_seq RBRACE'''
    if p[5]:
        sl = ["sequence-list:"] + p[5]  # ADDY
    else:
        sl = p[5]
    p[0] = [p[1]+":", p[2], p[3], p[4], sl, p[6]]

def p_seq_seq(p):
    '''seq_seq : seq_seq seq_decl
                 | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_seq_decl(p):
    '''seq_decl : activeOption OBJECT ID seq_type LBRACE RBRACE comment
         | quesID CALLS ID LPAREN optionalparams RPAREN optionalCons SEMIC comment
         | quesID CONSTRUCTS ID SEMIC comment
         | quesID DESTRUCTS ID SEMIC comment
         | quesID RETURNS optionalResult TO obj_id SEMIC comment
         | quesID SENDS optionalResult TO obj_id SEMIC comment'''
    if p[2] == 'object':
        p[0] = ["object:", p[1], p[2], p[3], p[4], p[5], p[6], p[7]]
    elif p[2] == 'calls':
        if p[5]:
            pll = ["param-list:"] + p[5]
        else:
            pll = p[5]
        p[0] = ["call:", p[1], p[2], p[3], p[4], pll, p[6], p[7], p[8], p[9]]
    elif p[2] == 'constructs' or p[2] == 'destructs':
        p[0] = [p[2][0:-1]+":", p[1], p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[2][0:-1]+":", p[1], p[2], p[3], p[4], p[5], p[6], p[7]]

def p_activeOption(p):
    '''activeOption : ACTIVE
                    | epsilon'''
    p[0] = p[1]

def p_seq_type(p):
    '''seq_type : COLON genericid
                | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = ["type:", p[2]]

def p_quesID(p):
    '''quesID : QUES
              | obj_id'''
    p[0] = p[1]

def p_obj_id(p):
    '''obj_id : ID optionalParens'''
    p[0] = p[1] + p[2]

def p_optionalParens(p):
    '''optionalParens : LPAREN RPAREN
                      | epsilon'''
    if p[1] == None:
        p[0] = ""
    else:
        p[0] = "()"

def p_optionalCons(p):
    '''optionalCons : CONSTRUCTS ID seq_type
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]+":", p[2]] + p[3]

def p_optionalResult(p):
    '''optionalResult : ID
                      | epsilon'''
    p[0] = p[1]

def p_deploydgm(p):
    '''deploydgm : DEPLOYMENTDIAGRAM ID LBRACE comment deploy_seq RBRACE'''
    if p[5]:
        ds = ["deploy-list"] + p[5]
    else:
        ds = p[5]
    p[0] = [p[1]+":", p[2], p[3], p[4], ds, p[6]]

def p_deploy_seq(p):
    '''deploy_seq : deploy_seq deploy_decl
                 | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_deploy_decl(p):
    '''deploy_decl : NODE ID LBRACE comment node_seq RBRACE comment linkoption'''
    if p[5]:
        nseq = ["node-contents"] + p[5] # ADDY
    else:
        nseq = p[5]
    p[0] = [p[1]+":", p[1], p[2], p[3], p[4], nseq, p[6], p[7], p[8]]

def p_node_seq(p):
    '''node_seq : node_seq node_decl
                 | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_node_decl(p):
    '''node_decl : ARTIFACT ID artifactTail
                 | attribute_assignment
                 | deploy_decl'''
    if p[1] == 'artifact':
        p[0] = ['artifact:', p[1], p[2], p[3]]
    else:
        p[0] = p[1]

def p_artifactTail(p):
    '''artifactTail : SEMIC comment
                    | LBRACE artifactAssigns attribute_assignment RBRACE comment'''
    if p[1] == ';':
        if p[2]:
            p[0] = [p[1], p[2]]
        else:
            p[0] = p[1]
    else:
        if p[2]:
            aas = ["artifact-assignment:"] + p[2]
        else:
            aas = p[2]
        p[0] = ["artifact-contents:", p[1], aas + [p[3]], p[4], p[5]] # ADDY

def p_artifactAssigns(p):
    '''artifactAssigns : artifactAssigns attribute_assignment
                       | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_linkoption(p):
    '''linkoption : STRING_CONSTANT1 LINK TO ID morelinks SEMIC comment
                  | epsilon'''
    if p[1] == None:
        p[0] = []
    elif p[7]:
        p[0] = ["link-sequence", ['link:', p[1], p[2], p[3], p[4]]] + p[5] + [p[6]] + [p[7]]
    else:
        p[0] = ["link-sequence", ['link:', p[1], p[2], p[3], p[4]]] + p[5] + [p[6]]

def p_morelinks(p):
    '''morelinks : morelinks COMMA STRING_CONSTANT1 LINK TO ID
                 | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + ['link:', p[3], p[4], p[5], p[6]]

def p_objdgm(p):
    '''objdgm : OBJECTDIAGRAM ID LBRACE comment obj_seq RBRACE'''
    if p[5]:
        os = ["object-list:"] + p[5]    # ADDY
    else:
        os = p[5]
    p[0] = [p[1]+":", p[2], p[3], p[4], os, p[6]]

def p_obj_seq(p):
    '''obj_seq : obj_seq obj_decl
                 | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_obj_decl(p):
    '''obj_decl : activeOption OBJECT ID COLON genericid LBRACE comment obj_contents RBRACE objassocs comment'''
    if p[8]:
        occ = ["object-contents"] + p[8]
    else:
        occ = p[8]
    if p[10]:
        al = ["association-list"] + p[10]
    else:
        al = p[10]
    if p[1]:
        p[0] = ['object:', p[1], p[2], p[3], p[4], p[5], p[6], p[7], occ, p[9], al, p[11]]
    else:
        p[0] = ['object:', p[2], p[3], p[4], p[5], p[6], p[7], occ, p[9], al, p[11]]

def p_obj_contents(p):
    '''obj_contents : obj_contents attribute_assignment
                      | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_attribute_assignment(p):
    '''attribute_assignment : ID EQ ID SEMIC comment
                            | ID EQ STRING_CONSTANT1 SEMIC comment
                            | ID EQ INT_CONSTANT SEMIC comment'''
    p[0] = ["assignAttribute:", p[1], p[2], p[3], p[4], p[5]]

def p_objassocs(p):
    '''objassocs : objassoc objassoclist SEMIC
                    | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2] + [p[3]]

def p_objassoclist(p):
    '''objassoclist : objassoclist COMMA objassoc
                        | epsilon'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1] + [p[3]]

def p_objassoc(p):
    '''objassoc : role usekeyword role ID'''
    p[0] = [p[2]+":", p[1], p[3], p[4]]

def p_error(p):
    global __global_error__
    global __global_error_string__
    tmperrstring = None
    if p:
        print "Syntax error at '%s'" % p.value, "near line",    \
            __global_line_number__
        tmperrstring = ("ERROR: Syntax error at '%s'" % p.value)    \
            + " near line " + str( __global_line_number__)
    else:
        print "Syntax error at EOF" 
        tmperrstring = "ERROR: Syntax error at EOF"
    if __global_error__ == None:
        __global_error__ = SyntaxError
        __global_error_string__ = tmperrstring

import ply.yacc as yacc
yacc.yacc()

def tokenizeComments(source, comments):
    ''' Put verbatim comments in the comments list, preserve newlines. '''
    result = ''
    i = 0
    lineno = 1
    while i < len(source):
        c = source[i]
        if c == '\n':
            lineno += 1
        if c == '@':
            startOfComment = lineno
            countOfNewlines = 0
            result = result + '@' + str(len(comments)) # @ index @
            remark = ''
            i += 1
            while i < len(source) and source[i] != '@':
                if source[i] == '\n':
                    lineno += 1
                    countOfNewlines += 1
                remark = remark + source[i]
                i += 1
            if i >= len(source):
                raise ValueError, ("ERROR, no closing @ for comment at line "
                    + str(startOfComment))
            comments.append(remark)
            for con in range(0, countOfNewlines):
                result = result + "\n"
            # Maintain line numbers via above loop.
            result = result + '@'       # Close the comment token.
        else:
             result = result + c
        i += 1
    return result

def cleantree(parsetree, comments):
    result = ()
    if (type(parsetree) == list) or (type(parsetree) == tuple):
        for entry in parsetree:
            if not entry:   # None, empty string or list
                continue
            if (type(entry) == list) or (type(entry) == tuple):
                if len(entry) == 3 and entry[0] == '@':
                    entry = ['@', comments[int(entry[1].strip())], '@']
                subpart = cleantree(entry, comments)
                if subpart:
                    result = result + (subpart,)
            else:
                result = result + (str(entry),)
    else:
        raise ValueError, ("COMPILER ERROR: "
            + "Illegal parsetree type: " + str(type(parsetree))
            + ": " + str(parsetree))
    return result

def compile(sourcefilename, debugflag=DEBUG):
    # External hook to the parser.
    global __global_error__
    global __global_error_string__
    global __StateMachineSymbolTable__
    sourcef = open(sourcefilename, 'r')
    source = sourcef.read()
    sourcef.close()
    comments = []
    source = tokenizeComments(source, comments)
    parsetree = yacc.parse(source,debug=debugflag)
    if parsetree != None:
        parsetree = cleantree(parsetree, comments)
        deepstr = pprint.pformat(parsetree, indent=4, width=80)
        fname = (sourcefilename + ".indent").replace('.','_') + ".py"
        sourcef = open(fname, "w")
        sourcef.write('parsetree = \\\n' + deepstr + '\n')
        sourcef.close()
        deepstr = pprint.pformat(parsetree, indent=0, width=80)
        fname = (sourcefilename + ".noindent").replace('.','_') + ".py"
        sourcef = open(fname, "w")
        sourcef.write('parsetree = \\\n' + deepstr + '\n')
        sourcef.close()
    if __global_error__:
        tmperror = __global_error__
        tmpstring = __global_error_string__
        __global_error__ = None             # reset for next time
        __global_error_string__ = None
        raise tmperror, tmpstring
    return parsetree

if __name__=='__main__':
    usage = \
      "python|jython JawsUMLparser.py INFILE"
    if len(sys.argv) != 2:
        sys.stderr.write(usage + '\n')
        sys.exit(1)
    else:
        parsetree = compile(sys.argv[1], debugflag=None)
