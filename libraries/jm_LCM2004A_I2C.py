from Arduino import *
from Wire import *

# Clear display
# =============
# Clears entire display and sets DDRAM address 0 in address rd_IR.
#
# Execution time: 1520us ???
#
HD44780_CLEAR       = 0b00000001

# Return home
# ===========
#
# Sets DDRAM address 0 in address rd_IR.
# Also returns display from being shifted to original position.
# DDRAM contents remain unchanged.
#
# Execution time: 1520us
#
HD44780_HOME        = 0b00000010

# Entry mode set
# ==============
#
# Sets cursor mode direction and specifies display shift.
# These operations are performed during data write and read.
#
# I/D = 1: Increment
# I/D = 0: Decrement
# S   = 1: Accompanies display shift
#
# Execution time: 37us
#
HD44780_ENTRY       = 0b00000100
HD44780_ENTRY_I_D   = 0b00000010
HD44780_ENTRY_S     = 0b00000001

# Display on/off control
# ======================
#
# Sets entire display (D) on/off, cursor on/off (C),
# and blinking of cursor position character (B).
#
# Execution time: 37us
#
HD44780_CONTROL     = 0b00001000
HD44780_CONTROL_D   = 0b00000100
HD44780_CONTROL_C   = 0b00000010
HD44780_CONTROL_B   = 0b00000001

# Cursor or display shift
# =======================
#
# Moves cursor and shifts display without changing DDRAM contents.
#
# S/C = 1: Display shift
# S/C = 0: Cursor move
# R/L = 1: Shift to the right
# R/L = 0: Shift to the left
#
# Execution time: 37us
#
HD44780_SHIFT       = 0b00010000
HD44780_SHIFT_S_C   = 0b00001000
HD44780_SHIFT_R_L   = 0b00000100

# Function set
# ============
#
# Sets interface data length (DL), number of data lines (N), and character font (F).
#
# DL  = 1: 8 bits, 0: 4bit mode
# N   = 1: 2 lines, 0: 1 line
# F   = 1: 5x10 dots, 0: 5x8 dots
#
# Execution time: 37us
#
HD44780_FUNCTION    = 0b00100000
HD44780_FUNCTION_DL = 0b00010000
HD44780_FUNCTION_N  = 0b00001000
HD44780_FUNCTION_F  = 0b00000100

# Set CGRAM address
# =================
#
# Sets CGRAM address.
# CGRAM data is sent and received after this setting.
#
# Execution time: 37us
#
HD44780_CGRAM       = 0b01000000
HD44780_CGRAM_ACG   = 0b00111111

# Set DDRAM address
# =================
#
# Sets DDRAM address.
# DDRAM data is sent and received after this setting.
#
# Execution time: 37us
#
HD44780_DDRAM       = 0b10000000
HD44780_DDRAM_ADD   = 0b01111111

# Read busy flag & address
# ========================
#
# Reads busy flag (BF) indicating internal operation is being performed
# and reads address rd_IR contents.
# BF  = 1: Internally operating
# BL  = 0: Instructions acceptable
# AC  = Address rd_IR used for both DD and CGRAM addresses
#
# Execution time: 0us
#
HD44780_READ        = 0b00000000
HD44780_READ_BF     = 0b10000000
HD44780_READ_AC     = 0b01111111

# ---------------------------------------------------------------------------

LCM2004A_I2C_ADR1   = 0x3F          # default PCF8574A I2C address
LCM2004A_I2C_ADR2   = 0x27          # alternative PCF8574 I2C address

LCM2004A_I2C_DB     = 0b11110000    # P7-P4: Four high order data bus pins
LCM2004A_I2C_DB7    = 0b10000000    # P7
LCM2004A_I2C_DB6    = 0b01000000    # P6
LCM2004A_I2C_DB5    = 0b00100000    # P5
LCM2004A_I2C_DB4    = 0b00010000    # P4
LCM2004A_I2C_BL     = 0b00001000    # P3: LCD backlight (1/0)
LCM2004A_I2C_E      = 0b00000100    # P2: Enables data bus input/output (1/0)
LCM2004A_I2C_R_W    = 0b00000010    # P1: Selects Read/Write (1/0)
LCM2004A_I2C_RS     = 0b00000001    # P0: Selects Instruction/Data register (0/1)

# ---------------------------------------------------------------------------


from Stream import *
from jm_PCF8574 import *

