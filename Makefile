################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

ADDON_NAME=service.alexelec.settings
ADDON_VERSION=7.0.0
DISTRONAME:=AlexELEC

BUILDDIR=build
DATADIR=/usr/share/kodi
ADDONDIR=$(DATADIR)/addons

################################################################################

all: $(BUILDDIR)/$(ADDON_NAME)

addon: $(BUILDDIR)/$(ADDON_NAME)-$(ADDON_VERSION).zip

install: $(BUILDDIR)/$(ADDON_NAME)
	mkdir -p $(DESTDIR)/$(ADDONDIR)
	cp -R $(BUILDDIR)/$(ADDON_NAME) $(DESTDIR)/$(ADDONDIR)

clean:
	rm -rf $(BUILDDIR)

uninstall:
	rm -rf $(DESTDIR)/$(ADDONDIR)/$(ADDON_NAME)

$(BUILDDIR)/$(ADDON_NAME): $(BUILDDIR)/$(ADDON_NAME)/resources
	mkdir -p $(BUILDDIR)/$(ADDON_NAME)
	cp -R src/*.png src/*.py $(BUILDDIR)/$(ADDON_NAME)
	cp COPYING $(BUILDDIR)/$(ADDON_NAME)
	cp addon.xml $(BUILDDIR)/$(ADDON_NAME)
	sed -e "s,@ADDONNAME@,$(ADDON_NAME),g" \
	    -e "s,@ADDONVERSION@,$(ADDON_VERSION),g" \
	    -e "s,@DISTRONAME@,$(DISTRONAME),g" \
	    -i $(BUILDDIR)/$(ADDON_NAME)/addon.xml
	cp changelog.txt $(BUILDDIR)/$(ADDON_NAME)

$(BUILDDIR)/$(ADDON_NAME)/resources: $(BUILDDIR)/$(ADDON_NAME)/resources/skins \
                                     $(BUILDDIR)/$(ADDON_NAME)/resources/language
	mkdir -p $(BUILDDIR)/$(ADDON_NAME)/resources
	cp -R src/resources/* $(BUILDDIR)/$(ADDON_NAME)/resources

$(BUILDDIR)/$(ADDON_NAME)/resources/skins: $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/default \
                                           $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/icons
	mkdir -p $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default
	cp -R skins/Default/* $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default

$(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/default:
	mkdir -p $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/default
	cp textures/$(DISTRONAME)/*.png $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/default

$(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/icons:
	mkdir -p $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/icons
	cp icons/*.png $(BUILDDIR)/$(ADDON_NAME)/resources/skins/Default/media/icons

$(BUILDDIR)/$(ADDON_NAME)/resources/language:
	mkdir -p $(BUILDDIR)/$(ADDON_NAME)/resources/language
	cp -R language/* $(BUILDDIR)/$(ADDON_NAME)/resources/language
	sed -e "s,@DISTRONAME@,$(DISTRONAME),g" \
	    -e "s,@ROOT_PASSWORD@,$(ROOT_PASSWORD),g" \
	    -i $(BUILDDIR)/$(ADDON_NAME)/resources/language/*/*.po

$(BUILDDIR)/$(ADDON_NAME)-$(ADDON_VERSION).zip: $(BUILDDIR)/$(ADDON_NAME)
	cd $(BUILDDIR); zip -r $(ADDON_NAME)-$(ADDON_VERSION).zip $(ADDON_NAME)
