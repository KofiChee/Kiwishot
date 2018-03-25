import sys
from Xlib import X, display, Xutil, xobject, Xcursorfont


class xselect:
    def __init__(self):
        # X display
        self.d = display.Display()

        # Screen
        self.screen = self.d.screen()

        # Draw on the root window (desktop surface)
        self.window = self.screen.root
     
    def select_region(self):

        # Set cursor to crosshair
        font = self.d.open_font('cursor')
        cursor = font.create_glyph_cursor(font, Xcursorfont.crosshair,
                                          Xcursorfont.crosshair+1,
                                          (65535, 65535, 65535), (0, 0, 0))

        self.window.grab_pointer(1,
                                 X.PointerMotionMask |
                                 X.ButtonReleaseMask |
                                 X.ButtonPressMask,
                                 X.GrabModeAsync,
                                 X.GrabModeAsync,
                                 X.NONE,
                                 cursor,
                                 X.CurrentTime)

        colormap = self.screen.default_colormap
        color = colormap.alloc_color(0, 0, 0)
        # Xor it because we'll draw with X.GXxor function
        xor_color = color.pixel ^ 0xffffff

        self.gc = self.window.create_gc(
            line_width=1,
            line_style=X.LineSolid,
            fill_style=X.FillOpaqueStippled,
            fill_rule=X.WindingRule,
            cap_style=X.CapButt,
            join_style=X.JoinMiter,
            foreground=xor_color,
            background=self.screen.black_pixel,
            function=X.GXxor,
            graphics_exposures=False,
            subwindow_mode=X.IncludeInferiors,
        )

        done = False
        started = False
        start = dict(x=0, y=0)
        end = dict(x=0, y=0)
        last = None

        while not done:
            e = self.d.next_event()

            # Window has been destroyed, quit
            if e.type == X.DestroyNotify:
                sys.exit(0)

            # Mouse button press
            elif e.type == X.ButtonPress:
                # Left mouse button?
                if e.detail == 1:
                    start = dict(x=e.root_x, y=e.root_y)
                    started = True

                # Right mouse button?
                elif e.detail == 3:
                    sys.exit(0)

            # Mouse button release
            elif e.type == X.ButtonRelease:
                end = dict(x=e.root_x, y=e.root_y)
                if last:
                    self.draw_rectangle(start, last)
                done = True
                pass

            # Mouse movement
            elif e.type == X.MotionNotify and started:
                if last:
                    self.draw_rectangle(start, last)
                    last = None

                last = dict(x=e.root_x, y=e.root_y)
                self.draw_rectangle(start, last)
                pass

            # Keyboard key
            elif e.type == X.KeyPress:
                sys.exit(0)

            elif e.type == X.EnterNotify:
                print('	EnterNotify')

        self.d.ungrab_pointer(0)
        self.d.flush()

        coords = self.get_coords(start, end)
        if coords['width'] <= 1 or coords['height'] <= 1:
            sys.exit(0)
        else:
            return coords

    def get_coords(self, start, end):
        safe_start = dict(x=0, y=0)
        safe_end = dict(x=0, y=0)

        if start['x'] > end['x']:
            safe_start['x'] = end['x']
            safe_end['x'] = start['x']
        else:
            safe_start['x'] = start['x']
            safe_end['x'] = end['x']

        if start['y'] > end['y']:
            safe_start['y'] = end['y']
            safe_end['y'] = start['y']
        else:
            safe_start['y'] = start['y']
            safe_end['y'] = end['y']

        return {
            'start': {
                'x': safe_start['x'],
                'y': safe_start['y'],
            },
            'end': {
                'x': safe_end['x'],
                'y': safe_end['y'],
            },
            'width': safe_end['x'] - safe_start['x'],
            'height': safe_end['y'] - safe_start['y'],
        }

    def draw_rectangle(self, start, end):
        coords = self.get_coords(start, end)
        self.window.rectangle(
            self.gc,
            coords['start']['x'],
            coords['start']['y'],
            coords['end']['x'] - coords['start']['x'],
            coords['end']['y'] - coords['start']['y']
        )