class jm_LCM2004A_I2C(Stream):
#class jm_LCM2004A_I2C(Stream, jm_PCF8574):

    # jm_LCM2004A_I2C...

    def __init__(self, i2c_address=0, wire=Wire):
        super(jm_LCM2004A_I2C, self).__init__()
        self._pcf8574 = jm_PCF8574(i2c_address, wire)
        self._connected = False
        self._BL = True # Backlight On
        self._entry_mode_set = 0
        self._display_control = 0
        self._cursor_display_shift = 0
        self._function_set = 0

    def __del__(self):
        del self._pcf8574
        super(jm_LCM2004A_I2C, self).__del__()

    def __bool__(self):
        return self.connected()

# ---------------------------------------------------------------------------

    # jm_PCF8574...

    def pcf8574(self):
        return self._pcf8574

    def i2c_address(self):
        return self._pcf8574.i2c_address()

    def wire(self):
        return self._pcf8574.wire()

    def connected(self):
        return (self._connected and self._pcf8574.connected())

# ---------------------------------------------------------------------------

    # Stream (and Print)...

    def begin(self, i2c_address=0): # return OK
        if (i2c_address == 0):
            if (self._pcf8574.connected() or (self._pcf8574.i2c_address() != 0x00)):
                return self.reset(self._pcf8574.i2c_address()) # redo reset() ?
            else:
                return (self.reset(LCM2004A_I2C_ADR1) or self.reset(LCM2004A_I2C_ADR2))
        else:
            return self.reset(i2c_address)

    def end(self):
        self._connected = False
        return self._pcf8574.end()

    def read_char(self):
        return self.rd_datareg()

    def write_char(self, c):
        return self.wr_datareg(c)

# ---------------------------------------------------------------------------

    # P7-P4: Four high order data bus pins...

    def wr_highorder(self, DB, RS, us): # return 1 or 0 (fail)
        if (not self.connected()): return 0

        s = bytes([
                (
                    (DB & LCM2004A_I2C_DB) |
                    (LCM2004A_I2C_BL if self._BL else 0) |
                    (LCM2004A_I2C_E  if i==1 else 0) |
                    0 |
                    (LCM2004A_I2C_RS if RS else 0)
                ) for i in range(3)
            ])

        #if (self._pcf8574.write(s) != 3): self._connected=False; return 0
        if (self._pcf8574.write(s[0]) != 1): self._connected=False; return 0
        if (self._pcf8574.write(s[1]) != 1): self._connected=False; return 0
        if (self._pcf8574.write(s[2]) != 1): self._connected=False; return 0
        self._pcf8574.wait(us + us/10) # add 10% HD44780U frequency shifting error (p.25)

        return 1

    def rd_highorder(self, RS): # return byte (high data) or -1 (fail)
        if (not self.connected()): return -1

        s = bytes([
                (
                    LCM2004A_I2C_DB |
                    (LCM2004A_I2C_BL if self._BL else 0) |
                    (LCM2004A_I2C_E  if i==1 else 0) |
                    LCM2004A_I2C_R_W |
                    (LCM2004A_I2C_RS if RS else 0)
                ) for i in range(3)
            ])

        #if (self._pcf8574.write(s[0:2]) != 2): self._connected=False; return -1
        if (self._pcf8574.write(s[0]) != 1): self._connected=False; return -1
        if (self._pcf8574.write(s[1]) != 1): self._connected=False; return -1
        result = self._pcf8574.read();
        if (result == -1): self._connected=False; return -1
        if (self._pcf8574.write(s[2]) != 1): self._connected=False; return -1

        return (result & LCM2004A_I2C_DB)

# ---------------------------------------------------------------------------

    # P7-P0: Eight data bus pins...

    def wr_databus(self, DB, RS, us): # return 1 or 0 (fail)
        if (self.wr_highorder((DB << 0), RS, 0) != 1): return 0
        if (self.wr_highorder((DB << 4), RS, us) != 1): return 0

        return 1

    def rd_databus(self, RS): # return byte or -1 (fail)
        result1 = self.rd_highorder(RS)
        if (result1 == -1): return -1
        result2 = self.rd_highorder(RS)
        if (result2 == -1): return -1

        return ((result1 >> 0) | (result2 >> 4))

# ---------------------------------------------------------------------------

    # IR: Instruction Register...

    def wr_instreg(self, data, us): # return 1 or 0 (fail)
        return self.wr_databus(data, False, us)

    def rd_instreg(self): # return byte or -1 (fail)
        return self.rd_databus(False)

# ---------------------------------------------------------------------------

    # DR: Data Register...

    def wr_datareg(self, data): # return 1 or 0 (fail)
        return self.wr_databus(data, True, 0)

    def rd_datareg(self): # return byte or -1 (fail)
        return self.rd_databus(True)


