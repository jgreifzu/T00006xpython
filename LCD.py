"""
/******** Communication commands */
#define MATRIX_BAUDRATE 0x39       // 1 arg
//#define MATRIX_BAUDRATE2 0xA4      // not supported

/******** text commands */
#define MATRIX_AUTOSCROLL_ON 0x51
#define MATRIX_AUTOSCROLL_OFF 0x52
#define MATRIX_CLEAR 0x58
#define MATRIX_CHANGESPLASH 0x40  // COL * ROW chars!
#define MATRIX_AUTOWRAPLINE_ON 0x43
#define MATRIX_AUTOWRAPLINE_OFF 0x44
#define MATRIX_SETCURSOR_POSITION 0x47    // 2 args: col, row
#define MATRIX_HOME 0x48
#define MATRIX_MOVECURSOR_BACK 0x4C
#define MATRIX_MOVECURSOR_FORWARD 0x4D
#define MATRIX_UNDERLINECURSOR_ON 0x4A
#define MATRIX_UNDERLINECURSOR_OFF 0x4B
#define MATRIX_BLOCKCURSOR_ON 0x53
#define MATRIX_BLOCKCURSOR_OFF 0x54

/****** special chars */
#define MATRIX_CUSTOM_CHARACTER 0x4E  // 9 args: char #, 8 bytes data
#define MATRIX_SAVECUSTOMCHARBANK 0xC1  // 9 args: char #, 8 bytes data
#define MATRIX_LOADCUSTOMCHARBANK 0xC0  // 9 args: char #, 8 bytes data
/***** Numbers & Bargraphs */
// not supported until we know what these look like
//#define MATRIX_PLACEMEDIUMDIGIT 0x6F
/***** display func */
#define MATRIX_DISPLAY_ON  0x42    // backlight. 1 argument afterwards, in minutes
#define MATRIX_DISPLAY_OFF  0x46
#define MATRIX_SET_BRIGHTNESS 0x99 // 1 arg: scale
#define MATRIX_SETSAVE_BRIGHTNESS 0x98 // 1 arg: scale
#define MATRIX_SET_CONTRAST 0x50 // 1 arg
#define MATRIX_SETSAVE_CONTRAST 0x91 // 1 arg
/***** GPO commands */
#define MATRIX_GPO_OFF 0x56
#define MATRIX_GPO_ON 0x57
#define MATRIX_GPO_START_ONOFF 0xC3

/***** Extra Adafruit commands */
#define EXTENDED_RGBBACKLIGHT 0xD0  // 3 args - R G B
#define EXTENDED_SETSIZE 0xD1  // 2 args - Cols & Rows
#define EXTENDED_TESTBAUD 0xD2  // zero args, prints baud rate to uart


#define MATRIX_STARTL_COMMAND 0xFE
"""


#to be used with tinkerkit t00006x connected with microusb cable
import serial
import time

class LCD:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.flush()
        self.clear_screen()
        self.move_home()
        self.current_text = [""] * 32
        self.cur_pos = 0
        print("init")
        
        
    def command(self, hexCommand, args=None):
        packet = bytearray()
        packet.append(0xFE)
        packet.append(hexCommand)
        if args != None:
            for i in args:
                packet.append(i)
        self.ser.write(packet)
        
    def clear_screen(self):
        self.command(0x58)
        self.current_text = [""] * 32
        self.cur_pos = 0
        
    def move_home(self):
        self.command(0x48)
        
    def set_autoscroll(self, onOrOff):
        if onOrOff:
            self.command(0x51)
            print("set autoscrolling on")
        else:
            self.command(0x52)
            
    def display_text(self, text):
        print("sending: " + text)
        self.ser.write(text.encode('utf-8'))
        for i in range(len(text)):
            print("loop: " + str(i))
            print("text[i] = " + text[i])
            print("cur_pos = " + str(self.cur_pos))
            print("current_text pos = " + self.current_text[i + self.cur_pos])
            print("\n")
            self.current_text[self.cur_pos] = text[i]
            self.cur_pos = self.cur_pos + 1
    
    def set_cursor_pos(self, col, row):
        self.command(0x47, [col,row])
        
    def move_cursor_fwd(self):
        self.command(0x4D)
        
    def move_cursor_rev(self):
        self.command(0x4C)    
        
        
        

screen = LCD()
screen.display_text("123")
screen.display_text("456")
screen.display_text("456")
screen.display_text("456")

print(screen.current_text)


