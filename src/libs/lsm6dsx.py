########################################
# Function: Driver for LSM6DSx IMU
# Author: Louis Barbier
# MIT License
########################################

import struct
import time
 
LSM6DSx_FUNC_CFG_ACCESS = 0x01
LSM6DSx_PIN_CTRL = 0x02 # RW (00111111)
# RESERVED 0x03
LSM6DSx_S4S_TPH_L = 0x04 # RW (0000000)
LSM6DSx_S4S_TPH_H = 0x05 # RW (0000000)
LSM6DSx_S4S_RR = 0x06 # RW (0000000)
LSM6DSx_FIFO_CTRL1 = 0x07 # RW (0000000)
LSM6DSx_FIFO_CTRL2 = 0x08 # RW (0000000)
LSM6DSx_FIFO_CTRL3 = 0x09 # RW (0000000)
LSM6DSx_FIFO_CTRL4 = 0x0A # RW (00000000)
LSM6DSx_COUNTER_BDR_REG1 = 0x0B # RW (00000000)
LSM6DSx_COUNTER_BDR_REG2 = 0x0C # RW (00000000)
LSM6DSx_INT1_CTRL = 0x0D # RW (00000000)
LSM6DSx_INT2_CTRL = 0x0E # RW (00000000)
LSM6DSx_WHO_AM_I = 0x0F # R (01101011)
LSM6DSx_CTRL1_XL = 0x10 # RW (00000000)
LSM6DSx_CTRL2_G = 0x11 # RW (00000000)
LSM6DSx_CTRL3_C = 0x12 # RW (00000100)
LSM6DSx_CTRL4_C = 0x13 # RW (00000000)
LSM6DSx_CTRL5_C = 0x14 # RW (00000000)
LSM6DSx_CTRL6_C = 0x15 # RW (00000000)
LSM6DSx_CTRL7_G = 0x16 # RW (00000000)
LSM6DSx_CTRL8_XL = 0x17 # RW (00000000)
LSM6DSx_CTRL9_XL = 0x18 # RW (11100000)
LSM6DSx_CTRL10_C = 0x19 # RW (00000000)
LSM6DSx_ALL_INT_SRC = 0x1A # R (output)
LSM6DSx_WAKE_UP_SRC = 0x1B # R (output)
LSM6DSx_TAP_SRC = 0x1C # R (output)
LSM6DSx_D6D_SRC = 0x1D # R (output)
LSM6DSx_STATUS_REG = 0x1E # R (output)
# RESERVED 0x1F
LSM6DSx_OUT_TEMP_L = 0x20 # R (output)
LSM6DSx_OUT_TEMP_H = 0x21 # R (output)
LSM6DSx_OUTX_L_G = 0x22 # R (output)
LSM6DSx_OUTX_H_G = 0x23 # R (output)
LSM6DSx_OUTY_L_G = 0x24 # R (output)
LSM6DSx_OUTY_H_G = 0x25 # R (output)
LSM6DSx_OUTZ_L_G = 0x26 # R (output)
LSM6DSx_OUTZ_H_G = 0x27 # R (output)
LSM6DSx_OUTX_L_A = 0x28 # R (output)
LSM6DSx_OUTX_H_A = 0x29 # R (output)
LSM6DSx_OUTY_L_A = 0x2A # R (output)
LSM6DSx_OUTY_H_A = 0x2B # R (output)
LSM6DSx_OUTZ_L_A = 0x2C # R (output)
LSM6DSx_OUTZ_H_A = 0x2D # R (output)
# RESERVED 0x2E => 0x34
LSM6DSx_EMB_FUNC_STATUS_MAINPAGE = 0x35 # R (output)
LSM6DSx_FSM_STATUS_A_MAINPAGE = 0x36 # R (output)
LSM6DSx_FSM_STATUS_B_MAINPAGE = 0x37 # R (output)
# RESERVED 0x38
LSM6DSx_STATUS_MASTER_MAINPAGE = 0x39 # R (output)
LSM6DSx_FIFO_STATUS1 = 0x3A # R (output)
LSM6DSx_FIFO_STATUS2 = 0x3B # R (output)
# RESERVED 0x3C => 0x3F
LSM6DSx_TIMESTAMP0 = 0x40 # R (output)
LSM6DSx_TIMESTAMP1 = 0x41 # R (output)
LSM6DSx_TIMESTAMP2 = 0x42 # R (output)
LSM6DSx_TIMESTAMP3 = 0x43 # R (output)
# RESERVED 0x44 => 0x55
LSM6DSx_TAP_CFG0 = 0x56 # RW (00000000)
LSM6DSx_TAP_CFG1 = 0x57 # RW (00000000)
LSM6DSx_TAP_CFG2 = 0x58 # RW (00000000)
LSM6DSx_TAP_THS_6D = 0x59 # RW (00000000)
LSM6DSx_INT_DUR2 = 0x5A # RW (00000000)
LSM6DSx_WAKE_UP_THS = 0x5B # RW (00000000)
LSM6DSx_WAKE_UP_DUR = 0x5C # RW (00000000)
LSM6DSx_FREE_FALL = 0x5D # RW (00000000)
LSM6DSx_MD1_CFG = 0x5E # RW (00000000)
LSM6DSx_MD2_CFG = 0x5F # RW (00000000)
LSM6DSx_S4S_ST_CMD_CODE = 0x60 # RW (00000000)
LSM6DSx_S4S_DT_REG = 0x61 # RW (00000000)
LSM6DSx_I3C_BUS_AVB = 0x62 # RW (00000000)
LSM6DSx_INTERNAL_FREQ_FINE = 0x63 # R (output)
# RESERVED 0x64 => 0x6E
LSM6DSx_INT_OIS = 0x6F # R (00000000)
LSM6DSx_CTRL1_OIS = 0x70 # R (00000000)
LSM6DSx_CTRL2_OIS = 0x71 # R (00000000)
LSM6DSx_CTRL3_OIS = 0x72 # R (00000000)
LSM6DSx_X_OFS_USR = 0x73 # RW (00000000)
LSM6DSx_Y_OFS_USR = 0x74 # RW (00000000)
LSM6DSx_Z_OFS_USR = 0x75 # RW (00000000)
# RESERVED 0x76 => 0x77
LSM6DSx_FIFO_DATA_OUT_TAG = 0x78 # R (output)
LSM6DSx_FIFO_DATA_OUT_X_L = 0x79 # R (output)
LSM6DSx_FIFO_DATA_OUT_X_H = 0x7A # R (output)
LSM6DSx_FIFO_DATA_OUT_Y_L = 0x7B # R (output)
LSM6DSx_FIFO_DATA_OUT_Y_H = 0x7C # R (output)
LSM6DSx_FIFO_DATA_OUT_Z_L = 0x7D # R (output)
LSM6DSx_FIFO_DATA_OUT_Z_H = 0x7E # R (output)