# ---------------------------------------------------------------------------

    def reset(self, i2c_address): # return OK
        if not self._pcf8574.connected():
            if not self._pcf8574.begin(i2c_address): self._connected=False; return False
        if (self._pcf8574.write(LCM2004A_I2C_BL if self._BL else 0) != 1): self._connected=False; return False

        # HD44780U software reset after Power On...

        #ms = millis()
        #if ms<40: self._pcf8574.wait((ms-40)*1000) # wait 40ms after Power On
        self._pcf8574.wait(40*1000) # wait 40ms after Power On

        self._connected = True

        #  Hardware Reset
        #  --------------
        #  1.   Display clear
        #  2.   Function set:
        #          DL = 1; 8-bit interface data
        #          N = 0; 1-line display
        #          F = 0; 5 × 8 dot character font
        #  3.   Display on/off control:
        #          D = 0; Display off
        #          C = 0; Cursor off
        #          B = 0; Blinking off
        #  4.   Entry mode set:
        #          I/D = 1; Increment by 1
        #          S = 0; No shift

        # Initializing by Instruction...

        if (self.wr_highorder(HD44780_FUNCTION | HD44780_FUNCTION_DL, False, 4100) != 1): return False
        if (self.wr_highorder(HD44780_FUNCTION | HD44780_FUNCTION_DL, False, 100) != 1): return False
        if (self.wr_highorder(HD44780_FUNCTION | HD44780_FUNCTION_DL, False, 37) != 1): return False

        # 8bit mode after above sequence.

        # switch from 8bit mode to 4bit mode...

        if (self.wr_highorder(HD44780_FUNCTION | 0                  , False, 37) != 1): return False

        # confirm 4bit mode and set 4x20 characters, 5x8 dots...

        # Function set default: 4bit mode; 2 lines; 5x8 dots
        if not self.function_set(
            HD44780_FUNCTION
            # HD44780_FUNCTION_DL
            | HD44780_FUNCTION_N
            # HD44780_FUNCTION_F
        ): return False

        # Display control: Display off; Cursor off; Blink off
        if not self.display_control(
            HD44780_CONTROL
            # HD44780_CONTROL_D
            # HD44780_CONTROL_C
            # HD44780_CONTROL_B
        ): return False

        #if not self.clear_display(): return False                         # Clear display
        #if not self.return_home(): return False                         # Return home

        # Entry mode set: Increment; not Accompanies display shift
        if not self.entry_mode_set(
            HD44780_ENTRY
            | HD44780_ENTRY_I_D
            # HD44780_ENTRY_S
        ): return False

        #if not self.return_home(): return False                         # Return home

        # Cursor display shift: no Display shift/Cursor move; Shift to the right
        if not self.cursor_display_shift(
            HD44780_SHIFT
            # HD44780_SHIFT_S_C
            | HD44780_SHIFT_R_L
        ): return False

        #if not self.return_home(): return False                         # Return home

        if not self.clear_display(): return False                         # Clear display

        # Display control: Display on; Cursor off; Blink off
        if not self.display_control(
            HD44780_CONTROL
            | HD44780_CONTROL_D
            # HD44780_CONTROL_C
            # HD44780_CONTROL_B
        ): return False

        return True

# ---------------------------------------------------------------------------

    def clear_display(self): # return OK
        return self.wr_instreg(HD44780_CLEAR, 1520)==1

    def return_home(self): # return OK
        return self.wr_instreg(HD44780_HOME, 37)==1 # 1520)==1

# ---------------------------------------------------------------------------

    def entry_mode_set(self, ems=None): # return OK
        if ems==None:
            return self._entry_mode_set
        else:
            self._entry_mode_set = ems
            return self.wr_instreg(self._entry_mode_set, 37)==1

    def display_control(self, dc=None): # return OK
        if dc==None:
            return self._display_control
        else:
            self._display_control = dc
            return self.wr_instreg(self._display_control, 37)==1

    def cursor_display_shift(self, cds=None): # return OK
        if cds==None:
            return self._cursor_display_shift
        else:
            self._cursor_display_shift = cds
            return self.wr_instreg(self._cursor_display_shift, 37)==1

    def function_set(self, fs=None): # return OK
        if fs==None:
            return self._function_set
        else:
            self._function_set = fs
            return self.wr_instreg(self._function_set, 37)==1

# ---------------------------------------------------------------------------

    def set_cgram_addr(self, ACG): # return OK
        return (self.wr_instreg(HD44780_CGRAM | (ACG & HD44780_CGRAM_ACG), 37) == 1)

    def set_ddram_addr(self, ADD): # return OK
        return (self.wr_instreg(HD44780_DDRAM | (ADD & HD44780_DDRAM_ADD), 37) == 1)

