builddir := build
sourcedir := src
datadir := data
linkdir := $(builddir)/lnk

romext := sfc
romfile := $(builddir)/SuperRoadBlaster.$(romext)

linker := wlalink
linkflags := -dsr
linkobjectfile := $(linkdir)/linkobjs.lst

assembler := wla-65816
assemblerflags := -o

spcasm = wla-spc700
spcflags = -o
spclinkflags := -sb
spclinkobjectfile := $(linkdir)/spclinkobjs.lst

gfxconverter :=./tools/gracon.py
verify := -verify on
gfx_font_flags := $(verify) -optimize off -palettes 1 -bpp 2 -mode bg
gfx_font4bpp_flags := $(verify) -optimize off -palettes 1 -bpp 4 -mode bg

gfx_bg_flags := $(verify) -optimize on -tilethreshold 15 -palettes 8 -bpp 4 -mode bg
gfx_directcolor_flags := $(verify) -optimize on -directcolor on -tilethreshold 10 -palettes 1 -bpp 8 -mode bg
gfx_video_flags := $(verify) -optimize on -tilethreshold 13 -maxtiles 512 -palettes 8 -bpp 4 -mode bg
gfx_sprite_flags := $(verify) -optimize on -tilethreshold 10 -palettes 2 -bpp 4 -mode sprite

msu1converter := ./tools/msu1blockwriter.py
msu1flags := -title 'SUPER ROAD BLASTER'

msu1audioconverter := ./tools/msu1pcmwriter.py
songconverter := ./tools/mod2snes.py

xmlchapterconverter := ./tools/xmlsceneparser.py

animation_converter := ./tools/animationWriter.py

sound_converter := snesbrr

RD := $(RM) -r
MD := mkdir -p

empty :=
space := $(empty) $(empty)

asmsource := 65816
asmobj := o
asmheader := h

spcsource := spc700
spcobject := spo
spcbinary := bin

image := png
tile := tiles
spriteanimation := animation

song := mod
spcsong := spcmod

sound := wav
spcsound := brr

msu1audio := pcm
msu1ext := msu
chapter_builddir := $(builddir)/$(datadir)/chapters



sourcefiles := $(shell find $(sourcedir)/ -type f -name '*.$(asmsource)')
objects := $(addprefix $(builddir)/,$(patsubst %.$(asmsource), %.$(asmobj), $(sourcefiles)))
configfiles := $(shell find $(sourcedir)/ -type f -name '*.inc' -o -name '*.opcodes' -o -name '*.registers')
scriptfiles := $(shell find $(sourcedir)/ -type f -name '*.inc' -o -name '*.opcodes' -o -name '*.script') $(shell find $(datadir)/ -type f -name '*.inc' -o -name '*.opcodes' -o -name '*.script')
interfacefiles := $(shell find $(sourcedir)/ -type f -name '*.interface')
inheritancefiles := $(shell find $(sourcedir)/ -type f -name '*.inheritance')


#this is a hack
videofile := $(shell find $(datadir)/ -type f -name '*.mp4')
convertedframefolder := cimg2
#convertedframefolder := /media/toshiba/build/data/frames
chapterfolder := $(datadir)/chapters
eventfolder := $(datadir)/events
scriptmaster := $(chapterfolder)/chapter.include

scripteventxml := xml
chapterscript := script
scripteventxmls := $(sort $(shell find $(datadir)/ -type f -name '*.$(scripteventxml)'))
chapterscripts := $(scripteventxmls:$(eventfolder)%.$(scripteventxml)=$(chapterfolder)%/chapter.$(chapterscript))
chapteridfiles := $(shell find $(datadir)/ -type f -name 'chapter.id.*')

spcsourcefiles := $(shell find $(sourcedir)/ -type f -name '*.$(spcsource)')
spcobjects := $(addprefix $(builddir)/,$(patsubst %.$(spcsource), %.$(spcobject), $(spcsourcefiles)))
spcbin = $(firstword $(addprefix $(builddir)/,$(patsubst %.$(spcsource), %.$(spcbinary), $(spcsourcefiles))))


graphics := $(shell find $(datadir)/ -type f -name '*.gfx_normal.$(image)')
graphics += $(shell find $(datadir)/ -type f -name '*.gfx_font*.$(image)')
converted_graphics := $(sort $(addprefix $(builddir)/,$(patsubst %.$(image), %.$(tile), $(graphics))))

video_graphics := $(shell find $(datadir)/ -type f -name '*.gfx_video.$(image)')
converted_video_graphics := $(sort $(addprefix $(builddir)/,$(patsubst %.$(image), %.$(tile), $(video_graphics))))

bg_animations := $(shell find $(datadir)/ -type d -name '*.gfx_bg')
bg_animations += $(shell find $(datadir)/ -type d -name '*.gfx_directcolor')
converted_bg_animations := $(sort $(addprefix $(builddir)/,$(addsuffix .$(spriteanimation), $(bg_animations))))
sprite_animations := $(shell find $(datadir)/ -type d -name '*.gfx_sprite')
converted_sprite_animations := $(sort $(addprefix $(builddir)/,$(addsuffix .$(spriteanimation), $(sprite_animations))))

songs := $(shell find $(datadir)/ -type f -name '*.$(song)')
converted_songs := $(addprefix $(builddir)/,$(patsubst %.$(song), %.$(spcsong), $(songs)))

sounds := $(shell find $(datadir)/ -type f -name '*.sfx_normal.$(sound)')
sounds += $(shell find $(datadir)/ -type f -name '*.sfx_loop.$(sound)')
converted_sounds := $(sort $(addprefix $(builddir)/,$(patsubst %.$(sound), %.$(spcsound), $(sounds))))

