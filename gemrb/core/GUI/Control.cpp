/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 *
 */

#include "GUI/Control.h"
#include "GUI/Window.h"

#include "win32def.h"

#include "ControlAnimation.h"
#include "Sprite2D.h"

#ifdef ANDROID
#include "Variables.h"
#endif

#include <cstdio>
#include <cstring>

namespace GemRB {

Control::Control(const Region& frame)
	: View(frame)
{
	InHandler = false;
	VarName[0] = 0;
	Value = 0;
	Owner = NULL;

	animation = NULL;
	AnimPicture = NULL;
	ControlType = IE_GUI_INVALID;
}

Control::~Control()
{
	if (InHandler) {
		Log(ERROR, "Control", "Destroying control inside event handler, crash may occur!");
	}
	delete animation;

	Sprite2D::FreeSprite(AnimPicture);
}

void Control::SetText(const String* string)
{
	SetText((string) ? *string : L"");
}

void Control::ResetEventHandler(ControlEventHandler &handler)
{
	handler = NULL;
}

//return -1 if there is an error
//return 1 if there is no handler (not an error)
//return 0 if the handler ran as intended
int Control::RunEventHandler(ControlEventHandler handler)
{
	if (InHandler) {
		Log(WARNING, "Control", "Nested event handlers are not supported!");
		return -1;
	}
	if (handler) {
		Window *wnd = Owner;
		if (!wnd) {
			return -1;
		}
		InHandler = true;
		//TODO: detect caller errors, trap them???
		handler(this);
		InHandler = false;
		return 0;
	}
	return 1;
}

void Control::UpdateState(const char* varname, unsigned int val)
{
	if (strnicmp(VarName, varname, MAX_VARIABLE_LENGTH-1) == 0) {
		UpdateState(val);
	}
}

void Control::SetFocus(bool focus)
{
	Owner->SetFocused((focus) ? this : NULL);
	MarkDirty();
}

bool Control::IsFocused()
{
	return Owner->FocusedView() == this;
}

void Control::SetAnimPicture(Sprite2D* newpic)
{
	Sprite2D::FreeSprite(AnimPicture);
	AnimPicture = newpic;
	MarkDirty();
}

}