LSM6DSx_SCALE_A = ('2', '16', '4', '8')
LSM6DSx_COE_A = (1, 8, 2, 4)
LSM6DSx_SCALE_G = ('250', '4000', '125', '', '500', '', '', '', '1000', '', '', '', '2000')
LSM6DSx_COE_G = (2, 32, 1, 0, 4, 0, 0, 0, 8, 0, 0, 0, 16)

LSM6DSR_SCALE_G = ('250', '4000', '125', '', '500', '', '', '', '1000', '', '', '', '2000')
LSM6DSL_SCALE_G = ('250', '', '125', '', '500', '', '', '', '1000', '', '', '', '2000')

class LSM6DSx:
    def __init__(self, i2c_bus, addr = 0x6A):
        self._bus = i2c_bus
        self._addr = int(addr)
        self._power = True
        self._power_a = 0x10
        self._power_g = 0x10
        self._wakeup_mode = 0
        self._chip = ""
        # Get chip name from chip reference ID 
        if self.read(LSM6DSx_WHO_AM_I) == 0x6B:
            self._chip = "LSM6DSR"
            LSM6DSx_SCALE_G = LSM6DSR_SCALE_G
        elif self.read(LSM6DSx_WHO_AM_I) == 0x6A:
            self._chip = "LSM6DSL"
            LSM6DSx_SCALE_G = LSM6DSL_SCALE_G
        else:
            raise Exception('[LSM6DSx] Sensor ID error (expected 0x6A or 0x6B, got '+hex(self.read(LSM6DSx_WHO_AM_I))+')')
        # RESET
        self.write(LSM6DSx_CTRL3_C, 1)
        time.sleep(0.2)
        if (self.read(LSM6DSx_CTRL3_C) & 0x1 == 0x1):
            raise Exception('[LSM6DSx] Soft reset not done in time')
        # Disable I3C
        self.read_modify_write(LSM6DSx_CTRL9_XL, 0x1, 0x1)
        # Enable BDU and address increment
        self.write(LSM6DSx_CTRL3_C, (0x0<<7) + (0x1<<6) + (0x0<<5) + (0x0<<4) + (0x0<<3) + (0x1<<2) + 0x0)
        # Enable bypass mode (disable FIFO mode)
        self.write(LSM6DSx_FIFO_CTRL4, 0x0)
        # Set ODR to 833Hz and full-scale to 16g
        self.write(LSM6DSx_CTRL1_XL, (0x7<<4) + (0x1<<2) + (0x0<<1))
        self._scale_a = 1
        # Set ODR to 833Hz and full-scale to 2000 dps
        self.write(LSM6DSx_CTRL2_G, (0x7<<4) + 0xC)
        self._scale_g = 12
    
    def read(self, reg, length=1):
        if length == 1:
            return self._bus.readfrom_mem(self._addr, int(reg), 1)[0]
        else:
            return self._bus.readfrom_mem(self._addr, int(reg), int(length))

    def write(self, reg, value):
        self._bus.writeto_mem(self._addr, int(reg), bytes([int(value)]))

    def read_modify_write(self, reg, dat, mask):
        reg_to_write = (self.read(reg) & ~mask) | (dat & mask)
        self.write(reg, reg_to_write)

    def scale_a(self, scale=None):
        if (scale is None) or (scale == ''):
            return LSM6DSx_SCALE_A[self._scale_a]
        else:
            scale = str(scale)
            if not scale in LSM6DSx_SCALE_A:
                return -1
            self._scale_a = LSM6DSx_SCALE_A.index(scale)
            self.read_modify_write(LSM6DSx_CTRL1_XL, self._scale_a<<2, 0x3<<2)
            return LSM6DSx_SCALE_A[self._scale_a]
    
    def get_available_scale_a(self):
        return [x for x in LSM6DSx_SCALE_A if not '']

    def scale_g(self, scale=None):
        if (scale is None) or (scale == ''):
            return LSM6DSx_SCALE_G[self._scale_g]
        else:
            scale = str(scale)
            if not scale in LSM6DSx_SCALE_G: 
                return -1
            self._scale_g = LSM6DSx_SCALE_G.index(scale)
            self.read_modify_write(LSM6DSx_CTRL2_G, self._scale_g, 0xF)
            return LSM6DSx_SCALE_G[self._scale_g]
        
    def get_available_scale_g(self):
        return [x for x in LSM6DSx_SCALE_G if not '']
    
    def read_acc_raw(self):
        acc_raw_val = self.read(LSM6DSx_OUTX_L_A, 6)
        ax, ay, az = struct.unpack('<hhh', bytearray(acc_raw_val)) # Little-endian
        return ax, ay, az
    
    def read_gyro_raw(self):
        gyro_raw_val = self.read(LSM6DSx_OUTX_L_G, 6)
        gx, gy, gz = struct.unpack('<hhh', bytearray(gyro_raw_val)) # Little-endian
        return gx, gy, gz

    def read_temp_raw(self):
        temp_raw_val = self.read(LSM6DSx_OUT_TEMP_L, 2)
        return struct.unpack('<h', bytearray(temp_raw_val))[0] # Little-endian

    def convert_a(self, a):
        return LSM6DSx_COE_A[self._scale_a]*0.061*a/1000.0

    def convert_g(self, g):
        return LSM6DSx_COE_G[self._scale_g]*4.375*g/1000.0

    def read_acc(self):
        ax_raw, ay_raw, az_raw = self.read_acc_raw()
        ax = self.convert_a(ax_raw)
        ay = self.convert_a(ay_raw)
        az = self.convert_a(az_raw)
        return ax, ay, az

    def read_gyro(self):
        gx_raw, gy_raw, gz_raw = self.read_acc_raw()
        gx = self.convert_a(gx_raw)
        gy = self.convert_a(gy_raw)
        gz = self.convert_a(gz_raw)
        return gx, gy, gz
    
    def read_temperature(self):
        return self.read_temp_raw()/256.0 + 25
    
    @property
    def data(self):
        return self.read_acc() + self.read_gyro()