# ---------------------------------------------------------------------------

    #def entry_mode_set_(self, I_D, S): # return OK
    #    return self.entry_mode_set(HD44780_ENTRY | (HD44780_ENTRY_I_D if I_D else 0) | (HD44780_ENTRY_S if S else 0))
    #
    #def display_control_(self, D, C, B): # return OK
    #    return self.display_control(HD44780_CONTROL | (HD44780_CONTROL_D if D else 0) | (HD44780_CONTROL_C if C else 0) | (HD44780_CONTROL_B if B else 0))
    #
    #def cursor_display_shift_(self, S_C, R_L): # return OK
    #    return self.cursor_display_shift(HD44780_SHIFT | (HD44780_SHIFT_S_C if S_C else 0) | (HD44780_SHIFT_R_L if R_L else 0))
    #
    #def function_set_(self, DL, N, F): # return OK
    #    return self.function_set(HD44780_FUNCTION | (HD44780_FUNCTION_DL if DL else 0) | (HD44780_FUNCTION_N if N else 0) | (HD44780_FUNCTION_F if F else 0))

# ---------------------------------------------------------------------------

    def set_cursor(self, col, row): # return OK
        return (self.set_ddram_addr(col + (64 if (row & 1) else 0) + (20 if (row & 2) else 0)) == 1)

# ---------------------------------------------------------------------------

    def write_cgram(self, index, count, font5x8): # return OK
        if not self.set_cgram_addr(index * 8): return False

        for i in range(count):
            if (self.write_bstr(font5x8[i*8: i*8+8]) != 8): return False
            delay(10)

        return True

# ---------------------------------------------------------------------------

    # LiquidCrystal compatibility
    # ===========================

    # high level commands, for the user!

    def clear(self):
        self.clear_display()

    def home(self):
        self.return_home()

    def setCursor(self, col, row):
        self.set_cursor(col, row)

    # Turn the display on/off (quickly)

    def noDisplay(self):
        self._display_control &= ~HD44780_CONTROL_D
        self.wr_instreg(self._display_control, 37)

    def display(self):
        self._display_control |= HD44780_CONTROL_D
        self.wr_instreg(self._display_control, 37)

    # Turns the underline cursor on/off

    def noCursor(self):
        self._display_control &= ~HD44780_CONTROL_C
        self.wr_instreg(self._display_control, 37)

    def cursor(self):
        self._display_control |= HD44780_CONTROL_C
        self.wr_instreg(self._display_control, 37)

    # Turn on and off the blinking cursor

    def noBlink(self):
        self._display_control &= ~HD44780_CONTROL_B
        self.wr_instreg(self._display_control, 37)

    def blink(self):
        self._display_control |= HD44780_CONTROL_B
        self.wr_instreg(self._display_control, 37)

    # These commands scroll the display without changing the RAM

    def scrollDisplayLeft(self):
        self._cursor_display_shift = (
            HD44780_SHIFT
            | HD44780_SHIFT_S_C
            # HD44780_SHIFT_R_L
        )
        self.wr_instreg(self._cursor_display_shift, 37)

    def scrollDisplayRight(self):
        self._cursor_display_shift = (
            HD44780_SHIFT
            | HD44780_SHIFT_S_C
            | HD44780_SHIFT_R_L
        )
        self.wr_instreg(self._cursor_display_shift, 37)

    # This is for text that flows Left to Right

    def leftToRight(self):
        self._entry_mode_set |= HD44780_ENTRY_I_D
        self.wr_instreg(self._entry_mode_set, 37)

    # This is for text that flows Right to Left

    def rightToLeft(self):
        self._entry_mode_set &= ~HD44780_ENTRY_I_D
        self.wr_instreg(self._entry_mode_set, 37)

    # This will 'right justify' text from the cursor

    def autoscroll(self):
        self._entry_mode_set |= HD44780_ENTRY_S
        self.wr_instreg(self._entry_mode_set, 37)

    # This will 'left justify' text from the cursor

    def noAutoscroll(self):
        self._entry_mode_set &= ~HD44780_ENTRY_S
        self.wr_instreg(self._entry_mode_set, 37)

    # Allows us to fill the first 8 CGRAM locations
    # with custom characters

    def createChar(self, location, charmap):
        self.write_cgram(location, 1, charmap)

    # mid level commands, for sending data/cmds

    def command(self, value):
        self.wr_instreg(value, 0)

    def send(self, value):
        self.wr_datareg(value)