sfx_normal_flags := -e
sfx_loop_flags := -e -l 0

video_sounds := $(shell find $(datadir)/ -type f -name '*.sfx_video.$(sound)')
converted_video_sounds := $(sort $(addprefix $(builddir)/,$(patsubst %.$(sound), %.$(msu1audio), $(video_sounds))))


chapterids := $(shell find $(datadir)/ -type f -name 'chapter.id.*')
buildchapterids := $(sort $(addprefix $(builddir)/,$(chapterids)))


msu1file := $(romfile:$(romext)=$(msu1ext))

#datafiles := $(msu1file) $(converted_graphics) $(converted_sprite_animations) $(converted_bg_animations) $(converted_songs) $(converted_sounds) $(spcbin)
datafiles := $(converted_graphics) $(converted_sprite_animations) $(converted_bg_animations) $(converted_songs) $(converted_sounds) $(spcbin)
builddirs := $(sort $(dir $(objects) $(datafiles)) $(linkdir))

#link 65816 objects
all: $(linkobjectfile)
	$(linker) $(linkflags) $(linkobjectfile) $(romfile)

#create necessary directory substructure in build directory
$(builddirs): $(chapterscripts)
	$(MD) $@

#create 65816 object linkfile
$(linkobjectfile): $(objects)
	$(shell echo "[objects]" > $(linkobjectfile))
	$(foreach obj, $(objects), $(shell echo "$(obj)" >> $(linkobjectfile)))

#compile 65816 assembler sourcefiles
#Static Pattern Rules $(targets): target-pattern: target-prereqs
$(objects): $(builddir)/%.$(asmobj): %.$(asmsource) %.$(asmheader) $(configfiles) $(scriptfiles) $(interfacefiles) $(inheritancefiles) $(datafiles) | $(builddirs)
	$(assembler) $(assemblerflags) $< $@

#link spc700 objects
$(spcbin): $(spclinkobjectfile)
	$(linker) $(spclinkflags) $(spclinkobjectfile) $(spcbin)

#create spc700 object linkfile
$(spclinkobjectfile): $(spcobjects)
	$(shell echo "[objects]" > $(spclinkobjectfile))
	$(foreach obj, $(spcobjects), $(shell echo "$(obj)" >> $(spclinkobjectfile)))

#compile spc700 assembler sourcefiles
$(spcobjects): $(builddir)/%.$(spcobject): %.$(spcsource) | $(builddirs)
	$(spcasm) $(spcflags) $< $@


#convert graphic files. conversion flags are determined by special string inside filename ".gfx_%." (e.g. fixed8x8.gfx_font.png) and fetched from corresponding variable name ($(gfx_font_flags) in this case)
$(converted_graphics): $(builddir)/%.$(tile): %.$(image) | $(builddirs)
	$(gfxconverter) $($(filter gfx_%, $(subst .,$(space), $@))_flags) -infile $< -outfilebase $(patsubst %.$(tile), %, $@)


#convert pro tracker mod files to custom spcmod format
$(converted_songs): $(builddir)/%.$(spcsong): %.$(song) | $(builddirs)
	$(songconverter) $< $(patsubst %.$(spcsong), %, $@)

#copy chapter id files over to build dir
$(buildchapterids): $(builddir)/%: % | $(builddirs)
	$(shell cp $< $@)


#build msu1 video file from converted video images
$(msu1file): $(buildchapterids) $(converted_video_graphics) $(converted_video_sounds) | $(builddirs)
	$(msu1converter) $(msu1flags) -infilebase $(chapter_builddir) -outfile $@

#convert wav files to custom msu1 audio format
$(converted_video_sounds): $(builddir)/%.$(msu1audio): %.$(sound) | $(builddirs)
	$(msu1audioconverter) -infile $< -outfile $@

#convert wav files to brr sample format
$(converted_sounds): $(builddir)/%.$(spcsound): %.$(sound) | $(builddirs)
	$(sound_converter) $($(filter sfx_%, $(subst .,$(space), $@))_flags) $< $@

#convert msu1 video graphic files. conversion flags are determined by special string inside filename ".gfx_%." (e.g. fixed8x8.gfx_font.png) and fetched from corresponding variable name ($(gfx_font_flags) in this case)
$(converted_video_graphics): $(builddir)/%.$(tile): %.$(image) | $(builddirs)
	$(gfxconverter) $($(filter gfx_%, $(subst .,$(space), $@))_flags) -infile $< -outfilebase $(patsubst %.$(tile), %, $@)

#convert sprite animation folders to sprite animation file
$(converted_sprite_animations): $(builddir)/%.$(spriteanimation): % | $(builddirs)
	$(animation_converter) -mode sprite -infolder $< -outfile $@

#convert bg animation folders to sprite animation file
$(converted_bg_animations): $(builddir)/%.$(spriteanimation): % | $(builddirs)
	$(animation_converter) $($(filter gfx_%, $(subst .,$(space), $@))_flags) -infolder $< -outfile $@


#hack used for initial script/chapter building, not really part of the actual build process
$(chapterscripts): $(chapterfolder)%/chapter.$(chapterscript):$(eventfolder)%.$(scripteventxml)
	$(xmlchapterconverter) -infile $< -outfolder $(chapterfolder)
#	$(xmlchapterconverter) -infile $< -outfolder $(chapterfolder) -videofile $(videofile) -convertedframefolder $(convertedframefolder) -convertedoutfolder $(builddir)/$(chapterfolder)

clean:
	$(RD) $(chapterfolder)
	$(RD) $(builddir)
