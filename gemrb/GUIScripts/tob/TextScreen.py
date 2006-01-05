# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2004 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/GUIScripts/tob/TextScreen.py,v 1.9 2006/01/05 18:04:31 avenger_teambg Exp $

# TextScreen.py - display Loading screen

###################################################

import GemRB
from GUIDefines import *

TextScreen = None
TextArea = None
Chapter = 0

def StartTextScreen ():
	global TextScreen, TextArea, Chapter

	GemRB.LoadWindowPack ("GUICHAP", 640, 480)
	LoadPic = GemRB.GetGameString (STR_LOADMOS)
	#if there is no preset loadpic, try to determine it from the chapter
	if LoadPic == "":
		Chapter = GemRB.GetVar("CHAPTER")
		#set ID according to the Chapter?
		ID = Chapter
	else:
		ID = 62
	TextScreen = GemRB.LoadWindow (ID)
	GemRB.SetWindowFrame (TextScreen)
	if LoadPic != "":
		GemRB.SetWindowPicture (TextScreen, LoadPic)
	TextArea = GemRB.GetControl (TextScreen, 2)
	GemRB.SetTextAreaFlags (TextScreen, TextArea, IE_GUI_TEXTAREA_SMOOTHSCROLL)
	GemRB.SetEvent (TextScreen, TextArea, IE_GUI_TEXTAREA_OUT_OF_TEXT, "FeedScroll")

	#done
	Button=GemRB.GetControl (TextScreen, 0)
	GemRB.SetText (TextScreen, Button, 11973)
	GemRB.SetEvent (TextScreen, Button, IE_GUI_BUTTON_ON_PRESS, "EndTextScreen")

	#replay
	Button=GemRB.GetControl (TextScreen, 3)
	GemRB.SetText (TextScreen, Button, 16510)
	GemRB.SetEvent (TextScreen, Button, IE_GUI_BUTTON_ON_PRESS, "ReplayTextScreen")

	GemRB.HideGUI ()
	GemRB.SetVisible (0, 0) #removing the gamecontrol screen

	GemRB.SetVisible (TextScreen, 1)
	GemRB.RewindTA (TextScreen, TextArea, 300)
	GemRB.GamePause(1, 1)


def FeedScroll ():
	global TextScreen, TextArea, Chapter

	TableName = GemRB.GetGameString (STR_LOADMOS)
	if TableName == "":
		#incrementchapter
		TableName = "CHPTXT"+str(Chapter)
		Table = GemRB.LoadTable(TableName)
		Value = GemRB.GetTableValue (Table, 1, 1)
	else:
		#textscreen
		Table = GemRB.LoadTable(TableName)
		Value = GemRB.GetTableValue (Table, 2, 1)
	GemRB.UnloadTable (Table)
	GemRB.TextAreaAppend (TextScreen, TextArea, Value)


def ReplayTextScreen ():
	global TextScreen, TextArea

	GemRB.SetEvent (TextScreen, TextArea, IE_GUI_TEXTAREA_OUT_OF_TEXT, "FeedScroll")
	GemRB.RewindTA (TextScreen, TextArea, 300)


def EndTextScreen ():
	global TextScreen

	GemRB.SetVisible (TextScreen, 0)
	GemRB.UnloadWindow (TextScreen)
	GemRB.SetVisible (0, 1) #enabling gamecontrol screen
	GemRB.UnhideGUI ()
	GemRB.GamePause(0, 1)
