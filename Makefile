#===============================================================================
#		Makefile for qytdl.py
#		PyQt5 frontend to Youtube-DL
#===============================================================================

PREFIX=/usr
SRC=src
DOC=doc
ICONS=data/icons
INSTALL_PATH=$(PREFIX)/share/qytdl
OUTPUTDIR=$(PREFIX)/bin
OUTPUT=qytdl
DOCPATH=$(PREFIX)/share/doc/qytdl
LICENSEPATH=$(PREFIX)/share/licenses/qytdl

install:
	install $(SRC)/*.py -D -t $(INSTALL_PATH)/src
	install $(ICONS)/*.png -D -t $(INSTALL_PATH)/data/icons/
	install README -D $(DOCPATH)/README
	install $(DOC)/CHANGES -D $(DOCPATH)/CHANGES
	install $(DOC)/LICENSE -D $(LICENSEPATH)/LICENSE
	install qytdl.sh $(OUTPUTDIR)/$(OUTPUT)

uninstall:
	rm -f $(OUTPUTDIR)/$(OUTPUT)
	rm -r $(INSTALL_PATH)
	rm -r $(DOCPATH)
	rm -r $(LICENSEPATH)
