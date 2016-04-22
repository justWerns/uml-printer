#       makefile for jawsuml project
#       Dr. Dale Parson. Spring 2016

all:		build

TARGET = jawsuml
DEBUG = 1
UMLFILES = $(wildcard *.uml)
JOBJFILES := $(subst .uml,_uml_indent.jobj,$(UMLFILES))
INDENTFILES := $(subst .uml,_uml_indent.py,$(UMLFILES))
REFFILES := $(subst _uml_indent.py,_uml_indent.ref,$(INDENTFILES))
MODULEFILES := $(subst .uml,_uml_indent,$(UMLFILES))

include ./makelib

build:	$(JOBJFILES) VisitParseTree.class

VisitParseTree.class:	VisitParseTree.java
		javac -g VisitParseTree.java

$(JOBJFILES):		JawsUMLparser.py PyToJava.py

%_uml_indent.jobj :		%.uml
		python JawsUMLparser.py $<
		CLASSPATH=. jython PyToJava.py `echo $@ | cut -d. -f1`

clean:		subclean
		/bin/rm -f parsetab* *.pyc *.class parser.out ply/*.class ply/*.pyc
		/bin/rm -f *indent.py *.jobj *jobj.debug *.dif *.out

test:	build $(REFFILES) JavaDumpTree

%_uml_indent.ref:		%_uml_indent.py
		diff $< $@ > $@.dif
		touch $@

JavaDumpTree:	VisitParseTree.class
		 CLASSPATH=. java VisitParseTree $(JOBJFILES) > JavaDumpTree.out
		 diff JavaDumpTree.out JavaDumpTree.ref > JavaDumpTree.dif
